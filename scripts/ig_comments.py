"""Instagram comments: list recent comments on the latest posts, or reply to one.
  list:  python scripts/ig_comments.py
  reply: python scripts/ig_comments.py <comment_id> "<text>"
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.ig_client import InstagramClient  # noqa: E402

c = InstagramClient()
if len(sys.argv) >= 3 and sys.argv[1] and sys.argv[2]:
    r = c._req("post", f"{sys.argv[1]}/replies", data={"message": sys.argv[2]})
    print("::notice title=replied::", r)
    sys.exit(0)
if len(sys.argv) >= 2 and sys.argv[1] == "media":
    for m in c._req("get", f"{c.user_id}/media", params={"fields": "caption,permalink,timestamp", "limit": 12}).get("data", []):
        print("MEDIA", m["timestamp"], m["permalink"], (m.get("caption") or "").split("\n")[0][:60], "|", "Part 14 of 15" in (m.get("caption") or ""))
    sys.exit(0)
media = c._req("get", f"{c.user_id}/media", params={"fields": "id,caption,permalink,timestamp,comments_count", "limit": 15}).get("data", [])
for m in media:
    if not m.get("comments_count"):
        continue
    cap = (m.get("caption") or "").split("\n")[0][:70]
    print(f"\n=== {m['timestamp']} {m['permalink']} | {cap}")
    raw = c._req("get", f"{m['id']}/comments", params={"fields": "id,text,username,timestamp,like_count,hidden,replies{id,text,username,timestamp}", "limit": 50})
    cs = raw.get("data", [])
    print(f"  count={m.get('comments_count')} returned={len(cs)} raw={str(raw)[:600]}")
    for x in cs:
        print(f"  [{x['id']}] {x['timestamp']} @{x.get('username')}: {x.get('text')}")
        for y in (x.get("replies") or {}).get("data", []):
            print(f"      ↳ [{y['id']}] @{y.get('username')}: {y.get('text')}")
