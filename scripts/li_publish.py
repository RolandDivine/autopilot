"""Publish one LinkedIn post by hand (Actions -> linkedin-publish).

    MEDIA=assets/reels/video.mp4  TEXT="..."  TITLE="optional title"
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.linkedin_client import LinkedInClient  # noqa: E402

c = LinkedInClient()
try:
    urn = c.create_post(os.environ["TEXT"], os.environ.get("MEDIA") or None, os.environ.get("TITLE") or None)
    print(f"::notice title=LinkedIn posted::{c.url(urn)}")
except Exception as e:
    print(f"::error title=LinkedIn failed::{str(e)[:500]}".replace("\n", " "))
    sys.exit(1)
