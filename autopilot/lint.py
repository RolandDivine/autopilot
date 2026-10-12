"""Mechanical checks before anything is posted (adapted from Jarvis's lint.mjs).

A FAIL blocks that platform's post and is reported in the day's review issue.
"""
import re

from . import load_config

EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")
URL = re.compile(r"https?://\S+")


def x_length(text):
    """X counts every URL as 23 characters."""
    return len(URL.sub("x" * 23, text))


def _banned_hits(text, cfg):
    lower = text.lower()
    hits = []
    for b in cfg["banned"]:
        if b in lower:
            if b in cfg.get("banned_ok_if_explaining", []) and re.search(r"(mislead|scam|red flag|never trust|promise)", lower):
                continue
            hits.append(b)
    return hits


def lint_slot(data, slot=None):
    """Return list of (level, platform, rule, detail)."""
    cfg = load_config()
    issues = []
    x = data.get("x", {})
    if x.get("enabled"):
        posts = x.get("posts") or []
        if not posts:
            issues.append(("FAIL", "x", "empty", "no posts"))
        for i, p in enumerate(posts, 1):
            t = p.get("text", "")
            n = x_length(t)
            if n > cfg["x_max_chars"]:
                issues.append(("FAIL", "x", "too-long", f"tweet {i}: {n} chars (max {cfg['x_max_chars']})"))
            if not t.strip():
                issues.append(("FAIL", "x", "empty", f"tweet {i} is empty"))
            if EMOJI.search(t):
                issues.append(("FAIL", "x", "emoji", f"tweet {i}"))
            for h in _banned_hits(t, cfg):
                issues.append(("FAIL", "x", "banned", f"tweet {i}: '{h}'"))
            if i == 1 and URL.search(t):
                issues.append(("WARN", "x", "link-in-first-tweet", "links cut reach and cost extra"))
            for m in p.get("media", []) or []:
                if slot and not slot.media_path(m).exists():
                    issues.append(("FAIL", "x", "missing-media", m))
            if "@defi_ring_master" in t:
                issues.append(("FAIL", "x", "wrong-handle", "X uses @RolandDivine2"))
    li = data.get("linkedin", {})
    if li.get("enabled"):
        t = li.get("text", "")
        if not t.strip():
            issues.append(("FAIL", "linkedin", "empty", "no text"))
        if len(t) > cfg["linkedin_max_chars"]:
            issues.append(("FAIL", "linkedin", "too-long", f"{len(t)} chars"))
        if EMOJI.search(t):
            issues.append(("FAIL", "linkedin", "emoji", ""))
        for h in _banned_hits(t, cfg):
            issues.append(("FAIL", "linkedin", "banned", f"'{h}'"))
        if URL.search(t):
            issues.append(("WARN", "linkedin", "link-in-post", "put links in first_comment"))
        if "@defi_ring_master" in t:
            issues.append(("FAIL", "linkedin", "wrong-handle", "LinkedIn uses @RolandDivine2"))
        m = li.get("media")
        if m and slot and not slot.media_path(m).exists():
            issues.append(("FAIL", "linkedin", "missing-media", m))
    ig = data.get("instagram", {})
    if ig.get("enabled"):
        cap = ig.get("caption", "")
        media = ig.get("media") or []
        if not cap.strip():
            issues.append(("FAIL", "instagram", "empty", "no caption"))
        if len(cap) > cfg.get("instagram_max_chars", 2200):
            issues.append(("FAIL", "instagram", "too-long", f"{len(cap)} chars"))
        tags = re.findall(r"(?<!\w)#\w+", cap)
        if len(tags) > cfg.get("instagram_max_hashtags", 5):
            issues.append(("FAIL", "instagram", "too-many-hashtags", f"{len(tags)}"))
        for h in _banned_hits(cap, cfg):
            issues.append(("FAIL", "instagram", "banned", f"'{h}'"))
        if "@RolandDivine2" in cap:
            issues.append(("FAIL", "instagram", "wrong-handle", "Instagram uses @defi_ring_master"))
        if not 1 <= len(media) <= 10:
            issues.append(("FAIL", "instagram", "media-count", f"{len(media)} images (1-10)"))
        for m in media:
            if not m.lower().endswith((".jpg", ".jpeg")):
                issues.append(("FAIL", "instagram", "not-jpeg", m))
            elif slot and not slot.media_path(m).exists():
                issues.append(("FAIL", "instagram", "missing-media", m))
    return issues


def blocked_platforms(issues):
    return {p for lvl, p, *_ in issues if lvl == "FAIL"}
