"""Explainer Reels from the Fish ELITE audio bank (assets/vo/exNN-*.mp3, 18 Oct 2026).

    python studio/explainers.py ex01-halving            -> assets/reels/ex01-halving.mp4
    python studio/explainers.py ex01-halving 5 30 60    -> preview PNGs
Setup per video: assets/viral/<name>/voice.{mp3,json} and /home/claude/money_audio/<name>.wav (see prep()).
"""
import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viral  # noqa: E402

ROOT = viral.ROOT
GEN = ROOT / "assets" / "gen"
FOLLOW = viral.FOLLOW


def prep(name):
    d = ROOT / "assets" / "viral" / name
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "assets" / "vo" / f"{name}.mp3", d / "voice.mp3")
    shutil.copy(ROOT / "assets" / "vo" / f"{name}.json", d / "voice.json")
    Path("/home/claude/money_audio").mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(d / "voice.mp3"), "-ar", "44100", "-ac", "1",
                    f"/home/claude/money_audio/{name}.wav"], check=True)


def halving_spec():
    def timeline(at, dur):
        t_every, t_cuts, t_new, t_blocks = at("every"), at("cuts"), at("new"), at("every", 15)
        t_2009, t_april, t_next, t_why = at("2009"), at("april"), at("next"), at("why")
        t_fewer, t_21, t_careful, t_past = at("fewer"), at("21"), at("careful"), at("past")
        t_markets, t_learn, t_see = at("markets"), at("learn"), at("see")
        bgs = [(-1, dur + 1, GEN / "hourglass-half.jpg")]
        cards = [
            {"kind": "html", "a": -1, "b": t_cuts - .1,
             "html": "<div class='kick'>Crypto · explained</div><div class='mid'>Every ~4 years, Bitcoin does what<br><span class='yel'>no central bank does.</span></div>"},
            {"kind": "stat", "a": t_cuts, "b": t_new - .1, "kick": "The halving", "value": "½", "cls": "yel",
             "label": "It cuts its own money printing in half"},
            {"kind": "html", "a": t_new, "b": t_blocks - .1,
             "html": "<div class='kick'>Where new bitcoin comes from</div><div class='mid'>A reward paid to <span class='yel'>miners</span>,</div>"
                     "<div class='sm' style='margin-top:16px'>the computers that secure the network.</div>"},
            {"kind": "stat", "a": t_blocks, "b": t_2009 - .1, "kick": "Every 210,000 blocks", "value": "~4 years", "cls": "yel",
             "label": "the block reward halves"},
            {"kind": "bars", "a": t_2009, "b": t_next - .1, "kick": "Bitcoin per block", "title": "The reward keeps halving", "max": 50,
             "bars": [{"t": "50", "v": 50, "q": "2009"}, {"t": "25", "v": 25, "q": "2012"}, {"t": "12.5", "v": 12.5, "q": "2016"},
                      {"t": "6.25", "v": 6.25, "q": "2020"}, {"t": "3.125", "v": 3.125, "q": "Apr 2024"}]},
            {"kind": "timeline", "a": t_next, "b": t_why - .1, "kick": "What's next", "title": "The next halving",
             "pts": [{"x": 15, "t": "Apr 2024", "s": "3.125 BTC"}, {"x": 55, "t": "~2028", "s": "1.5625 BTC"},
                     {"x": 88, "t": "~2140", "s": "last bitcoin"}]},
            {"kind": "stat", "a": t_why, "b": t_careful - .1, "kick": "Why it matters", "value": "21M", "cls": "yel",
             "label": "the most bitcoin that will ever exist", "sub": "Fewer new coins every day"},
            {"kind": "html", "a": t_careful, "b": t_learn - .1,
             "html": "<div class='kick'>But careful</div><div class='mid'>Past halvings came before big price runs.</div>"
                     "<div class='mid red' style='margin-top:14px'>That's not a rule.</div>"
                     "<div class='sm' style='margin-top:16px'>The halving is known years in advance.</div>"},
            {"kind": "html", "a": t_learn, "b": t_see - .3,
             "html": "<div class='kick'>Kobo's rule</div><div class='mid'>Learn how it works.<br><span class='yel'>Don't bet your rent on a pattern.</span></div>"
                     "<div class='sm' style='margin-top:16px'>Education, not financial advice.</div>"},
            {"kind": "html", "a": t_see - .3, "b": dur + 1, "html": FOLLOW.format("Crypto, explained straight.")},
        ]
        return bgs, cards

    return viral.std("ex01-halving", timeline)


def drainers_spec():
    def timeline(at, dur):
        t_wallet, t_connect, t_says, t_once = at("wallet", 7), at("connect"), at("says"), at("once")
        t_rules, t_type, t_read, t_if = at("kobo's"), at("type"), at("read"), at("if", 44)
        t_keep, t_check, t_one, t_see = at("keep"), at("check"), at("one", 60), at("see", 65)
        bgs = [(-1, dur + 1, GEN / "coin-siphon.jpg")]
        cards = [
            {"kind": "html", "a": -1, "b": t_wallet - .1,
             "html": "<div class='kick'>Crypto · safety</div><div class='mid'>Lose everything<br><span class='red'>without sharing your seed phrase.</span></div>"},
            {"kind": "html", "a": t_wallet, "b": t_connect - .1,
             "html": "<div class='kick'>A wallet drainer</div><div class='mid'>A fake website</div>"
                     "<div class='sm' style='margin-top:16px'>Free airdrop · new mint · a copy of a popular app</div>"},
            {"kind": "html", "a": t_connect, "b": t_says - .1,
             "html": "<div class='kick'>The trap</div><div class='mid'>Connect, then <span class='yel'>sign</span></div>"
                     "<div class='sm' style='margin-top:16px'>That signature can be a permission.</div>"},
            {"kind": "stat", "a": t_says, "b": t_once - .1, "kick": "What you just approved", "value": "Unlimited", "cls": "red",
             "label": "\"This contract may spend my tokens.\"", "sub": "Until you revoke it"},
            {"kind": "html", "a": t_once, "b": t_rules - .1,
             "html": "<div class='kick'>Then</div><div class='mid'>No password needed.<br><span class='red'>They just move the tokens.</span></div>"},
            {"kind": "checks", "a": t_rules, "b": t_keep - .1, "kick": "Kobo's rules", "title": "Before you sign",
             "items": [{"t": "Never connect from a DM or a reply link", "d": .4},
                       {"t": "Type the address yourself", "d": t_type - t_rules},
                       {"t": "Read it. \"Approve\" you didn't expect? Reject", "d": t_read - t_rules}]},
            {"kind": "checks", "a": t_keep, "b": t_one - .1, "kick": "Kobo's rules", "title": "Protect what you have",
             "items": [{"t": "A separate small wallet for new apps", "d": .3},
                       {"t": "Check approvals on revoke.cash", "d": t_check - t_keep},
                       {"t": "Revoke what you don't use", "d": t_check - t_keep + 3}]},
            {"kind": "html", "a": t_one, "b": t_see - .3,
             "html": "<div class='mid'>One click can cost everything.<br><span class='yel'>Slow down.</span></div>"},
            {"kind": "html", "a": t_see - .3, "b": dur + 1, "html": FOLLOW.format("Crypto, explained straight.")},
        ]
        return bgs, cards

    return viral.std("ex02-drainers", timeline)


def pig_spec():
    def timeline(at, dur):
        bgs = [(-1, dur + 1, GEN / "pig-phone.jpg")]
        cards = [
            {"kind": "html", "a": -1, "b": 6.6,
             "html": "<div class='kick'>Crypto · scams</div><div class='mid'>It starts with<br><span class='yel'>a wrong-number text.</span></div>"},
            {"kind": "html", "a": 6.6, "b": 13.3,
             "html": "<div class='kick'>Weeks of chatting</div><div class='mid'>A friend.<br><span class='yel'>Sometimes more.</span></div>"},
            {"kind": "html", "a": 13.3, "b": 23.0,
             "html": "<div class='kick'>Then, casually</div><div class='mid'>\"This crypto app<br>is making me rich.\"</div>"
                     "<div class='sm' style='margin-top:16px'>Screenshots · offers to teach you</div>"},
            {"kind": "checks", "a": 23.0, "b": 38.9, "kick": "The trap", "title": "You deposit",
             "items": [{"t": "A little. The app shows profits", "d": .3}, {"t": "More. Then you try to withdraw", "d": 3.5},
                       {"t": "\"Taxes\", \"fees\", a \"verification charge\"", "d": 8.4}]},
            {"kind": "html", "a": 38.9, "b": 48.0,
             "html": "<div class='kick'>The app was fake from day one</div><div class='mid'>They call it<br><span class='red'>pig butchering.</span></div>"
                     "<div class='sm' style='margin-top:16px'>Fatten the victim with trust, then take everything.</div>"},
            {"kind": "stat", "a": 48.0, "b": 61.0, "kick": "FBI IC3, 2024", "value": "$9.3B", "cls": "red",
             "label": "lost by Americans to crypto fraud", "sub": "Investment scams were the biggest share", "src": "FBI IC3 2024 report"},
            {"kind": "checks", "a": 61.0, "b": 70.5, "kick": "Kobo's rules", "title": "Stay safe",
             "items": [{"t": "Never invest through someone you met online", "d": .4},
                       {"t": "Can't withdraw? Stop sending", "d": 7.0}]},
            {"kind": "html", "a": 70.5, "b": dur + 1, "html": FOLLOW.format("Crypto, explained straight.")},
        ]
        return bgs, cards

    return viral.std("ex03-pigbutchering", timeline)


def poison_spec():
    def timeline(at, dur):
        bgs = [(-1, dur + 1, GEN / "twin-keys.jpg")]
        addr = "<div class='sm' style='margin-top:18px;font-family:monospace;font-size:54px'>{}</div>"
        cards = [
            {"kind": "html", "a": -1, "b": 5.8,
             "html": "<div class='kick'>Crypto · scams</div><div class='mid'>A scam that needs<br><span class='red'>zero clicks.</span></div>"},
            {"kind": "html", "a": 5.8, "b": 13.0,
             "html": "<div class='kick'>What most people check</div><div class='mid'>The first and last<br>few characters</div>"
                     + addr.format("<span class='yel'>0x7a3f</span>…e91c4b<span class='yel'>d2f9</span>")},
            {"kind": "html", "a": 13.0, "b": 20.3,
             "html": "<div class='kick'>The scammer's copy</div><div class='mid'>Same start. Same end.</div>"
                     + addr.format("<span class='yel'>0x7a3f</span>" + "<span class='red'>…08bb12</span>" + "<span class='yel'>d2f9</span>")},
            {"kind": "html", "a": 20.3, "b": 30.0,
             "html": "<div class='kick'>Address poisoning</div><div class='mid'>A tiny (or $0) transfer<br>lands in <span class='red'>your history.</span></div>"},
            {"kind": "html", "a": 30.0, "b": 45.4,
             "html": "<div class='kick'>Next time you send</div><div class='mid'>You copy from history.<br><span class='red'>It's their address.</span></div>"
                     "<div class='sm' style='margin-top:16px'>Crypto transfers can't be reversed.</div>"},
            {"kind": "checks", "a": 45.4, "b": 64.3, "kick": "Kobo's rules", "title": "Before you send",
             "items": [{"t": "Never copy from transaction history", "d": 1.6}, {"t": "Use your wallet's address book", "d": 5.4},
                       {"t": "Big amount? Send a small test first", "d": 9.2}, {"t": "Check the WHOLE address", "d": 14.7}]},
            {"kind": "html", "a": 64.3, "b": 67.6,
             "html": "<div class='mid'>10 extra seconds<br><span class='yel'>can save everything.</span></div>"},
            {"kind": "html", "a": 67.6, "b": dur + 1, "html": FOLLOW.format("Crypto, explained straight.")},
        ]
        return bgs, cards

    return viral.std("ex04-addresspoisoning", timeline)


def terra_spec():
    def timeline(at, dur):
        bgs = [(-1, dur + 1, GEN / "coin-collapse.jpg")]
        cards = [
            {"kind": "html", "a": -1, "b": 10.5,
             "html": "<div class='kick'>Crypto · history · May 2022</div><div class='mid'>A \"$1 coin\" fell<br><span class='red'>to almost zero in days.</span></div>"},
            {"kind": "html", "a": 10.5, "b": 18.6,
             "html": "<div class='kick'>UST</div><div class='mid'>Most stablecoins hold<br>cash or bonds.<br><span class='red'>UST didn't.</span></div>"},
            {"kind": "html", "a": 18.6, "b": 30.6,
             "html": "<div class='kick'>How it worked</div><div class='mid'>An algorithm +<br>a sister token, <span class='yel'>Luna</span></div>"
                     "<div class='sm' style='margin-top:16px'>1 UST could always be swapped for $1 of Luna. Fine, while people trusted it.</div>"},
            {"kind": "stat", "a": 30.6, "b": 37.6, "kick": "Anchor protocol", "value": "~20%", "cls": "yel",
             "label": "a year paid on UST", "sub": "Billions flowed in"},
            {"kind": "checks", "a": 37.6, "b": 54.8, "kick": "The death spiral", "title": "Then",
             "items": [{"t": "Big withdrawals: UST slips below $1", "d": .3}, {"t": "People swap UST for Luna and sell", "d": 5.6},
                       {"t": "Luna crashes, UST gets weaker, repeat", "d": 10.8}]},
            {"kind": "html", "a": 54.8, "b": 58.9,
             "html": "<div class='mid'><span class='red'>Tens of billions</span><br>of dollars in value, gone.</div>"},
            {"kind": "checks", "a": 58.9, "b": 68.6, "kick": "Kobo's lesson", "title": "Before you chase a yield",
             "items": [{"t": "Too good? Ask where it comes from", "d": .3}, {"t": "\"Stable\" is a promise. Check the backing", "d": 5.6}]},
            {"kind": "html", "a": 68.6, "b": dur + 1, "html": FOLLOW.format("Crypto, explained straight.")},
        ]
        return bgs, cards

    return viral.std("ex05-terra", timeline)


SPECS = {"ex05-terra": terra_spec, "ex04-addresspoisoning": poison_spec, "ex01-halving": halving_spec, "ex02-drainers": drainers_spec, "ex03-pigbutchering": pig_spec}

if __name__ == "__main__":
    name = sys.argv[1]
    prep(name)
    pv = [float(x) for x in sys.argv[2:]]
    out = ROOT / "assets" / "reels" / f"{name}.mp4"
    print(asyncio.run(viral.render(SPECS[name](), out, pv or None)))
