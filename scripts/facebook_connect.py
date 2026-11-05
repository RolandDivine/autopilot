"""Connect the Facebook Page, then report which platform secrets are present (values never printed)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import fb_client  # noqa: E402


def main():
    for k in ("FB_APP_ID", "FB_APP_SECRET", "FB_USER_TOKEN", "TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET",
              "X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET"):
        print(f"secret {k}: {'set' if os.environ.get(k) else 'MISSING'}")
    missing = [k for k in ("FB_APP_ID", "FB_APP_SECRET", "FB_USER_TOKEN") if not os.environ.get(k)]
    if missing:
        print(f"::error::Facebook secrets missing: {', '.join(missing)}")
        sys.exit(1)
    try:
        d = fb_client.connect(os.environ["FB_APP_ID"].strip(), os.environ["FB_APP_SECRET"].strip(),
                              os.environ["FB_USER_TOKEN"].strip(), os.environ.get("PAGE") or None)
    except fb_client.FacebookError as e:
        print(f"::error::{e}")
        sys.exit(1)
    print(f"connected Page: {d['page_name']} ({d['page_id']})")
    print(f"page tasks: {', '.join(d['tasks'])}")
    print(f"pages available: {', '.join(p['name'] for p in d['all_pages'])}")
    info = fb_client.FacebookClient().me()
    print(f"check: {info.get('name')} | followers {info.get('fan_count')} | {info.get('link')}")
    print(f"::notice::Facebook connected: {d['page_name']}")


if __name__ == "__main__":
    main()
