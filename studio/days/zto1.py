"""Zero to One, decoded: a 4-part business series (Roland, 23 Oct 2026: "extra posts, not the already scheduled ones").
Fri 23 – Mon 26 Oct, slot 1300 each day: one Instagram carousel + one LinkedIn PDF post. Not on YouTube (crypto only).
All lessons are paraphrased in our own words; at most one short quote per post, attributed. Run from studio/: python days/zto1.py
Nightly builds must NOT overwrite queue/<date>/1300.json on these four days.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "assets" / "gen"
SRC = "Source: Peter Thiel with Blake Masters, Zero to One: Notes on Startups, or How to Build the Future (2014). Lessons paraphrased."
TAGS = "#business #entrepreneurship #startups #founders #zerotoone"


def end(part, nxt):
    return [("r", "📌 Save this. 📤 Send it to a founder who needs it."),
            ("r", f"Part {part} of 4: **Zero to One, decoded.** " + (f"Tomorrow: {nxt}." if nxt else "That's the series. Which lesson hit hardest? 👇")),
            ("r", "Follow **@defi_ring_master** for business, AI and crypto, explained straight.")]


DAYS = {
    "2026-10-23": dict(
        name="zto1-1", img="black-cube.jpg", kicker="Business · Zero to One, part 1",
        hook="Copying what works is easy. ==Building from zero pays.==",
        title="Zero to One, part 1: 0 to 1 vs 1 to n, and the contrarian question",
        slides=[
            [("q", "Roland, what's the big idea in Zero to One? 📘"),
             ("r", "Copying something that already works is **1 to n.**"),
             ("r", "Creating something new is ==0 to 1.== Peter Thiel argues that's where real value comes from.")],
            [("r", "**Lesson 1: copying is the default** 📋"),
             ("r", "Another restaurant. Another payments app. Another \"Uber for X\"."),
             ("r", "It feels safe because it's proven. That's also why ==everyone else is doing it.==")],
            [("r", "**Lesson 2: the contrarian question** ❓"),
             ("r", "Thiel asks founders: what important truth do very few people agree with you on?"),
             ("r", "A good answer isn't \"everyone is wrong\". It's ==a specific truth you can build on.==")],
            [("r", "**Lesson 3: secrets still exist** 🔐"),
             ("r", "Most people assume everything worth knowing is already known."),
             ("r", "Thiel disagrees: there are still ==hidden truths== about what people need and how things work.")],
            [("r", "**Where to look for them** 🔎"),
             ("r", "Problems people complain about but have accepted."),
             ("r", "Things experts call impossible. Markets ==big companies ignore== because they look too small.")],
            [("r", "**Try it on Nigeria** 🇳🇬"),
             ("r", "1 to n: another fintech app with the same features as ten others."),
             ("r", "0 to 1: solving a problem ==nobody has solved here yet,== in a way that works here.")],
            end(1, "why competition is for losers"),
        ],
        cap="Zero to One by Peter Thiel, part 1: why copying is the crowded road and the one question every founder should answer. 📘\n\n0 to 1 vs 1 to n, the contrarian question, and where to look for secrets. Swipe →\n\n📌 Save it\n📤 Send it to a founder friend\n\n" + TAGS,
        li="""Most businesses are copies. That's not an insult. It's a strategy, and a very crowded one.

Peter Thiel's Zero to One splits progress into two kinds:
→ 1 to n: copying what already works. Another restaurant, another payments app, another "Uber for X"
→ 0 to 1: making something new that didn't exist before

Copies can make money. But they fight for the same customers, compete on price and rarely build something that lasts.

The book's most useful tool is one question it asks every founder: what important truth do very few people agree with you on?

Three lessons I'd take from part one:

1. A copy feels safe because someone else proved it works. That's exactly why everyone else is doing it too.

2. Secrets still exist. Look at problems people complain about but have accepted, and markets big companies ignore because they look small.

3. A contrarian answer isn't "everyone is wrong". It's a specific truth you can build a business on.

In Nigeria, the 0-to-1 opportunities are often the unglamorous ones: problems everyone works around every day.

This is part 1 of 4 on the business lessons in Zero to One. Next: why competition destroys profits.

What's one truth about doing business in Nigeria that most people would disagree with you on?""",
    ),
    "2026-10-24": dict(
        name="zto1-2", img="glass-house.jpg", kicker="Business · Zero to One, part 2",
        hook="Competition feels safe. ==It kills your profit.==",
        title="Zero to One, part 2: competition is for losers",
        slides=[
            [("q", "Roland, isn't competition good for business? ⚔️"),
             ("r", "Good for customers, yes."),
             ("r", "For your profits? Thiel's answer is ==no.==")],
            [("r", "**Lesson 4: competition kills profit** 📉"),
             ("r", "When ten businesses sell the same thing, they cut prices until nobody makes real money."),
             ("r", "A business with ==no close substitute== keeps its margins and can plan for years, not weeks.")],
            [("r", "**Lesson 5: be honest about your market** 🎭"),
             ("r", "Copycats describe their market so narrowly they look unique: \"the only Ghanaian restaurant in Lekki\"."),
             ("r", "Ask the real question: ==what else could your customer buy instead?==")],
            [("r", "**Lesson 6: what makes a business hard to copy** 🏰"),
             ("r", "1. Technology that's **10x better**, not 10% better\n2. **Network effects:** it gets better as more people use it"),
             ("r", "3. **Economies of scale:** it gets cheaper as it grows\n4. A **brand** people trust")],
            [("r", "**Lesson 7: start small, then dominate** 🎯"),
             ("r", "Amazon started with books. Facebook started at one university. PayPal started with eBay's ==power sellers.=="),
             ("r", "Win a small market completely, then expand step by step.")],
            [("r", "**Lesson 8: don't chase \"disruption\"** 💥"),
             ("r", "Picking a fight with giants makes you their target."),
             ("r", "And rivalry makes you ==copy your rival== instead of building something new.")],
            end(2, "why being last can beat being first"),
        ],
        cap="Zero to One by Peter Thiel, part 2: why competition is for losers, and what makes a business hard to copy. ⚔️\n\nThe 4 moats, the start-small rule, and why \"disruption\" is a trap. Swipe →\n\n📌 Save it\n📤 Send it to a founder in a crowded market\n\n" + TAGS,
        li=""""Competition is for losers." That's Peter Thiel, and it's the most misunderstood idea in Zero to One.

He doesn't mean don't work hard. He means: if your business is the same as ten others, all ten of you will cut prices until nobody makes real money.

Walk through any market where ten shops sell the same phones on the same street. The customers win. The owners fight over thin margins.

What I'd take from part two:

1. Aim for a business with no close substitute. That's what lets you keep your margins and plan for years, not weeks.

2. Be honest about your market. Copycats define it so narrowly they look unique. The real test: what else could your customer buy instead?

3. Build what's hard to copy: technology that's 10x better, network effects, economies of scale, and a brand people trust.

4. Start small and win it completely. Amazon started with books, Facebook with one university, PayPal with eBay's power sellers.

5. Don't pick fights with giants. Rivalry makes you copy them instead of building something new.

Part 2 of 4 on the business lessons in Zero to One. Next: why being last can beat being first.

Which market around you is so crowded that nobody makes real money?""",
    ),
    "2026-10-25": dict(
        name="zto1-3", img="hourglass-half.jpg", kicker="Business · Zero to One, part 3",
        hook="Being first is overrated. ==Be the last mover.==",
        title="Zero to One, part 3: last mover advantage, the power law and having a plan",
        slides=[
            [("q", "Roland, isn't it best to be first to market? 🏁"),
             ("r", "Not always."),
             ("r", "Thiel argues the winner is often the ==last mover==: the last one to make a great leap, who then owns the market for years.")],
            [("r", "**Lesson 9: most value is in the future** ⏳"),
             ("r", "A great company earns most of its value from profits ==years from now.=="),
             ("r", "So the real question isn't \"can we grow this year?\" It's \"will this still matter in 10 years?\"")],
            [("r", "**Lesson 10: the power law** 📈"),
             ("r", "A few things produce most of the results."),
             ("r", "In venture investing, the best investment often ==returns more than all the others combined.==")],
            [("r", "**What that means for you** 🎯"),
             ("r", "Ten side hustles at half effort rarely add up."),
             ("r", "Find the ==one thing== you can be great at, and go deep.")],
            [("r", "**Lesson 11: you're not a lottery ticket** 🎟️"),
             ("r", "Many people treat success as luck: try lots of small things and hope one hits."),
             ("r", "Thiel argues for a ==definite plan==: decide what you're building and work towards it.")],
            [("r", "**Lesson 12: a plan beats endless pivoting** 🗺️"),
             ("r", "Testing and learning is useful. Tiny tweaks with no direction go nowhere."),
             ("r", "A ==bold plan, adjusted as you learn,== beats wandering.")],
            end(3, "the foundations, team and sales lessons"),
        ],
        cap="Zero to One by Peter Thiel, part 3: why the last mover wins, the power law, and why you're not a lottery ticket. ⏳\n\nTime, focus and planning, in 6 slides. Swipe →\n\n📌 Save it\n📤 Send it to the friend running 10 side hustles\n\n" + TAGS,
        li="""Being first is overrated. Being last can be worth more.

In Zero to One, Peter Thiel argues the real prize is being the last mover: making the last great improvement in a market, then owning it for years.

Part three of the book is about time and focus. What I'd take from it:

1. Most of a great company's value sits in the future. The question isn't "can we grow fast this year?" It's "will this still matter in ten years?"

2. Results follow a power law. A few things produce most of the outcome. In venture capital, one investment often returns more than all the others combined.

3. So ten side hustles at half effort rarely add up. Find the one thing you can be great at and go deep.

4. You are not a lottery ticket. Treating success as luck makes people try everything a little. A definite plan, adjusted as you learn, beats wandering.

That last one is hard advice in Nigeria, where uncertainty pushes everyone to spread themselves across many small bets. Sometimes that's survival. It rarely builds something that lasts.

Part 3 of 4 on the business lessons in Zero to One. Next: the foundations that decide whether a startup survives.

What's the one thing you'd go all in on if you stopped hedging?""",
    ),
    "2026-10-26": dict(
        name="zto1-4", img="clockwork-receipts.jpg", kicker="Business · Zero to One, part 4",
        hook="Most startups die from ==bad foundations,== not bad ideas.",
        title="Zero to One, part 4: foundations, team, sales and the 7 questions",
        slides=[
            [("q", "Roland, what kills most startups early? 🧱"),
             ("r", "Thiel's law:"),
             ("r", "A startup ==messed up at its foundation== can't be fixed later.")],
            [("r", "**Lesson 13: choose co-founders carefully** 🤝"),
             ("r", "Start with people you have ==real history with.=="),
             ("r", "Agree early, in writing: who owns what, who decides what, and who works full-time.")],
            [("r", "**Lesson 14: build a tight team** 🧩"),
             ("r", "Hire people who'd love working ==together,== on a mission they believe in."),
             ("r", "Give each person one clear job, so they're not fighting over the same work.")],
            [("r", "**Lesson 15: sales matters as much as product** 📣"),
             ("r", "\"Build it and they will come\" is a myth."),
             ("r", "If you can't ==reach customers at a cost you can afford,== a great product still dies.")],
            [("r", "**Match sales to deal size** 💰"),
             ("r", "Big contracts: the founder in the room, selling personally."),
             ("r", "Small purchases: marketing, referrals, ==word of mouth.== The middle is the hardest place to be.")],
            [("r", "**Lesson 16: the 7 questions** ✅"),
             ("r", "1. **Engineering:** 10x better?\n2. **Timing:** why now?\n3. **Monopoly:** a big share of a small market?\n4. **People:** the right team?"),
             ("r", "5. **Distribution:** how will you sell?\n6. **Durability:** still here in 10 years?\n7. **Secret:** ==what do you see that others don't?==")],
            end(4, None),
        ],
        cap="Zero to One by Peter Thiel, part 4: foundations, team, sales, and the 7 questions every business must answer. 🧱\n\nThe final part of the series. Swipe →\n\n📌 Save it\n📤 Send it to your co-founder\n\n" + TAGS,
        li="""Most startups don't die from a bad idea. They die from bad foundations.

Peter Thiel calls it Thiel's law: a startup messed up at its foundation cannot be fixed.

The last part of Zero to One is the most practical. What I'd take from it:

1. Co-founders: start with people you have real history with. Agree early, in writing, on ownership, who decides what, and who works full-time.

2. Team: hire people who'd love working together on a mission they believe in. Give each person one clear area so they aren't fighting over the same work.

3. Sales: "build it and they will come" is a myth. If you can't reach customers at a cost the business can afford, a great product still dies.

4. Match your sales to your deal size. Big contracts need the founder in the room. Small purchases need marketing and word of mouth. The middle is the hardest place to be.

5. Before you build, answer seven questions: engineering, timing, monopoly, people, distribution, durability, and the secret only you see.

That's the end of my four-part series on the business lessons in Zero to One.

Which of the seven questions is your business weakest on right now?""",
    ),
}


def plain(t):
    return re.sub(r"[*=]", "", t).replace("\n", " ")


def build(date, d):
    Q = ROOT / "queue" / date
    IG, MEDIA = Q / "instagram", Q / "media"
    n = d["name"]
    cover(GEN / d["img"], d["hook"], IG / f"{n}-0.jpg", kicker=d["kicker"])
    rest = carousel(d["slides"], "Business · Zero to One", IG, n, offset=1)
    media = [f"instagram/{n}-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
    alt = [f"Cover. Text: {plain(d['hook'])}"] + ["Chat: " + " ".join(plain(t) for _, t in s) for s in d["slides"]]
    from PIL import Image
    pages = [cover(GEN / d["img"], d["hook"], MEDIA / f"{n}-p0.jpg", kicker=d["kicker"], handle="Roland Divine")]
    li_slides = d["slides"][:-1] + [[("r", "Save this for later 📌"), ("r", "Repost it for a founder who needs it ♻️"),
                                     ("r", "Follow **Roland Divine** for business, AI and crypto, explained straight.")]]
    pages += carousel(li_slides, "Business · Zero to One", MEDIA, f"{n}-p", offset=1, handle="Roland Divine")
    ims = [Image.open(x).convert("RGB") for x in pages]
    ims[0].save(MEDIA / f"{n}.pdf", save_all=True, append_images=ims[1:], resolution=150)
    (Q / "1300.json").write_text(json.dumps({
        "title": d["title"], "kind": "lesson", "series": "zero-to-one", "x": {"enabled": False},
        "linkedin": {"enabled": True, "text": d["li"], "media": f"media/{n}.pdf", "media_title": d["title"], "first_comment": SRC},
        "instagram": {"enabled": True, "caption": d["cap"], "media": media, "music": "Bill Withers – Lovely Day", "alt": alt}},
        indent=1, ensure_ascii=False))
    return Q


if __name__ == "__main__":
    for date, d in DAYS.items():
        print("built", build(date, d))
