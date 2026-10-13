"""Day 3 · Wed 14 Oct 2026 (LinkedIn, terminal style). Run from studio/:  python days/day3.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import rd_terminal as R
from export import export

QUEUE = Path(__file__).resolve().parents[2] / "queue" / "2026-10-14"


def news():
    T = 1
    return [R.slide(0, T, R.command("news --wed-14-oct") +
                    R.h2("$672M of leveraged bets wiped out in a day.") +
                    R.pre(f"btc  ~$84,200 → ~$81,000\n\nliquidated in 24h: $672M\n"
                          f" ├── bets on up:   $586M\n └── bets on down:  $86M\n\n"
                          f"{R.amber('borrowed money cuts both ways')}", top=18, size=12.5) +
                    R.note("# US CPI lands today, 1:30 PM Lagos.<br># source: KuCoin daily market report, 13 Oct."))]


def crypto2():
    T = 7
    return [
        R.slide(0, T, R.command("learn crypto --lesson 2/100") +
                R.h1("What a blockchain is, in plain words.") +
                R.pre(f"crypto from zero\n{R.amber('lesson 2 of 100')}", top=24, size=13)),
        R.slide(1, T, R.tag("fact") + R.h2("start with a notebook.") +
                R.pre(f"an ajo group keeps one book:\n who paid, how much, when\n\n"
                      f"problem: {R.amber('one person holds it')}\n  └── they can change it", size=12.5)),
        R.slide(2, T, R.tag("fact") + R.h2("now give everyone a copy.") +
                R.pre(f"thousands of computers\neach hold the same book\n\n"
                      f"change your copy?\n  └── {R.amber('everyone else disagrees')}", size=12.5) +
                R.note("# no single owner, no single point to cheat.")),
        R.slide(3, T, R.tag("fact") + R.h2("pages are blocks. linked, they form a chain.") +
                R.pre(f"[page 1] ← [page 2] ← [page 3]\n\neach page carries a fingerprint\nof the page before it.\n\n"
                      f"edit an old page →\n{R.amber('every page after it breaks')}", size=12)),
        R.slide(4, T, R.tag("fact") + R.h2("who writes the next page?") +
                R.pre(f"bitcoin: miners compete\n  using computing power\n\nethereum: validators\n"
                      f"  who lock up coins as a deposit\n\n{R.amber('cheating costs them money')}", size=12.5)),
        R.slide(5, T, R.command("homework --2min") + R.h2("your 2-minute task") +
                R.pre(f"explain a blockchain to a\nfriend using only the\nnotebook example.\n\n"
                      f"{R.amber('if they get it, you do too.')}", top=20, size=13)),
        R.signoff(6, T, "crypto from zero. lesson 3 drops thursday."),
    ]


def builders2():
    T = 7
    return [
        R.slide(0, T, R.command("learn build --lesson 2/100") +
                R.h1("The 150-day build challenge: how it works.") +
                R.pre(f"builders from zero\n{R.amber('lesson 2 of 100')}", top=24, size=13)),
        R.slide(1, T, R.tag("fact") + R.h2("one goal: launch something real.") +
                R.pre(f"start:   12 Oct 2026\nlaunch:  {R.amber('4 Feb 2027')}\n\n"
                      f"a builders lesson most days.\nfree. in public. together.", size=12.5)),
        R.slide(2, T, R.tag("fact") + R.h2("the road, in 5 stages.") +
                R.pre(f"{R.gold('01')} find a real problem  →10 nov\n{R.gold('02')} validate + plan     →10 dec\n"
                      f"{R.gold('03')} build + beta test   → 9 jan\n{R.gold('04')} get launch-ready\n"
                      f"{R.gold('05')} {R.amber('launch day: 4 feb')}", size=12)),
        R.slide(3, T, R.tag("thesis") + R.h2("no idea yet? good.") +
                R.pre(f"stage 1 starts with problems,\nnot ideas.\n\n"
                      f"you'll pick one you're close to\n{R.amber('before you build anything')}", size=12.5)),
        R.slide(4, T, R.tag("thesis") + R.h2("the rules.") +
                R.pre(f"{R.gold('01')}  ship small, ship often\n{R.gold('02')}  show your work in public\n"
                      f"{R.gold('03')}  talk to real users\n{R.gold('04')}  {R.amber('done beats perfect')}", size=12.5)),
        R.slide(5, T, R.command("homework --2min") + R.h2("your 2-minute task") +
                R.pre(f"comment \"I'm in\" and one\nthing that annoys you every\nweek.\n\n"
                      f"{R.amber('that list is where we start.')}", top=20, size=13)),
        R.signoff(6, T, "building in public for 150 days. join the build."),
    ]


POSTS = {"news3": (news, "$672M of leveraged bets wiped out in a day"),
         "crypto2": (crypto2, "Crypto lesson 2: what a blockchain is"),
         "build2": (builders2, "Builders lesson 2: the 150-day build challenge")}

if __name__ == "__main__":
    R.use_platform("x_linkedin")
    for name, (fn, cap) in POSTS.items():
        print(name, export(fn(), cap, QUEUE / "media", name)[1])
