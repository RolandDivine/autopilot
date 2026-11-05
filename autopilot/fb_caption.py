"""Turn an Instagram caption into a Facebook one (Roland, 5 Nov 2026).

- carousels show as photo albums on Facebook: "Swipe" -> "Tap through the photos"
- "Save it" lines go; Facebook rewards comments, so every post ends with a question
- "Follow @defi_ring_master" -> "Follow the Page"; "on my profile" -> "on this Page"
- "Tomorrow at 8 AM" teasers -> "Next post" (a Facebook copy may land later than the Instagram one)
- 2-3 hashtags at most
"""
import re

ASK = "💬 Questions? Ask in the comments and I'll answer."


def fb_caption(caption, media_type):
    out, tags = [], []
    for line in (caption or "").splitlines():
        s = line.strip()
        if re.fullmatch(r"(#\S+\s*)+", s):
            tags += s.split()
            continue
        if s.startswith("📌"):
            s = re.sub(r"📌\s*Save (it|this)[^·]*", "", s).strip(" ·")
            if not s:
                continue
        s = s.replace("🔔 Follow @defi_ring_master", "🔔 Follow the Page").replace("@defi_ring_master", "this Page")
        if media_type == "CAROUSEL_ALBUM":
            s = re.sub(r"\bSwipe →", "Tap through the photos 👇", s)
            s = re.sub(r"\bSwipe\b", "Tap through the photos", s)
            s = re.sub(r"\bslide (\d+)", r"photo \1", s)
        s = s.replace("Explained like a chat. Tap through the photos 👇", "Explained like a chat 👇")
        s = re.sub(r" (for (Part \d+|the next part|the final part)) tomorrow", r" \1", s)
        s = s.replace("all parts are on my profile", "all parts are on this Page")
        s = s.replace("Tomorrow at 8 AM I'm showing you", "In the next post I'm showing you").replace("Tomorrow at 8 AM:", "Next post:")
        s = s.replace("🔔 Turn on notifications so you don't miss it", "🔔 Follow the Page so you don't miss it")
        out.append(s)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    if "💬" not in text:
        if "Education, not financial advice." in text:
            text = text.replace("Education, not financial advice.", ASK + "\n\nEducation, not financial advice.")
        else:
            text = (text + "\n\n" + ASK).strip()
    tags = [t for t in tags if t.lower() != "#lagos"][:3]
    if tags:
        text += "\n\n" + " ".join(tags)
    return text


def first_line(caption):
    return next((l.strip() for l in (caption or "").splitlines() if l.strip() and not l.strip().startswith("#")), "")
