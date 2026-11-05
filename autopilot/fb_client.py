"""Facebook Page: post, comment, moderate, delete (Graph API, Page access token).

Connect once with Actions -> facebook-connect (needs FB_APP_ID, FB_APP_SECRET, FB_USER_TOKEN).
That swaps the short user token for a Page token that does not expire and keeps it encrypted
in secrets/facebook.enc (same key as the other tokens: LINKEDIN_CLIENT_SECRET).
"""
import json
import os
import time

import requests

from . import li_token

GRAPH = "https://graph.facebook.com/v24.0"
FILE = li_token.FILE.parent / "facebook.enc"


class FacebookError(RuntimeError):
    pass


def save(data):
    FILE.parent.mkdir(exist_ok=True)
    FILE.write_bytes(li_token._fernet().encrypt(json.dumps(data).encode()))


def load():
    if FILE.exists() and os.environ.get("LINKEDIN_CLIENT_SECRET"):
        return json.loads(li_token._fernet().decrypt(FILE.read_bytes()))
    return None


def _check(r, what):
    if not r.ok:
        raise FacebookError(f"{what} failed: HTTP {r.status_code} {r.text[:400]}")
    return r.json()


def connect(app_id, app_secret, user_token, page_hint=None):
    """Short user token -> long-lived user token -> never-expiring Page token. Returns saved dict."""
    long_user = _check(requests.get(f"{GRAPH}/oauth/access_token", timeout=30, params={
        "grant_type": "fb_exchange_token", "client_id": app_id, "client_secret": app_secret,
        "fb_exchange_token": user_token}), "token exchange")["access_token"]
    pages = _check(requests.get(f"{GRAPH}/me/accounts", timeout=30, params={
        "access_token": long_user, "fields": "id,name,access_token,tasks", "limit": 100}), "list pages")["data"]
    if not pages:
        raise FacebookError("no Pages found: in Graph API Explorer, tick your Page when Facebook asks which Pages to allow")
    if page_hint:
        hit = [p for p in pages if page_hint.lower() in (p["name"].lower(), p["id"])]
        pages = hit or pages
    page = pages[0]
    data = {"page_id": page["id"], "page_name": page["name"], "access_token": page["access_token"],
            "tasks": page.get("tasks", []), "connected": time.strftime("%Y-%m-%d"),
            "all_pages": [{"id": p["id"], "name": p["name"]} for p in pages]}
    save(data)
    return data


class FacebookClient:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        tok = load()
        if not tok:
            raise FacebookError("Facebook not connected yet: run Actions -> facebook-connect")
        self.page_id, self.token = tok["page_id"], tok["access_token"]

    def _req(self, method, path, **kw):
        kw.setdefault("timeout", 120)
        params = kw.pop("params", {}) or {}
        params["access_token"] = self.token
        return _check(requests.request(method, f"{GRAPH}/{path}", params=params, **kw), f"{method} {path}")

    def me(self):
        return self._req("GET", self.page_id, params={"fields": "id,name,fan_count,link"})

    def post_text(self, message, link=None):
        if self.dry_run:
            return {"id": "dry-run"}
        data = {"message": message}
        if link:
            data["link"] = link
        return self._req("POST", f"{self.page_id}/feed", data=data)

    def post_photos(self, image_urls, message):
        """One photo, or several as a single multi-photo post."""
        if self.dry_run:
            return {"id": "dry-run"}
        if len(image_urls) == 1:
            return self._req("POST", f"{self.page_id}/photos", data={"url": image_urls[0], "caption": message})
        ids = [self._req("POST", f"{self.page_id}/photos", data={"url": u, "published": "false"})["id"]
               for u in image_urls]
        data = {"message": message}
        for i, pid in enumerate(ids):
            data[f"attached_media[{i}]"] = json.dumps({"media_fbid": pid})
        return self._req("POST", f"{self.page_id}/feed", data=data)

    def post_video(self, video_url, description, title=None):
        if self.dry_run:
            return {"id": "dry-run"}
        data = {"file_url": video_url, "description": description}
        if title:
            data["title"] = title
        return self._req("POST", f"{self.page_id}/videos", data=data)

    def recent_posts(self, limit=10):
        return self._req("GET", f"{self.page_id}/posts", params={
            "fields": "id,message,created_time,permalink_url", "limit": limit})["data"]

    def comments(self, object_id, limit=50):
        return self._req("GET", f"{object_id}/comments", params={
            "fields": "id,from,message,created_time,is_hidden", "limit": limit, "filter": "toplevel"})["data"]

    def reply(self, comment_id, message):
        return self._req("POST", f"{comment_id}/comments", data={"message": message})

    def hide_comment(self, comment_id, hidden=True):
        return self._req("POST", comment_id, data={"is_hidden": "true" if hidden else "false"})

    def delete(self, object_id):
        """Delete a post or comment (removes it from Facebook)."""
        return self._req("DELETE", object_id)
