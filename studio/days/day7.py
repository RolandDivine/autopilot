"""Day 7 · Sun 18 Oct 2026. Run from studio/:  python days/day7.py
08:00 pays off the 17 Oct teaser ("Do you know why ChatGPT keeps forgetting your business? It has no home.").
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-18"
GEN = ROOT / "assets" / "gen"

# ── 08:00 · teaser payoff · ChatGPT Projects (search: "how to chatgpt projects work", "how do i chatgpt")
proj_hook = "Stop re-explaining your business to ChatGPT. ==Give it a home.=="
proj_ig = [
    [("q", "Roland, why does ChatGPT keep forgetting my business? 😩"),
     ("r", "Because every new chat starts from zero."),
     ("r", "The fix is free: a ==Project.== One home for your business, with its own rules and files.")],
    [("r", "**Step 1: create the project** 📁"),
     ("r", "In the ChatGPT sidebar → **New project**."),
     ("r", "Name it after your business. ==Projects work on every plan, Free included.==")],
    [("r", "**Step 2: write the instructions** ✍️"),
     ("r", "Project menu (⋯) → **Instructions**."),
     ("r", "\"We sell handmade bags in Lagos. Prices in naira. Friendly tone. Never promise delivery in under 3 days.\"")],
    [("r", "**Step 3: add your files** 📎"),
     ("r", "Price list, FAQ, product details, past emails."),
     ("r", "Free plan: ==5 files== per project. Plus: 25.")],
    [("r", "**Step 4: chat inside the project** 💬"),
     ("r", "Every new chat there ==already knows== your rules and your files."),
     ("r", "No more pasting the same intro every day.")],
    [("q", "Any catch?"),
     ("r", "Instructions only apply **inside** that project."),
     ("r", "And don't upload anything private you wouldn't email. ==Your files sit with OpenAI.==")],
    [("r", "Set it up once tonight. Save hours every week. ⏳"),
     ("r", "📌 Save this. 📤 Send it to the friend who types the same prompt every day."),
     ("r", "Follow **@defi_ring_master** for AI that saves you time.")],
]
proj_cap = """Stop re-explaining your business to ChatGPT. Give it a home. 🏠

ChatGPT Projects: 4 steps, free on every plan, and the one thing you shouldn't upload. Swipe →

📌 Save it
📤 Send it to the friend who types the same prompt every day

#chatgpt #ai #productivity #smallbusiness"""
proj_li = """ChatGPT keeps forgetting your business because every new chat starts from zero.

The fix takes ten minutes and it's free: give your business its own Project.

A Project is a home inside ChatGPT with its own instructions and files. Every chat you start inside it already knows your rules. It works on every plan, including Free.

How to set it up:

1. In the ChatGPT sidebar, select New project and name it after your business

2. Open the project menu and add Instructions. Be specific: what you sell, where, your tone, your prices, what you never promise

3. Upload what it should know: price list, FAQ, product details. The Free plan allows 5 files per project, Plus allows 25

4. Start every work chat inside the project. No more pasting the same introduction every morning

The catch: the instructions only apply inside that project, and your files are stored with OpenAI. Don't upload anything you wouldn't put in an email.

The mistake I'd avoid: one giant project for everything. Make one per job (customer replies, social posts, invoices) and keep each one sharp.

What's the first project you'd set up?

Source: OpenAI Help Center, "Projects in ChatGPT"."""

# ── 13:00 · crypto · how stablecoins work (search: "how to stablecoins work", "how stablecoin issuers make money",
#    "how to buy stablecoins")
stab_hook = "Your $1 stablecoin earns interest. ==Just not for you.=="
stab_ig = [
    [("q", "Roland, how does a stablecoin stay at $1? 🤔"),
     ("r", "For every coin, the company says it holds ==$1 in reserves==: cash, short-term US Treasury bills, repo."),
     ("r", "You can swap 1 coin for $1 with the issuer. That keeps the price pinned.")],
    [("r", "**Here's the part nobody tells you:**"),
     ("r", "Those Treasury bills **pay interest.**"),
     ("r", "The issuer keeps it. You get ==zero.== 💸")],
    [("r", "**The numbers:**"),
     ("r", "Tether (USDT) made about **$13 billion** profit in 2024, with more than ==$186 billion== USDT in circulation by end-2025."),
     ("r", "Circle (USDC) earned **$2.7 billion** in 2025, mostly reserve interest.")],
    [("q", "So who checks the $1 is really there?"),
     ("r", "In the US, the **GENIUS Act** (2025) now requires 1:1 reserves in cash or short-term Treasuries, with ==monthly disclosure.=="),
     ("r", "It also bans issuers from paying holders interest.")],
    [("q", "Is it safe then?"),
     ("r", "Safer than most crypto, ==but not guaranteed.== Pegs have broken before (USDC dipped to $0.87 in March 2023 when a bank failed)."),
     ("r", "And if it sits on an exchange, you carry the exchange's risk too.")],
    [("r", "**Use stablecoins as a tool:** sending money, parking value between trades."),
     ("r", "Not a savings account. ==Know who holds the reserves.== 🔍"),
     ("r", "Education, not financial advice. Follow **@defi_ring_master** for crypto, explained straight.")],
]
stab_cap = """Your $1 stablecoin earns interest. Just not for you. 💸

How USDT and USDC stay at $1, who keeps the interest, and the risk nobody mentions. Swipe →

📤 Send this to the friend who keeps their savings in USDT
Education, not financial advice.

#stablecoins #crypto #usdt #usdc #bitcoin"""
stab_li = """Your $1 stablecoin earns interest. Just not for you.

Here's how USDT and USDC actually work, and who gets paid.

For every coin in circulation, the issuer says it holds $1 in reserves: cash, short-term US Treasury bills and repo. Big holders can swap 1 coin for $1 with the issuer, and that's what keeps the price pinned.

Those Treasury bills pay interest. The issuer keeps it. You get nothing.

The numbers:
→ Tether made about $13 billion in profit in 2024, with more than $186 billion USDT in circulation by end-2025
→ Circle reported $2.7 billion in revenue and reserve income for 2025, almost all of it interest on reserves

In the US, the GENIUS Act (2025) now requires 1:1 reserves in cash or short-term Treasuries, monthly disclosure, and bans issuers from paying holders interest.

Is a stablecoin safe? Safer than most crypto, but it can still break. USDC fell to about $0.87 in March 2023 when Silicon Valley Bank failed while holding part of its reserves. And a stablecoin on an exchange carries that exchange's risk too.

The mistake I'd avoid: treating USDT like a savings account. It's a tool for moving and parking money, not a place to earn.

Which stablecoin do you use most, and why that one?

Education, not financial advice.

Sources: Tether and Circle reports via Transak (2026); GENIUS Act, S.1582; Reuters (March 2023)."""

# ── 19:00 · AI · vibe coding (search: "how to vibe coding", "how to vibe coding free", "how safe is vibe coding")
vibe_hook = "You can build an app ==by just describing it.== Here's the catch."
vibe_ig = [
    [("q", "Roland, what's this \"vibe coding\" everyone's talking about? 👀"),
     ("r", "You describe the app in plain English. The AI ==writes the code.=="),
     ("r", "You test it, tell it what's wrong, repeat.")],
    [("r", "**Free tools to try tonight:**"),
     ("r", "**Lovable:** polished apps, 5 free credits a day."),
     ("r", "**Bolt:** fast builds, free daily token limit. ==Both run in your browser.==")],
    [("r", "**How to start (the right way):**"),
     ("r", "1️⃣ Pick one tiny problem. A booking form, a price calculator."),
     ("r", "2️⃣ Describe **who uses it** and **what they click**, step by step.")],
    [("r", "3️⃣ Build one screen at a time. Test it before asking for more."),
     ("r", "4️⃣ When something breaks, paste the exact error back to the AI."),
     ("r", "Small prompts ==save your free credits.==")],
    [("q", "So I don't need developers anymore?"),
     ("r", "Not so fast. ⚠️ A 2026 Carnegie Mellon study: AI code passed **61%** of functional tests…"),
     ("r", "…but only ==10.5%== passed security tests.")],
    [("r", "**The rule:** vibe code your prototype, not your bank."),
     ("r", "Never put real customer data or payments in it until ==someone who codes has checked it.== 🔐")],
    [("r", "Build something small this weekend. 🛠️"),
     ("r", "📌 Save this. 📤 Send it to the friend with an app idea and no developer."),
     ("r", "Follow **@defi_ring_master** to build with AI, step by step.")],
]
vibe_cap = """You can build an app by just describing it. Here's the catch. 🛠️

Vibe coding: 2 free tools, how to start, and the security number nobody talks about. Swipe →

📌 Save it
📤 Send it to the friend with an app idea and no developer

#vibecoding #ai #nocode #buildinpublic"""
vibe_li = """You can now build an app by describing it in plain English. That's vibe coding.

It's real, it's useful, and there's one number you should know before you trust it.

How it works: you describe what you want, the AI writes the code, you test it and tell it what's wrong.

Two tools you can try for free tonight:
→ Lovable: polished interfaces, 5 free credits a day
→ Bolt: fast builds, a free daily token allowance

How I'd start:
1. Pick one tiny problem: a booking form, a price calculator, a waitlist page
2. Describe who uses it and what they click, step by step
3. Build one screen at a time and test it before asking for more
4. When it breaks, paste the exact error back to the AI

The catch: a 2026 Carnegie Mellon study found AI-written code passed 61% of functional tests, but only 10.5% passed security tests.

So vibe code your prototype, not your bank. Don't put real customer data or payments into it until someone who can read code has checked it.

The mistake I'd avoid: one giant prompt for the whole app. Small steps burn fewer credits and break less.

What's the first small tool you'd build if code wasn't the problem?

Sources: Zapier, "Lovable vs. Bolt" (July 2026); Carnegie Mellon University (2026)."""

# ── 21:00 · teaser for 19 Oct 08:00 (start learning cybersecurity free, no experience). Logged in studio/teasers.md.
TEASER = ("circuit-lock.jpg",
          "Do you know you can start learning cybersecurity ==this week, free, with no experience?==",
          "Tomorrow · 8 AM",
          """Do you know you can start learning cybersecurity this week, free, with no experience? 🔐

Tomorrow at 8 AM: the free path I'd follow from zero, step by step.

🔔 Turn on notifications so you don't miss it
📤 Send this to the friend who keeps saying they want to get into tech

#cybersecurity #tech #learning #careers""")

STORIES = {
    "s0900": ("glass-house.jpg", "ChatGPT keeps forgetting your business? ==The fix is on my page.==", "New post · tap my profile"),
    "s1100": ("anchor-coin.jpg", "Do you hold any stablecoins? ==Which one, and why?==", "Reply 👇"),
    "s1400": ("anchor-coin.jpg", "Your stablecoin earns interest. ==Who keeps it?== Answer on my page.", "New post · tap my profile"),
    "s1700": ("typewriter-app.jpg", "If code wasn't a problem, ==what app would you build?==", "Reply 👇"),
    "s2100": None,
}

POSTS = {
    "0800": ("proj", "glass-house.jpg", proj_hook, "AI · how to", proj_ig, proj_cap, proj_li,
             "How to: ChatGPT Projects", "Anita Baker – Giving You the Best That I Got", "pdf"),
    "1300": ("stab", "anchor-coin.jpg", stab_hook, "Crypto · explained", stab_ig, stab_cap, stab_li,
             "Explained: how stablecoins make money", "Tracy Chapman – Give Me One Reason", "image"),
    "1900": ("vibe", "typewriter-app.jpg", vibe_hook, "AI · build", vibe_ig, vibe_cap, vibe_li,
             "How to: vibe coding, free", "Sade – By Your Side", "image"),
}


def build():
    IG, MEDIA, ST = Q / "instagram", Q / "media", Q / "stories"
    for d in (IG, MEDIA, ST):
        d.mkdir(parents=True, exist_ok=True)
    for slot, (name, img, hook, kicker, slides, cap, li, title, music, li_kind) in POSTS.items():
        cover(GEN / img, hook, IG / f"{name}-0.jpg", kicker=kicker)
        rest = carousel(slides, "AI, crypto & business", IG, name, offset=1)
        media = [f"instagram/{name}-0.jpg"] + [f"instagram/{Path(p).name}" for p in rest]
        d = {"title": title, "kind": "lesson", "x": {"enabled": False}, "linkedin": {"enabled": False},
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
                      "music": "Lionel Richie – Stuck on You"}}, indent=1, ensure_ascii=False))
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
