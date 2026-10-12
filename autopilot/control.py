"""Read Roland's commands from the day's review issue comments.

Commands (one per comment or one per line, case-insensitive):
    skip 8am | skip 1pm | skip 7pm | skip all
    skip 1pm x        skip only X for that slot (also: linkedin)
    pause             stop all posting until "resume" (applies from this day on)
    resume
"""
import json
import re

from . import ROOT

SLOT_WORDS = {"8am": "0800", "8": "0800", "0800": "0800", "morning": "0800", "news": "0800",
              "1pm": "1300", "13": "1300", "1300": "1300", "afternoon": "1300",
              "7pm": "1900", "19": "1900", "1900": "1900", "evening": "1900"}
PLATFORMS = {"x": "x", "twitter": "x", "linkedin": "linkedin", "li": "linkedin", "instagram": "instagram", "ig": "instagram", "insta": "instagram"}
CONTROL = ROOT / "control.json"


def parse(comments):
    """Return {"skip": {(slot, platform)}, "pause": bool|None}. platform None = both."""
    skip, pause = set(), None
    for body in comments:
        for line in body.lower().splitlines():
            line = line.strip()
            m = re.match(r"^skip\s+(\S+)(?:\s+(\S+))?", line)
            if m:
                target, plat = m.group(1), PLATFORMS.get(m.group(2) or "", None)
                if target == "stories":
                    skip.add(("stories", None))
                    continue
                slots = ["0800", "1300", "1900"] if target == "all" else [SLOT_WORDS.get(target)]
                for s in slots:
                    if s:
                        skip.add((s, plat))
            elif line.startswith("pause"):
                pause = True
            elif line.startswith("resume"):
                pause = False
    return {"skip": skip, "pause": pause}


def is_skipped(cmds, slot, platform):
    return (slot, None) in cmds["skip"] or (slot, platform) in cmds["skip"]


def paused():
    if CONTROL.exists():
        return bool(json.loads(CONTROL.read_text()).get("paused"))
    return False


def set_paused(value):
    CONTROL.write_text(json.dumps({"paused": bool(value)}, indent=2) + "\n")
