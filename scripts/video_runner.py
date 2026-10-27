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
    now = dt.datetime.now(dt.timezone.utc)
    day = os.environ.get("DAY") or now.date().isoformat()
    f = os.path.join(ROOT, "queue", "vo", f"posts-{day}.json")
    if not os.path.exists(f):
        print(f"no videos for {day}")
        return
    log = os.path.join(ROOT, "log", "videos.jsonl")
    done = set()
    if os.path.exists(log):
        for line in open(log):
            try:
                r = json.loads(line)
                if r.get("ok"):
                    done.add((r["date"], r["key"]))
            except Exception:
                pass
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
        subprocess.run(["git", "add", log], cwd=ROOT)
        subprocess.run(["git", "commit", "-qm", f"video {day} {key}: {'posted' if ok else 'failed'}"], cwd=ROOT)
        subprocess.run(["git", "push", "-q"], cwd=ROOT)


if __name__ == "__main__":
    main()
