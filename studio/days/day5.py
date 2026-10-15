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

I checked the numbers. The answer is no, and the real problem is somewhere else.

The bottle claim came from a 2023 study estimating about 500 ml of water for every 10 to 50 replies from an older model. It spread everywhere. The newer, measured numbers are a lot smaller:

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

wa_li = """Your customers are messaging you at 2 AM.

Starting now, WhatsApp can answer them for you.

Meta has rolled out Meta Business Agent inside the WhatsApp Business app. It's an AI that replies to customer chats on your behalf: it answers questions, recommends products from your catalog, books appointments, and hands tricky conversations back to a human.

Setting it up takes about 10 minutes:

1. Open WhatsApp Business and go to Tools
2. Tap Meta Business Agent, link your account and confirm
3. Let it learn from your past chats and add your catalog or website
4. Message it from a second number and fix the answers you don't like
5. Then switch it on

Before you trust it with your customers, know this:

→ It launched free. Meta says paid tiers will come through WhatsApp Business Premium
→ It's rolling out gradually, so it may not be on your account yet
→ It only replies. No broadcasts, no follow-ups
→ While it's on, broadcast lists, disappearing messages and message editing are switched off

The mistake I'd avoid: handing it everything on day one.

Give it the 10 questions you answer every single day (price, location, delivery time). Keep the complaints and the big deals for yourself.

The full step-by-step is in the slides.

If you run a business on WhatsApp, which question would you hand to it first?

Source: TechCrunch, 3 June 2026."""

gem_li = """Most people who say "I'll learn AI later" are waiting for a course.

You don't need one. You can build your first AI agent tonight, for free, without writing code.

Here's how I'd do it with Google Gemini's Gems:

1. Pick one boring task
Replying to the same customer questions. Turning meeting notes into a to-do list. Drafting your weekly report. One task, not your whole job.

2. Open gemini.google.com on a computer
Go to the Gem manager and create a new Gem. You build it on the web and use it on your phone afterwards.

3. Brief it like a new staff member
"You reply to customers of my bakery. Prices are in the attached file. Keep it short and friendly. If someone complains, tell them the owner will call back."

4. Give it what it needs to know
Upload your price list, FAQ or old emails. Then test it with 10 real questions and fix the instructions until the answers are right.

That's it. It knows your files, it follows your rules, and it does one job well.

Is it a full "agent" that takes actions on its own? Not yet. That's the next step, connecting it to tools that send emails or update sheets. But this is where everyone who builds agents starts.

What's the one task you'd hand to your first AI agent?"""

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

# ── 21:00 · Instagram feed + story · "Do you know…?" teaser for tomorrow's 8 AM post (Roland, 15 Oct).
#    The promise must be kept: tomorrow's 8 AM post answers it. Logged in studio/teasers.md.
TEASER = ("chrome-hourglass.jpg",
          "Do you know your business is stuck because ==you're doing work a free tool could do?==",
          "Tomorrow · 8 AM",
          """Do you know your business is stuck because you're doing work a free tool could do? ⏳

Tomorrow at 8 AM I'm showing you the tasks you can hand off this weekend, and the free tools that do them.

🔔 Turn on notifications so you don't miss it
📤 Send this to the business owner who's always "too busy"

#smallbusiness #automation #ai #entrepreneur""")

# ── Stories (Instagram only)
STORIES = {
    "s0900": ("ice-server.jpg", "Every AI chat drinks a bottle of water. ==True or false?==", "New post · tap my profile"),
    "s1100": ("phone-glow.jpg", "What question do customers ask you ==10 times a day?==", "Reply 👇"),
    "s1400": ("phone-glow.jpg", "WhatsApp can now ==reply for you.== How to turn it on is on my page.", "New post · tap my profile"),
    "s1700": ("paper-robot.jpg", "Which boring task would you ==hand to an AI== first?", "Reply 👇"),
    "s2100": None,  # the teaser (below) is the 9 PM story
}


def build():
    IG, MEDIA, ST = Q / "instagram", Q / "media", Q / "stories"
    posts = {
        "0800": ("water", "ice-server.jpg", water_hook, "AI · myth check", water_ig, water_cap, water_li,
                 "Myth check: AI and water", "Bill Withers – Lovely Day", "image"),
        "1300": ("wa", "phone-glow.jpg", wa_hook, "Business · AI", wa_ig, wa_cap, wa_li,
                 "How to: WhatsApp AI agent", "Earth, Wind & Fire – September", "pdf"),
        "1900": ("gem", "paper-robot.jpg", gem_hook, "AI · how to", gem_ig, gem_cap, gem_li,
                 "How to: first AI agent, free", "Sade – Smooth Operator", "image"),
    }
    for slot, (name, img, hook, kicker, slides, cap, li, title, music, li_kind) in posts.items():
        cover(GEN / img, hook, IG / f"{name}-0.jpg", kicker=kicker)
        rest = carousel(slides, "AI & business", IG, name, offset=1)
        media = [f"instagram/{name}-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
        d = {"title": title, "kind": "lesson", "x": {"enabled": False},
             "linkedin": {"enabled": False},
             "instagram": {"enabled": True, "caption": cap, "media": media, "music": music}}
        if li and li_kind == "image":
            cover(GEN / img, hook, MEDIA / f"{name}-cover.jpg", kicker=kicker, handle="Roland Divine", swipe=False)
            d["linkedin"] = {"enabled": True, "text": li, "media": f"media/{name}-cover.jpg"}
        elif li:  # PDF: the scroll-stopping cover first, then the chat slides, LinkedIn signoff last
            from PIL import Image
            pages = [cover(GEN / img, hook, MEDIA / f"{name}-p0.jpg", kicker=kicker, handle="Roland Divine")]
            li_slides = slides[:-1] + [[("r", "Save this for later 📌"),
                                        ("r", "Repost it for someone who needs it ♻️"),
                                        ("r", "Follow **Roland Divine** for AI, crypto and building, explained straight.")]]
            pages += carousel(li_slides, "AI & business", MEDIA, f"{name}-p", offset=1, handle="Roland Divine")
            ims = [Image.open(x).convert("RGB") for x in pages]
            ims[0].save(MEDIA / f"{name}.pdf", save_all=True, append_images=ims[1:], resolution=150)
            d["linkedin"] = {"enabled": True, "text": li, "media": f"media/{name}.pdf", "media_title": title}
        (Q / f"{slot}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
    img, hook, kicker, cap = TEASER
    cover(GEN / img, hook, IG / "teaser-0.jpg", kicker=kicker, swipe=False)
    (Q / "2100.json").write_text(json.dumps({
        "title": "Teaser: tomorrow 8 AM", "kind": "story", "x": {"enabled": False}, "linkedin": {"enabled": False},
        "instagram": {"enabled": True, "caption": cap, "media": ["instagram/teaser-0.jpg"],
                      "music": "Phil Collins – In the Air Tonight"}}, indent=1, ensure_ascii=False))
    cover(GEN / img, hook, ST / "s2100.jpg", kicker=kicker, size=(1080, 1920), pos="top", swipe=False)
    st = []
    for at, v in STORIES.items():
        if v is None:
            st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
            continue
        img, text, foot = v
        cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (Q / "stories.json").write_text(json.dumps(st, indent=2))


if __name__ == "__main__":
    build()
    print("built", Q)
