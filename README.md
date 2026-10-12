# Autopilot

Posts Roland's content to **X (@RolandDivine2)** and **LinkedIn** three times a day: 8 AM, 1 PM and 7 PM Lagos time. It runs on GitHub's servers, so Roland's laptop can be off.

## How a day works

1. **~8 PM the night before:** Claude writes tomorrow's posts into `queue/YYYY-MM-DD/` (`0800.json`, `1300.json`, `1900.json`, plus images and PDFs in `media/`).
2. **Right after that:** a GitHub Issue called **"Day N · Tue 13 Oct · review"** opens with every post, ready to read on your phone (GitHub app).
3. **Posts go out on their own** unless you leave a comment on that day's issue:

| Comment | What it does |
|---|---|
| `skip 1pm` | Skip the 1 PM post on both platforms |
| `skip 7pm x` | Skip only the X part of the 7 PM post (`linkedin` works the same way) |
| `skip all` | Skip the whole day |
| `pause` | Stop all posting from now on |
| `resume` | Start posting again |

To change wording, tap **edit this post** in the issue, then the pencil icon. Edit the text and commit before the post's time.

4. After each post, the bot comments the live links on the issue. Every post is recorded in `log/posted.jsonl`, and nothing is ever posted twice.
5. **Checks before posting:** posts are blocked for too-long tweets, emoji, hype phrases ("guaranteed returns", "agree?"), the wrong handle, or missing images. The issue explains which check failed.
6. **11 PM daily:** X stats are saved to `log/metrics.jsonl`, images older than 14 days are deleted, and you get a warning a week before the LinkedIn sign-in expires.

## One-time setup (about 30 minutes)

### X: about $5–10 a month
1. Go to https://console.x.com and sign in as @RolandDivine2. Create a Project and an App.
2. Add credit under **Billing**. $10 lasts months: each post costs about $0.015.
3. In App **Settings → User authentication**, set permissions to **Read and write** (type: Web App or Automated bot; any callback URL, e.g. `http://localhost`).
4. In **Keys and tokens**, copy the API Key and Secret, then generate an Access Token and Secret. Generate them *after* step 3 so they have write access.

### LinkedIn: free
1. https://www.linkedin.com/developers/apps → **Create app**. It needs a Company Page; any page you admin will do.
2. **Products** tab: add **Sign In with LinkedIn using OpenID Connect** and **Share on LinkedIn**.
3. **Auth** tab: add redirect URL `http://localhost:8765/callback`. Copy the Client ID and Client Secret.
4. On your computer, download this repo and run `python scripts/linkedin_auth.py`. Paste the ID and secret, then approve in the browser. It prints three values.

### Add them to GitHub
Repo → **Settings → Secrets and variables → Actions → New repository secret**. Add:

`X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`,
`LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN`, `LINKEDIN_TOKEN_EXPIRES`

### Test
**Actions → post → Run workflow** (leave "dry run" ticked). This shows what would be posted without posting anything.

## Files
- `config.json`: post times, handles, length limits and blocked phrases.
- `autopilot/`: the code (`post.py`, `review.py`, `maintenance.py`, plus the X and LinkedIn clients).
- `tests/`: run with `pytest`.
