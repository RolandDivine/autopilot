"""Day 10 · Wed 21 Oct 2026. Run from studio/:  python days/day10.py
08:00 pays off the 20 Oct teaser ("Do you know one signature can empty your crypto wallet?").
21:00 teases 22 Oct 08:00 (which apps used your microphone / camera: iPhone App Privacy Report, Android Privacy dashboard).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-21"
GEN = ROOT / "assets" / "gen"

# ── 08:00 · teaser payoff · token approvals (search: "how to revoke token approvals", "wallet drained after signing")
appr_hook = "One click on \"approve\" can ==empty your wallet.== Check yours."
appr_ig = [
    [("q", "Roland, how can someone drain my wallet without my seed phrase? 😨"),
     ("r", "With your **permission.** Literally."),
     ("r", "When a crypto app asks you to ==\"approve\"==, you let its contract move your tokens.")],
    [("r", "**How the scam works** 🎣"),
     ("r", "A fake airdrop or mint site asks you to connect and sign."),
     ("r", "The signature is an approval, often ==unlimited.== Then they move your tokens whenever they like.")],
    [("r", "**The numbers** 📊"),
     ("r", "Scam Sniffer counted **$83.85 million** stolen by wallet-drainer phishing in 2025, from **106,106** victims."),
     ("r", "The biggest single theft: ==$6.5 million==, from one Permit signature.")],
    [("r", "**The 2-minute check** 🔍"),
     ("r", "Go to **revoke.cash** or Etherscan's **Token Approval Checker.**"),
     ("r", "Paste your wallet address. You'll see ==every app that can still spend your tokens.==")],
    [("r", "**Revoke what you don't use** ✂️"),
     ("r", "Old DEXs, forgotten mints, anything \"unlimited\" you don't recognise."),
     ("r", "Each revoke is a transaction, so it ==costs a little gas.==")],
    [("q", "How do I avoid it next time?"),
     ("r", "Never sign from a link in a DM or reply. Read the wallet pop-up: **approve** or **permit** = ==spend permission.=="),
     ("r", "Keep a separate small wallet for trying new apps.")],
    [("r", "Do the check tonight. It takes 2 minutes. ⏱️"),
     ("r", "📌 Save this. 📤 Send it to the friend who connects their wallet to everything."),
     ("r", "Education, not financial advice. Follow **@defi_ring_master**.")],
]
appr_cap = """How to check and revoke token approvals in your crypto wallet. One click on "approve" can empty it. ✍️

How approval scams work, the 2025 numbers, and the 2-minute check that shows who can still spend your tokens. Swipe →

📌 Save it
📤 Send it to the friend who connects their wallet to everything
Education, not financial advice.

#crypto #web3 #cryptosecurity #defi"""
appr_li = """Most crypto wallets that get drained never leak a seed phrase. The owner signs the theft themselves.

Here's how it works, and the two-minute check I'd do tonight.

When a crypto app asks you to "approve", you give its smart contract permission to move your tokens. Often that permission is unlimited, and it stays live until you revoke it.

Drainer sites use this. A fake airdrop or mint page asks you to connect and sign. The signature is an approval or a Permit, and they move your tokens whenever they like.

The scale: Scam Sniffer counted $83.85 million stolen by wallet-drainer phishing in 2025, across 106,106 victims. The biggest single theft was $6.5 million, from one Permit signature.

The check:
1. Open revoke.cash or Etherscan's Token Approval Checker
2. Paste your wallet address
3. Revoke anything you don't use or don't recognise, starting with unlimited approvals
4. Expect a small gas fee per revoke, because each one is a transaction

To avoid it next time: never sign from a link in a DM or a reply, read the wallet pop-up before you click, and keep a small separate wallet for trying new apps.

The mistake I'd avoid: thinking "I only connected, I didn't send anything." Connecting is harmless. Signing an approval is not.

When did you last check your approvals?

Education, not financial advice.

Sources: Scam Sniffer 2025 Crypto Phishing Report; Trust Wallet, "Token approvals and wallet drainers"."""

# ── 13:00 · AI · Gemini free cut (search: "is gemini still free", "gemini flash lite free", "best free ai")
gem_hook = "Free Gemini just got ==a lot smaller.== Here's what to use."
gem_ig = [
    [("q", "Roland, why does free Gemini feel weaker lately? 🤔"),
     ("r", "Because it is."),
     ("r", "Since ==9 October 2026==, free users only get **Gemini 3.5 Flash-Lite**, Google's lightest model.")],
    [("r", "**What changed** 📉"),
     ("r", "Free accounts lost **3.6 Flash** and **3.1 Pro.**"),
     ("r", "Google spotted it in its support pages, ==not a big announcement.==")],
    [("r", "**What it costs to get it back** 💳"),
     ("r", "**Google AI Plus**, $4.99/month: keeps Flash, but Pro is going too."),
     ("r", "**Google AI Pro**, ==$19.99/month==: every model, plus Deep Think.")],
    [("q", "So what should I use for free?"),
     ("r", "**ChatGPT** and **Claude** free plans: strong for writing and thinking."),
     ("r", "**Perplexity** free: best when you need ==answers with sources.==")],
    [("r", "**My setup** 🧰"),
     ("r", "Writing and planning: ChatGPT or Claude."),
     ("r", "Research: Perplexity. Google Docs and Gmail help: ==Flash-Lite is still fine for that.==")],
    [("r", "**The catch** ⚠️"),
     ("r", "Free tiers change without warning. This one changed in a week."),
     ("r", "Don't build your business on ==one free plan.== Keep a second option ready.")],
    [("r", "📌 Save this. 📤 Send it to the friend who uses Gemini for everything."),
     ("r", "Follow **@defi_ring_master** for AI that saves you time and money.")],
]
gem_cap = """Free Gemini just got a lot smaller. Here's what to use. 📉

What Google removed on 9 October, what it costs to get it back, and the free tools I'd use instead. Swipe →

📌 Save it
📤 Send it to the friend who uses Gemini for everything

#ai #gemini #chatgpt #productivity"""
gem_li = """Free Gemini quietly got a lot smaller this month.

Since 9 October 2026, free Gemini users only get Gemini 3.5 Flash-Lite, Google's lightest model. Free accounts lost 3.6 Flash and 3.1 Pro. It surfaced through a change in Google's support pages, reported by 9to5Google, not a big launch event.

What it costs to get it back:
→ Google AI Plus, $4.99 a month: keeps Flash, but loses Pro on a date Google emails you
→ Google AI Pro, $19.99 a month: every model, plus Deep Think

If you don't want to pay, this is the free setup I'd use:
→ Writing, planning and thinking: the ChatGPT or Claude free plans
→ Research with sources: Perplexity's free plan
→ Quick help inside Gmail and Docs: Flash-Lite is still fine for that

The bigger lesson is about free tiers. They change without warning, and this one changed in about a week. If a free AI tool sits inside your daily work, keep a second option ready.

The mistake I'd avoid: paying for three AI subscriptions at once. Pick one paid tool for the work that matters and use free tiers for the rest.

Which AI tool do you use most for work right now, and is it free or paid?

Sources: Google Gemini Apps Help, via 9to5Google (3 Oct 2026); Tom's Guide (6 Oct 2026); findskill.ai."""

# ── 19:00 · business · Google Business Profile (search: "how to put my business on google maps", "google business profile verification")
gbp_hook = "Your customers search Google Maps. ==Can they find you?=="
gbp_ig = [
    [("q", "Roland, how do I get my business on Google Maps? 📍"),
     ("r", "With a free **Google Business Profile.**"),
     ("r", "It's what shows when people search ==\"near me\".==")],
    [("r", "**Step 1: find or add your business** 🔎"),
     ("r", "Search your business name on Google Maps."),
     ("r", "Listed? Tap ==\"Own this business?\"== Not listed? Tap \"Add your business to Google\".")],
    [("r", "**Step 2: the basics** ✍️"),
     ("r", "Name, category, address or service area, phone, website."),
     ("r", "Pick the ==most specific category.== \"Bakery\" beats \"Food\".")],
    [("r", "**Step 3: verify** ✅"),
     ("r", "Google picks the method: video, phone, email or postcard."),
     ("r", "Video = one continuous take, ==30 seconds+==: your street, your signage, inside, proof you run it.")],
    [("q", "How long does it take?"),
     ("r", "Phone or email: minutes. Video: up to **5 business days.**"),
     ("r", "Postcard: ==1–2 weeks.== Don't request a new one, it cancels the old code.")],
    [("r", "**Step 4: make people choose you** ⭐"),
     ("r", "Real photos, opening hours, a short description."),
     ("r", "Ask happy customers for reviews and ==reply to every one.==")],
    [("r", "**Never show** ID, bank or tax numbers in your video. 🔐"),
     ("r", "📌 Save this. 📤 Send it to a business owner who's not on Maps yet."),
     ("r", "Follow **@defi_ring_master** for free tools that grow your business.")],
]
gbp_cap = """Your customers search Google Maps. Can they find you? 📍

How to get your business on Google Maps for free: 4 steps, how verification works, and what never to show in your video. Swipe →

📌 Save it
📤 Send it to a business owner who's not on Maps yet

#smallbusiness #googlemaps #marketing #business"""
gbp_li = """When someone searches "near me", they're not looking at your Instagram. They're looking at Google Maps.

Getting your business there is free. Here's how.

1. Search your business name on Google Maps. If it's listed, tap "Own this business?". If not, tap "Add your business to Google"

2. Add the basics: name, the most specific category you can find ("Bakery" beats "Food"), address or service area, phone and website

3. Verify. Google picks the method for you: phone, email, video or postcard. For video, record one continuous take of at least 30 seconds showing your street and nearby landmarks, your signage, the inside, and proof you run it, like keys or your till

4. Make people choose you: real photos, opening hours, a short description, and reviews from happy customers, with a reply to every one

How long it takes: phone or email in minutes, video up to 5 business days, a postcard 1 to 2 weeks. Requesting a new postcard cancels the old code, so wait.

Never show ID, bank or tax numbers in the verification video.

The mistake I'd avoid: setting it up and forgetting it. Profiles with fresh photos and answered reviews win the "near me" search.

How do most of your new customers find you today?

Sources: Google Business Profile Help; Bluehost, "Verify your Google Business Profile" (2026)."""

# ── 21:00 · teaser for 22 Oct 08:00 (which apps used your mic/camera). Logged in studio/teasers.md.
TEASER = ("phone-glow.jpg",
          "Do you know your phone can show you ==which apps were listening?==",
          "Tomorrow · 8 AM",
          """Do you know your phone can show you which apps were listening? 🎙️

It's built into your iPhone and Android, and most people have never opened it. Tomorrow at 8 AM: where to find it, step by step.

🔔 Turn on notifications so you don't miss it
📤 Send this to the friend who thinks their phone is spying on them

#privacy #iphone #android #tech""")

STORIES = {
    "s0900": ("glass-pen-coins.jpg", "Who can still spend your crypto? ==The 2-minute check is on my page.==", "New post · tap my profile"),
    "s1100": ("glass-pen-coins.jpg", "Have you ever signed something in your wallet ==without reading it?==", "Reply 👇"),
    "s1400": ("glass-dome-brain.jpg", "Which AI do you use most: ==ChatGPT, Gemini or Claude?==", "Reply 👇"),
    "s1700": ("glass-pen-coins.jpg", "Checked your wallet approvals yet? ==It takes 2 minutes.==", "Tap my profile · today's post"),
    "s2100": None,
}

POSTS = {
    "0800": ("appr", "glass-pen-coins.jpg", appr_hook, "Crypto · safety", appr_ig, appr_cap, appr_li,
             "How to: check and revoke token approvals", "Phil Collins – Another Day in Paradise", "pdf"),
    "1300": ("gem", "glass-dome-brain.jpg", gem_hook, "AI · news you can use", gem_ig, gem_cap, gem_li,
             "Explained: free Gemini is now Flash-Lite only", "George Michael – Careless Whisper", "image"),
    "1900": ("gbp", "map-shop.jpg", gbp_hook, "Business · how to", gbp_ig, gbp_cap, gbp_li,
             "How to: get your business on Google Maps, free", "Whitney Houston – I Wanna Dance with Somebody", "pdf"),
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


# ── Instagram rules (Roland, 21 Oct 2026 review): 1 carousel + 1 Reel a day on Instagram, two lanes
#    (crypto safety & money, AI tools), teasers as stories only, alt text on every image. LinkedIn keeps all 3 posts.
IG_OFF = {"1300", "1900", "2100"}
ALT = {"0800": ["A glass fountain pen signs a dark contract and the ink turns into a stream of gold coins. Text: One click on approve can empty your wallet. Check yours.",
                "Chat: how can someone drain my wallet without my seed phrase? With your permission: an approve lets a contract move your tokens.",
                "Chat: how the scam works. A fake airdrop or mint site asks you to sign an approval, often unlimited.",
                "Chat: the numbers. Scam Sniffer counted 83.85 million dollars stolen by wallet drainers in 2025 from 106,106 victims.",
                "Chat: the 2-minute check. Paste your wallet address into revoke.cash or Etherscan's Token Approval Checker.",
                "Chat: revoke approvals you don't use. Each revoke costs a little gas.",
                "Chat: never sign from a link in a DM. Approve or permit means spend permission. Use a separate small wallet.",
                "Chat: do the check tonight. Save this and send it to a friend. Education, not financial advice."]}


def ig_rules():
    for slot in ("0800", "1300", "1900", "2100"):
        f = Q / f"{slot}.json"
        d = json.loads(f.read_text())
        if slot in IG_OFF:
            d["instagram"]["enabled"] = False
        if slot in ALT:
            d["instagram"]["alt"] = ALT[slot]
        f.write_text(json.dumps(d, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    ig_rules()
