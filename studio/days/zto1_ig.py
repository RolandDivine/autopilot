"""Instagram version of Zero to One, decoded (Roland, 23 Oct 2026): people-photo covers (same as LinkedIn) +
a more conversational WhatsApp-style chat that talks WITH the reader, asks them questions, and ends with a CTA.
Only touches the instagram part of queue/<date>/1300.json. Run from studio/: python days/zto1_ig.py"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TAGS = "#business #entrepreneurship #startups #founders #zerotoone"
FOLLOW = "Follow **@defi_ring_master** and turn on 🔔 to join a community of builders learning business, AI and crypto together."

IG = {
    "2026-10-23": ("zto1-1", [
        [("q", "Roland, I keep hearing about this book Zero to One. Is it worth it? 📘"),
         ("r", "Honestly? It's one of the books founders keep coming back to."),
         ("r", "Give me 2 minutes and I'll give you the gist. ==Deal?== 🤝")],
        [("q", "Okay, go 👀"),
         ("r", "Peter Thiel says there are 2 ways to build."),
         ("r", "**1 to n:** copy what already works.\n**0 to 1:** build something ==that didn't exist before.==")],
        [("q", "But copying is safer na? It's already proven 😅"),
         ("r", "True! And that's exactly the problem."),
         ("r", "If it's proven, ==everyone is already doing it.== Now you're fighting 10 others on price.")],
        [("r", "Quick one. Look around your street 👀"),
         ("r", "How many people sell the exact same thing?"),
         ("r", "That's 1 to n. ==Lots of noise, thin profit.==")],
        [("r", "**Thiel's favourite question** ❓"),
         ("r", "What important truth do very few people agree with you on?"),
         ("r", "Sit with it for a second. ==Your answer could be your business.==")],
        [("q", "What if I don't have a \"secret\"? 🤔"),
         ("r", "Start with problems people complain about but have just accepted."),
         ("r", "Or markets big companies ignore because they look ==too small.== That's where secrets hide.")],
        [("r", "So, your turn 👇"),
         ("r", "Comment one truth about business in Nigeria ==most people would disagree with.=="),
         ("r", "I'll reply to every answer. 💬")],
        [("r", "This is Part 1 of 4: **Zero to One, decoded.** 📚 Part 2 drops tomorrow."),
         ("r", FOLLOW),
         ("r", "📌 Save it · 📤 Send it to your business partner")],
    ], "Zero to One by Peter Thiel, explained like a chat: why copying is the crowded road, and the one question every founder should answer. 📘\n\nPart 1 of 4. Swipe →\n\n💬 Comment: what's one truth about business in Nigeria most people would disagree with?\n📌 Save it · 📤 Send it to your business partner\n🔔 Follow @defi_ring_master for Part 2 tomorrow\n\n" + TAGS),
    "2026-10-24": ("zto1-2", [
        [("q", "Roland, competition is good for business, abi? ⚔️"),
         ("r", "For customers? Yes 😄"),
         ("r", "For your profit? Peter Thiel says ==no.==")],
        [("q", "How? 🤨"),
         ("r", "Picture 10 shops selling the same phone on one street."),
         ("r", "One drops the price. Then everyone does. ==Nobody makes real money.==")],
        [("r", "The goal is a business with ==no close substitute.=="),
         ("r", "When customers can't just walk next door, you keep your margin and can plan for years, not weeks.")],
        [("q", "But my business IS unique 💁🏾"),
         ("r", "Let me test you small 😅"),
         ("r", "If your customer didn't buy from you, ==what would they buy instead?== That's your real competition.")],
        [("r", "**What makes a business hard to copy** 🏰"),
         ("r", "1. Tech that's **10x better**, not 10%\n2. **Network effects:** better as more people join"),
         ("r", "3. **Scale:** cheaper as you grow\n4. A **brand** people trust")],
        [("q", "So where do I even start?"),
         ("r", "Small. Very small. 🎯"),
         ("r", "Amazon started with books. Facebook with one university. ==Win a small market completely,== then expand.")],
        [("r", "And please, don't pick fights with giants 🙏🏾"),
         ("r", "Rivalry makes you copy them instead of building something new.")],
        [("r", "Your turn 👇 Which market near you is ==so crowded nobody makes money?=="),
         ("r", "Part 2 of 4: **Zero to One, decoded.** Part 3 drops tomorrow. " + FOLLOW),
         ("r", "📌 Save it · 📤 Send it to a founder friend")],
    ], "Zero to One by Peter Thiel, part 2: why competition is for losers, and what makes a business hard to copy. ⚔️\n\nExplained like a chat. Swipe →\n\n💬 Comment: which market near you is so crowded nobody makes money?\n📌 Save it · 📤 Send it to a founder friend\n🔔 Follow @defi_ring_master for Part 3 tomorrow\n\n" + TAGS),
    "2026-10-25": ("zto1-3", [
        [("q", "Roland, isn't it best to be first to market? 🏁"),
         ("r", "That's what everyone thinks."),
         ("r", "Peter Thiel says the winner is often the ==last mover==: the last one to make a big leap, who then owns the market for years.")],
        [("q", "Hmm, why does that matter?"),
         ("r", "Because most of a great company's value comes from profits ==years from now.=="),
         ("r", "So don't just ask \"can I grow this month?\" Ask \"will this still matter in 10 years?\"")],
        [("r", "**The power law** 📈"),
         ("r", "A few things produce most of the results."),
         ("r", "In venture capital, one great investment often ==returns more than all the others combined.==")],
        [("q", "So what does that mean for me? 🤔"),
         ("r", "Be honest: how many side hustles are you running right now? 😅"),
         ("r", "Ten things at half effort rarely add up. ==Find the one thing== and go deep.")],
        [("r", "**You're not a lottery ticket** 🎟️"),
         ("r", "A lot of us try small things everywhere and hope one hits."),
         ("r", "Thiel argues for a ==definite plan:== decide what you're building, then work towards it every day.")],
        [("q", "But plans change now 🤷🏾‍♂️"),
         ("r", "Of course! Adjust as you learn."),
         ("r", "Just don't wander. ==A bold plan you keep adjusting== beats random pivoting.")],
        [("r", "Your turn 👇"),
         ("r", "If you stopped hedging, what's the ==one thing you'd go all in on?=="),
         ("r", "Tell me in the comments. I read every one. 💬")],
        [("r", "Part 3 of 4: **Zero to One, decoded.** 📚 The final part drops tomorrow."),
         ("r", FOLLOW),
         ("r", "📌 Save it · 📤 Send it to the friend with 10 side hustles")],
    ], "Zero to One by Peter Thiel, part 3: why the last mover wins, the power law, and why you're not a lottery ticket. ⏳\n\nExplained like a chat. Swipe →\n\n💬 Comment: what's the one thing you'd go all in on?\n📌 Save it · 📤 Send it to the friend with 10 side hustles\n🔔 Follow @defi_ring_master for the final part tomorrow\n\n" + TAGS),
    "2026-10-26": ("zto1-4", [
        [("q", "Roland, why do so many startups die early? 🧱"),
         ("r", "Usually not because of the idea."),
         ("r", "Thiel's law: a startup ==messed up at its foundation== can't be fixed later.")],
        [("q", "Foundation like how?"),
         ("r", "Co-founders first 🤝"),
         ("r", "Start with people you have ==real history with.== Then agree in writing: who owns what, who decides, who's full-time.")],
        [("r", "I know, money and paperwork talk feels awkward with friends 😬"),
         ("r", "But it's ==far more awkward later.== Have the talk early.")],
        [("r", "**Your team** 🧩"),
         ("r", "Hire people who'd love working together on a mission they believe in."),
         ("r", "Give each person ==one clear job,== so nobody fights over the same work.")],
        [("q", "And if the product is really good, people will just come, right? 😅"),
         ("r", "That's one of the most expensive myths in business."),
         ("r", "If you can't ==reach customers at a cost you can afford,== a great product still dies.")],
        [("r", "**Match your selling to the deal size** 💰"),
         ("r", "Big contracts: you, the founder, in the room."),
         ("r", "Small purchases: marketing, referrals, word of mouth. ==The middle is the hardest.==")],
        [("r", "**The 7 questions** ✅"),
         ("r", "Engineering · Timing · Monopoly · People\nDistribution · Durability · Secret"),
         ("r", "Which one is your business ==weakest on?== Tell me 👇")],
        [("r", "That's the end of **Zero to One, decoded.** 📚 Thank you for following all 4 parts! 🙏🏾"),
         ("r", FOLLOW),
         ("r", "📌 Save the series · 📤 Send it to your co-founder")],
    ], "Zero to One by Peter Thiel, part 4: foundations, team, sales and the 7 questions every business must answer. 🧱\n\nThe final part, explained like a chat. Swipe →\n\n💬 Comment: which of the 7 questions is your business weakest on?\n📌 Save the series · 📤 Send it to your co-founder\n🔔 Follow @defi_ring_master and join a community of builders\n\n" + TAGS),
}


def plain(t):
    return re.sub(r"[*=]", "", t).replace("\n", " ")


for date, (name, slides, cap) in IG.items():
    Q = ROOT / "queue" / date
    IGD = Q / "instagram"
    for old in IGD.glob(f"{name}-*.jpg"):
        old.unlink()
    shutil.copy(Q / "media" / f"{name}-ed-li0.jpg", IGD / f"{name}-0.jpg")
    rest = carousel(slides, "Business · Zero to One", IGD, name, offset=1)
    media = [f"instagram/{name}-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
    f = Q / "1300.json"
    j = json.loads(f.read_text())
    hook = {"zto1-1": "Copying is easy. Building from zero is where the value is.", "zto1-2": "Ten shops, same phones, same street. Nobody wins.",
            "zto1-3": "Being first is overrated. Be the last mover.", "zto1-4": "Most startups die from bad foundations, not bad ideas."}[name]
    j["instagram"].update({"caption": cap, "media": media,
                           "alt": [f"Photo of people working together. Text: {hook}"] + ["Chat: " + " ".join(plain(t) for _, t in s) for s in slides]})
    f.write_text(json.dumps(j, indent=1, ensure_ascii=False))
    print(date, len(media), "images")
