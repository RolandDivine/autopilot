"""One-time LinkedIn sign-in. Run on YOUR computer (not GitHub):

    python scripts/linkedin_auth.py

Before running:
  1. https://www.linkedin.com/developers/apps → Create app (any name, e.g. "Roland Autopilot").
     LinkedIn requires a Company Page to attach the app to; any page you admin works.
  2. Products tab → request "Sign In with LinkedIn using OpenID Connect" and "Share on LinkedIn".
  3. Auth tab → add redirect URL:  http://localhost:8765/callback
  4. Copy the Client ID and Client Secret; this script asks for them.

It prints LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN and LINKEDIN_TOKEN_EXPIRES.
Paste those three into GitHub → your autopilot repo → Settings → Secrets and variables → Actions.
Nothing is stored or sent anywhere else.
"""
import datetime as dt
import http.server
import json
import secrets
import threading
import urllib.parse
import urllib.request
import webbrowser

REDIRECT = "http://localhost:8765/callback"
SCOPES = "openid profile w_member_social"


def main():
    client_id = input("LinkedIn Client ID: ").strip()
    client_secret = input("LinkedIn Client Secret: ").strip()
    state = secrets.token_urlsafe(16)
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            got.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>Done. You can close this tab and go back to the terminal.</h2>")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("localhost", 8765), H)
    t = threading.Thread(target=srv.handle_request, daemon=True)
    t.start()
    url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode({
        "response_type": "code", "client_id": client_id, "redirect_uri": REDIRECT,
        "scope": SCOPES, "state": state})
    print("\nOpening LinkedIn in your browser. Approve, then come back here.\n", url)
    webbrowser.open(url)
    t.join()
    if got.get("state") != state or "error" in got:
        raise SystemExit(f"Sign-in failed: {got}")

    data = urllib.parse.urlencode({
        "grant_type": "authorization_code", "code": got["code"], "redirect_uri": REDIRECT,
        "client_id": client_id, "client_secret": client_secret}).encode()
    tok = json.load(urllib.request.urlopen(urllib.request.Request(
        "https://www.linkedin.com/oauth/v2/accessToken", data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})))
    access = tok["access_token"]
    me = json.load(urllib.request.urlopen(urllib.request.Request(
        "https://api.linkedin.com/v2/userinfo", headers={"Authorization": f"Bearer {access}"})))
    expires = (dt.date.today() + dt.timedelta(seconds=int(tok.get("expires_in", 5184000)))).isoformat()

    print("\nAdd these three as GitHub Actions secrets:\n")
    print(f"LINKEDIN_ACCESS_TOKEN = {access}")
    print(f"LINKEDIN_PERSON_URN   = urn:li:person:{me['sub']}")
    print(f"LINKEDIN_TOKEN_EXPIRES = {expires}")
    print(f"\n(Signed in as {me.get('name')}. Token valid until {expires}.)")


if __name__ == "__main__":
    main()
