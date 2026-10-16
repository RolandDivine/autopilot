"""Day 6 · Sat 17 Oct 2026. Run from studio/:  python days/day6.py
08:00 pays off the 16 Oct teaser (tasks a small business can automate this weekend + free tools).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-17"
GEN = ROOT / "assets" / "gen"

# ── 08:00 · teaser payoff · small business automation (search: "how to automate my business",
#    "best ai agents for small business", "small business ai")
auto_hook = "5 jobs you can ==hand off this weekend.== For free."
auto_ig = [
    [("q", "Roland, you said I'm doing work a free tool could do. Like what? 🤔"),
     ("r", "Five jobs most small businesses still do ==by hand.=="),
     ("r", "Each one takes an afternoon to set up. All free to start.")],
    [("r", "**1. Bookings** 📅"),
     ("r", "Stop the \"what time works for you?\" back-and-forth."),
     ("r", "**Google Calendar booking page** (free with a Google account) or **Calendly free** (1 event type). Send ==one link.==")],
    [("r", "**2. The same WhatsApp answers** 💬"),
     ("r", "WhatsApp Business → **Business tools**: greeting message, away message, ==quick replies.=="),
     ("r", "Type /price and your price list appears.")],
    [("r", "**3. Invoices and chasing payment** 🧾"),
     ("r", "**Zoho Invoice** has a free plan with ==recurring invoices and automatic payment reminders.=="),
     ("r", "No more awkward \"just following up\" messages.")],
    [("r", "**4. Orders and sign-ups** 📝"),
     ("r", "A **Google Form** drops every order straight into a ==Google Sheet.=="),
     ("r", "**5. Social posts** 📲 Schedule the whole week of Facebook and Instagram posts in **Meta Business Suite**, free.")],
    [("q", "What's the catch?"),
     ("r", "Free plans have limits: Calendly free has no reminder emails, and most tools cap users."),
     ("r", "And don't automate a mess. ==Fix the process first==, then hand it off.")],
    [("r", "Pick **one** this weekend. Just one. ✅"),
     ("r", "📌 Save this. 📤 Send it to the business owner who's always \"too busy\"."),
     ("r", "Follow **@defi_ring_master** for AI and tools that save you hours.")],
]
auto_cap = """5 jobs you can hand off this weekend. For free. ⏳

Bookings, WhatsApp answers, invoices, orders and posts: the free tool for each and the catch. Swipe →

📌 Save it for the weekend
📤 Send it to the business owner who's always "too busy"

#smallbusiness #automation #productivity #entrepreneur"""
auto_li = """Your business isn't short of time. It's spending it on work a free tool could do.

Here are five jobs you can hand off this weekend, and the tool for each one.

1. Bookings
Stop the "what time works for you?" back-and-forth. A Google Calendar booking page is free with a personal Google account. Calendly's free plan gives you one event type. Send one link instead of ten messages.

2. The same WhatsApp answers
WhatsApp Business has greeting messages, away messages and quick replies under Business tools. Save your price list as a quick reply and send it in two taps.

3. Invoices and chasing payment
Zoho Invoice has a free plan with recurring invoices and automatic payment reminders. The tool does the awkward follow-up, not you.

4. Orders and sign-ups
A Google Form sends every order straight into a Google Sheet. No more scrolling through chats to find who ordered what.

5. Social posts
Meta Business Suite lets you schedule a full week of Facebook and Instagram posts for free.

The catch: free plans have limits. Calendly's free plan has no reminder emails, and most tools cap the number of users.

The mistake I'd avoid: automating a messy process. If your pricing changes every week, a quick reply just sends the wrong price faster. Fix the process first, then hand it off.

Pick one this weekend. Just one.

Which of these five eats the most of your week right now?"""

# ── 13:00 · crypto myth check · phone mining (search: "how to bitcoin mine on phone",
#    "how to bitcoin mine on pc", "how do i bitcoin mine")
mine_hook = "Can your phone mine Bitcoin? ==Here's the math.=="
mine_ig = [
    [("q", "Roland, can I mine Bitcoin on my phone? 📱⛏️"),
     ("r", "Technically yes. In practice, ==no.=="),
     ("r", "Here are the numbers.")],
    [("r", "The whole Bitcoin network does about **970 quintillion guesses a second** (≈970 EH/s, Oct 2026)."),
     ("r", "A phone does ==less than 1 million.=="),
     ("r", "That's like one raindrop against every ocean on Earth.")],
    [("q", "So how long would my phone take to win a block?"),
     ("r", "Mining alone: about ==37 billion years.==\nA laptop: about **185 million years.**"),
     ("r", "The universe is 13.8 billion years old. 😅")],
    [("q", "But I've seen mining apps paying people!"),
     ("r", "Apple's rules don't allow apps that mine on your phone. Google Play banned them in **2018.**"),
     ("r", "So most \"mining apps\" are ==cloud-mining schemes or ad farms==, and many never let you withdraw.")],
    [("q", "Do the big machines make money?"),
     ("r", "A top machine (~473 TH/s) earns about **$19 a day**, but uses about **$23** of power at $0.17/kWh."),
     ("r", "Miners profit with ==cheap power at scale==, not at home.")],
    [("r", "**The honest answer:**"),
     ("r", "Mining is an industry now, not a side hustle."),
     ("r", "Any app promising daily Bitcoin from your phone is ==selling you something.== ⚠️")],
    [("r", "📤 Send this to the friend with a \"mining app\" on their phone."),
     ("r", "Education, not financial advice."),
     ("r", "Follow **@defi_ring_master** for crypto, explained straight.")],
]
mine_cap = """Can your phone mine Bitcoin? Here's the math. 📱⛏️

37 billion years, app store bans, and why most "mining apps" are selling you something. Swipe →

📤 Send this to the friend with a mining app
Education, not financial advice.

#bitcoin #crypto #cryptoscams #bitcoinmining"""
mine_li = """Can you mine Bitcoin on your phone?

Technically yes. In practice, the math says no, and the apps that say otherwise are selling you something.

The numbers, as of October 2026:

→ The Bitcoin network does about 970 EH/s, roughly 970 quintillion guesses a second
→ A phone does less than 1 million a second. A laptop, around 100 million
→ Mining alone, a phone would expect to find a block in about 37 billion years. A laptop, about 185 million years

Even the big machines struggle at home. A top-end miner (around 473 TH/s) earns about $19 a day, but burns about $23 of electricity at $0.17 per kWh. Mining pays when you have cheap power at industrial scale.

So what are all those "mining apps"?

Apple's App Store rules don't allow apps that mine on the device. Google Play banned on-device mining in 2018. What's left is mostly cloud-mining schemes and ad farms, and many cap or block withdrawals. Trend Micro found fake cloud-mining apps on Google Play back in 2021.

The mistake I'd avoid: paying a "mining" app or platform to "boost" your earnings. That boost is usually how the scheme makes its money.

Mining is an industry now, not a side hustle.

Have you or someone you know ever tried a phone mining app? What happened when it was time to withdraw?

Education, not financial advice.

Sources: mempool.space (network hashrate); OneMiners profitability estimates (Oct 2026); Apple App Review Guidelines 3.1.5; Google Play policy (2018); Trend Micro (2021)."""

# ── 19:00 · cybersecurity how-to · apps with access to your Google account
#    (HN: "I never authorized an integration that scans my secrets"; search: cybersecurity questions)
keys_hook = "How many apps can read your Gmail ==right now?=="
keys_ig = [
    [("q", "Roland, which apps can see my Google account? 👀"),
     ("r", "Every \"Sign in with Google\" and every \"Allow access\" you ever clicked."),
     ("r", "Most people have ==dozens== and forgot them all.")],
    [("r", "**Check in 2 minutes:**"),
     ("r", "1️⃣ Go to **myaccount.google.com/linkedapps**\n(or Google Account → Security → your connections to third-party apps)"),
     ("r", "2️⃣ Scroll the list. ==Be honest== about what you still use.")],
    [("r", "Google sorts them into 4 kinds:"),
     ("r", "🔑 **Sign in with Google**\n🔗 **Linked account**\n📂 **Access to your Google Account** (can read some of your data)\n🤖 **Agent access**"),
     ("r", "The ==\"Access to your Google Account\"== ones matter most.")],
    [("r", "3️⃣ Tap an app → **See details** → read what it can access."),
     ("r", "4️⃣ Don't use it anymore? **Remove access** → **Confirm.** ✅")],
    [("q", "Does that delete my data from the app?"),
     ("r", "No. Removing access ==stops future access==. Data it already took stays with that app."),
     ("r", "Delete your account inside the app too if you're worried.")],
    [("r", "Make it a habit: ==every 3 months==, 2 minutes. 🗓️"),
     ("r", "📌 Save this. 📤 Send it to the friend who signs into everything with Google."),
     ("r", "Follow **@defi_ring_master** for tech that keeps you safe.")],
]
keys_cap = """How many apps can read your Gmail right now? 👀

The 2-minute check, the 4 kinds of access, and the one thing removing access doesn't do. Swipe →

📌 Save it
📤 Send it to the friend who signs into everything with Google

#cybersecurity #google #privacy #techtips"""
keys_li = """How many apps can read your Gmail right now?

Most people don't know. Every "Sign in with Google" and every "Allow access" you ever clicked is still on a list.

Here's the 2-minute check:

1. Go to myaccount.google.com/linkedapps (or Google Account, then Security, then your connections to third-party apps and services)

2. Look at the four kinds of access Google lists:
→ Sign in with Google
→ Linked account
→ Access to your Google Account (the app can read some of your data)
→ Agent access (Gemini or your AI agents can use the app)

3. Open anything you don't recognise, select See details, and read what it can reach

4. If you don't use it anymore, select Remove access and confirm

The catch nobody mentions: removing access stops future access. It doesn't delete the data the app already collected. For that, delete your account inside the app itself.

The mistake I'd avoid: clicking "Allow" on a free tool because it saves you five minutes. Read what it asks for. A PDF converter has no reason to read your email.

Do this every three months. It takes two minutes.

When you check your list, how many apps are on it that you don't remember connecting?

Source: Google Account Help, "Manage connections between your Google Account and third parties"."""

# ── 21:00 · teaser for 18 Oct 08:00 (ChatGPT Projects: give ChatGPT a home for your business). Logged in studio/teasers.md.
TEASER = ("jar-notes.jpg",
          "Do you know why ChatGPT keeps forgetting your business? ==It has no home.==",
          "Tomorrow · 8 AM",
          """Do you know why ChatGPT keeps forgetting your business? 🫙

Tomorrow at 8 AM: how to give it a home, so you stop explaining yourself in every new chat.

🔔 Turn on notifications so you don't miss it
📤 Send this to the friend who re-types the same prompt every day

#chatgpt #ai #productivity #smallbusiness""")

STORIES = {
    "s0900": ("clockwork-receipts.jpg", "5 jobs you can ==hand off this weekend.== Free tools on my page.", "New post · tap my profile"),
    "s1100": ("phone-ore.jpg", "Have you ever tried a ==\"mining app\"?== What happened?", "Reply 👇"),
    "s1400": ("phone-ore.jpg", "Can your phone mine Bitcoin? ==The math is on my page.==", "New post · tap my profile"),
    "s1700": ("glass-keys.jpg", "When did you last check ==which apps can read your email?==", "Reply 👇"),
    "s2100": None,
}


def build():
    IG, MEDIA, ST = Q / "instagram", Q / "media", Q / "stories"
    for d in (IG, MEDIA, ST):
        d.mkdir(parents=True, exist_ok=True)
    posts = {
        "0800": ("auto", "clockwork-receipts.jpg", auto_hook, "Business · free tools", auto_ig, auto_cap, auto_li,
                 "How to: 5 jobs to automate this weekend", "Whitney Houston – I Wanna Dance with Somebody", "pdf"),
        "1300": ("mine", "phone-ore.jpg", mine_hook, "Crypto · myth check", mine_ig, mine_cap, mine_li,
                 "Myth check: mining Bitcoin on your phone", "George Michael – Faith", "image"),
        "1900": ("keys", "glass-keys.jpg", keys_hook, "Security · how to", keys_ig, keys_cap, keys_li,
                 "How to: check apps with access to your Google account", "Lionel Richie – Hello", "image"),
    }
    for slot, (name, img, hook, kicker, slides, cap, li, title, music, li_kind) in posts.items():
        cover(GEN / img, hook, IG / f"{name}-0.jpg", kicker=kicker)
        rest = carousel(slides, "AI, crypto & business", IG, name, offset=1)
        media = [f"instagram/{name}-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
        d = {"title": title, "kind": "lesson", "x": {"enabled": False},
             "linkedin": {"enabled": False},
             "instagram": {"enabled": True, "caption": cap, "media": media, "music": music}}
        if li_kind == "image":
            cover(GEN / img, hook, MEDIA / f"{name}-cover.jpg", kicker=kicker, handle="Roland Divine", swipe=False)
            d["linkedin"] = {"enabled": True, "text": li, "media": f"media/{name}-cover.jpg"}
        else:
            from PIL import Image
            pages = [cover(GEN / img, hook, MEDIA / f"{name}-p0.jpg", kicker=kicker, handle="Roland Divine")]
            li_slides = slides[:-1] + [[("r", "Save this for later 📌"),
                                        ("r", "Repost it for someone who needs it ♻️"),
                                        ("r", "Follow **Roland Divine** for AI, crypto and building, explained straight.")]]
            pages += carousel(li_slides, "AI, crypto & business", MEDIA, f"{name}-p", offset=1, handle="Roland Divine")
            ims = [Image.open(x).convert("RGB") for x in pages]
            ims[0].save(MEDIA / f"{name}.pdf", save_all=True, append_images=ims[1:], resolution=150)
            d["linkedin"] = {"enabled": True, "text": li, "media": f"media/{name}.pdf", "media_title": title}
        (Q / f"{slot}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
    img, hook, kicker, cap = TEASER
    cover(GEN / img, hook, IG / "teaser-0.jpg", kicker=kicker, swipe=False)
    (Q / "2100.json").write_text(json.dumps({
        "title": "Teaser: tomorrow 8 AM", "kind": "story", "x": {"enabled": False}, "linkedin": {"enabled": False},
        "instagram": {"enabled": True, "caption": cap, "media": ["instagram/teaser-0.jpg"],
                      "music": "Michael Bolton – How Am I Supposed to Live Without You"}}, indent=1, ensure_ascii=False))
    cover(GEN / img, hook, ST / "s2100.jpg", kicker=kicker, size=(1080, 1920), pos="top", swipe=False)
    st = []
    for at, v in STORIES.items():
        if v is not None:
            img, text, foot = v
            cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (Q / "stories.json").write_text(json.dumps(st, indent=2))


if __name__ == "__main__":
    build()
    print("built", Q)
