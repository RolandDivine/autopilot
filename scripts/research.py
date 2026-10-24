"""Nightly research pull (runs in GitHub Actions, which has open internet).

Writes research/<date>.json with:
  trends   Google Trends "trending now" for US, GB, NG, IN, with the news headlines attached
  reddit   top posts of the last 24h in AI / crypto / business / infrastructure subreddits
  hn       Hacker News top stories (tech, AI, infrastructure)
  questions  Google autocomplete for question stems ("how to ...", "is it safe ...") per topic
  instagram  per-post stats for @defi_ring_master (likes, comments, reach, saves, shares, views)
"""
import datetime as dt
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
UA = {"User-Agent": "Mozilla/5.0 (research bot for RolandDivine/autopilot)"}
out = {"date": dt.date.today().isoformat(), "errors": {}}


def safe(name, fn):
    try:
        out[name] = fn()
    except Exception as e:  # keep going; one source failing must not kill the rest
        out["errors"][name] = str(e)[:300]


def trends():
    ns = {"ht": "https://trends.google.com/trending/rss"}
    res = {}
    for geo in ("US", "GB", "NG", "IN"):
        r = requests.get(f"https://trends.google.com/trending/rss?geo={geo}", headers=UA, timeout=30)
        r.raise_for_status()
        items = []
        for it in ET.fromstring(r.content).iter("item"):
            items.append({
                "q": it.findtext("title"),
                "traffic": it.findtext("ht:approx_traffic", namespaces=ns),
                "news": [n.findtext("ht:news_item_title", namespaces=ns) for n in it.findall("ht:news_item", ns)][:2],
            })
        res[geo] = items
    return res


SUBS = ["artificial", "ChatGPT", "ClaudeAI", "LocalLLaMA", "OpenAI", "CryptoCurrency", "Bitcoin",
        "Entrepreneur", "smallbusiness", "startups", "SideProject", "devops", "selfhosted", "sysadmin"]


def reddit():
    res = {}
    for s in SUBS:
        r = requests.get(f"https://www.reddit.com/r/{s}/top.json?t=day&limit=12", headers=UA, timeout=30)
        if not r.ok:
            res[s] = f"HTTP {r.status_code}"
            continue
        res[s] = [{"title": c["data"]["title"], "score": c["data"]["score"], "comments": c["data"]["num_comments"]}
                  for c in r.json()["data"]["children"]]
    return res


def hn():
    ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=30).json()[:30]
    items = [requests.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json", timeout=30).json() for i in ids]
    return [{"title": x.get("title"), "score": x.get("score"), "comments": x.get("descendants")} for x in items if x]


TOPICS = ["ai agents", "chatgpt", "claude", "ai tools", "vibe coding", "bitcoin", "crypto", "stablecoin",
          "start a business", "small business ai", "automate", "cloud", "data center", "cybersecurity"]
STEMS = ["how to", "how do i", "is it safe to", "best", "why is", "can i"]


def questions():
    res = {}
    for t in TOPICS:
        got = []
        for s in STEMS:
            r = requests.get("https://suggestqueries.google.com/complete/search",
                             params={"client": "firefox", "q": f"{s} {t}"}, headers=UA, timeout=20)
            if r.ok:
                got += r.json()[1]
        res[t] = list(dict.fromkeys(got))
    return res


def instagram():
    from autopilot.ig_client import InstagramClient
    c = InstagramClient()
    media = c._req("get", f"{c.user_id}/media", params={
        "fields": "id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count",
        "limit": 50})["data"]
    rows = []
    for m in media:
        row = {k: m.get(k) for k in ("timestamp", "media_type", "media_product_type", "permalink",
                                     "like_count", "comments_count")}
        row["caption"] = (m.get("caption") or "")[:70]
        metrics = "reach,saved,shares,views,total_interactions"
        try:
            ins = c._req("get", f"{m['id']}/insights", params={"metric": metrics})["data"]
            row.update({d["name"]: d["values"][0]["value"] for d in ins})
        except Exception as e:
            row["insights_error"] = str(e)[:160]
        if m.get("media_product_type") == "REELS":  # watch-time signals (ms)
            try:
                ins = c._req("get", f"{m['id']}/insights", params={"metric": "ig_reels_avg_watch_time,ig_reels_video_view_total_time"})["data"]
                row.update({d["name"]: d["values"][0]["value"] for d in ins})
            except Exception as e:
                row["reels_error"] = str(e)[:160]
        rows.append(row)
    try:
        acc = c._req("get", c.user_id, params={"fields": "followers_count,media_count"})
        return {"account": acc, "posts": rows}
    except Exception:
        return {"posts": rows}


for name, fn in [("trends", trends), ("reddit", reddit), ("hn", hn), ("questions", questions), ("instagram", instagram)]:
    safe(name, fn)

path = ROOT / "research" / f"{out['date']}.json"
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(f"::notice title=research saved::{path.name}; errors: {list(out['errors'])}")
for k, v in out["errors"].items():
    print(f"::warning title={k} failed::{v}")
