"""YouTube for Autopilot (YouTube Data API v3).

The Google OAuth client ID is public and lives in config.json ("youtube_client_id"). The client
secret is the YOUTUBE_CLIENT_SECRET Actions secret. The sign-in (a long-lived refresh token) is kept
in secrets/youtube.enc, encrypted with that secret, so only GitHub Actions can read it.
Connect / renew: open the sign-in link (README), approve, paste the address-bar URL into
Actions -> youtube-connect -> Run workflow.
"""
import base64
import hashlib
import json
import os
import time
import urllib.parse
from pathlib import Path

import requests
from cryptography.fernet import Fernet

from . import ROOT, load_config

FILE = ROOT / "secrets" / "youtube.enc"
REDIRECT = "https://github.com/RolandDivine/autopilot"
SCOPES = " ".join("https://www.googleapis.com/auth/" + s for s in [
    "youtube", "youtube.force-ssl", "youtube.upload", "youtube.readonly", "yt-analytics.readonly"])
TOKEN_URL = "https://oauth2.googleapis.com/token"


class YouTubeError(Exception):
    pass


def _secret():
    s = os.environ.get("YOUTUBE_CLIENT_SECRET")
    if not s:
        raise YouTubeError("missing secret: YOUTUBE_CLIENT_SECRET")
    return s


def _fernet():
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(_secret().encode()).digest()))


def client_id():
    cid = load_config().get("youtube_client_id")
    if not cid:
        raise YouTubeError('add "youtube_client_id" to config.json')
    return cid


def sign_in_link():
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "response_type": "code", "client_id": client_id(), "redirect_uri": REDIRECT, "scope": SCOPES,
        "access_type": "offline", "prompt": "consent", "state": "autopilot-youtube"})


def save(data):
    FILE.parent.mkdir(exist_ok=True)
    FILE.write_bytes(_fernet().encrypt(json.dumps(data).encode()))


def load():
    if not FILE.exists():
        return None
    return json.loads(_fernet().decrypt(FILE.read_bytes()))


def exchange_code(code):
    r = requests.post(TOKEN_URL, timeout=30, data={
        "grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT,
        "client_id": client_id(), "client_secret": _secret()})
    if not r.ok:
        raise YouTubeError(f"token exchange failed: HTTP {r.status_code} {r.text[:300]}")
    return r.json()


class YouTubeClient:
    API = "https://www.googleapis.com/youtube/v3"

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        if dry_run:
            return
        tok = load()
        if not tok or not tok.get("refresh_token"):
            raise YouTubeError("YouTube not connected yet: run the youtube-connect workflow")
        r = requests.post(TOKEN_URL, timeout=30, data={
            "grant_type": "refresh_token", "refresh_token": tok["refresh_token"],
            "client_id": client_id(), "client_secret": _secret()})
        if not r.ok:
            raise YouTubeError(f"sign-in refresh failed (reconnect with youtube-connect): HTTP {r.status_code} {r.text[:300]}")
        self.h = {"Authorization": f"Bearer {r.json()['access_token']}"}

    def api(self, method, path, params=None, body=None, base=None):
        r = requests.request(method, f"{base or self.API}/{path}", headers=self.h, params=params or {},
                             json=body, timeout=60)
        if not r.ok:
            raise YouTubeError(f"{method} {path}: HTTP {r.status_code} {r.text[:400]}")
        return r.json() if r.text else {}

    def channel(self):
        r = requests.get(f"{self.API}/channels", headers=self.h, timeout=30, params={"part": "snippet", "mine": "true"})
        if not r.ok:
            raise YouTubeError(f"channels: HTTP {r.status_code} {r.text[:300]}")
        items = r.json().get("items") or []
        return items[0] if items else None

    def upload(self, path, title, description="", tags=None, privacy="public", category="27", ai=True):
        """Upload an MP4. Vertical videos up to 3 minutes become Shorts. Returns (video_id, url)."""
        if self.dry_run:
            print("[dry-run] YouTube:", path, title)
            return "DRYRUN", None
        path = Path(path)
        meta = {"snippet": {"title": title[:100], "description": description[:5000], "tags": tags or [],
                            "categoryId": category},
                "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False,
                           "containsSyntheticMedia": bool(ai)}}
        size = path.stat().st_size
        r = requests.post("https://www.googleapis.com/upload/youtube/v3/videos", timeout=60,
                          params={"uploadType": "resumable", "part": "snippet,status"},
                          headers={**self.h, "Content-Type": "application/json; charset=UTF-8",
                                   "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)},
                          data=json.dumps(meta))
        if not r.ok:
            raise YouTubeError(f"upload start: HTTP {r.status_code} {r.text[:400]}")
        loc = r.headers["Location"]
        for attempt in range(4):
            with path.open("rb") as f:
                u = requests.put(loc, data=f, timeout=900, headers={**self.h, "Content-Type": "video/mp4"})
            if u.ok:
                vid = u.json()["id"]
                return vid, f"https://youtube.com/shorts/{vid}"
            if u.status_code < 500:
                raise YouTubeError(f"upload: HTTP {u.status_code} {u.text[:400]}")
            time.sleep(10 * (attempt + 1))
        raise YouTubeError("upload failed after retries")
