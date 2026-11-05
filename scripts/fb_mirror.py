"""Copy Instagram feed posts to the Facebook Page.

MODE=export  -> writes log/ig_media.json (every feed post: type, caption, date, stats) and prints the Page details.
MODE=publish -> reads log/fb_plan.json, a list of {"ig_id", "caption", "pin"(optional)} in posting order (oldest first).
                Media is fetched fresh from Instagram at post time (its CDN links expire).
                Carousels and photos -> multi-photo Page post; Reels/videos -> Facebook Reel.
                Already-mirrored ids (log/fb_mirrored.jsonl) are skipped, so a re-run never double-posts.
"""
import json
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import ROOT, load_config  # noqa: E402
from autopilot.fb_caption import fb_caption, first_line  # noqa: E402
from autopilot.fb_client import GRAPH, FacebookClient, FacebookError  # noqa: E402
from autopilot.ig_client import InstagramClient  # noqa: E402

DONE = ROOT / "log" / "fb_mirrored.jsonl"


def export(ig, fb):
    print("page:", json.dumps(fb._req("GET", fb.page_id, params={"fields": "name,username,category,about,link"})))
    items, after = [], None
    while True:
        p = {"fields": "id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count",
             "limit": 50}
        if after:
            p["after"] = after
        d = ig._req("get", f"{ig.user_id}/media", params=p)
        items += d.get("data", [])
        after = d.get("paging", {}).get("cursors", {}).get("after")
        if not d.get("paging", {}).get("next"):
            break
    items.sort(key=lambda m: m["timestamp"])
    (ROOT / "log" / "ig_media.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
    print(f"exported {len(items)} posts")


def media_urls(ig, ig_id):
    m = ig._req("get", ig_id, params={"fields": "media_type,media_url,children{media_type,media_url}"})
    if m["media_type"] == "CAROUSEL_ALBUM":
        kids = m["children"]["data"]
        return "carousel", [(k["media_type"], k["media_url"]) for k in kids]
    return m["media_type"].lower(), [(m["media_type"], m["media_url"])]


def post_reel(fb, video_url, caption):
    start = fb._req("POST", f"{fb.page_id}/video_reels", data={"upload_phase": "start"})
    vid = start["video_id"]
    # Facebook can't fetch Instagram's CDN links, so download here and upload the bytes.
    dl = requests.get(video_url, timeout=300)
    if not dl.ok:
        raise FacebookError(f"download from Instagram failed: HTTP {dl.status_code}")
    r = requests.post(f"https://rupload.facebook.com/video-upload/v24.0/{vid}", timeout=600, data=dl.content,
                      headers={"Authorization": f"OAuth {fb.token}", "offset": "0",
                               "file_size": str(len(dl.content))})
    if not r.ok:
        raise FacebookError(f"reel upload failed: HTTP {r.status_code} {r.text[:300]}")
    fb._req("POST", f"{fb.page_id}/video_reels", data={
        "upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED", "description": caption})
    for _ in range(40):  # wait until Facebook has processed and published it
        try:
            st = fb._req("GET", vid, params={"fields": "status,post_id,permalink_url"})
        except FacebookError:  # Facebook sometimes can't read a Reel for a moment after publishing
            time.sleep(8)
            continue
        phase = st.get("status", {}).get("video_status")
        if phase == "ready" and st.get("status", {}).get("publishing_phase", {}).get("status") != "in_progress":
            return {"id": st.get("post_id") or vid, "video_id": vid, "url": st.get("permalink_url")}
        if phase == "error":
            raise FacebookError(f"reel processing failed: {st}")
        time.sleep(8)
    return {"id": vid, "video_id": vid, "note": "still processing"}


def publish(ig, fb):
    plan = json.loads((ROOT / "log" / "fb_plan.json").read_text())
    done = {json.loads(l)["ig_id"] for l in DONE.read_text().splitlines()} if DONE.exists() else set()
    limit = int(os.environ.get("LIMIT") or 999)
    n = bad = 0
    for item in plan:
        if item["ig_id"] in done or n >= limit:
            continue
        try:
            kind, media = media_urls(ig, item["ig_id"])
            if kind in ("video", "reels"):
                res = post_reel(fb, media[0][1], item["caption"])
            else:
                photos = [u for t, u in media if t == "IMAGE"]
                res = fb.post_photos(photos, item["caption"])
            if item.get("pin"):
                try:
                    fb._req("POST", res["id"], data={"is_pinned": "true"})
                    res["pinned"] = True
                except FacebookError as e:
                    res["pinned"] = f"failed: {e}"
            rec = {"ig_id": item["ig_id"], "kind": kind, "fb": res, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            with DONE.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            n += 1
            print(f"OK {item['ig_id']} {kind} -> {res}")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"FAILED {item['ig_id']}: {e}")
        time.sleep(20)  # pace it so Facebook doesn't treat the batch as spam
    print(f"::notice::posted {n}, failed {bad}, skipped {len(done)} already done")


def record(rec):
    rec["at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with DONE.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def sync(ig, fb):
    """Daily flow: copy every new Instagram feed post / Reel (newer than facebook_sync_since) to the Page."""
    since = load_config().get("facebook_sync_since", "2026-11-05T11:05:00+0000")
    done = {json.loads(l)["ig_id"] for l in DONE.read_text().splitlines()} if DONE.exists() else set()
    recent = ig._req("get", f"{ig.user_id}/media", params={
        "fields": "id,caption,media_type,timestamp", "limit": 25}).get("data", [])
    recent.sort(key=lambda m: m["timestamp"])
    # Instagram sometimes ends up with the same post twice; Facebook gets it once.
    seen = {first_line(m.get("caption")) for m in recent if m["id"] in done}
    new = [m for m in recent if m["timestamp"] > since and m["id"] not in done]
    n = 0
    for m in new:
        head = first_line(m.get("caption"))
        if head and head in seen:
            record({"ig_id": m["id"], "kind": "skipped", "reason": "duplicate of an Instagram post already copied"})
            print(f"SKIP duplicate {m['id']}: {head[:60]}")
            continue
        caption = fb_caption(m.get("caption"), m["media_type"])
        try:
            kind, media = media_urls(ig, m["id"])
        except KeyError:  # Instagram withholds the file (e.g. licensed music): nothing to copy
            record({"ig_id": m["id"], "kind": "skipped", "reason": "Instagram gives no media file"})
            print(f"::warning::Instagram post {m['id']} has no downloadable file; upload it to Facebook by hand")
            continue
        try:
            if kind in ("video", "reels"):
                res = post_reel(fb, media[0][1], caption)
            else:
                res = fb.post_photos([u for t, u in media if t == "IMAGE"], caption)
        except Exception as e:  # noqa: BLE001  (retried on the next run)
            print(f"::warning::Facebook copy of {m['id']} failed: {e}")
            continue
        record({"ig_id": m["id"], "kind": kind, "fb": res, "first_line": head})
        seen.add(head)
        n += 1
        print(f"OK {m['id']} {kind} -> {res}")
        time.sleep(20)
    print(f"::notice::Facebook: {n} new post(s) copied" if n else "nothing new for Facebook")


def main():
    ig, fb = InstagramClient(), FacebookClient()
    {"export": export, "sync": sync}.get(os.environ.get("MODE"), publish)(ig, fb)


if __name__ == "__main__":
    main()
