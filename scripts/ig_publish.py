"""Publish repo images to Instagram by hand (Actions -> instagram-publish).

    KIND=stories  PATHS="assets/stories/start-here-1.jpg assets/stories/start-here-2.jpg"
    KIND=post     PATHS="a-1.jpg a-2.jpg"  CAPTION="..."
    KIND=reel     PATHS="assets/reels/video.mp4"  CAPTION="..."
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.ig_client import InstagramClient  # noqa: E402

repo = os.environ.get("GITHUB_REPOSITORY", "RolandDivine/autopilot")
paths = os.environ["PATHS"].split()
urls = [f"https://raw.githubusercontent.com/{repo}/main/{p}" for p in paths]
c = InstagramClient()
ok = True
if os.environ.get("KIND", "stories") == "stories":
    for u in urls:
        try:
            print(f"::notice title=story posted::{c.publish_story(u)} {u.rsplit('/', 1)[-1]}")
        except Exception as e:
            ok = False
            print(f"::error title=story failed::{str(e)[:500]}".replace("\n", " "))
            break
elif os.environ.get("KIND") == "reel":
    for u in urls:
        try:
            mid, link = c.publish_reel(u, os.environ.get("CAPTION", ""))
            print(f"::notice title=reel published::{link or mid}")
        except Exception as e:
            ok = False
            print(f"::error title=reel failed::{str(e)[:500]}".replace("\n", " "))
            break
else:
    try:
        mid, link = c.publish(urls, os.environ.get("CAPTION", ""))
        print(f"::notice title=post published::{link or mid}")
    except Exception as e:
        ok = False
        print(f"::error title=post failed::{str(e)[:500]}".replace("\n", " "))
sys.exit(0 if ok else 1)
