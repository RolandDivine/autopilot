"""Post carousels and single images to Instagram (Creator/Business account) with the
Instagram API with Instagram Login. No Facebook Page needed.

Token: GitHub secret INSTAGRAM_TOKEN (long-lived, from the Meta app dashboard). The daily job
refreshes it before it expires and keeps the fresh copy encrypted in secrets/instagram.enc,
so it never needs renewing by hand.

Instagram fetches images from a public URL, and only JPEG is accepted. Images are served from
raw.githubusercontent.com, so the repo must be public.
"""
import datetime as dt
import os
import time

import requests

from . import load_config, li_token

GRAPH = "https://graph.instagram.com"
FILE = li_token.FILE.parent / "instagram.enc"


class InstagramError(RuntimeError):
    pass


def load_token():
    """Prefer the refreshed copy in the repo; fall back to the GitHub secret."""
    if FILE.exists() and os.environ.get("LINKEDIN_CLIENT_SECRET"):
        import json
        return json.loads(li_token._fernet().decrypt(FILE.read_bytes()))
    tok = os.environ.get("INSTAGRAM_TOKEN")
    return {"access_token": tok, "refreshed": None} if tok else None


def refresh_token():
    """Swap the token for a fresh 60-day one (allowed once it is 24h old). Returns new expiry or None."""
    tok = load_token()
    if not tok:
        return None
    last = tok.get("refreshed")
    if last and dt.date.today() - dt.date.fromisoformat(last) < dt.timedelta(days=7):
        return tok.get("expires")
    r = requests.get(f"{GRAPH}/refresh_access_token", timeout=30,
                     params={"grant_type": "ig_refresh_token", "access_token": tok["access_token"]})
    if not r.ok:
        raise InstagramError(f"token refresh failed: HTTP {r.status_code} {r.text[:300]}")
    d = r.json()
    expires = (dt.date.today() + dt.timedelta(seconds=int(d.get("expires_in", 5184000)))).isoformat()
    import json
    FILE.parent.mkdir(exist_ok=True)
    FILE.write_bytes(li_token._fernet().encrypt(json.dumps(
        {"access_token": d["access_token"], "refreshed": dt.date.today().isoformat(), "expires": expires}).encode()))
    return expires


def public_url(slot_path, rel):
    repo = os.environ.get("GITHUB_REPOSITORY", "RolandDivine/autopilot")
    root = slot_path.parent.relative_to(slot_path.parents[2])  # queue/<date>
    return f"https://raw.githubusercontent.com/{repo}/main/{root.as_posix()}/{rel}"


class InstagramClient:
    def __init__(self, dry_run=False):
        cfg = load_config()
        self.base = f"{GRAPH}/{cfg.get('instagram_api_version', 'v24.0')}"
        self.dry_run = dry_run
        if not dry_run:
            tok = load_token()
            if not tok:
                raise InstagramError("Instagram not connected yet: add the INSTAGRAM_TOKEN secret")
            self.token = tok["access_token"]
            try:
                me = self._req("get", "me", params={"fields": "user_id,username"})
            except InstagramError as e:
                # The saved refreshed copy can die (password change, Meta security reset). Fall back to the
                # INSTAGRAM_TOKEN secret Roland updates, and drop the dead copy so the daily refresh re-saves it.
                env = os.environ.get("INSTAGRAM_TOKEN")
                if "190" not in str(e) or not env or env == self.token:
                    raise
                self.token = env
                me = self._req("get", "me", params={"fields": "user_id,username"})
                if FILE.exists():
                    FILE.unlink()
            self.user_id = me.get("user_id") or me["id"]
            self.username = me.get("username")

    def _req(self, method, path, **kw):
        kw.setdefault("params", {})["access_token"] = self.token
        r = requests.request(method, f"{self.base}/{path}", timeout=60, **kw)
        if r.status_code >= 300:
            raise InstagramError(f"{method.upper()} {path}: HTTP {r.status_code} {r.text[:400]}")
        return r.json()

    def _wait(self, container_id, tries=30):
        for _ in range(tries):
            st = self._req("get", container_id, params={"fields": "status_code,status"})
            if st.get("status_code") == "FINISHED":
                return
            if st.get("status_code") in ("ERROR", "EXPIRED"):
                raise InstagramError(f"container {container_id}: {st}")
            time.sleep(4)
        raise InstagramError(f"container {container_id} not ready after {tries * 4} seconds")

    def _publish(self, creation_id):
        """media_publish, retrying while Instagram says the media is not ready yet (code 9007) or a transient error
        (HTTP 500 / "is_transient": true). Retrying the same container can't create a duplicate post."""
        for attempt in range(8):
            try:
                return self._req("post", f"{self.user_id}/media_publish", data={"creation_id": creation_id})["id"]
            except InstagramError as e:
                if self._published(creation_id):
                    # Instagram sometimes answers HTTP 500 but publishes anyway (28 Oct 2026); never post twice.
                    return self._latest_id() or f"published:{creation_id}"
                retry = "9007" in str(e) or "not ready" in str(e) or '"is_transient":true' in str(e) or "HTTP 500" in str(e)
                if not retry or attempt == 7:
                    raise
                time.sleep(5 + attempt * 5)

    def _published(self, creation_id):
        try:
            return self._req("get", creation_id, params={"fields": "status_code"}).get("status_code") == "PUBLISHED"
        except Exception:
            return False

    def _latest_id(self):
        try:
            data = self._req("get", f"{self.user_id}/media", params={"fields": "id", "limit": 1}).get("data") or []
            return data[0]["id"] if data else None
        except Exception:
            return None

    def publish_story(self, image_url):
        """One image story (disappears after 24h; add it to a highlight in the app). Returns media_id."""
        if self.dry_run:
            print("[dry-run] Instagram story:", image_url)
            return "DRYRUN"
        if image_url.lower().endswith(".mp4"):  # video story, 3-60 seconds
            cid = self._req("post", f"{self.user_id}/media", data={"video_url": image_url, "media_type": "STORIES"})["id"]
            self._wait(cid, tries=90)
        else:
            cid = self._req("post", f"{self.user_id}/media", data={"image_url": image_url, "media_type": "STORIES"})["id"]
            self._wait(cid)
        return self._publish(cid)

    def publish_reel(self, video_url, caption, share_to_feed=True):
        """MP4 video as a Reel (vertical 9:16). Returns (media_id, permalink)."""
        if self.dry_run:
            print("[dry-run] Instagram reel:", video_url, "caption:", caption[:120])
            return "DRYRUN", None
        cid = self._req("post", f"{self.user_id}/media",
                        data={"media_type": "REELS", "video_url": video_url, "caption": caption,
                              "share_to_feed": "true" if share_to_feed else "false"})["id"]
        self._wait(cid, tries=90)  # video processing can take a few minutes
        mid = self._publish(cid)
        try:
            link = self._req("get", mid, params={"fields": "permalink"}).get("permalink")
        except InstagramError:
            link = None
        return mid, link

    def _media(self, data, alt=None):
        """Create a media container, with alt text when given (Roland, 21 Oct 2026: alt text is a search signal).
        If Instagram rejects the alt_text field, retry once without it so the post still goes out."""
        if alt:
            try:
                return self._req("post", f"{self.user_id}/media", data={**data, "alt_text": alt[:1000]})["id"]
            except InstagramError as e:
                if "alt_text" not in str(e) and "param" not in str(e).lower():
                    raise
        return self._req("post", f"{self.user_id}/media", data=data)["id"]

    def publish(self, image_urls, caption, alt=None):
        """1 URL = single image post; 2-10 = carousel. alt = list of alt texts (one per image) or None.
        Returns (media_id, permalink)."""
        if self.dry_run:
            print("[dry-run] Instagram:", len(image_urls), "images;", image_urls[:2], "caption:", caption[:120])
            return "DRYRUN", None
        alt = alt or []
        if len(image_urls) == 1:
            cid = self._media({"image_url": image_urls[0], "caption": caption}, alt[0] if alt else None)
        else:
            children = []
            for i, u in enumerate(image_urls[:10]):
                children.append(self._media({"image_url": u, "is_carousel_item": "true"}, alt[i] if i < len(alt) else None))
            for c in children:
                self._wait(c)
            cid = self._req("post", f"{self.user_id}/media",
                            data={"media_type": "CAROUSEL", "children": ",".join(children), "caption": caption})["id"]
        self._wait(cid)
        mid = self._publish(cid)
        try:
            link = self._req("get", mid, params={"fields": "permalink"}).get("permalink")
        except InstagramError:
            link = None
        return mid, link
