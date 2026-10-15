"""Klærus launch post (product Roland built): Instagram Chat Bubbles carousel + LinkedIn terminal
document with real screenshots. Run from studio/:  python days/klaerus.py

Copy rules come from the Klærus content brief: paper-trading demo only, no real-money / on-chain /
wallet / regulation claims, no returns, no public link until one is live.
"""
import base64
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SRC = Path("/home/claude/klaerus_tour/img")
SHOTS = ROOT / "assets" / "klaerus"
OUT = ROOT / "assets" / "klaerus" / "out"

CROPS = {  # name: (source screenshot, crop box in 1170-wide phone pixels)
    "chart": ("i-007", (0, 1240, 1170, 1700)),     # LIQ and FULL PAYOUT lines on the chart
    "ticket": ("i-015", (0, 1330, 1170, 2310)),    # entry, exit price, pays up to, execute
    "result": ("i-035", (0, 1010, 1170, 2195)),    # +$147.50 You called it
}


def crops():
    SHOTS.mkdir(parents=True, exist_ok=True)
    for name, (src, box) in CROPS.items():
        dst = SHOTS / f"{name}.jpg"
        if SRC.exists():
            Image.open(SRC / f"{src}.png").convert("RGB").crop(box).save(dst, quality=90)
    return {n: SHOTS / f"{n}.jpg" for n in CROPS}


def instagram(S):
    slides = [
        [("q", "Roland, what have you been building? 👀"),
         ("r", "**Klærus**: a trading app that shows you two prices ==before== you trade:"),
         ("img", (S["chart"], 330)),
         ("r", "🔴 you're out · 🟢 you get paid")],
        [("q", "Why does that matter?"),
         ("r", "Most trading apps give you a leverage slider and a moving number."),
         ("r", "You find out what **20×** meant when the position is gone ==and you've lost more than you meant to.=="),
         ("r", "I wanted the opposite.")],
        [("r", "**Pick a direction and a time.** The ticket tells you everything up front:"),
         ("img", (S["ticket"], 485)),
         ("r", "$250 → **up to $687.50.** Out at **$107.32.**")],
        [("q", "And the most I can lose?"),
         ("r", "**Your stake.** That's it."),
         ("r", "No borrowing, no margin call, no negative balance."),
         ("r", "==Not a setting. A fact.==")],
        [("q", "What if I change my mind mid-trade?"),
         ("r", "Ahead and nervous? **Cut Profit.**\nBehind and done? **Stopout.**"),
         ("r", "It quotes what you'd get ==right now==. You're never locked in.")],
        [("q", "Does the house win?"),
         ("r", "Over time, **yes.** Every payout is set a bit below fair value. That's how it makes money."),
         ("r", "The difference: the app ==publishes its own margin==, contract by contract."),
         ("r", "Prices come from the real market. Nobody picks the result.")],
        [("img", (S["result"], 600)),
         ("r", "That's **play money.** Klærus is a demo right now: $1,000 to test, no sign-up, ==no real money.==")],
        [("q", "How do I try it? 🙋🏾"),
         ("r", "Comment **DEMO** and I'll send you the link when it goes live."),
         ("r", "Then tell me what breaks 🛠️ Built in public."),
         ("r", "Follow **@defi_ring_master**. Not financial advice.")],
    ]
    return carousel(slides, "Build in public", OUT / "instagram", "klaerus")


def _b64(p):
    return "data:image/jpeg;base64," + base64.b64encode(Path(p).read_bytes()).decode()


def linkedin(S):
    import rd_terminal as R
    from export import export
    R.use_platform("x_linkedin")
    T = 7

    def shot(p, h):
        return (f'<div style="margin-top:14px;text-align:center"><img src="{_b64(p)}" style="height:{h}px;'
                f'max-width:100%;border:1px solid #d9d4c7;border-radius:8px"></div>')

    slides = [
        R.slide(0, T, R.command("build --in-public klaerus") +
                R.h1("I built a trading app that shows you the answer first.") +
                R.pre(f"payout before you trade\nexit price on the chart\n{R.amber('stake = maximum loss')}",
                      top=22, size=13)),
        R.slide(1, T, R.tag("fact") + R.h2("the problem with leverage.") +
                R.pre(f"pick 20× because everyone does\n  └── price moves against you\n"
                      f"       └── position gone\n            └── {R.amber('lost more than you meant to')}",
                      size=12)),
        R.slide(2, T, R.tag("fact") + R.h2("two prices, drawn before you commit.") +
                shot(S["chart"], 180) +
                R.note("# red: where the trade ends.<br># green: where the full payout lands.", top=10)),
        R.slide(3, T, R.tag("fact") + R.h2("the ticket tells you the outcome range.") +
                shot(S["ticket"], 250)),
        R.slide(4, T, R.tag("fact") + R.h2("your stake is the most you can lose.") +
                R.pre(f"no borrowing\nno margin call\nno negative balance\n\n"
                      f"cut profit or stop out mid-trade\nat a quoted price\n\n{R.amber('not a setting. a fact.')}",
                      size=12.5)),
        R.slide(5, T, R.tag("thesis") + R.h2("it publishes its own house edge.") +
                R.pre(f"every payout sits below fair value.\nthat is the business model.\n\n"
                      f"the app lists its margin per\ncontract, generated from the\nlive settings.\n\n"
                      f"{R.amber('status: paper-trading demo')}\n{R.dim('play money, no real deposits')}",
                      size=12)),
        R.signoff(6, T, "comment DEMO and I'll send the link when it's live. then tell me what breaks."),
    ]
    return export(slides, "I built a trading app that shows you the answer first", OUT / "linkedin", "klaerus")


if __name__ == "__main__":
    S = crops()
    print(instagram(S))
    print(linkedin(S))
