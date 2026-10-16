"""Upload repo videos to YouTube (Actions -> youtube-publish).

    PATHS="assets/reels/video.mp4"  TITLE="..."  DESCRIPTION="..."  TAGS="ai,crypto"  PRIVACY=public
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.yt_client import YouTubeClient  # noqa: E402

c = YouTubeClient()
ok = True
for p in os.environ["PATHS"].split():
    try:
        vid, url = c.upload(p, os.environ["TITLE"], os.environ.get("DESCRIPTION", ""),
                            [t.strip() for t in os.environ.get("TAGS", "").split(",") if t.strip()],
                            os.environ.get("PRIVACY") or "public")
        print(f"::notice title=youtube published::{url}")
    except Exception as e:
        ok = False
        print(f"::error title=youtube failed::{str(e)[:500]}".replace("\n", " "))
        break
sys.exit(0 if ok else 1)
