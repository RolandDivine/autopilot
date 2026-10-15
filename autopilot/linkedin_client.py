"""Post to your personal LinkedIn profile with the official Posts API.

Secrets:
    LINKEDIN_ACCESS_TOKEN   from scripts/linkedin_auth.py (scopes: openid profile w_member_social)
    LINKEDIN_PERSON_URN     urn:li:person:XXXX (printed by the same script)

Tokens expire (usually 60 days). check_token() warns 7 days ahead.
"""
import json
import os
import re
import time
import urllib.parse

import requests

from . import load_config


class LinkedInError(RuntimeError):
    pass


_RESERVED = re.compile(r"([\\|{}@\[\]()<>#*_~])")


def escape_commentary(text):
    """LinkedIn 'little text' format: reserved characters must be backslash-escaped
    or the post is cut off / rejected. Hashtags written as #word are kept as hashtags."""
    out = _RESERVED.sub(r"\\\1", text)
    # re-allow plain hashtags (#word) so they still link
    return re.sub(r"\\#(?=\w)", "#", out)


class LinkedInClient:
    def __init__(self, dry_run=False):
        self.cfg = load_config()
        self.base = self.cfg["linkedin_api_base"].rstrip("/")
        self.dry_run = dry_run
        self.author = "urn:li:person:DRYRUN"
        if not dry_run:
            from . import li_token
            tok = li_token.load()
            if not tok:
                raise LinkedInError("LinkedIn not connected yet: run Actions -> linkedin-connect")
            self.author = tok["person_urn"]
            self.s = requests.Session()
            self.s.headers.update({
                "Authorization": f"Bearer {tok['access_token']}",
                "LinkedIn-Version": self.cfg["linkedin_api_version"],
                "X-Restli-Protocol-Version": "2.0.0",
                "Content-Type": "application/json",
            })

    def _check(self, r, what):
        if r.status_code >= 300:
            hint = ""
            if r.status_code == 401:
                hint = " (LinkedIn sign-in expired: renew it with the linkedin-connect workflow)"
            if "VERSION" in r.text.upper():
                hint = " (update linkedin_api_version in config.json to a current YYYYMM)"
            raise LinkedInError(f"{what} failed: HTTP {r.status_code} {r.text[:500]}{hint}")
        return r

    def _upload(self, kind, path):
        """kind: 'images' or 'documents'. Returns the asset URN."""
        if self.dry_run:
            return f"urn:li:{kind[:-1]}:DRY-{os.path.basename(path)}"
        r = self._check(self.s.post(f"{self.base}/rest/{kind}?action=initializeUpload",
                                    data=json.dumps({"initializeUploadRequest": {"owner": self.author}}), timeout=30),
                        f"{kind} init")
        val = r.json()["value"]
        urn = val.get("image") or val.get("document")
        with open(path, "rb") as f:
            up = requests.put(val["uploadUrl"], data=f.read(),
                              headers={"Authorization": self.s.headers["Authorization"]}, timeout=120)
        self._check(up, f"{kind} upload")
        # images and documents are processed asynchronously; wait until LinkedIn says AVAILABLE
        if True:
            for _ in range(24):
                st = self.s.get(f"{self.base}/rest/{kind}/{urllib.parse.quote(urn)}", timeout=30)
                if st.ok and st.json().get("status") == "AVAILABLE":
                    break
                time.sleep(5)
        return urn

    def _upload_video(self, path):
        """MP4 upload via the Videos API (multi-part). Returns the video URN once it is AVAILABLE."""
        if self.dry_run:
            return f"urn:li:video:DRY-{os.path.basename(path)}"
        size = os.path.getsize(path)
        r = self._check(self.s.post(f"{self.base}/rest/videos?action=initializeUpload",
                                    data=json.dumps({"initializeUploadRequest": {
                                        "owner": self.author, "fileSizeBytes": size,
                                        "uploadCaptions": False, "uploadThumbnail": False}}), timeout=30),
                        "video init")
        val = r.json()["value"]
        urn, token = val["video"], val.get("uploadToken", "")
        etags = []
        with open(path, "rb") as f:
            for part in val["uploadInstructions"]:
                f.seek(part["firstByte"])
                chunk = f.read(part["lastByte"] - part["firstByte"] + 1)
                up = requests.put(part["uploadUrl"], data=chunk,
                                  headers={"Content-Type": "application/octet-stream"}, timeout=300)
                self._check(up, "video upload")
                etags.append(up.headers.get("etag") or up.headers.get("ETag"))
        self._check(self.s.post(f"{self.base}/rest/videos?action=finalizeUpload",
                                data=json.dumps({"finalizeUploadRequest": {
                                    "video": urn, "uploadToken": token, "uploadedPartIds": etags}}), timeout=60),
                    "video finalize")
        for _ in range(60):  # processing can take a few minutes
            st = self.s.get(f"{self.base}/rest/videos/{urllib.parse.quote(urn)}", timeout=30)
            if st.ok and st.json().get("status") == "AVAILABLE":
                return urn
            if st.ok and st.json().get("status") == "PROCESSING_FAILED":
                raise LinkedInError(f"video processing failed: {st.text[:300]}")
            time.sleep(10)
        return urn

    def create_post(self, text, media_path=None, media_title=None):
        body = {
            "author": self.author,
            "commentary": escape_commentary(text),
            "visibility": "PUBLIC",
            "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }
        if media_path:
            ext = os.path.splitext(media_path)[1].lower()
            kind = {".pdf": "documents", ".mp4": "videos"}.get(ext, "images")
            urn = self._upload_video(media_path) if kind == "videos" else self._upload(kind, media_path)
            media = {"id": urn}
            if kind in ("documents", "videos") and (media_title or kind == "documents"):
                media["title"] = media_title or "Document"
            body["content"] = {"media": media}
        if self.dry_run:
            print("[dry-run] LinkedIn post:", json.dumps(body)[:600])
            return "urn:li:share:DRYRUN"
        r = self._check(self.s.post(f"{self.base}/rest/posts", data=json.dumps(body), timeout=60), "create post")
        return r.headers.get("x-restli-id") or r.headers.get("x-linkedin-id")

    def comment(self, post_urn, text):
        if self.dry_run:
            print("[dry-run] LinkedIn first comment:", text)
            return
        enc = urllib.parse.quote(post_urn, safe="")
        body = {"actor": self.author, "object": post_urn, "message": {"text": text}}
        self._check(self.s.post(f"{self.base}/rest/socialActions/{enc}/comments", data=json.dumps(body), timeout=30),
                    "first comment")

    @staticmethod
    def url(post_urn):
        return f"https://www.linkedin.com/feed/update/{post_urn}"
