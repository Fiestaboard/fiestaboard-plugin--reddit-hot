# Reddit Hot Setup Guide

Display the top hot post title and score from any subreddit.

## Overview

The Reddit Hot plugin fetches the top post from a configured subreddit using Reddit's public JSON API. It shows the post title, score, and comment count. No API key required, but Reddit rate-limits unauthenticated requests.

- API reference: https://www.reddit.com/dev/api/

### Prerequisites

No API key required. Reddit requires a descriptive User-Agent.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **Reddit Hot**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `reddit_hot` plugin variables:
   ```
   {{{ reddit_hot.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `reddit_hot.title` | Post title (truncated to fit board) | `Python 4.0 released` |
| `reddit_hot.score` | Post score (upvotes minus downvotes) | `45321` |
| `reddit_hot.comments` | Number of comments | `1023` |
| `reddit_hot.subreddit` | Subreddit name | `programming` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `subreddit` | Subreddit | Subreddit name without the r/ prefix (e.g. programming). | `programming` |
| `post_index` | Post Position | Which post to display (1 = top hot post). | `1` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to fetch the hot post. Respect Reddit rate limits (>=300s recommended). | `300` |

## Troubleshooting

- **Rate limited (429)** — increase the refresh interval to at least 300 seconds.
- **Empty subreddit** — check the subreddit name is spelled correctly.

