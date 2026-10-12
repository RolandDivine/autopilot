"""The posting queue.

Layout:
    queue/YYYY-MM-DD/0800.json   one file per slot (Lagos time)
    queue/YYYY-MM-DD/media/...   images and PDFs referenced by those files
    log/posted.jsonl             one line per published post (the source of truth for "already posted")

Slot file format:
{
  "title": "Crypto from zero 1: What money is",
  "kind": "news" | "lesson" | "story" | "spotlight",
  "x": {
    "enabled": true,
    "posts": [ {"text": "...", "media": ["media/crypto1-cover.png"]}, {"text": "..."} ]
  },
  "linkedin": {
    "enabled": true,
    "text": "...",
    "media": "media/crypto1.pdf",          # optional: .pdf (document) or .png/.jpg (image)
    "media_title": "Crypto from zero 1",    # shown on LinkedIn document posts
    "first_comment": "Sources: ..."         # optional
  }
}
"""
import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path

from . import ROOT, load_config

QUEUE = ROOT / "queue"
LOG = ROOT / "log" / "posted.jsonl"


def lagos_now(now_utc=None):
    cfg = load_config()
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    return now_utc.astimezone(dt.timezone(dt.timedelta(hours=cfg["utc_offset_hours"])))


@dataclass
class Slot:
    date: str   # YYYY-MM-DD
    slot: str   # HHMM
    path: Path

    @property
    def key(self):
        return f"{self.date}/{self.slot}"

    def load(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def media_path(self, rel):
        return self.path.parent / rel


def slot_datetime(date, slot, cfg=None):
    cfg = cfg or load_config()
    tz = dt.timezone(dt.timedelta(hours=cfg["utc_offset_hours"]))
    d = dt.date.fromisoformat(date)
    return dt.datetime(d.year, d.month, d.day, int(slot[:2]), int(slot[2:]), tzinfo=tz)


def posted_keys():
    if not LOG.exists():
        return set()
    keys = set()
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            keys.add((rec["key"], rec["platform"]))
    return keys


def record(key, platform, result):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    rec = {"key": key, "platform": platform, "at": dt.datetime.now(dt.timezone.utc).isoformat(), **result}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def due_slots(now_utc=None):
    """Slots whose time has passed within the grace window and that still have an unposted platform."""
    cfg = load_config()
    now = lagos_now(now_utc)
    grace = dt.timedelta(minutes=cfg["slot_grace_minutes"])
    done = posted_keys()
    out = []
    for day in {(now - dt.timedelta(days=1)).date().isoformat(), now.date().isoformat()}:
        folder = QUEUE / day
        if not folder.is_dir():
            continue
        for slot in cfg["slots"]:
            p = folder / f"{slot}.json"
            if not p.exists():
                continue
            when = slot_datetime(day, slot, cfg)
            if when <= now <= when + grace:
                s = Slot(day, slot, p)
                data = s.load()
                pending = [pl for pl in ("x", "linkedin")
                           if data.get(pl, {}).get("enabled") and (s.key, pl) not in done]
                if pending:
                    out.append(s)
    return sorted(out, key=lambda s: (s.date, s.slot))
