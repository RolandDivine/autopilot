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


def buy1():
    T = 7
    return [
        R.slide(0, T, R.command("guide crypto --buy-safely") +
                R.h1("How to buy your first crypto safely.") +
                R.pre(f"a 5-step checklist\n{R.amber('works in any country')}", top=24, size=13)),
        R.slide(1, T, R.tag("fact") + R.h2("step 1: pick a regulated exchange.") +
                R.pre(f"check your country's regulator\nlist before you sign up.\n\n"
                      f"download the app from the\n{R.amber('official site, not an ad link')}", size=12.5)),
        R.slide(2, T, R.tag("fact") + R.h2("step 2: lock the door first.") +
                R.pre(f"{R.gold('01')}  strong unique password\n{R.gold('02')}  2FA with an authenticator app\n"
                      f"    {R.dim('(not SMS)')}\n{R.gold('03')}  {R.amber('support never DMs you first')}", size=12.5)),
        R.slide(3, T, R.tag("fact") + R.h2("step 3: start with a test amount.") +
                R.pre(f"buy small  →  withdraw small\n           →  check it arrived\n\n"
                      f"only then move more.\n{R.amber('mistakes on-chain are final')}", size=12.5)),
        R.slide(4, T, R.tag("fact") + R.h2("step 4: know your local rules.") +
                R.pre(f"example, nigeria:\nbinance stopped naira deposits,\nwithdrawals and p2p in 2024.\n\n"
                      f"use sec-licensed platforms.\n\n"
                      f"p2p: {R.amber('wait for the money in')}\n{R.amber('your bank, not a screenshot')}", size=12)),
        R.slide(5, T, R.tag("thesis") + R.h2("step 5: own your keys, guard the phrase.") +
                R.pre(f"12-24 word recovery phrase\n  = full access to your money\n\n"
                      f"write it on paper. never type\nit into a site or a chat.\n\n"
                      f"{R.amber('anyone asking for it is a thief')}", size=12)),
        R.signoff(6, T, "practical crypto, no hype. save this checklist."),
    ]


def robot1():
    T = 7
    return [
        R.slide(0, T, R.command("build --in-public") +
                R.h1("I built my own posting robot with AI.") +
                R.pre(f"the new way to build\n{R.amber('one person + AI + free tools')}", top=24, size=13)),
        R.slide(1, T, R.tag("fact") + R.h2("the problem: posting daily while busy.") +
                R.pre(f"3 posts a day, 2 platforms\n  └── every single day\n       └── {R.amber('not while running companies')}",
                      size=12.5)),
        R.slide(2, T, R.tag("fact") + R.h2("step 1: describe it in plain words.") +
                R.pre(f"\"post my content at 8am, 1pm\nand 7pm. let me review it\nthe night before. let me\n"
                      f"cancel any post.\"\n\n{R.amber('that was the whole spec')}", size=12)),
        R.slide(3, T, R.tag("fact") + R.h2("step 2: free building blocks.") +
                R.pre(f"{R.gold('github')}     stores posts, runs\n           them on a schedule\n"
                      f"{R.gold('linkedin')}   official posting api\n{R.gold('instagram')}  official posting api\n"
                      f"{R.gold('claude')}     wrote and fixed the code", size=12)),
        R.slide(4, T, R.tag("fact") + R.h2("step 3: ship, then fix what breaks.") +
                R.pre(f"day 2: github's timer ran\nhours late.\n  └── fix: a backup trigger\n\n"
                      f"{R.amber('real users find real bugs')}", size=12.5)),
        R.slide(5, T, R.tag("thesis") + R.h2("the blueprint has changed.") +
                R.pre(f"before: a team, months, money\nnow:    one person, days,\n        mostly free tools\n\n"
                      f"{R.amber('the skill is knowing what')}\n{R.amber('to build and steering AI')}", size=12)),
        R.signoff(6, T, "building in public for 150 days. join the build."),
    ]


POSTS = {"news3": (news, "$672M of leveraged bets wiped out in a day"),
         "buy1": (buy1, "How to buy your first crypto safely"),
         "robot1": (robot1, "I built my own posting robot with AI")}

if __name__ == "__main__":
    R.use_platform("x_linkedin")
    for name, (fn, cap) in POSTS.items():
        print(name, export(fn(), cap, QUEUE / "media", name)[1])
