"""Day 5 · Fri 16 Oct 2026 · first day of the new format (Roland, 15 Oct):
topics from live search demand, a generated scroll-stopping cover, LinkedIn = text + one image (no PDFs),
LinkedIn once a day. Run from studio/:  python days/day5.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-16"
GEN = ROOT / "assets" / "gen"

# ── 08:00 · LinkedIn + Instagram · AI water myth (search: "how do data centers use so much water",
#    "is it safe to live near data centers")
water_hook = "Does every ChatGPT chat drink a ==bottle of water?=="
water_ig = [
    [("q", "Roland, is it true every AI chat drinks a bottle of water? 😳"),
     ("r", "That idea came from a **2023 estimate** for an older model: about ==500 ml for every 10–50 replies.=="),
     ("r", "Newer numbers are much smaller.")],
    [("r", "**Google (2025):** a typical Gemini prompt uses about ==0.26 ml== of water."),
     ("r", "**OpenAI (2025):** about **0.32 ml** per ChatGPT query."),
     ("r", "That's about ==5 drops.== 💧")],
    [("q", "So the bottle thing is fake?"),
     ("r", "Mostly outdated. Even if you count the water used to make the electricity, it's around **1–2 ml** a prompt."),
     ("r", "One bottle ≈ ==hundreds of chats==, not 20.")],
    [("q", "Then why are people fighting data centers?"),
     ("r", "Because the problem is **local**, not per chat."),
     ("r", "One big data center can need ==millions of litres a day== for cooling, sometimes in places already short of water.")],
    [("r", "**The honest answer:**"),
     ("r", "Your prompt: a few drops."),
     ("r", "A giant data center next to a dry town: ==a real fight.==\n\nBoth are true.")],
    [("r", "Use AI without guilt, but ask ==where it's built== 🌍"),
     ("r", "Send this to the friend who says ChatGPT is drinking all the water 😄"),
     ("r", "Follow **@defi_ring_master** for AI, crypto and building, explained straight.")],
]
water_li = """Does every ChatGPT chat really drink a bottle of water?

That claim came from a 2023 study estimating about 500 ml of water for every 10 to 50 replies from an older model. It spread everywhere. The newer, measured numbers are a lot smaller:

→ Google (2025): a typical Gemini text prompt uses about 0.26 ml of water
→ OpenAI (2025): about 0.32 ml per ChatGPT query
→ Even counting the water used to generate the electricity, estimates land around 1 to 2 ml per prompt

So one bottle of water covers hundreds of chats, not 20.

But that doesn't mean the water worry is made up. It's just aimed at the wrong place.

The real issue is local. A single large data center can need millions of litres a day for cooling, and some are being built in regions that are already short of water. That's why communities are pushing back.

Your prompt: a few drops.
A giant data center next to a dry town: a real fight.

Both are true, and the second one is the conversation worth having as AI infrastructure gets built out across the world, including in Africa.

Should countries require new data centers to publish their water use before they're approved?

Sources: Google Cloud, "Measuring the environmental impact of AI inference" (2025); Sam Altman, "The Gentle Singularity" (2025); Li et al., UC Riverside (2023)."""

water_cap = """Does every ChatGPT chat drink a bottle of water? 💧

The real numbers are surprising, and so is the part people get wrong. Swipe →

📤 Send this to the friend who says AI is drinking all the water

#ai #chatgpt #datacenters #tech"""

# ── 13:00 · Instagram · WhatsApp AI agent (search: "how do i automate whatsapp messages",
#    "how do i automate my business", "how can ai help small businesses")
wa_hook = "Your WhatsApp can now reply to customers ==while you sleep.=="
wa_ig = [
    [("q", "Roland, wait. WhatsApp can reply by itself now? 👀"),
     ("r", "Yes. It's called **Meta Business Agent**, inside the ==WhatsApp Business app.=="),
     ("r", "It answers questions, recommends products, books appointments, and hands tough chats back to you.")],
    [("r", "**How to turn it on:**"),
     ("r", "1️⃣ Open WhatsApp Business → **Tools**\n2️⃣ Tap **Meta Business Agent**\n3️⃣ Link your account and confirm"),
     ("r", "4️⃣ Let it learn from your past chats. Add your ==catalog or website.==")],
    [("r", "5️⃣ **Test it from another number** before you switch it on."),
     ("r", "Ask it the questions your customers ask. Fix the answers you don't like."),
     ("r", "Then activate it. ✅")],
    [("q", "Is it free?"),
     ("r", "It launched **free**. Meta says paid tiers will come through ==WhatsApp Business Premium.=="),
     ("r", "It's rolling out gradually, so it may not show on your account yet.")],
    [("q", "Any catch?"),
     ("r", "It only **replies**. No broadcasts, no follow-ups."),
     ("r", "While it's on, broadcast lists, disappearing messages and message editing ==are switched off.==")],
    [("r", "Start small: give it ==the 10 questions you answer every day== (price, location, delivery)."),
     ("r", "Send this to a business owner who answers the same DMs all day 📤"),
     ("r", "Follow **@defi_ring_master** for AI that saves you hours.")],
]
wa_cap = """Your WhatsApp can now reply to customers while you sleep 😴📲

Meta Business Agent is inside the WhatsApp Business app. Here's how to switch it on, what it costs and the catch nobody mentions. Swipe →

📌 Save it for later
📤 Send it to a business owner who's always on WhatsApp

Source: TechCrunch, June 2026.

#whatsappbusiness #smallbusiness #ai #automation"""

# ── 19:00 · Instagram · first AI agent, free (search: "how to build ai agents for free",
#    "how to create ai agents", "how do i create ai agent")
gem_hook = "Build your first ==AI agent== tonight. Free."
gem_ig = [
    [("q", "Roland, I want to build an AI agent but I can't code 😩"),
     ("r", "You don't need to. Start with a **Gem** in Google Gemini."),
     ("r", "==Free==, and about 10 minutes.")],
    [("r", "**Step 1: pick one boring task.**"),
     ("r", "Replying to customer questions. Turning notes into a to-do list. Writing your weekly report."),
     ("r", "One task. ==Not your whole life.==")],
    [("r", "**Step 2: open gemini.google.com on a computer.**"),
     ("r", "Open the **Gem manager** → new Gem."),
     ("r", "You create Gems on the web, then ==use them on your phone.==")],
    [("r", "**Step 3: brief it like a new staff member.**"),
     ("r", "\"You reply to customers of my bakery. Prices are in the file. Keep it short and friendly. If someone complains, say Roland will call back.\"")],
    [("r", "**Step 4: upload what it should know.**"),
     ("r", "Price list, FAQ, old emails."),
     ("r", "Then ==test it with 10 real questions== and fix the instructions until it's right.")],
    [("q", "Wait, that's an agent?"),
     ("r", "It's your first one: it knows your files and follows your rules. 🧠"),
     ("r", "Next level is letting it ==take actions== (send emails, update sheets). That's a future post.")],
    [("r", "Build it tonight 📌 Save this."),
     ("r", "Tag the friend who keeps saying \"I'll learn AI later\" 😄"),
     ("r", "Follow **@defi_ring_master** to build with AI, step by step.")],
]
gem_cap = """Build your first AI agent tonight. Free. No code. 🤖

4 steps with Google Gemini's Gems, plus the one mistake that makes most people give up. Swipe →

📌 Save it and do it tonight
📤 Tag the friend who keeps saying "I'll learn AI later"

#ai #aiagents #gemini #nocode #productivity"""

# ── Stories (Instagram only)
STORIES = {
    "s0900": ("ice-server.jpg", "Every AI chat drinks a bottle of water. ==True or false?==", "New post · tap my profile"),
    "s1100": ("phone-glow.jpg", "What question do customers ask you ==10 times a day?==", "Reply 👇"),
    "s1400": ("phone-glow.jpg", "WhatsApp can now ==reply for you.== How to turn it on is on my page.", "New post · tap my profile"),
    "s1700": ("paper-robot.jpg", "Which boring task would you ==hand to an AI== first?", "Reply 👇"),
    "s2100": ("paper-robot.jpg", "Your first AI agent, ==free, in 10 minutes.== Guide is up.", "New post · tap my profile"),
}


def build():
    IG, MEDIA, ST = Q / "instagram", Q / "media", Q / "stories"
    posts = {
        "0800": ("water", "ice-server.jpg", water_hook, "AI · myth check", water_ig, water_cap, water_li,
                 "Myth check: AI and water", "Bill Withers – Lovely Day"),
        "1300": ("wa", "phone-glow.jpg", wa_hook, "Business · AI", wa_ig, wa_cap, None,
                 "How to: WhatsApp AI agent", "Earth, Wind & Fire – September"),
        "1900": ("gem", "paper-robot.jpg", gem_hook, "AI · how to", gem_ig, gem_cap, None,
                 "How to: first AI agent, free", "Sade – Smooth Operator"),
    }
    for slot, (name, img, hook, kicker, slides, cap, li, title, music) in posts.items():
        cover(GEN / img, hook, IG / f"{name}-0.jpg", kicker=kicker)
        rest = carousel(slides, "AI & business", IG, name, offset=1)
        media = [f"instagram/{name}-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
        d = {"title": title, "kind": "lesson", "x": {"enabled": False},
             "linkedin": {"enabled": False},
             "instagram": {"enabled": True, "caption": cap, "media": media, "music": music}}
        if li:
            cover(GEN / img, hook, MEDIA / f"{name}-cover.jpg", kicker=kicker, handle="Roland Divine", swipe=False)
            d["linkedin"] = {"enabled": True, "text": li, "media": f"media/{name}-cover.jpg"}
        (Q / f"{slot}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
    st = []
    for at, (img, text, foot) in STORIES.items():
        cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (Q / "stories.json").write_text(json.dumps(st, indent=2))


if __name__ == "__main__":
    build()
    print("built", Q)
