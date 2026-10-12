"""Publish every slot that is due. Safe to run as often as you like: posted slots are logged and never re-posted.

    python -m autopilot.post            # real
    python -m autopilot.post --dry-run  # print payloads, post nothing
"""
import argparse
import sys
import traceback

from . import control, github
from .lint import blocked_platforms, lint_slot
from .linkedin_client import LinkedInClient
from .queue import due_slots, posted_keys, record
from .x_client import XClient


def run(dry_run=False, now_utc=None):
    slots = due_slots(now_utc)
    if not slots:
        print("nothing due")
        return 0
    errors = 0
    clients = {}

    def client(platform):
        if platform not in clients:
            clients[platform] = XClient(dry_run) if platform == "x" else LinkedInClient(dry_run)
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
        for platform in ("x", "linkedin"):
            cfgp = data.get(platform, {})
            if not cfgp.get("enabled") or (s.key, platform) in done:
                continue
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
        print(f"{s.key}:", *notes, sep="\n  ")
        if issue and notes and not dry_run:
            github.comment(issue["number"], f"**{s.slot[:2]}:{s.slot[2:]} result**\n\n" + "\n".join(f"- {n}" for n in notes))
    return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.exit(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
