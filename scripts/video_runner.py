"""Post today's videos on time from GitHub Actions (workflow: videos). No Claude session needed.

Reads queue/vo/posts-<UTC date>.json. Each entry posts once, at its "at" time (UTC "HH:MM"); defaults: keys starting
"ex" -> 11:00, "kobo" -> 17:00, "liclip" -> 07:00. Entries can set "skip": true. Results go to log/videos.jsonl.
"""
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = {"ex": "11:00", "kobo": "17:00", "liclip": "07:00"}


def main():
    # Roland, 28 Oct 2026: "don't skip anything". GitHub can drop scheduled runs for hours, so a video that is late
    # still posts, and yesterday's file is checked too (a video missed before midnight UTC posts the next morning).
    now = dt.datetime.now(dt.timezone.utc)
    days = [os.environ["DAY"]] if os.environ.get("DAY") else [(now - dt.timedelta(days=1)).date().isoformat(), now.date().isoformat()]
    for day in days:
        run_day(day, now)


def load_done(log, now):
    """(date, key) pairs already on Instagram, or claimed by a run in the last 45 minutes."""
    done = set()
    if not os.path.exists(log):
        return done
    for line in open(log):
        try:
            r = json.loads(line)
            # once Instagram has it, never re-post the video (1 Nov: a YouTube failure re-posted a Reel twice)
            if r.get("ok") or "instagram-publish.yml', 'success'" in r.get("out", ""):
                done.add((r["date"], r["key"]))
            elif r.get("claim") and now - dt.datetime.fromisoformat(r["at"]) < dt.timedelta(minutes=45):
                done.add((r["date"], r["key"]))
        except Exception:
            pass
    return done


def push_log(log, msg):
    subprocess.run(["git", "add", log], cwd=ROOT)
    subprocess.run(["git", "commit", "-qm", msg], cwd=ROOT)
    for _ in range(4):
        if subprocess.run(["git", "push", "-q"], cwd=ROOT).returncode == 0:
            return True
        subprocess.run(["git", "pull", "-q", "--rebase"], cwd=ROOT)
    return False


def run_day(day, now):
    f = os.path.join(ROOT, "queue", "vo", f"posts-{day}.json")
    if not os.path.exists(f):
        print(f"no videos for {day}")
        return
    log = os.path.join(ROOT, "log", "videos.jsonl")
    done = load_done(log, now)
    entries = json.load(open(f))
    for key, d in entries.items():
        if d.get("skip") or (day, key) in done:
            continue
        at = d.get("at") or next((v for k, v in DEFAULT.items() if key.startswith(k)), None)
        if not at:
            continue
        h, m = map(int, at.split(":"))
        if now < dt.datetime.fromisoformat(day).replace(hour=h, minute=m, tzinfo=dt.timezone.utc) and not os.environ.get("FORCE"):
            continue
        # 4 Nov 2026: two overlapping runs both posted ex15. Re-read the latest log and push a claim line
        # BEFORE publishing; a fresh claim (<45 min) from another run means skip.
        subprocess.run(["git", "pull", "-q", "--rebase"], cwd=ROOT)
        if (day, key) in load_done(log, now):
            print(f"{key}: already posted or claimed by another run, skipping")
            continue
        with open(log, "a") as fh:
            fh.write(json.dumps({"date": day, "key": key, "at": now.isoformat(), "claim": True}) + "\n")
        if not push_log(log, f"video {day} {key}: claim"):
            print(f"{key}: could not push claim, will retry next tick")
            continue
        args = [sys.executable, os.path.join(ROOT, "studio", "post_video.py"), f"queue/vo/posts-{day}.json", key]
        if key.startswith("liclip"):
            args.append("nostory")
        p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
        out = (p.stdout + p.stderr)[-3000:]
        ok = p.returncode == 0 and "'failure'" not in out and "timed out" not in out
        print(f"::notice title={key} {'posted' if ok else 'FAILED'}::{out[-900:]}")
        subprocess.run(["git", "pull", "-q", "--rebase"], cwd=ROOT)
        with open(log, "a") as fh:
            fh.write(json.dumps({"date": day, "key": key, "at": now.isoformat(), "ok": ok, "out": out[-1500:]}) + "\n")
        push_log(log, f"video {day} {key}: {'posted' if ok else 'failed'}")


if __name__ == "__main__":
    main()
