"""Runs inside GitHub Actions (workflow: youtube-connect).

REDIRECT_URL is the full address-bar URL Google sends you to after you approve,
e.g. https://github.com/RolandDivine/autopilot?state=autopilot-youtube&code=4/0A...
"""
import datetime as dt
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import yt_client  # noqa: E402


def main():
    raw = os.environ.get("REDIRECT_URL", "").strip()
    q = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
    if q.get("error"):
        sys.exit(f"Google said: {q['error'][0]}")
    code = (q.get("code") or [""])[0]
    if not code:
        sys.exit("No code found. Paste the whole address-bar URL that starts with https://github.com/RolandDivine/autopilot?")
    tok = yt_client.exchange_code(code)
    if not tok.get("refresh_token"):
        sys.exit("Google didn't return a long-term sign-in. Open the sign-in link again (it asks for consent each time).")
    yt_client.save({"refresh_token": tok["refresh_token"], "connected": dt.date.today().isoformat()})
    ch = yt_client.YouTubeClient().channel()
    name = ch["snippet"]["title"] if ch else "(no channel on this Google account)"
    yt_client.save({"refresh_token": tok["refresh_token"], "connected": dt.date.today().isoformat(), "channel": name})
    print(f"::notice title=YouTube connected::{name}")


if __name__ == "__main__":
    main()
