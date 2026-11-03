"""Hourly safety net: if anything due today is more than 40 minutes late and still not posted, open an alert issue
(GitHub emails Roland). Posting itself never depends on this; it only shouts when GitHub's timer has stalled."""
import datetime as dt
import json

from . import github
from .queue import LOG, QUEUE, ROOT, slot_datetime

LATE = dt.timedelta(minutes=40)


def main():
    now = dt.datetime.now(dt.timezone.utc)
    day = now.date().isoformat()
    done, vids = set(), set()
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            try:
                r = json.loads(line)
                done.add((r["key"], r["platform"]))
            except Exception:
                pass
    vlog = ROOT / "log" / "videos.jsonl"
    if vlog.exists():
        for line in vlog.read_text().splitlines():
            try:
                r = json.loads(line)
                if r.get("ok") or "instagram-publish.yml', 'success'" in r.get("out", ""):
                    vids.add((r["date"], r["key"]))
            except Exception:
                pass
    late = []
    q = QUEUE / day
    for f in sorted(q.glob("[0-9][0-9][0-9][0-9].json")) if q.is_dir() else []:
        s = json.loads(f.read_text())
        for plat in ("instagram", "linkedin", "x"):
            if (s.get(plat) or {}).get("enabled") and (f"{day}/{f.stem}", plat) not in done \
                    and now > slot_datetime(day, f.stem) + LATE:
                late.append(f"{f.stem} {plat}")
    st = q / "stories.json"
    for x in json.loads(st.read_text()) if st.exists() else []:
        if (f"{day}/story-{x['at']}", "instagram") not in done and now > slot_datetime(day, x["at"]) + LATE:
            late.append(f"story {x['at']}")
    vf = QUEUE / "vo" / f"posts-{day}.json"
    for key, v in (json.loads(vf.read_text()).items() if vf.exists() else []):
        at = v.get("at")
        if at and not v.get("skip") and (day, key) not in vids:
            h, m = map(int, at.split(":"))
            if now > dt.datetime(now.year, now.month, now.day, h, m, tzinfo=dt.timezone.utc) + LATE:
                late.append(f"video {key} ({at} UTC)")
    if not late:
        print("ok: nothing overdue")
        return
    print("::warning title=overdue::" + ", ".join(late))
    tag = f"overdue-{day}"
    if github.available() and not github.find_day_issue(tag):
        github.ensure_label("action-needed", "D73A4A")
        github.create_issue(f"Posts running late ({day})",
                            "These are more than 40 minutes late and not posted yet: " + ", ".join(late) +
                            ".\n\nThe 5-minute timer keeps retrying on its own. If this stays open for an hour, "
                            "run the **post** and **videos** workflows from the Actions tab (dry_run unticked).",
                            [f"day:{tag}", "action-needed"])


if __name__ == "__main__":
    main()
