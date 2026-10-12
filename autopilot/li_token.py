"""LinkedIn sign-in stored in the repo, encrypted with the LINKEDIN_CLIENT_SECRET Actions secret.

Only GitHub Actions (which holds that secret) can read it. Renewing = click the sign-in link,
approve, paste the address-bar URL into Actions -> linkedin-connect -> Run workflow.
"""
import base64
import hashlib
import json
import os
import urllib.parse

from cryptography.fernet import Fernet

from . import ROOT, load_config

FILE = ROOT / "secrets" / "linkedin.enc"
REDIRECT = "https://github.com/RolandDivine/autopilot"
SCOPES = "openid profile w_member_social"


def _fernet():
    secret = os.environ.get("LINKEDIN_CLIENT_SECRET")
    if not secret:
        raise RuntimeError("missing secret: LINKEDIN_CLIENT_SECRET")
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(secret.encode()).digest()))


def sign_in_link():
    return "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode({
        "response_type": "code", "client_id": load_config()["linkedin_client_id"],
        "redirect_uri": REDIRECT, "scope": SCOPES, "state": "autopilot"})


def save(data):
    FILE.parent.mkdir(exist_ok=True)
    FILE.write_bytes(_fernet().encrypt(json.dumps(data).encode()))


def load():
    """{"access_token","person_urn","expires","name"} or None."""
    if os.environ.get("LINKEDIN_ACCESS_TOKEN") and os.environ.get("LINKEDIN_PERSON_URN"):
        return {"access_token": os.environ["LINKEDIN_ACCESS_TOKEN"],
                "person_urn": os.environ["LINKEDIN_PERSON_URN"],
                "expires": os.environ.get("LINKEDIN_TOKEN_EXPIRES")}
    if not FILE.exists() or not os.environ.get("LINKEDIN_CLIENT_SECRET"):
        return None
    return json.loads(_fernet().decrypt(FILE.read_bytes()))
