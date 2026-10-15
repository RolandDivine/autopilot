"""Instagram house style (chosen 12 Oct 2026, permanent): Chat Bubbles.

A lesson is a chat between a curious friend ("q") and Roland ("r").

    from ig_chat import carousel, story
    slides = [
        [("q", "Roland, how does ChatGPT actually work? 🤔"), ("r", "Easier than you think. **3 simple steps.**")],
        [("r", "**Step 1: it read a huge library.**"), ("r", "Books, websites... it learned ==patterns==.")],
        ...
    ]
    carousel(slides, "AI lesson 2", "queue/2026-10-13/instagram", "ai2")   # -> ai2-1.jpg ... (1080x1350)
    story([("q", "..."), ("r", "...")], "AI lesson 2", "queue/2026-10-13/stories", "s1")  # -> s1.jpg (1080x1920)

A screenshot bubble: ("img", ("path.jpg", height_px)).
Markup inside bubble text: **bold**, ==yellow highlight==. Keep 2–4 bubbles per slide,
each under ~160 characters, so text stays big. The last slide should ask people to save
and send the post, and to follow @defi_ring_master.
"""
import asyncio
import html
import re
from pathlib import Path

from playwright.async_api import async_playwright

from ig_options import FONT_CSS

NAME = "Roland Divine"
HANDLE = "@defi_ring_master"


def fmt(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"==(.+?)==", r"<span class='hl'>\1</span>", t)
    return t.replace("\n", "<br>")


def _css(h, pad_top, pad_bottom, fs):
    return (f"*{{box-sizing:border-box;margin:0;padding:0}}html,body{{width:1080px;height:{h}px;overflow:hidden}}"
            f"body{{background:#EFE7DE;font-family:Jakarta;color:#111;padding:{pad_top}px 70px {pad_bottom}px;position:relative}}"
            ".top{display:flex;align-items:center;gap:22px;background:#fff;border-radius:30px;padding:26px 32px;margin-bottom:52px}"
            ".av{width:84px;height:84px;border-radius:50%;background:#FFD84D;display:flex;align-items:center;justify-content:center;font:800 36px Jakarta}"
            f".b{{max-width:82%;padding:30px 36px;border-radius:34px;font-size:{fs}px;line-height:1.38;margin-bottom:26px}}"
            ".q{background:#fff;border-top-left-radius:8px}.r{background:#D9FDD3;margin-left:auto;border-top-right-radius:8px}"
            ".hl{background:#FFD84D;padding:0 8px;border-radius:6px;font-weight:800}"
            f".foot{{position:absolute;left:70px;right:70px;bottom:{60 if h == 1350 else 230}px;display:flex;justify-content:space-between;font-size:28px;color:#6b6257}}")


def _img(spec):
    """("img", (path, height_px)) -> a rounded screenshot card, centred, base64-inlined."""
    import base64
    path, h = spec
    data = base64.b64encode(Path(path).read_bytes()).decode()
    return (f"<div style='text-align:center;margin:4px 0 30px'><img src='data:image/jpeg;base64,{data}' "
            f"style='height:{h}px;max-width:100%;border-radius:28px;box-shadow:0 10px 30px rgba(0,0,0,.18);"
            f"border:6px solid #fff'></div>")


def _page(bubbles, label, foot_right, h=1350):
    fs = 42 if h == 1350 else 48
    top = (f"<div class='top'><div class='av'>RD</div><div><b style='font-size:36px'>{NAME}</b>"
           f"<div style='font-size:28px;color:#6b7280'>{html.escape(label)} · online</div></div></div>")
    body = "".join(_img(text) if who == "img" else f"<div class='b {who}'>{fmt(text)}</div>"
                   for who, text in bubbles)
    foot = f"<div class='foot'><span>{HANDLE}</span><span>{foot_right}</span></div>"
    pad = (90, 140) if h == 1350 else (250, 330)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{_css(h, pad[0], pad[1], fs)}</style></head>"
            f"<body>{top}{body}{foot}</body></html>")


async def _shoot(pages, out, h):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": h})
        for html_, path in pages:
            await pg.set_content(html_, wait_until="load")
            await pg.wait_for_timeout(150)
            over = await pg.evaluate("document.body.scrollHeight > window.innerHeight + 2")
            if over:
                raise ValueError(f"{path.name}: too much text for one slide; split it")
            await pg.screenshot(path=str(path), type="jpeg", quality=92)
        await b.close()


def carousel(slides, label, outdir, name, offset=0):
    """offset: number of slides before these (e.g. 1 for a cover), so the page counter stays right."""
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    n = len(slides) + offset
    pages = [(_page(s, label, f"{i+1+offset}/{n}" + (" →" if i + offset < n - 1 else "")), out / f"{name}-{i+1}.jpg")
             for i, s in enumerate(slides)]
    asyncio.run(_shoot(pages, out, 1350))
    return [str(p) for _, p in pages]


def story(bubbles, label, outdir, name):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.jpg"
    asyncio.run(_shoot([(_page(bubbles, label, "", 1920), path)], out, 1920))
    return str(path)
