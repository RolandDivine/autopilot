"""Publish every slot that is due. Safe to run as often as you like: posted slots are logged and never re-posted.

    python -m autopilot.post            # real
    python -m autopilot.post --dry-run  # print payloads, post nothing
"""
import argparse
import sys
import traceback

from . import control, github, load_config
from .lint import blocked_platforms, lint_slot
from .linkedin_client import LinkedInClient
from .queue import due_slots, posted_keys, record
from .x_client import XClient
from .ig_client import InstagramClient, public_url


def run_stories(dry_run=False, now_utc=None):
    """queue/<date>/stories.json: [{"at": "0900", "media": "stories/s0900.jpg"}, ...]. Instagram only."""
    import datetime as dt
    import json
    from .queue import QUEUE, lagos_now, slot_datetime
    from .ig_client import InstagramClient, public_url
    if not load_config().get("instagram_autopost"):
        return 0
    now = lagos_now(now_utc)
    grace = dt.timedelta(minutes=load_config().get("story_grace_minutes", 90))
    done = posted_keys()
    errors, client = 0, None
    for day in sorted({(now - dt.timedelta(days=1)).date().isoformat(), now.date().isoformat()}):
        f = QUEUE / day / "stories.json"
        if not f.exists():
            continue
        issue = github.find_day_issue(day) if github.available() else None
        cmds = control.parse(github.owner_comments(issue["number"]) if issue else [])
        for st in json.loads(f.read_text(encoding="utf-8")):
            key = f"{day}/story-{st['at']}"
            when = slot_datetime(day, st["at"])
            if (key, "instagram") in done or not (when <= now <= when + grace):
                continue
            if control.paused() or ("stories", None) in cmds["skip"]:
                record(key, "instagram", {"status": "skipped"}) if not dry_run else None
                continue
            try:
                client = client or InstagramClient(dry_run)
                mid = client.publish_story(public_url(f, st["media"]))
                if not dry_run:
                    record(key, "instagram", {"status": "posted", "id": mid, "kind": "story"})
                print(f"::notice title=story {st['at']}::posted {mid}")
            except Exception as e:
                errors += 1
                print(f"::error title=story {st['at']} failed::{str(e)[:400]}".replace("\n", " "))
    return errors


def run(dry_run=False, now_utc=None):
    story_errors = run_stories(dry_run, now_utc)
    slots = due_slots(now_utc)
    if not slots:
        print("nothing due")
        return 1 if story_errors else 0
    errors = story_errors
    clients = {}

    def client(platform):
        if platform not in clients:
            clients[platform] = {"x": XClient, "linkedin": LinkedInClient, "instagram": InstagramClient}[platform](dry_run)
        return clients[platform]

    for s in slots:
        data = s.load()
        issue = github.find_day_issue(s.date) if github.available() else None
        cmds = control.parse(github.owner_comments(issue["number"]) if issue else [])
        if cmds["pause"] is not None:
            control.set_paused(cmds["pause"])
        notes = []
        if control.paused():
            print(f"{s.key}: paused, not posting")
            continue
        issues = lint_slot(data, s)
        blocked = blocked_platforms(issues)
        done = posted_keys()
        for platform in ("x", "linkedin", "instagram"):
            cfgp = data.get(platform, {})
            if not cfgp.get("enabled") or (s.key, platform) in done:
                continue
            if platform == "instagram" and not load_config().get("instagram_autopost"):
                continue  # Roland posts Instagram by hand until autopost is switched on
            if control.is_skipped(cmds, s.slot, platform):
                record(s.key, platform, {"status": "skipped"})
                notes.append(f"{platform}: skipped as you asked")
                continue
            if platform in blocked:
                msgs = "; ".join(f"{r} {d}" for lvl, p, r, d in issues if p == platform and lvl == "FAIL")
                notes.append(f"{platform}: **not posted**, check failed: {msgs}")
                errors += 1
                continue
            try:
                if platform == "x":
                    ids = client("x").post_thread(cfgp["posts"], s.path.parent)
                    url = client("x").url(ids[0]) if not dry_run else None
                    if not dry_run:
                        record(s.key, "x", {"status": "posted", "ids": ids, "url": url})
                    notes.append(f"X posted: {url}")
                elif platform == "instagram":
                    urls = [public_url(s.path, m) for m in cfgp["media"]]
                    mid, link = client("instagram").publish(urls, cfgp["caption"], cfgp.get("alt"))
                    if not dry_run:
                        record(s.key, "instagram", {"status": "posted", "id": mid, "url": link})
                    notes.append(f"Instagram posted: {link}")
                    if cfgp.get("music"):
                        notes.append(f"🎵 Add music now: {cfgp['music']} (open the post → ⋯ → Edit → add music)")
                else:
                    media = str(s.media_path(cfgp["media"])) if cfgp.get("media") else None
                    urn = client("linkedin").create_post(cfgp["text"], media, cfgp.get("media_title"))
                    if cfgp.get("first_comment"):
                        try:
                            client("linkedin").comment(urn, cfgp["first_comment"])
                        except Exception as e:  # the post is live; don't fail the slot over the comment
                            notes.append(f"LinkedIn first comment failed: {e}")
                    url = LinkedInClient.url(urn)
                    if not dry_run:
                        record(s.key, "linkedin", {"status": "posted", "urn": urn, "url": url})
                    notes.append(f"LinkedIn posted: {url}")
            except Exception as e:
                errors += 1
                traceback.print_exc()
                notes.append(f"{platform}: **failed**: {str(e)[:400]}")
                print(f"::error title={platform} failed::{str(e)[:400]}".replace("\n", " "))
        print(f"{s.key}:", *notes, sep="\n  ")
        for n in notes:
            print(f"::notice title={s.key}::{n}".replace("\n", " "))
        if issue and notes and not dry_run:
            github.comment(issue["number"], f"**{s.slot[:2]}:{s.slot[2:]} result**\n\n" + "\n".join(f"- {n}" for n in notes))
    return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    try:
        rc = run(dry_run=args.dry_run)
    except Exception as e:
        traceback.print_exc()
        print(f"::error title=autopilot crashed::{type(e).__name__}: {str(e)[:500]}".replace("\n", " "))
        rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
