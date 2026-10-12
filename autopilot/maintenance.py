"""Nightly upkeep: X metrics, LinkedIn token warning, media pruning.

    python -m autopilot.maintenance
"""
import datetime as dt
import json
import os
import shutil

from . import ROOT, github, load_config
from .queue import LOG, QUEUE

METRICS = ROOT / "log" / "metrics.jsonl"


def collect_x_metrics():
    if not os.environ.get("X_API_KEY") or not LOG.exists():
        return 0
    from .x_client import XClient
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=14)
    first_ids = {}
    for line in LOG.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("platform") == "x" and rec.get("status") == "posted" and rec.get("ids"):
            if dt.datetime.fromisoformat(rec["at"]) >= cutoff:
                first_ids[rec["ids"][0]] = rec["key"]
    if not first_ids:
        return 0
    m = XClient().metrics(list(first_ids))
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    with METRICS.open("a", encoding="utf-8") as f:
        for tid, pm in m.items():
            f.write(json.dumps({"at": now, "platform": "x", "key": first_ids[tid], "id": tid, **pm}) + "\n")
    return len(m)


def check_linkedin_token():
    exp = os.environ.get("LINKEDIN_TOKEN_EXPIRES")  # YYYY-MM-DD, printed by scripts/linkedin_auth.py
    if not exp:
        return None
    days = (dt.date.fromisoformat(exp) - dt.date.today()).days
    if days <= 7 and github.available():
        title = f"LinkedIn sign-in expires in {days} days"
        body = ("Autopilot will stop posting to LinkedIn when it expires.\n\n"
                "Fix (2 minutes): on your computer run `python scripts/linkedin_auth.py`, then update the "
                "`LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_TOKEN_EXPIRES` secrets in Settings → Secrets and variables → Actions.")
        github.ensure_label("action-needed", "D73A4A")
        # one warning per week is enough
        r = github.find_day_issue(f"token-{exp}")
        if not r:
            github.create_issue(title, body, [f"day:token-{exp}", "action-needed"])
    return days


def prune_media():
    days = load_config()["prune_media_after_days"]
    cutoff = dt.date.today() - dt.timedelta(days=days)
    removed = 0
    for folder in QUEUE.glob("20*-*-*"):
        try:
            if dt.date.fromisoformat(folder.name) < cutoff and (folder / "media").exists():
                shutil.rmtree(folder / "media")
                removed += 1
        except ValueError:
            continue
    return removed


def main():
    print("x metrics rows:", collect_x_metrics())
    print("linkedin token days left:", check_linkedin_token())
    print("media folders pruned:", prune_media())


if __name__ == "__main__":
    main()
