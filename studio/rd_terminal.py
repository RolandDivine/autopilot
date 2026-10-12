"""Roland Divine Ogbaji — "Terminal" brand system for carousels.

Signature elements (every post, every time):
  1. Prompt bar on every slide: roland@defi:~$  (roland in amber), ring_master on the right.
  2. A "> command" line above each cover headline, and a blinking-style amber cursor "_" ending the cover headline.
  3. Claim tag on every content slide in brackets: [fact] [interpretation] [scenario] [thesis].
  4. Footer: the platform handle on the left (@defi_ring_master on Instagram, @RolandDivine2 on X/LinkedIn); block progress ■■□□□□ 2/6 on the right.
  5. Monospace everything. White background, black text, one yellow highlighter for the key number or phrase. No other colours.
  6. Same sign-off slide to close every carousel ($ whoami).
"""
BG = "#FFFFFF"; INK = "#0C0C0C"; AMBER = "#B98100"; MUTED = "#8E8E8E"; LINE = "#ECECEC"; DIM = "#2E2D2A"
HIGHLIGHT = "#FFD84D"
MONO = "'Liberation Mono','DejaVu Sans Mono',Menlo,Consolas,monospace"
NAME = "Roland Divine Ogbaji"
# Handle depends on where the asset will be posted:
#   instagram  -> @defi_ring_master
#   x_linkedin -> @RolandDivine2  (X and LinkedIn)
import os
HANDLES = {"instagram": ("defi_ring_master", "ring_master"), "x_linkedin": ("RolandDivine2", "RolandDivine2")}
PLATFORM = os.environ.get("RD_PLATFORM", "instagram")
HANDLE, TOPRIGHT = HANDLES[PLATFORM]


def use_platform(platform):
    """Call before building: 'instagram' or 'x_linkedin'."""
    global HANDLE, TOPRIGHT, PLATFORM
    PLATFORM = platform
    HANDLE, TOPRIGHT = HANDLES[platform]
DESCRIPTOR = "founder · defi builder · market analyst"
TAGS = ("fact", "interpretation", "scenario", "thesis")


def topbar():
    return (f'<div style="position:absolute;top:26px;left:30px;right:30px;display:flex;justify-content:space-between;'
            f'font:400 11px {MONO};color:{MUTED};z-index:5"><span><span style="color:{AMBER}">roland</span>@defi:~$</span>'
            f'<span>{TOPRIGHT}</span></div>')


def footer(i, total):
    blocks = "".join("■" if k <= i else "□" for k in range(total))
    return (f'<div style="position:absolute;bottom:24px;left:30px;right:30px;display:flex;justify-content:space-between;'
            f'font:400 11px {MONO};color:{MUTED};z-index:5"><span>@{HANDLE}</span>'
            f'<span><span style="color:{AMBER if i == total - 1 else INK};letter-spacing:1px">{blocks}</span>&nbsp; {i+1}/{total}'
            f'{"" if i == total - 1 else " →"}</span></div>')


def tag(label):
    assert label in TAGS
    return f'<div style="font:400 11px {MONO};color:{MUTED};margin-bottom:12px">[{label}]</div>'


def command(cmd):
    return f'<div style="font:400 12px {MONO};color:{AMBER};margin-bottom:16px">&gt; {cmd}</div>'


def cursor():
    return f'<span style="color:{AMBER}">_</span>'


def h1(text):
    return f'<h1 style="font:700 28px/1.2 {MONO};letter-spacing:-0.8px;color:{INK}">{text}{cursor()}</h1>'


def h2(text):
    return f'<h2 style="font:700 24px/1.22 {MONO};letter-spacing:-0.6px;color:{INK}">{text}</h2>'


def note(text, top=14):
    return f'<div style="font:400 12px/1.6 {MONO};color:{MUTED};margin-top:{top}px">{text}</div>'


def pre(text, top=22, size=12.5):
    return (f'<pre style="font:400 {size}px/1.75 {MONO};color:{INK};margin-top:{top}px;white-space:pre">{text}</pre>')


def amber(t):
    return f'<span style="background:{HIGHLIGHT};color:{INK};padding:0 3px">{t}</span>'


def dim(t):
    return f'<span style="color:{MUTED}">{t}</span>'


def slide(i, total, body):
    return (f'<div class="slide" style="background:{BG};">{topbar()}'
            f'<div style="position:absolute;inset:0;padding:64px 30px 58px;display:flex;flex-direction:column;'
            f'justify-content:center;z-index:2">{body}</div>{footer(i, total)}</div>')


def signoff(i, total, line="clear thinking on markets, crypto and building."):
    body = (command("whoami") +
            f'<div style="font:700 26px/1.2 {MONO};letter-spacing:-0.6px;color:{INK}">{NAME}{cursor()}</div>'
            f'<div style="font:400 12px {MONO};color:{MUTED};margin-top:10px">{DESCRIPTOR}</div>'
            f'<div style="font:400 13.5px/1.6 {MONO};color:{INK};margin-top:26px">{line}</div>'
            f'<div style="font:400 13.5px {MONO};color:{INK};margin-top:26px">$ follow {amber("@" + HANDLE)}</div>'
            f'<div style="font:400 11px {MONO};color:{MUTED};margin-top:28px"># education, not financial advice</div>')
    return slide(i, total, body)


def page(slides_html, total, caption, title="roland@defi"):
    css = ("*{box-sizing:border-box;margin:0;padding:0}"
           f"body{{background:#E9E8E4;font-family:{MONO};display:flex;justify-content:center;padding:24px 0}}"
           f"svg text{{font-family:{MONO}}}"
           ".ig-frame{width:420px;background:#fff;border-radius:12px;overflow:hidden}"
           ".ig-header{display:flex;align-items:center;gap:10px;padding:12px 14px;font:600 13px sans-serif}"
           ".carousel-viewport{width:420px;height:525px;overflow:hidden;position:relative}"
           ".carousel-track{display:flex;height:100%;transition:transform .35s ease}"
           ".slide{position:relative;flex:0 0 420px;width:420px;height:525px;overflow:hidden}"
           ".ig-dots{display:none}.ig-caption{padding:6px 14px 14px;font:13px sans-serif}")
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{css}</style></head><body>'
            f'<div class="ig-frame"><div class="ig-header">{HANDLE}</div>'
            f'<div class="carousel-viewport"><div class="carousel-track">{slides_html}</div></div>'
            f'<div class="ig-dots"></div><div class="ig-caption"><b>{HANDLE}</b> {caption}</div></div></body></html>')


def gold(t):
    """Dark-gold text for list numbers, so the highlighter stays on the one key point."""
    return f'<span style="color:{AMBER}">{t}</span>'
