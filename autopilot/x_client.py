"""Post to X with the official API (OAuth 1.0a user context).

Secrets (GitHub Actions secrets):
    X_API_KEY, X_API_SECRET            app "consumer" keys
    X_ACCESS_TOKEN, X_ACCESS_SECRET    your account's tokens (app must have Read and Write)

Pricing note: X's API is pay-per-use. Every tweet in a thread is one post.
"""
import mimetypes
import os
import time

import requests
from requests_oauthlib import OAuth1

from . import load_config


class XError(RuntimeError):
    pass


class XClient:
    def __init__(self, dry_run=False):
        self.cfg = load_config()
        self.base = self.cfg["x_api_base"].rstrip("/")
        self.dry_run = dry_run
        if not dry_run:
            missing = [k for k in ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET") if not os.environ.get(k)]
            if missing:
                raise XError(f"missing secrets: {', '.join(missing)}")
            self.auth = OAuth1(os.environ["X_API_KEY"], os.environ["X_API_SECRET"],
                               os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_SECRET"])

    def _check(self, r, what):
        if r.status_code >= 300:
            raise XError(f"{what} failed: HTTP {r.status_code} {r.text[:500]}")
        return r.json() if r.content else {}

    def upload_media(self, path):
        """Simple upload for images (PNG/JPG/GIF under 5 MB)."""
        if self.dry_run:
            return f"dry-media:{os.path.basename(path)}"
        mime = mimetypes.guess_type(path)[0] or "image/png"
        with open(path, "rb") as f:
            r = requests.post(f"{self.base}/2/media/upload", auth=self.auth,
                              files={"media": (os.path.basename(path), f, mime)},
                              data={"media_category": "tweet_image", "media_type": mime}, timeout=60)
        data = self._check(r, "media upload")
        media_id = (data.get("data") or {}).get("id") or data.get("media_id_string")
        if not media_id:
            raise XError(f"media upload returned no id: {data}")
        return media_id

    def create_post(self, text, reply_to=None, media_ids=None):
        body = {"text": text}
        if reply_to:
            body["reply"] = {"in_reply_to_tweet_id": reply_to}
        if media_ids:
            body["media"] = {"media_ids": list(media_ids)}
        if self.dry_run:
            print("[dry-run] X post:", body)
            return f"dry-{abs(hash(text)) % 10**8}"
        for attempt in range(3):
            r = requests.post(f"{self.base}/2/tweets", auth=self.auth, json=body, timeout=30)
            if r.status_code == 429 and attempt < 2:
                time.sleep(30 * (attempt + 1))
                continue
            return self._check(r, "create post")["data"]["id"]

    def post_thread(self, posts, media_root):
        """posts: [{"text":..., "media":[relpath,...]}]. Returns list of tweet ids."""
        ids, prev = [], None
        for p in posts:
            media_ids = [self.upload_media(str(media_root / m)) for m in (p.get("media") or [])]
            prev = self.create_post(p["text"], reply_to=prev, media_ids=media_ids or None)
            ids.append(prev)
        return ids

    def metrics(self, tweet_ids):
        """Public metrics for up to 100 tweets (each read is billed)."""
        if self.dry_run or not tweet_ids:
            return {}
        r = requests.get(f"{self.base}/2/tweets", auth=self.auth, timeout=30,
                         params={"ids": ",".join(tweet_ids[:100]), "tweet.fields": "public_metrics,created_at"})
        data = self._check(r, "metrics")
        return {t["id"]: t.get("public_metrics", {}) for t in data.get("data", [])}

    def url(self, tweet_id):
        return f"https://x.com/{self.cfg['handles']['x']}/status/{tweet_id}"
