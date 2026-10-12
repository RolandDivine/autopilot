from pathlib import Path  # example only: Day 1 slide copy, for tone and layout reference
from rd_terminal import *

OUT = Path("/home/claude/day1"); OUT.mkdir(exist_ok=True)

# ---------- Crypto 1: What money is, and why crypto exists ----------
T = 7
c = [
    slide(0, T, command("learn crypto --lesson 1/100") +
          h1("Before crypto, understand money.") +
          pre(f"crypto from zero\n{amber('lesson 1 of 100')}", top=24, size=13)),
    slide(1, T, tag("fact") + h2("money does 3 jobs.") +
          pre(f"{gold('01')}  pay for things\n    {dim('medium of exchange')}\n"
              f"{gold('02')}  keep value over time\n    {dim('store of value')}\n"
              f"{gold('03')}  put a price on things\n    {dim('unit of account')}")),
    slide(2, T, tag("fact") + h2("who sits between you and your money?") +
          pre(f"you\n └── your bank\n      └── central bank\n           └── {amber('government')}") +
          note("# they keep it running. they can also print more,<br># delay transfers or freeze accounts.")),
    slide(3, T, tag("fact") + h2("2008: a nine-page idea.") +
          pre(f"before   you → bank → bank → them\n"
              f"bitcoin  you ──────────────→ {amber('them')}", top=24) +
          note("# 'Bitcoin: A Peer-to-Peer Electronic Cash System'<br># by Satoshi Nakamoto, 31 Oct 2008. first block: 3 Jan 2009.")),
    slide(4, T, tag("interpretation") + h2("so why does crypto exist?") +
          pre(f"{gold('01')}  send value without a middleman\n"
              f"{gold('02')}  supply rules anyone can check\n"
              f"    {dim('(bitcoin: max 21 million)')}\n"
              f"{gold('03')}  open to anyone with internet") +
          note("# not risk-free: prices swing hard. we cover risk soon.")),
    slide(5, T, command("homework --2min") + h2("your 2-minute task") +
          pre(f"list 3 things you paid for\nthis week.\n\nfor each, write who stood\nin the middle.\n\n{amber('bank? app? agent? nobody?')}", top=20, size=13)),
    signoff(6, T, "learning crypto from zero. lesson 2 drops in two days."),
]

# ---------- AI 1: What AI is (and is not) ----------
a = [
    slide(0, T, command("learn ai --lesson 1/100") +
          h1("AI isn't magic. Here's what it actually is.") +
          pre(f"ai from zero\n{amber('lesson 1 of 100')}", top=24, size=13)),
    slide(1, T, tag("fact") + h2("AI = software that learns patterns.") +
          pre(f"many examples  →  training  →  pattern\n"
              f"new question   →  pattern   →  {amber('best guess')}", top=24, size=12)),
    slide(2, T, tag("fact") + h2("chat AI predicts the next word.") +
          pre(f"\"the capital of nigeria is ...\"\n\n"
              f"abuja  {'█'*18}{'░'*2}  {amber('likely')}\n"
              f"lagos  {'█'*4}{'░'*16}  less likely", size=12.5) +
          note("# illustrative, not real model output.")),
    slide(3, T, tag("fact") + h2("good at, bad at.") +
          pre(f"{amber('GOOD AT')}            {dim('BAD AT')}\n"
              f"{dim('─────────────────  ─────────────────')}\n"
              f"drafting           exact facts with\n"
              f"summarising        no source\n"
              f"explaining         today's news, unless\n"
              f"brainstorming      it can search\n"
              f"                   saying \"I don't know\"", size=12)),
    slide(4, T, tag("interpretation") + h2("treat it like a fast intern.") +
          pre(f"it drafts. {amber('you decide.')}\n\n"
              f"01  give it context\n02  check its facts\n03  you own the result", top=22)),
    slide(5, T, command("homework --2min") + h2("your 2-minute task") +
          pre(f"ask any AI assistant:\n\n\"explain my job to a\n10-year-old in 3 sentences.\"\n\n{amber('then mark what it got wrong.')}", top=20, size=13)),
    signoff(6, T, "learning AI from zero. lesson 2 drops tomorrow."),
]

# ---------- News card (single slide) ----------
n = [slide(0, 1, command("news --mon-12-oct") + h2("Prediction markets head to the Supreme Court.") +
           pre(f"swap  →  CFTC    {dim('1 rulebook')}\n"
               f"bet   →  states  {amber('50 rulebooks')}", top=22, size=13) +
           note("# Flaherty v. KalshiEX. Kalshi's response is due 9 Nov.<br># details in the caption."))]

for name, sl, cap in (("crypto1", c, "Lesson 1: what money is, and why crypto exists."),
                      ("ai1", a, "Lesson 1: what AI is, and what it is not."),
                      ("news1", n, "Prediction markets head to the Supreme Court.")):
    (OUT / f"{name}.html").write_text(page("".join(sl), len(sl), cap), encoding="utf-8")
print("ok")
