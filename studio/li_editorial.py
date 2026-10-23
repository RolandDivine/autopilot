"""LinkedIn editorial carousel (Roland, 23 Oct 2026: "don't use abstract... what works on LinkedIn is people gathering,
people talking, an actual human being"). Cover = full-bleed photo of real-looking people + headline; inside = clean
editorial lesson slides; last = photo + CTA. 1080x1350 pages, saved as a PDF document post.
"""
import asyncio
import base64
import re
from pathlib import Path

from playwright.async_api import async_playwright

from ig_options import face

CSS = face("Jakarta", "plus-jakarta-sans", (500, 600, 700, 800))
BASE = f"""{CSS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;font-family:Jakarta;position:relative}}
.ph{{position:absolute;inset:0;background-size:cover;background-position:center}}
.fade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05) 30%,rgba(0,0,0,.55) 55%,rgba(0,0,0,.92) 100%)}}
.tag{{display:inline-block;font:800 26px Jakarta;letter-spacing:3px;text-transform:uppercase;color:#111;background:#FFD84D;padding:10px 20px;border-radius:8px}}
.by{{display:flex;align-items:center;gap:18px;font:700 30px Jakarta}}
.by i{{width:62px;height:62px;border-radius:50%;background:#FFD84D;color:#111;display:flex;align-items:center;justify-content:center;font:800 24px Jakarta;font-style:normal}}
.by span{{display:block;font:500 22px Jakarta;opacity:.75}}
mark{{background:#FFD84D;color:#111;padding:0 10px;border-radius:6px;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
"""


def b64(p):
    p = Path(p)
    return f"data:image/{'png' if p.suffix == '.png' else 'jpeg'};base64," + base64.b64encode(p.read_bytes()).decode()


def md(t):
    t = re.sub(r"==(.+?)==", r"<mark>\1</mark>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t.replace("\n", "<br>")


def cover_html(img, tag, hook, sub):
    return f"""<html><head><style>{BASE}
.box{{position:absolute;left:72px;right:72px;bottom:96px;color:#fff}}
h1{{font:800 86px/1.06 Jakarta;letter-spacing:-2.5px;margin:28px 0 22px}}
p{{font:500 34px/1.4 Jakarta;opacity:.9;margin-bottom:40px}}
.sw{{position:absolute;right:72px;bottom:110px;font:700 26px Jakarta;color:#fff;opacity:.85}}
</style></head><body><div class="ph" style="background-image:url('{b64(img)}')"></div><div class="fade"></div>
<div class="box"><div class="tag">{tag}</div><h1>{md(hook)}</h1><p>{md(sub)}</p>
<div class="by"><i>RD</i><div>Roland Divine<span>Founder · builder · Lagos</span></div></div></div>
<div class="sw">swipe →</div></body></html>"""


def lesson_html(num, title, lines, page, total, kicker):
    body = "".join(f"<li>{md(x)}</li>" for x in lines)
    return f"""<html><head><style>{BASE}
body{{background:#F6F2EA;color:#141414}}
.top{{position:absolute;left:80px;right:80px;top:70px;display:flex;justify-content:space-between;font:700 24px Jakarta;letter-spacing:2px;text-transform:uppercase;color:#7a7368}}
.n{{position:absolute;left:72px;top:150px;font:800 230px/1 Jakarta;color:#FFD84D;letter-spacing:-8px;-webkit-text-stroke:3px #141414}}
.c{{position:absolute;left:80px;right:80px;top:430px}}
h2{{font:800 70px/1.08 Jakarta;letter-spacing:-2px;margin-bottom:44px}}
ul{{list-style:none}} li{{font:500 40px/1.4 Jakarta;margin-bottom:30px;padding-left:44px;position:relative}}
li:before{{content:"";position:absolute;left:0;top:20px;width:20px;height:20px;border-radius:50%;background:#141414}}
mark{{padding:0 8px}}
.foot{{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;align-items:center}}
.foot .by{{font-size:26px}} .foot .by i{{width:52px;height:52px;font-size:20px}} .pg{{font:700 26px Jakarta;color:#7a7368}}
</style></head><body><div class="top"><span>{kicker}</span><span>Zero to One, decoded</span></div>
<div class="n">{num}</div><div class="c"><h2>{md(title)}</h2><ul>{body}</ul></div>
<div class="foot"><div class="by"><i>RD</i><div>Roland Divine</div></div><div class="pg">{page}/{total} →</div></div></body></html>"""


def end_html(img, line, nxt):
    return f"""<html><head><style>{BASE}
.box{{position:absolute;left:72px;right:72px;bottom:100px;color:#fff}}
h1{{font:800 72px/1.1 Jakarta;letter-spacing:-2px;margin:26px 0 30px}}
.cta{{font:600 36px/1.6 Jakarta;margin-bottom:40px}}
</style></head><body><div class="ph" style="background-image:url('{b64(img)}')"></div><div class="fade" style="background:linear-gradient(180deg,rgba(0,0,0,.25),rgba(0,0,0,.9) 70%)"></div>
<div class="box"><div class="tag">{nxt}</div><h1>{md(line)}</h1>
<div class="cta">📌 Save this for later<br>♻️ Repost it for a founder who needs it<br>➕ Follow for business, AI and crypto, explained straight</div>
<div class="by"><i>RD</i><div>Roland Divine<span>Founder · builder · Lagos</span></div></div></div></body></html>"""


async def _shoot(pages):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for html, out in pages:
            await pg.set_content(html)
            await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(out), type="jpeg", quality=90)
        await b.close()


def build(outdir, name, img, tag, hook, sub, lessons, end_line, nxt, kicker):
    """lessons: [(num, title, [lines])]. Returns the list of page paths (cover, lessons..., end) and writes <name>.pdf."""
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    total = len(lessons) + 2
    pages = [(cover_html(img, tag, hook, sub), out / f"{name}-li0.jpg")]
    for i, (num, title, lines) in enumerate(lessons):
        pages.append((lesson_html(num, title, lines, i + 2, total, kicker), out / f"{name}-li{i + 1}.jpg"))
    pages.append((end_html(img, end_line, nxt), out / f"{name}-li{total - 1}.jpg"))
    asyncio.run(_shoot(pages))
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for _, p in pages]
    ims[0].save(out / f"{name}.pdf", save_all=True, append_images=ims[1:], resolution=150)
    return [p for _, p in pages]
