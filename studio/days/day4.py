"""Day 4 · Thu 15 Oct 2026 (LinkedIn, terminal style). Run from studio/:  python days/day4.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import rd_terminal as R
from export import export

QUEUE = Path(__file__).resolve().parents[2] / "queue" / "2026-10-15"


def news():
    T = 1
    return [R.slide(0, T, R.command("news --thu-15-oct") +
                    R.h2("US inflation came in hot. Bitcoin dropped.") +
                    R.pre(f"inflation (yearly)\n expected:  3.6%\n actual:    {R.amber('3.7%')}\n\n"
                          f"bitcoin:  -$1,000 in minutes\n10y yield: 5.3%", top=18, size=12.5) +
                    R.note("# markets move on surprises, not numbers.<br># source: CoinDesk, 14 Oct 2026."))]


def wallet1():
    T = 7
    return [
        R.slide(0, T, R.command("guide crypto --wallets") +
                R.h1("Which crypto wallet should you use?") +
                R.pre(f"a plain-english guide\n{R.amber('works in any country')}", top=24, size=13)),
        R.slide(1, T, R.tag("fact") + R.h2("two kinds of wallet.") +
                R.pre(f"{R.gold('custodial')}  the exchange holds\n           your keys. like a bank.\n\n"
                      f"{R.gold('self-custody')}  you hold the keys.\n           {R.amber('like cash in your own safe.')}", size=12)),
        R.slide(2, T, R.tag("thesis") + R.h2("which one, when?") +
                R.pre(f"small amounts, still learning\n  → a regulated exchange\n\n"
                      f"holding long-term\n  → {R.amber('your own wallet')}", size=12.5)),
        R.slide(3, T, R.tag("fact") + R.h2("hot vs cold.") +
                R.pre(f"{R.gold('hot')}   phone/browser app\n      online, easy to use\n\n"
                      f"{R.gold('cold')}  hardware device\n      offline, {R.amber('hardest to hack')}", size=12.5)),
        R.slide(4, T, R.tag("fact") + R.h2("set it up safely.") +
                R.pre(f"{R.gold('01')} download from the official site\n{R.gold('02')} recovery phrase on paper\n"
                      f"   never a screenshot or cloud\n{R.gold('03')} {R.amber('send a test amount first')}", size=12)),
        R.slide(5, T, R.tag("fact") + R.h2("the 3 mistakes that cost the most.") +
                R.pre(f"{R.gold('01')} wrong network: same coin,\n   different chain = lost\n"
                      f"{R.gold('02')} fake wallet apps\n{R.gold('03')} \"sync your wallet\" sites\n"
                      f"   {R.amber('asking for your phrase')}", size=12)),
        R.signoff(6, T, "practical crypto, no hype. save this guide."),
    ]


def aicv1():
    T = 7
    return [
        R.slide(0, T, R.command("guide ai --cv") +
                R.h1("Use AI to write a CV that gets interviews.") +
                R.pre(f"4 steps, any AI chat tool\n{R.amber('chatgpt, claude or gemini')}", top=24, size=13)),
        R.slide(1, T, R.tag("thesis") + R.h2("don't type \"write my CV\".") +
                R.pre(f"you'll get a generic CV that\nsounds like everyone else's.\n\n"
                      f"give it {R.amber('the job ad')} + {R.amber('your')}\n{R.amber('real experience')} instead.", size=12.5)),
        R.slide(2, T, R.tag("fact") + R.h2("step 1: the prompt.") +
                R.pre(f"\"here is the job ad and my\nexperience. rewrite my bullet\npoints for this role. use\n"
                      f"numbers. {R.amber('do not invent')}\n{R.amber('anything.')}\"", size=12)),
        R.slide(3, T, R.tag("fact") + R.h2("step 2: duties → results.") +
                R.pre(f"{R.dim('before:')} managed social media\n\n{R.dim('after:')}  grew instagram from\n"
                      f"        2k to 9k in 6 months\n\n{R.amber('ask: what did it change?')}", size=12) +
                R.note("# example numbers. use your own.")),
        R.slide(4, T, R.tag("fact") + R.h2("step 3: beat the robot filter.") +
                R.pre(f"many companies scan CVs with\nsoftware first.\n\nask the AI: \"which keywords\n"
                      f"from the job ad are {R.amber('missing')}\n{R.amber('from my CV?')}\"", size=12)),
        R.slide(5, T, R.tag("thesis") + R.h2("step 4: you have the final say.") +
                R.pre(f"read every line out loud.\nis it true? does it sound\nlike you?\n\n"
                      f"{R.amber('AI drafts. you decide.')}", size=12.5)),
        R.signoff(6, T, "AI for real work, not hype. save this guide."),
    ]


POSTS = {"news4": (news, "US inflation came in hot. Bitcoin dropped."),
         "wallet1": (wallet1, "Which crypto wallet should you use?"),
         "aicv1": (aicv1, "Use AI to write a CV that gets interviews")}

if __name__ == "__main__":
    R.use_platform("x_linkedin")
    for name, (fn, cap) in POSTS.items():
        print(name, export(fn(), cap, QUEUE / "media", name)[1])
