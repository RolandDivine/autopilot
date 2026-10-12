"""Check the Instagram connection without posting: prints the account the token belongs to."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.ig_client import InstagramClient  # noqa: E402

try:
    c = InstagramClient()
    print(f"::notice title=instagram connected::@{c.username} (id {c.user_id})")
except Exception as e:
    print(f"::error title=instagram check failed::{str(e)[:500]}".replace("\n", " "))
    sys.exit(1)
