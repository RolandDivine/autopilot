"""Tue 3 Nov 2026 (nightly build, 31 Oct). Run from repo root:  python3 studio/days/week45b.py

Plan:
  Tue 3   08:00 Instagram chat-first carousel + LinkedIn PDF (Tuesday PDF day, same slides): the fake Claude Code
          extension in Cursor's marketplace (29 Oct 2026) and the one-line check. Week 45's first Instagram carousel.
          12:00 Reel ex17 quishing (already in queue/vo/posts-2026-11-03.json).
Stories 09/11/14/17/21, abstract images only (reused: glass-keys, qr-sticker, circuit-lock; no Figma credits spent).
Search demand: Hacker News #1-tier story 30 Oct ("Backdoor in Claude Code for VS Code extension on the Cursor
Marketplace", 685 points / 435 comments); "how ai agents"/"is it safe to use ai agents" autocomplete in research/2026-10-30.json.
Facts: Cursor security notice, 29 Oct 2026 (updated 30 Oct): https://cursor.com/blog/claude-code-extension-security-notice
No install count is used (Cursor's notice gives none). No invented anecdotes.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "assets" / "gen"
SRC = "https://cursor.com/blog/claude-code-extension-security-notice"

BODY = [
    [("q", "Roland, I code with AI in Cursor. Someone said an extension there ==had a backdoor?== 😳"),
     ("r", "True. On 29 Oct, fake versions of the \"Claude Code\" extension sat in Cursor's marketplace for about 11 hours."),
     ("r", "Versions 2.1.312 and 2.1.313. ==Not made by Anthropic.==")],
    [("r", "**What it did** 🚪"),
     ("r", "Sent the attacker your username, computer name, Git email and IP address."),
     ("r", "Then tried to add a hidden SSH key: ==a secret door into your computer.==")],
    [("q", "I'll just uninstall it then 👍🏾"),
     ("r", "Not enough. It dropped its own scripts that keep retrying the connection every 60 seconds."),
     ("r", "Cursor says ==uninstalling may not remove it.==")],
    [("r", "**How to check in 1 minute** ✅"),
     ("r", "Look in your SSH authorized_keys file for a key named ==svc-telemetry==."),
     ("r", "Cursor's notice has a one-line check for Mac and Windows. No key = not affected.")],
    [("r", "**Found it?** 🚨"),
     ("r", "Run Cursor's clean-up script from the notice. If unsure, rebuild the machine."),
     ("r", "From a clean device, ==change your passwords, tokens and API keys.==")],
    [("r", "**The lesson for every AI tool** 🧠"),
     ("r", "A famous name in a marketplace is not proof it's real."),
     ("r", "Every extension can run code on your machine. ==Install fewer. Check the publisher.==")],
]
IG_END = [
    [("r", "Your turn 👇"),
     ("r", "Do you check an extension's publisher ==before you install it?=="),
     ("r", "Be honest. Yes, no, or \"I do now\" 💬")],
    [("r", "📌 Save this · 📤 Send it to a friend who codes with AI"),
     ("r", "Follow **@defi_ring_master** and turn on 🔔 to join a community learning AI and money safety together."),
     ("r", "Source: Cursor security notice, 29 Oct 2026.")],
]
LI_END = [
    [("r", "📌 Save this · 🔁 Repost it for a developer friend"),
     ("r", "Follow **Roland Divine** for AI and crypto safety you can act on."),
     ("r", "Source: Cursor security notice, 29 Oct 2026.")],
]

IG_CAP = """Is Cursor's Claude Code extension safe? Check your computer for this one key 🔑

A fake version sat in Cursor's marketplace for about 11 hours and tried to open a secret door into your machine. The 1-minute check and what to do if you find it. Swipe →

💬 Comment: do you check the publisher before you install?
📌 Save it · 📤 Send it to a friend who codes with AI
🔔 Follow @defi_ring_master

#cybersecurity #aitools #cursor #coding #developers"""

LI_TEXT = """If you code with AI in Cursor, check your computer for one key today.

On 29 October, fake versions of the "Claude Code" extension sat in Cursor's marketplace for about 11 hours. Not made by Anthropic. Versions 2.1.312 and 2.1.313.

What they did:

→ Sent the attacker your username, computer name, Git email and IP address.
→ Tried to add a hidden SSH key, a back door into your machine.
→ Installed scripts that retry that connection every 60 seconds. Cursor says uninstalling the extension may not remove them.

The 1-minute check: look in your SSH authorized_keys file for a key named svc-telemetry. Cursor's notice has a one-line command for Mac and Windows. Found it? Run Cursor's clean-up script, then rotate your passwords, tokens and API keys from a clean device.

To Cursor's credit, they pulled it the same day, rebuilt the marketplace and published the indicators.

Here's what I'd do as a builder: treat every extension like a new hire with the keys to your laptop. Fewer of them, a known publisher, and a reason for each one. A famous name in a marketplace is not proof it's real.

The guide is in the PDF. Save it for your team.

A question for developers:
How many extensions are installed in your editor right now, and could you name who publishes each one?"""

LI_SRC = f"Source: Cursor, \"Security notice: malicious version of Anthropic.claude-code (2.1.312 and 2.1.313)\", 29 Oct 2026 (updated 30 Oct): {SRC}"

CTA = ("circuit-lock.jpg", "Learning AI and money safety? ==Follow and turn on 🔔==", "Send this to a friend")
STORIES = {
    "s0900": ("glass-keys.jpg", "Code with AI? ==Check for this one key.==", "New post · tap my profile"),
    "s1100": ("glass-keys.jpg", "Do you check who made an extension ==before you install it?==", "Reply 👇"),
    "s1400": ("qr-sticker.png", "Don't scan that QR code ==until you check this.==", "New Reel · tap my profile"),
    "s1700": ("qr-sticker.png", "A QR code is just a link. ==Treat it like one.==", "Today's Reel · tap my profile"),
    "s2100": CTA,
}


def alt_of(slides):
    return ["Chat: " + " ".join(re.sub(r"[*=]", "", t).replace("\n", ", ") for _, t in s) for s in slides]


def build(day="2026-11-03"):
    Q = ROOT / "queue" / day
    ST, MEDIA, IG = Q / "stories", Q / "media", Q / "instagram"
    for x in (ST, MEDIA, IG):
        x.mkdir(parents=True, exist_ok=True)
    for old in list(IG.glob("ext-*.jpg")) + list(MEDIA.glob("ext-li-*.jpg")):
        old.unlink()
    ig_slides = BODY + IG_END
    ig = carousel(ig_slides, "AI · safety", IG, "ext", offset=0)
    li_slides = BODY + LI_END
    li = carousel(li_slides, "AI · safety", MEDIA, "ext-li", offset=0, handle="Roland Divine")
    ims = [Image.open(p).convert("RGB") for p in li]
    ims[0].save(MEDIA / "fake-extension.pdf", save_all=True, append_images=ims[1:], resolution=150)
    slot = {
        "title": "How to: check for the fake Claude Code extension (Cursor)",
        "kind": "lesson",
        "x": {"enabled": False},
        "instagram": {"enabled": True, "caption": IG_CAP, "media": [f"instagram/{Path(p).name}" for p in ig],
                      "music": "Anita Baker – Sweet Love", "alt": alt_of(ig_slides)},
        "linkedin": {"enabled": True, "text": LI_TEXT, "media": "media/fake-extension.pdf",
                     "media_title": "Fake Claude Code extension: the 1-minute check", "first_comment": LI_SRC},
    }
    (Q / "0800.json").write_text(json.dumps(slot, indent=1, ensure_ascii=False))
    st = []
    for at, (img, text, foot) in STORIES.items():
        cover(GEN / img, text, ST / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
        st.append({"at": at[1:], "media": f"stories/{at}.jpg"})
    (Q / "stories.json").write_text(json.dumps(st, indent=2))
    print("built", Q, len(LI_TEXT), "LI chars")


if __name__ == "__main__":
    build()
