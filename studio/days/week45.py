"""Sun 1 – Mon 2 Nov 2026 (nightly build, 28 Oct). Run from repo root:  python3 studio/days/week45.py

Plan:
  Sun 1   No LinkedIn (weekend). No Instagram carousel (this week already had 2: fake alert 28 Oct, fake job 31 Oct).
          12:00 Reel ex18 rug pull / honeypot (Fish ELITE).  18:00 Kobo 15, season finale (stories + Reel off).
  Mon 2   08:00 LinkedIn "what I built or broke": the GitHub scheduler gap that skipped the 28 Oct 8 AM post (real, from
          our own Actions history). 12:00 Reel ex10 Arup deepfake (Fish ELITE). Kobo season is finished.
Stories 09/11/14/17/21 both days, abstract images only.
Facts: GitHub Actions run history 27-28 Oct (runs at 01:19 and 12:48 UTC on 28 Oct, nothing between); GitHub Docs on schedule
delays/drops. No invented anecdotes.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "assets" / "gen"

LI_MON = """Your scheduled job will not always run on schedule.

Mine didn't. Here's what happened, and what I'd tell any builder who relies on one.

My content system, Autopilot, publishes my posts for me. Until last week, publishing ran inside AI chat sessions. Then I hit a usage limit and everything froze for three days. Nothing went out.

So I moved publishing to GitHub Actions: a scheduled job every hour, no chat session needed.

The next day, Wednesday, GitHub's scheduler went quiet for almost 12 hours. My 8 AM post never went out. No error. No alert. Just silence.

What it taught me:

→ A schedule is a request, not a promise. GitHub's own docs say scheduled runs can be delayed under heavy load, and some can be dropped.

→ "Nothing failed" is not the same as "it worked". Check that the post exists, not just that the job didn't crash.

→ Every single point of failure is a promise to your audience you might not keep.

The mistake I'd avoid: building the clever part first and the boring safety net last.

Builders, a question:
What do you use to make sure scheduled jobs actually run, and how do you find out when they don't?"""

LI_SRC = ("Source: GitHub Docs, \"Events that trigger workflows\" → schedule: scheduled runs can be delayed during periods "
          "of high load, and some queued jobs may be dropped. https://docs.github.com/en/actions/reference/events-that-trigger-workflows#schedule")

CTA = ("circuit-lock.jpg", "Learning money and crypto safety? ==Follow and turn on 🔔==", "Send this to a friend")
DAYS = {
    "2026-11-01": {
        "stories": {
            "s0900": ("coin-collapse.jpg", "You can buy it. ==You can't sell it.==", "New Reel at 12 · tap my profile"),
            "s1100": ("coin-collapse.jpg", "Ever bought a coin because ==the group chat did?==", "Reply 👇"),
            "s1400": ("coin-collapse.jpg", "Check the holders ==before you buy.==", "Today's Reel · tap my profile"),
            "s1700": ("phone-glow.jpg", "Kobo's season finale: ==3 scams to know.==", "At 6 PM · tap my profile"),
            "s2100": CTA,
        },
    },
    "2026-11-02": {
        "li": (LI_MON, "people-whiteboard.png", "My scheduler ==went quiet for 12 hours.==", "Building Autopilot", LI_SRC),
        "stories": {
            "s0900": ("twin-keys.jpg", "Your boss on video ==might be a deepfake.==", "New Reel at 12 · tap my profile"),
            "s1100": ("twin-keys.jpg", "Would you spot ==a deepfake video call?==", "Reply 👇"),
            "s1400": ("twin-keys.jpg", "$25 million. ==One fake video call.==", "Today's Reel · tap my profile"),
            "s1700": ("twin-keys.jpg", "Big payment request? ==Call back on a known number.==", "Tap my profile"),
            "s2100": ("circuit-lock.jpg", "Which scam should I explain next? ==Reply 👇==", "Your question could be next"),
        },
    },
}


def build(day, d):
    Q = ROOT / "queue" / day
    ST, MEDIA = Q / "stories", Q / "media"
    ST.mkdir(parents=True, exist_ok=True)
    if "li" in d:
        MEDIA.mkdir(parents=True, exist_ok=True)
        text, img, hook, kicker, src = d["li"]
        cover(GEN / img, hook, MEDIA / "li-cover.jpg", kicker=kicker, handle="Roland Divine", swipe=False)
        slot = {"title": f"LinkedIn: {kicker}", "kind": "story", "x": {"enabled": False}, "instagram": {"enabled": False},
                "linkedin": {"enabled": True, "text": text, "media": "media/li-cover.jpg", "first_comment": src}}
        (Q / "0800.json").write_text(json.dumps(slot, indent=1, ensure_ascii=False))
    st = []
    for at, (img, text, foot) in d["stories"].items():
        cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (Q / "stories.json").write_text(json.dumps(st, indent=2))
    print("built", Q)


if __name__ == "__main__":
    for day, d in DAYS.items():
        build(day, d)
