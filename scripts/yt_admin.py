"""Manage the YouTube channel (Actions -> youtube-admin). OPS is a JSON list of operations, run in order:

  {"op": "list_videos"}                                   -> every upload: id, title, privacy, views (into the job summary)
  {"op": "set_privacy", "ids": ["..."], "privacy": "private"}   (public / unlisted / private; never deletes)
  {"op": "update_video", "id": "...", "title": "...", "description": "...", "tags": [...]}
  {"op": "update_channel", "description": "...", "keywords": "...", "trailer": "<video id>", "country": "NG"}
  {"op": "create_playlist", "title": "...", "description": "...", "privacy": "public", "video_ids": [...]}
  {"op": "add_to_playlist", "playlist_id": "...", "video_ids": [...]}
  {"op": "list_sections"} / {"op": "set_sections", "sections": [<channelSection resources>]}
  {"op": "banner", "path": "assets/youtube/banner.jpg"}
  {"op": "watermark", "path": "assets/youtube/watermark.png"}
  {"op": "caption", "id": "<video id>", "path": "<.srt or .vtt>", "language": "en"}
  {"op": "analytics", "days": 28}                         -> views, watch time, subs per video
  {"op": "list_comments", "max": 50} / {"op": "reply", "comment_id": "...", "text": "..."}
  {"op": "hide_comment", "comment_id": "..."}             (sets moderation status to heldForReview)
Results go to the job summary and to log/youtube/<date>-<op>.json is NOT written (repo is public): summary only.
"""
import datetime as dt
import json
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.yt_client import YouTubeClient  # noqa: E402

c = YouTubeClient()
ch = c.api("GET", "channels", {"part": "id,snippet,brandingSettings,contentDetails", "mine": "true"})["items"][0]
CID, UPLOADS = ch["id"], ch["contentDetails"]["relatedPlaylists"]["uploads"]
out = []


def say(title, data):
    out.append(f"### {title}\n```json\n{json.dumps(data, indent=1, ensure_ascii=False)[:60000]}\n```")
    txt = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    parts = [txt[i:i + 3000] for i in range(0, len(txt), 3000)][:30]
    for n, part in enumerate(parts):  # annotations are how results are read back (max 10 per level)
        lvl = ("notice", "warning", "error")[n // 10]
        print(f"::{lvl} title={title} {n + 1}/{len(parts)}::{part}")


def uploads():
    ids, tok = [], None
    while True:
        r = c.api("GET", "playlistItems", {"part": "contentDetails", "playlistId": UPLOADS, "maxResults": 50, **({"pageToken": tok} if tok else {})})
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        tok = r.get("nextPageToken")
        if not tok:
            return ids


def videos(ids):
    res = []
    for i in range(0, len(ids), 50):
        res += c.api("GET", "videos", {"part": "snippet,status,statistics,contentDetails", "id": ",".join(ids[i:i + 50])}).get("items", [])
    return res


def upload_media(url, path, mime, params):
    with open(path, "rb") as f:
        r = requests.post(url, headers={**c.h, "Content-Type": mime}, params=params, data=f, timeout=300)
    if not r.ok:
        raise RuntimeError(f"{url}: HTTP {r.status_code} {r.text[:300]}")
    return r.json() if r.text else {}


def run(o):
    op = o["op"]
    if op == "list_videos":
        say("videos", [{"id": v["id"], "title": v["snippet"]["title"], "privacy": v["status"]["privacyStatus"],
                        "published": v["snippet"]["publishedAt"][:10], "views": v.get("statistics", {}).get("viewCount")}
                       for v in videos(uploads())])
    elif op == "set_privacy":
        assert o["privacy"] in ("public", "unlisted", "private")
        for v in videos(o["ids"]):
            c.api("PUT", "videos", {"part": "status"}, {"id": v["id"], "status": {**v["status"], "privacyStatus": o["privacy"]}})
        say("privacy set", {"ids": o["ids"], "privacy": o["privacy"]})
    elif op == "update_video":
        v = videos([o["id"]])[0]
        sn = {k: v["snippet"][k] for k in ("title", "description", "tags", "categoryId") if k in v["snippet"]}
        sn.update({k: o[k] for k in ("title", "description", "tags") if k in o})
        c.api("PUT", "videos", {"part": "snippet"}, {"id": o["id"], "snippet": sn})
        say("video updated", {"id": o["id"], "title": sn["title"]})
    elif op == "update_channel":
        b = ch["brandingSettings"]
        bc = b.setdefault("channel", {})
        for k, key in (("description", "description"), ("keywords", "keywords"), ("trailer", "unsubscribedTrailer"), ("country", "country")):
            if k in o:
                bc[key] = o[k]
        c.api("PUT", "channels", {"part": "brandingSettings"}, {"id": CID, "brandingSettings": {"channel": bc}})
        say("channel updated", {k: o[k] for k in o if k != "op"})
    elif op == "create_playlist":
        p = c.api("POST", "playlists", {"part": "snippet,status"}, {"snippet": {"title": o["title"], "description": o.get("description", "")},
                                                                    "status": {"privacyStatus": o.get("privacy", "public")}})
        for vid in o.get("video_ids", []):
            c.api("POST", "playlistItems", {"part": "snippet"}, {"snippet": {"playlistId": p["id"], "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        say("playlist created", {"id": p["id"], "title": o["title"], "videos": len(o.get("video_ids", []))})
    elif op == "add_to_playlist":
        for vid in o["video_ids"]:
            c.api("POST", "playlistItems", {"part": "snippet"}, {"snippet": {"playlistId": o["playlist_id"], "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        say("added to playlist", o)
    elif op == "list_sections":
        say("sections", c.api("GET", "channelSections", {"part": "snippet,contentDetails", "mine": "true"}).get("items", []))
    elif op == "set_sections":
        for s in c.api("GET", "channelSections", {"part": "id", "mine": "true"}).get("items", []):
            c.api("DELETE", "channelSections", {"id": s["id"]})
        for i, s in enumerate(o["sections"]):
            s.setdefault("snippet", {})["position"] = i
            c.api("POST", "channelSections", {"part": "snippet,contentDetails"}, s)
        say("sections set", len(o["sections"]))
    elif op == "banner":
        url = upload_media("https://www.googleapis.com/upload/youtube/v3/channelBanners/insert", o["path"], "image/jpeg", {})["url"]
        c.api("PUT", "channels", {"part": "brandingSettings"}, {"id": CID, "brandingSettings": {**{"channel": ch["brandingSettings"]["channel"]}, "image": {"bannerExternalUrl": url}}})
        say("banner set", {"path": o["path"]})
    elif op == "watermark":
        meta = {"timing": {"type": "offsetFromEnd", "offsetMs": 15000, "durationMs": 15000}, "position": {"type": "corner", "cornerPosition": "topRight"}}
        r = requests.post("https://www.googleapis.com/upload/youtube/v3/watermarks/set", headers=c.h, timeout=120,
                          params={"channelId": CID, "uploadType": "multipart"},
                          files={"meta": (None, json.dumps(meta), "application/json"), "media": (os.path.basename(o["path"]), open(o["path"], "rb"), "image/png")})
        if not r.ok:
            raise RuntimeError(f"watermark: HTTP {r.status_code} {r.text[:300]}")
        say("watermark set", {"path": o["path"]})
    elif op == "caption":
        r = requests.post("https://www.googleapis.com/upload/youtube/v3/captions", headers=c.h, timeout=120,
                          params={"part": "snippet", "uploadType": "multipart"},
                          files={"meta": (None, json.dumps({"snippet": {"videoId": o["id"], "language": o.get("language", "en"), "name": "English"}}), "application/json"),
                                 "media": (os.path.basename(o["path"]), open(o["path"], "rb"), "application/octet-stream")})
        if not r.ok:
            raise RuntimeError(f"caption: HTTP {r.status_code} {r.text[:300]}")
        say("caption added", {"id": o["id"]})
    elif op == "analytics":
        end = dt.date.today()
        start = end - dt.timedelta(days=int(o.get("days", 28)))
        r = c.api("GET", "reports", {"ids": "channel==MINE", "startDate": start.isoformat(), "endDate": end.isoformat(),
                                     "metrics": "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,likes,shares",
                                     "dimensions": "video", "sort": "-views", "maxResults": 50},
                  base="https://youtubeanalytics.googleapis.com/v2")
        say("analytics", {"columns": [h["name"] for h in r.get("columnHeaders", [])], "rows": r.get("rows", [])})
    elif op == "list_comments":
        r = c.api("GET", "commentThreads", {"part": "snippet", "allThreadsRelatedToChannelId": CID, "maxResults": o.get("max", 50)})
        say("comments", [{"id": t["snippet"]["topLevelComment"]["id"], "video": t["snippet"]["videoId"],
                          "author": t["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                          "text": t["snippet"]["topLevelComment"]["snippet"]["textOriginal"][:300]} for t in r.get("items", [])])
    elif op == "reply":
        c.api("POST", "comments", {"part": "snippet"}, {"snippet": {"parentId": o["comment_id"], "textOriginal": o["text"]}})
        say("replied", {"comment_id": o["comment_id"]})
    elif op == "hide_comment":
        c.api("POST", "comments/setModerationStatus", {"id": o["comment_id"], "moderationStatus": "heldForReview"})
        say("comment held", {"comment_id": o["comment_id"]})
    else:
        raise SystemExit(f"unknown op {op}")

failed = False
for o in json.loads(os.environ.get("OPS") or "[]"):
    try:
        run(o)
    except Exception as e:
        failed = True
        print(f"::error title={o.get('op')} failed::{type(e).__name__}: {str(e)[:900]}".replace("\n", " "))
        break

with open(os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null"), "a") as f:
    f.write("\n\n".join(out))
sys.exit(1 if failed else 0)
