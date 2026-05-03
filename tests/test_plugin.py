"""Tests for the reddit_hot plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.reddit_hot import RedditHotPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "reddit_hot",
    "name": "Reddit Hot",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "subreddit": {
                "type": "string",
                "title": "Subreddit",
                "description": "Subreddit name without the r/ prefix (e.g. programming).",
                "default": "programming"
            },
            "post_index": {
                "type": "integer",
                "title": "Post Position",
                "description": "Which post to display (1 = top hot post).",
                "default": 1,
                "minimum": 1,
                "maximum": 25
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to fetch the hot post. Respect Reddit rate limits (>=300s recommended).",
                "default": 300,
                "minimum": 120
            }
        },
        "required": [
            "subreddit"
        ]
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "data": {
        "children": [
            {
                "data": {
                    "title": "Python 4.0 released with new features",
                    "score": 45321,
                    "num_comments": 1023,
                    "subreddit": "programming",
                    "author": "example_user"
                }
            }
        ]
    }
}
""")


@pytest.fixture
def plugin():
    return RedditHotPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = RedditHotPlugin(MANIFEST)
    p.config = json.loads("""
{
    "subreddit": "programming",
    "post_index": 1
}
""")
    return p


class TestRedditHotPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "reddit_hot"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    def test_manifest_has_demo_config(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        assert "demo" in m, "manifest must have a 'demo' key"
        demo = m["demo"]
        assert "template" in demo, "demo must have a 'template'"
        assert isinstance(demo["template"], list), "demo.template must be a list"
        assert len(demo["template"]) == 6, "demo.template must have 6 lines"
        assert "line_metadata" in demo, "demo must have 'line_metadata'"
        assert len(demo["line_metadata"]) == 6, "demo.line_metadata must have 6 entries"

    @patch("plugins.reddit_hot.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "title" in result.data, "missing variable: title"
        assert "score" in result.data, "missing variable: score"
        assert "comments" in result.data, "missing variable: comments"
        assert "subreddit" in result.data, "missing variable: subreddit"

    @patch("plugins.reddit_hot.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.reddit_hot.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

