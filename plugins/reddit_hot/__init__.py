"""Display the top hot post title and score from any subreddit."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://www.reddit.com/r/{subreddit}/hot.json"
USER_AGENT = "FiestaBoard Reddit Hot Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--reddit-hot)"


class RedditHotPlugin(PluginBase):
    """Reddit Hot plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "reddit_hot"

    def fetch_data(self) -> PluginResult:
        try:
            subreddit = self.config.get("subreddit") or "programming"
            post_index = int(self.config.get("post_index") or 1) - 1

            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            response = requests.get(
                url,
                params={"limit": max(post_index + 1, 5)},
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            posts = data.get("data", {}).get("children", [])
            if not posts or post_index >= len(posts):
                return PluginResult(available=False, error="No posts found")

            post = posts[post_index]["data"]
            title = str(post.get("title", ""))[:22]
            score = int(post.get("score", 0))
            comments = int(post.get("num_comments", 0))

            return PluginResult(
                available=True,
                data={
                    "title": title,
                    "score": score,
                    "comments": comments,
                    "subreddit": subreddit,
                },
            )
        except Exception as e:
            logger.exception("Error fetching Reddit hot post")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        if not config.get("subreddit"):
            errors.append("subreddit is required")
        return errors

    def cleanup(self) -> None:
        pass
