# Reddit Hot Plugin

Display the top hot post title and score from any subreddit.

![Reddit Hot Display](./docs/board-display.png)

**→ [Setup Guide](./docs/SETUP.md)**

## Overview

The Reddit Hot plugin fetches the top post from a configured subreddit using Reddit's public JSON API. It shows the post title, score, and comment count. No API key required, but Reddit rate-limits unauthenticated requests.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `reddit_hot.title` | Post title (truncated to fit board) | `Python 4.0 released` |
| `reddit_hot.score` | Post score (upvotes minus downvotes) | `45321` |
| `reddit_hot.comments` | Number of comments | `1023` |
| `reddit_hot.subreddit` | Subreddit name | `programming` |

## Example Templates

```
r/{{reddit_hot.subreddit}}
{{reddit_hot.title}}

Score: {{reddit_hot.score}}
Comments: {{reddit_hot.comments}}

```

## Configuration

| Setting | Name | Description | Required |
|---|---|---|---|
| `subreddit` | Subreddit | Subreddit name without the r/ prefix (e.g. programming). | Yes |
| `post_index` | Post Position | Which post to display (1 = top hot post). | No |

## Features

- Reddit public JSON API (no key needed)
- Configurable subreddit
- Post position selection
- Score and comment count
- No API key required

## Author

FiestaBoard Team
