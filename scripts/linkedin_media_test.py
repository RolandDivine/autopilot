"""Prove LinkedIn media posting end to end: upload an image and a PDF, publish each as a post,
then delete the post a few seconds later so nothing stays on the profile."""
import os
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.linkedin_client import LinkedInClient  # noqa: E402

c = LinkedInClient()
ok = True
for path, title in (("tests/assets/sample.png", None), ("tests/assets/sample.pdf", "Autopilot test")):
    try:
        urn = c.create_post("Autopilot media test. This post deletes itself in a few seconds.", path, title)
        print(f"::notice title=published {os.path.basename(path)}::{urn}")
        time.sleep(4)
        d = c.s.delete(f"{c.base}/rest/posts/{urllib.parse.quote(urn, safe='')}", timeout=30)
        print(f"::notice title=deleted {os.path.basename(path)}::HTTP {d.status_code} {d.text[:200]}")
        if d.status_code >= 300:
            ok = False
    except Exception as e:
        ok = False
        print(f"::error title={os.path.basename(path)} failed::{str(e)[:500]}".replace("\n", " "))
sys.exit(0 if ok else 1)
