"""Day 9 · Tue 20 Oct 2026 (catch-up evening: no nightly build ran on 18/19 Oct). Run from studio/:  python days/day9.py
19:00 pays off the 18 Oct teaser ("Do you know you can start learning cybersecurity this week, free, with no experience?").
21:00 teases 21 Oct 08:00 (wallet approvals: one signature can empty your wallet).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "queue" / "2026-10-20"
GEN = ROOT / "assets" / "gen"

# ── 19:00 · teaser payoff · free cybersecurity path from zero
cyb_hook = "Learn cybersecurity from zero. ==Free. Starting tonight.=="
cyb_ig = [
    [("q", "Roland, can I really learn cybersecurity free, with no experience? 🔐"),
     ("r", "Yes. Here's the path I'd follow, in order."),
     ("r", "==4 free steps==, plus the catch. Real courses, real labs.")],
    [("r", "**Step 1: the basics** 🧱"),
     ("r", "**Cisco Networking Academy: Introduction to Cybersecurity.** Free, self-paced."),
     ("r", "Pass the final exam and you get a ==free Credly badge.==")],
    [("r", "**Step 2: how attacks work** 🛡️"),
     ("r", "**Fortinet NSE 1 and NSE 2:** free self-paced courses, ==each ends with an online exam.=="),
     ("r", "Add **IBM's Cybersecurity Fundamentals** for a second free badge.")],
    [("r", "**Step 3: get your hands dirty** 💻"),
     ("r", "**TryHackMe** free rooms: practice in a browser, no setup."),
     ("r", "**OverTheWire Bandit:** free puzzles that teach you the ==Linux command line.==")],
    [("r", "**Step 4: web security** 🌐"),
     ("r", "**PortSwigger Web Security Academy:** free lessons and labs on how websites get hacked."),
     ("r", "It's made by the company behind ==Burp Suite==, a tool pros use daily.")],
    [("q", "What about Google's certificate?"),
     ("r", "Free to **audit** on Coursera. The certificate costs ==$49 a month.=="),
     ("r", "And ISC2's free CC program closed to new sign-ups in May 2026.")],
    [("r", "**The catch:** free badges won't get you hired on their own. 🎯"),
     ("r", "Build a small home lab, write up what you solved, ==show your work.=="),
     ("r", "📌 Save this. 📤 Send it to the friend who wants to get into tech.")],
]
cyb_cap = """Learn cybersecurity from zero. Free. Starting tonight. 🔐

The 4-step free path I'd follow, and the catch nobody tells beginners. Swipe →

📌 Save it
📤 Send it to the friend who keeps saying they want to get into tech

#cybersecurity #tech #learning #careers"""
cyb_li = """You can start learning cybersecurity this week. Free. No experience needed.

Here's the path I'd follow from zero, in order.

1. Basics: Cisco Networking Academy's Introduction to Cybersecurity. Free and self-paced. Pass the final exam for a free Credly badge

2. How attacks work: Fortinet's NSE 1 and NSE 2 are free self-paced courses, each ending with an online exam. IBM's Cybersecurity Fundamentals adds a second free badge

3. Hands-on practice: TryHackMe's free rooms run in your browser, no setup. OverTheWire's Bandit teaches you the Linux command line through puzzles

4. Web security: PortSwigger's Web Security Academy has free lessons and labs on how websites actually get hacked

5. Google's Cybersecurity Certificate is free to audit on Coursera. The certificate itself costs $49 a month

6. Write up everything you solve. That's your portfolio

One update: ISC2's free Certified in Cybersecurity program closed to new enrolments in May 2026, so ignore older posts that still promise it.

The mistake I'd avoid: collecting badges and calling it experience. Free certificates won't get you hired on their own. A small home lab and clear write-ups of what you broke and fixed will.

Which part of security would you want to learn first: defending networks, or breaking into websites?

Sources: Cisco Networking Academy; Fortinet Training Institute; IBM SkillsBuild; PortSwigger; Coursera; ISC2 (April 2026); StationX (Aug 2026)."""

# ── 21:00 · teaser for 21 Oct 08:00 (wallet approvals / revoke). Logged in studio/teasers.md.
TEASER = ("glass-pen-coins.jpg",
          "Do you know one signature can ==empty your crypto wallet?==",
          "Tomorrow · 8 AM",
          """Do you know one signature can empty your crypto wallet? ✍️

No password. No seed phrase. Just one click on "approve". Tomorrow at 8 AM: how it happens, and the 2-minute check that protects you.

🔔 Turn on notifications so you don't miss it
📤 Send this to the friend who connects their wallet to everything

#crypto #web3 #cryptosecurity #defi""")

STORIES = {
    "s1930": ("circuit-lock.jpg", "Free cybersecurity path from zero: ==it's on my page.==", "New post · tap my profile"),
    "s2100": None,
}

POSTS = {
    "1900": ("cyb", "circuit-lock.jpg", cyb_hook, "Tech · how to", cyb_ig, cyb_cap, cyb_li,
             "How to: learn cybersecurity free, from zero", "Luther Vandross – Never Too Much", "pdf"),
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
