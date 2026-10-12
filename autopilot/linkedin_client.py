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
        self.author = os.environ.get("LINKEDIN_PERSON_URN", "urn:li:person:DRYRUN")
        if not dry_run:
            if not os.environ.get("LINKEDIN_ACCESS_TOKEN") or not os.environ.get("LINKEDIN_PERSON_URN"):
                raise LinkedInError("missing secrets: LINKEDIN_ACCESS_TOKEN / LINKEDIN_PERSON_URN")
            self.s = requests.Session()
            self.s.headers.update({
                "Authorization": f"Bearer {os.environ['LINKEDIN_ACCESS_TOKEN']}",
                "LinkedIn-Version": self.cfg["linkedin_api_version"],
                "X-Restli-Protocol-Version": "2.0.0",
                "Content-Type": "application/json",
            })

    def _check(self, r, what):
        if r.status_code >= 300:
            hint = ""
            if r.status_code == 401:
                hint = " (token expired or revoked: re-run scripts/linkedin_auth.py)"
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
        # documents are processed asynchronously; give LinkedIn a moment
        if kind == "documents":
            for _ in range(12):
                st = self.s.get(f"{self.base}/rest/documents/{urllib.parse.quote(urn)}", timeout=30)
                if st.ok and st.json().get("status") == "AVAILABLE":
                    break
                time.sleep(5)
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
            kind = "documents" if ext == ".pdf" else "images"
            urn = self._upload(kind, media_path)
            media = {"id": urn}
            if kind == "documents":
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
