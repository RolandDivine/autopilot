"""LinkedIn editorial versions of the Zero to One series (people photos, Roland 23 Oct). Run from studio/: python days/zto1_li.py"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import li_editorial  # noqa: E402
from zto1 import DAYS, ROOT  # noqa: E402

GEN = ROOT / "assets" / "gen"
META = {
    "2026-10-23": ("people-whiteboard.png", "Part 1 of 4", "Copying is easy. ==Building from zero== is where the value is.",
                   "The business lessons from Peter Thiel's Zero to One, applied to building in Nigeria.",
                   "Ask yourself: what truth do ==few people agree with you on?==", "Next: competition is for losers"),
    "2026-10-24": ("people-market.png", "Part 2 of 4", "Ten shops, same phones, same street. ==Nobody wins.==",
                   "Why competition kills profit, and what makes a business hard to copy.",
                   "Win a small market ==completely.== Then expand.", "Next: be the last mover"),
    "2026-10-25": ("people-mentor.png", "Part 3 of 4", "Being first is overrated. ==Be the last mover.==",
                   "Time, focus and why you are not a lottery ticket.",
                   "Find the one thing. ==Go deep.==", "Next: foundations, team and sales"),
    "2026-10-26": ("people-cofounders.png", "Part 4 of 4", "Most startups die from ==bad foundations,== not bad ideas.",
                   "Co-founders, team, sales and the 7 questions every business must answer.",
                   "Which of the 7 questions is your ==weakest?==", "Zero to One, decoded · the end"),
}
EMO = re.compile(r"[\U0001F000-\U0001FAFF☀-➿️\U0001F1E6-\U0001F1FF]+")


def clean(t):
    import unicodedata
    return "".join(c for c in EMO.sub("", t) if unicodedata.category(c) != "So").strip()


for date, d in DAYS.items():
    img, tag, hook, sub, end_line, nxt = META[date]
    lessons = []
    for s in d["slides"][1:-1]:
        head = clean(s[0][1]).replace("**", "").strip()
        m = re.match(r"Lesson (\d+): (.+)", head)
        num, title = (m.group(1), m.group(2)) if m else ("+", head)
        lines = [clean(t) for _, t in s[1:]]
        lines = [re.sub(r"^\d\. ", "", x) for l in lines for x in l.split("\n")]
        lessons.append((num, title[0].upper() + title[1:], lines))
    Q = ROOT / "queue" / date
    li_editorial.build(Q / "media", d["name"] + "-ed", GEN / img, tag, hook, sub, lessons, end_line, nxt, "Business lessons")
    f = Q / "1300.json"
    j = json.loads(f.read_text())
    j["linkedin"]["media"] = f"media/{d['name']}-ed.pdf"
    f.write_text(json.dumps(j, indent=1, ensure_ascii=False))
    print(date, len(lessons) + 2, "pages")
