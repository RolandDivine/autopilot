"""Fri 6 + Sat 7 Nov 2026 (nightly build, 4 Nov). Run from repo root:  python3 studio/days/week45d.py

Plan:
  Fri 6   08:00 LinkedIn single image only (Fri = Nigeria innovating + motivation; IG off: week 45 carousel cap reached):
          Paystack and Moniepoint, the "overnight" successes that took 5 and 9 years. Principle-led, no invented anecdote.
          11:00 UTC Reel ex06 Mt Gox (40 s cut, payoff first: "An exchange is not a vault").
  Sat 7   No LinkedIn (weekend), no IG carousel (cap). 11:00 UTC Reel ex08 Bitcoin ETF (38 s cut). Stories both days.
Facts: Stripe acquires Paystack, Oct 2020 (https://stripe.com/newsroom/news/paystack-joins-stripe; price reported >$200M);
Moniepoint $110M round, valued >$1B, Oct 2024 (https://nairametrics.com/2024/10/29/moniepoint-valued-at-1-billion-as-google-others-invest-110-million).
Images reused from assets/gen (no Figma credits spent).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "assets" / "gen"

LI_TEXT = """Paystack took five years to become an "overnight" success. Moniepoint took nine.

If you're two years into building something and it still feels small, read this before you quit.

Paystack started in 2015. In October 2020, Stripe bought it, in a deal reported at over $200 million.

Moniepoint also started in 2015, as TeamApt, building banking software for other companies. In October 2024 it raised $110 million and was valued at over $1 billion.

From the outside, both looked sudden. From the inside, it was years of work most people never saw.

What I take from it as a builder:

→ Consistency beats intensity. Five years of showing up beats five brilliant weeks.
→ Boring problems pay. Payments, POS, business banking. Real pain, real customers.
→ Build together. Neither company was built by one person. Find the people you can build with for a decade.

Nigeria doesn't lack talent. What separates the winners is staying in the game long enough for the compounding to show.

A question for builders reading this:
What's one thing you've kept doing for more than a year, even when nobody was watching?"""

LI_SRC = ("Sources: Stripe, \"Paystack joins Stripe\" (Oct 2020): https://stripe.com/newsroom/news/paystack-joins-stripe · "
          "Nairametrics, \"Moniepoint valued at $1 billion\" (Oct 2024): "
          "https://nairametrics.com/2024/10/29/moniepoint-valued-at-1-billion-as-google-others-invest-110-million")

STORIES = {
    "2026-11-06": {
        "s0900": ("glass-house.jpg", "Is all your crypto ==on one app?==", "Reply 👇"),
        "s1100": ("coin-siphon.jpg", "Stop overpaying ==crypto fees.==", "Yesterday's Reel · tap my profile"),
        "s1400": ("glass-house.jpg", "Your exchange ==is not a vault.==", "New Reel · tap my profile"),
        "s1700": ("twin-keys.jpg", "Do you hold ==your own keys?==", "Yes or no 👇"),
        "s2100": ("black-cube.jpg", "Do you know what you ==really own in a Bitcoin ETF?==", "Answer tomorrow · 12 PM Reel"),
    },
    "2026-11-07": {
        "s0900": ("black-cube.jpg", "Bitcoin ETF or your own wallet? ==Which would you pick?==", "Reply 👇"),
        "s1100": ("glass-house.jpg", "Not your keys, ==not your coins.==", "Yesterday's Reel · tap my profile"),
        "s1400": ("black-cube.jpg", "Bitcoin ETF: ==you don't hold the keys.==", "New Reel · tap my profile"),
        "s1700": ("black-cube.jpg", "Simplicity or control: ==which matters more?==", "Reply 👇"),
        "s2100": ("circuit-lock.jpg", "Learning AI and money safety? ==Follow and turn on 🔔==", "Send this to a friend"),
    },
}


def stories(day):
    ST = ROOT / "queue" / day / "stories"
    ST.mkdir(parents=True, exist_ok=True)
    st = []
    for at, (img, text, foot) in STORIES[day].items():
        cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (ROOT / "queue" / day / "stories.json").write_text(json.dumps(st, indent=2))


def fri(day="2026-11-06"):
    Q = ROOT / "queue" / day
    (Q / "media").mkdir(parents=True, exist_ok=True)
    cover(GEN / "hourglass-half.jpg", "\"Overnight\" success took ==5 to 9 years==", Q / "media" / "li-cover.jpg",
          kicker="Nigeria · building", handle="Roland Divine", swipe=False)
    slot = {
        "title": "LinkedIn: Paystack and Moniepoint, the 5- and 9-year overnight successes",
        "kind": "lesson",
        "x": {"enabled": False},
        "instagram": {"enabled": False},
        "linkedin": {"enabled": True, "text": LI_TEXT, "media": "media/li-cover.jpg", "first_comment": LI_SRC},
    }
    (Q / "0800.json").write_text(json.dumps(slot, indent=1, ensure_ascii=False))
    stories(day)
    print("built", day, len(LI_TEXT), "LI chars")


def sat(day="2026-11-07"):
    stories(day)
    print("built", day, "stories only")


if __name__ == "__main__":
    fri()
    sat()
