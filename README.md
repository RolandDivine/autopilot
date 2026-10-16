# Autopilot

Posts Roland's content to **LinkedIn (RolandDivine2)**, **Instagram (@defi_ring_master)** and **YouTube** three times a day: 8 AM, 1 PM and 7 PM Lagos time. It runs on GitHub's servers, so Roland's laptop can be off.

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
3. In App **Settings → User authentication**, set permissions to **Read and write** (type: Web App or Automated bot; callback and website URL: `https://x.com/RolandDivine2`).
4. In **Keys and tokens**, copy the API Key and Secret, then generate an Access Token and Secret. Generate them *after* step 3 so they have write access.

### YouTube: free, no computer needed
1. At [console.cloud.google.com](https://console.cloud.google.com), create a project called **Autopilot**. Under **APIs & Services → Library**, enable **YouTube Data API v3**.
2. Under **Google Auth Platform**: set **Branding** (app name Autopilot, your email). Under **Audience**, choose **External** and click **Publish app**, so the sign-in doesn't expire after 7 days.
3. Under **Clients → Create client**, choose **Web application** and add the redirect URI `https://github.com/RolandDivine/autopilot`.
4. Put the **Client ID** in `config.json` as `youtube_client_id` (it's public). Add the **Client secret** as the Actions secret `YOUTUBE_CLIENT_SECRET` (Settings → Secrets and variables → Actions). Never paste the secret anywhere else.
5. Open the YouTube sign-in link (`python -c "from autopilot.yt_client import sign_in_link; print(sign_in_link())"`), choose your channel's Google account, click **Advanced → Go to Autopilot** on the "unverified app" screen, and allow. Copy the address you land on, then run **Actions → youtube-connect** with it, within a few minutes.
6. Post with **Actions → youtube-publish**. Vertical MP4s up to 3 minutes become Shorts.

Note: Google keeps uploads from a new, unaudited API project **private** until the project passes the free [YouTube API audit](https://support.google.com/youtube/contact/yt_api_form). Until then, flip each video to Public in YouTube Studio.

### LinkedIn: free, no computer needed
1. In the LinkedIn developer app's **Auth** tab, add the redirect URL `https://github.com/RolandDivine/autopilot`. In the **Products** tab, add **Sign In with LinkedIn using OpenID Connect** and **Share on LinkedIn**.
2. Add the GitHub secret `LINKEDIN_CLIENT_SECRET` (the app's Client Secret).
3. Open the [LinkedIn sign-in link](https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78hozpq7114k7y&redirect_uri=https%3A%2F%2Fgithub.com%2FRolandDivine%2Fautopilot&scope=openid+profile+w_member_social&state=autopilot) and click **Allow**. You land back on this repo, with a long address in the browser bar.
4. Copy that whole address. Go to **Actions → linkedin-connect → Run workflow**, paste it and click Run. Do this within 5 minutes, because the code expires.

The sign-in lasts about 60 days. A week before it ends, Autopilot opens an issue with the same 1-minute steps.

### Instagram: free (Creator or Business account)
1. Go to https://developers.facebook.com/apps and choose **Create app**. Pick the use case **Manage messaging & content on Instagram**.
2. In the app, open **Instagram → API setup with Instagram login**. Under **Generate access tokens**, click **Add account** and log in as @defi_ring_master. Then click **Generate token** and copy it.
3. Add it as the GitHub secret `INSTAGRAM_TOKEN`. Autopilot refreshes it every week on its own, so you only do this once.
4. Run **Actions → instagram-check**. A green tick means it can see @defi_ring_master.
5. Instagram downloads the images from a public link, so this repo must be **public**. That makes the code and upcoming posts visible. Keys stay hidden in Secrets, and the LinkedIn sign-in is stored encrypted. Only your own comments control posting.
6. Set `"instagram_autopost": true` in `config.json`.

### Add them to GitHub
Repo → **Settings → Secrets and variables → Actions → New repository secret**. Add:

`LINKEDIN_CLIENT_SECRET`, `INSTAGRAM_TOKEN` (X is off; its four keys are optional)

### Test
**Actions → post → Run workflow** (leave "dry run" ticked). This shows what would be posted without posting anything.

## Files
- `config.json`: post times, handles, length limits and blocked phrases.
- `autopilot/`: the code (`post.py`, `review.py`, `maintenance.py`, plus the X and LinkedIn clients).
- `tests/`: run with `pytest`.
