"""Runs inside GitHub Actions (workflow: linkedin-connect).

Input REDIRECT_URL is the full address-bar URL LinkedIn sends you to after you approve,
e.g. https://github.com/RolandDivine/autopilot?code=AQT...&state=autopilot
"""
import datetime as dt
import os
import sys
import urllib.parse

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import load_config, li_token  # noqa: E402


def main():
    raw = os.environ.get("REDIRECT_URL", "").strip()
    q = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
    code = (q.get("code") or [raw if raw and "://" not in raw else ""])[0]
    if q.get("error"):
        sys.exit(f"LinkedIn said: {q.get('error_description', q['error'])[0]}")
    if not code:
        sys.exit("No code found. Paste the whole address-bar URL that starts with https://github.com/RolandDivine/autopilot?code=")
    r = requests.post("https://www.linkedin.com/oauth/v2/accessToken", timeout=30, data={
        "grant_type": "authorization_code", "code": code, "redirect_uri": li_token.REDIRECT,
        "client_id": load_config()["linkedin_client_id"], "client_secret": os.environ["LINKEDIN_CLIENT_SECRET"]})
    if not r.ok:
        sys.exit(f"Token exchange failed: HTTP {r.status_code} {r.text[:300]} "
                 "(codes expire after a few minutes and work once: click the sign-in link again)")
    tok = r.json()
    me = requests.get("https://api.linkedin.com/v2/userinfo", timeout=30,
                      headers={"Authorization": f"Bearer {tok['access_token']}"})
    me.raise_for_status()
    me = me.json()
    expires = (dt.date.today() + dt.timedelta(seconds=int(tok.get("expires_in", 5184000)))).isoformat()
    li_token.save({"access_token": tok["access_token"], "person_urn": f"urn:li:person:{me['sub']}",
                   "expires": expires, "name": me.get("name")})
    print(f"Connected LinkedIn for {me.get('name')}. Valid until {expires}.")


if __name__ == "__main__":
    main()
