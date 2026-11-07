"""Comment-to-DM and DM keyword auto-replies (Roland, 7 Nov 2026).

Someone comments PLAN / SIGNALS / SWAN on a post whose caption asks for it -> we reply publicly under the comment
("Sent! Check your DMs") and send ONE private reply DM with the content (Instagram's private-reply API).
Someone DMs the keyword (incl. message requests the API returns) -> we reply with the same content.

Texts live in config/keyword_replies.json. Handled comment/message IDs are kept in state/ig_keywords.json so nobody
gets the same reply twice. Modes:  python scripts/ig_keywords.py [run|check|dry]
Needs the Instagram token to carry instagram_business_manage_comments and instagram_business_manage_messages.
"""
import json
import os
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.ig_client import InstagramClient, InstagramError  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config/keyword_replies.json").read_text())["keywords"]
STATE = ROOT / "state/ig_keywords.json"
MODE = (sys.argv[1] if len(sys.argv) > 1 else "run").lower()


def load_state():
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {"comments": {}, "messages": {}, "log": []}


def keyword_in(text, allowed):
    """A comment/DM counts if it is basically just the keyword (<= 4 words), e.g. 'PLAN', 'plan 🙏', 'Signals please'."""
    words = re.findall(r"[A-Za-z]+", text or "")
    if not words or len(words) > 4:
        return None
    for w in words:
        if w.upper() in allowed:
            return w.upper()
    return None


def name_of(username):
    return f"@{username}" if username else "there"


def main():
    c = InstagramClient()
    st = load_state()
    sent = 0

    if MODE == "check":
        for label, path, params in [
            ("media", f"{c.user_id}/media", {"fields": "id,comments_count", "limit": 15}),
            ("conversations", f"{c.user_id}/conversations", {"platform": "instagram", "limit": 3}),
        ]:
            try:
                d = c._req("get", path, params=params).get("data", [])  # never print raw responses: paging URLs carry the token
                print(label, "OK", len(d), "items", [{k: v for k, v in x.items() if k in ("id", "comments_count")} for x in d])
                if label == "media":
                    for m in d:
                        if m.get("comments_count"):
                            cs = c._req("get", f"{m['id']}/comments", params={"fields": "id", "limit": 5}).get("data", [])
                            print("  comments on", m["id"], "count", m["comments_count"], "returned", len(cs))
            except InstagramError as e:
                print(label, "FAILED", str(e).split("access_token")[0][:300])
        return

    # 1) comments on posts whose caption asks for a keyword
    media = c._req("get", f"{c.user_id}/media", params={"fields": "id,caption,timestamp,comments_count", "limit": 30}).get("data", [])
    for m in media:
        cap = (m.get("caption") or "").upper()
        allowed = {k for k in CFG if re.search(rf"COMMENT\s+[\"“]?{k}\b", cap)}
        if not allowed or not m.get("comments_count"):
            continue
        try:
            cs = c._req("get", f"{m['id']}/comments", params={"fields": "id,text,username,timestamp,from", "limit": 50}).get("data", [])
        except InstagramError as e:
            print("comments FAILED (token needs instagram_business_manage_comments?):", e)
            break
        for x in cs:
            if x["id"] in st["comments"] or x.get("username") == c.username:
                continue
            kw = keyword_in(x.get("text"), allowed)
            if not kw:
                continue
            k = CFG[kw]
            dm = k["dm"].replace("{name}", name_of(x.get("username")))[:1000]
            res = {"kw": kw, "user": x.get("username"), "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            if MODE == "dry":
                print("WOULD reply", x["id"], res)
                continue
            try:
                c._req("post", f"{c.user_id}/messages", json={"recipient": {"comment_id": x["id"]}, "message": {"text": dm}})
                res["dm"] = "ok"
            except InstagramError as e:
                res["dm"] = f"FAILED {str(e)[:200]}"
            try:
                txt = random.choice(k["comment_replies"]) if res["dm"] == "ok" else "DM me the word " + kw + " and I'll send it 📩"
                c._req("post", f"{x['id']}/replies", data={"message": f"@{x.get('username')} {txt}" if x.get("username") else txt})
                res["reply"] = "ok"
            except InstagramError as e:
                res["reply"] = f"FAILED {str(e)[:200]}"
            st["comments"][x["id"]] = res
            st["log"] = (st["log"] + [res])[-300:]
            sent += 1
            print("comment", x["id"], res)
            time.sleep(3)  # stay well under Instagram's rate limits

    # 2) DMs that are just the keyword
    try:
        convs = c._req("get", f"{c.user_id}/conversations", params={"platform": "instagram", "fields": "id,updated_time", "limit": 25}).get("data", [])
    except InstagramError as e:
        print("conversations FAILED (token needs instagram_business_manage_messages?):", e)
        convs = []
    for cv in convs:
        try:
            msgs = c._req("get", cv["id"], params={"fields": "messages.limit(5){id,message,from,created_time}"}).get("messages", {}).get("data", [])
        except InstagramError as e:
            print("messages FAILED", cv["id"], e)
            continue
        for msg in msgs[:3]:  # newest first; only look at recent messages
            frm = msg.get("from") or {}
            if msg["id"] in st["messages"] or frm.get("id") == c.user_id or frm.get("username") == c.username:
                continue
            kw = keyword_in(msg.get("message"), set(CFG))
            if not kw:
                continue
            dm = CFG[kw]["dm"].replace("{name}", name_of(frm.get("username")))[:1000]
            res = {"kw": kw, "user": frm.get("username"), "dm_in": True, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            if MODE == "dry":
                print("WOULD dm", msg["id"], res)
                continue
            try:
                c._req("post", f"{c.user_id}/messages", json={"recipient": {"id": frm["id"]}, "message": {"text": dm}})
                res["dm"] = "ok"
            except InstagramError as e:
                res["dm"] = f"FAILED {str(e)[:200]}"
            st["messages"][msg["id"]] = res
            st["log"] = (st["log"] + [res])[-300:]
            sent += 1
            print("dm", msg["id"], res)
            time.sleep(3)

    if MODE != "dry":
        STATE.parent.mkdir(exist_ok=True)
        STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False))
    print(f"::notice title=keyword replies::{sent} sent")


if __name__ == "__main__":
    main()
