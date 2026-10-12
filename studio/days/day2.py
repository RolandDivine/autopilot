"""Day 2 · Tue 13 Oct 2026. Run from studio/:  python days/day2.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import rd_terminal as R
from export import export

QUEUE = Path(__file__).resolve().parents[2] / "queue" / "2026-10-13"


def news():
    T = 1
    return [R.slide(0, T, R.command("news --tue-13-oct") +
                    R.h2("Why a US inflation number moves crypto.") +
                    R.pre(f"inflation up\n └── rates stay high\n      └── safe bonds pay more\n"
                          f"           └── {R.amber('less money for risk')}", top=20, size=12.5) +
                    R.note("# US CPI: Wed 14 Oct, 1:30 PM Lagos.<br># forecast 3.6% a year (last: 3.4%). source: CoinDesk."))]


def ai2():
    T = 7
    s = [
        R.slide(0, T, R.command("learn ai --lesson 2/100") +
                R.h1("How AI chat assistants work, simply.") +
                R.pre(f"ai from zero\n{R.amber('lesson 2 of 100')}", top=24, size=13)),
        R.slide(1, T, R.tag("fact") + R.h2("step 1: it read a huge library.") +
                R.pre(f"books, websites, code, articles\n        ↓\n    training\n        ↓\n"
                      f"a model that knows {R.amber('patterns')}\nin language", size=12.5)),
        R.slide(2, T, R.tag("fact") + R.h2("step 2: your words become tokens.") +
                R.pre(f"\"how do I save money?\"\n\n[how] [do] [I] [save] [money] [?]\n\n"
                      f"{R.dim('a token is a word or a piece of one')}", size=12.5)),
        R.slide(3, T, R.tag("fact") + R.h2("step 3: it predicts, one token at a time.") +
                R.pre(f"start  →  \"Start\"\n       →  \"Start by\"\n       →  \"Start by tracking\"\n"
                      f"       →  {R.amber('...until the answer ends')}", size=12.5) +
                R.note("# it writes the reply word by word, picking<br># the most likely next piece each time.")),
        R.slide(4, T, R.tag("interpretation") + R.h2("so it sounds sure, even when wrong.") +
                R.pre(f"{R.gold('01')}  it predicts likely words,\n    not checked facts\n"
                      f"{R.gold('02')}  it can invent sources\n    {R.dim('(called hallucination)')}\n"
                      f"{R.gold('03')}  {R.amber('you')} do the fact-check", size=12.5)),
        R.slide(5, T, R.command("homework --2min") + R.h2("your 2-minute task") +
                R.pre(f"ask an AI a question you\nalready know the answer to.\n\n"
                      f"then ask: \"how sure are you,\nand where is this from?\"\n\n{R.amber('notice what it admits.')}",
                      top=20, size=13)),
        R.signoff(6, T, "learning AI from zero. lesson 3 drops thursday."),
    ]
    return s


def builders1():
    T = 7
    return [
        R.slide(0, T, R.command("learn build --lesson 1/100") +
                R.h1("Why most products never launch.") +
                R.pre(f"builders from zero\n{R.amber('lesson 1 of 100')}", top=24, size=13)),
        R.slide(1, T, R.tag("thesis") + R.h2("the idea is rarely the problem.") +
                R.pre(f"idea        {'█' * 4}{'░' * 12}\nbuilding    {'█' * 7}{'░' * 9}\n"
                      f"{R.amber('finishing')}   {'█' * 16}", size=12.5) +
                R.note("# illustrative: where most projects stall.")),
        R.slide(2, T, R.tag("thesis") + R.h2("trap 1: building in secret.") +
                R.pre(f"months of work\n  └── nobody has seen it\n       └── {R.amber('nobody needs it')}", size=12.5) +
                R.note("# show people early. a sketch is enough.")),
        R.slide(3, T, R.tag("thesis") + R.h2("trap 2: waiting for perfect.") +
                R.pre(f"\"one more feature\"\n\"one more week\"\n\"after the redesign\"\n\n{R.amber('launch day never comes.')}",
                      size=12.5)),
        R.slide(4, T, R.tag("thesis") + R.h2("trap 3: no deadline.") +
                R.pre(f"no date   →  no pressure\nno pressure  →  no finish\n\n"
                      f"{R.gold('fix')}: pick a date and\n     {R.amber('tell someone')}", size=12.5)),
        R.slide(5, T, R.command("homework --2min") + R.h2("your 2-minute task") +
                R.pre(f"write one sentence:\n\n\"I will launch ______\nby ______.\"\n\n{R.amber('our launch day: 4 Feb 2027.')}",
                      top=20, size=13)),
        R.signoff(6, T, "building in public for 150 days. join the build."),
    ]


POSTS = {"news2": (news, "Why a US inflation number moves crypto"),
         "ai2": (ai2, "AI lesson 2: how AI chat assistants work"),
         "build1": (builders1, "Builders lesson 1: why most products never launch")}

if __name__ == "__main__":
    for platform, sub in (("x_linkedin", "media"), ("instagram", "instagram")):
        R.use_platform(platform)
        for name, (fn, cap) in POSTS.items():
            print(platform, name, export(fn(), cap, QUEUE / sub, name)[1])
