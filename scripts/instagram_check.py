import datetime as dt
"""Check the Instagram connection without posting: prints the account, profile fields and 28-day account insights (read-only)."""
import json
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

def show(title, fn):
    try:
        print(f"::notice title={title}::" + json.dumps(fn(), ensure_ascii=False)[:3500])
    except Exception as e:
        print(f"::warning title={title} unavailable::{str(e)[:300]}")

show("recent media", lambda: c._req("get", f"{c.user_id}/media", params={"fields": "id,timestamp,media_type,permalink,caption", "limit": 6}).get("data"))
show("profile", lambda: c._req("get", "me", params={"fields": "username,name,account_type,biography,website,followers_count,follows_count,media_count,profile_picture_url"}))
for m, extra in [("reach,views,accounts_engaged,total_interactions,profile_links_taps,follows_and_unfollows", {"metric_type": "total_value"}),
                 ("reach", {"breakdown": "media_product_type", "metric_type": "total_value"}),
                 ("reach", {"breakdown": "follow_type", "metric_type": "total_value"})]:
    show(f"insights {m} {extra.get('breakdown','')}".strip(), lambda m=m, extra=extra: c._req("get", f"{c.user_id}/insights", params={"metric": m, "period": "day", "since": os.environ.get("SINCE") or (dt.date.today() - dt.timedelta(days=7)).isoformat(), "until": os.environ.get("UNTIL") or dt.date.today().isoformat(), **extra}).get("data"))
show("audience country", lambda: c._req("get", f"{c.user_id}/insights", params={"metric": "follower_demographics", "period": "lifetime", "metric_type": "total_value", "breakdown": "country"}).get("data"))
