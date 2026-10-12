"""Render brand slides to PNGs (1080x1350) and a LinkedIn PDF.

    from rd_terminal import *          # run with PYTHONPATH=studio and RD_PLATFORM=x_linkedin
    from export import export
    export(slides, caption, "queue/2026-10-13/media", "crypto2")
    -> crypto2-1.png ... crypto2-N.png and crypto2.pdf
"""
import asyncio
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

import rd_terminal

HIDE = ".ig-header,.ig-dots,.ig-caption,.x-topbar,.x-dots"


async def _shoot(html, total, out, name, frame):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 420, "height": 525}, device_scale_factor=1080 / 420)
        await page.set_content(html, wait_until="load")
        await page.wait_for_timeout(1200)
        await page.evaluate("""([hide, frame]) => {
          document.querySelectorAll(hide).forEach(e=>e.style.display='none');
          const f=document.querySelector(frame); if(f) f.style.cssText='width:420px;height:525px;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';
          document.body.style.cssText='padding:0;margin:0;display:block;overflow:hidden;';
        }""", [HIDE, frame])
        paths = []
        for i in range(total):
            await page.evaluate("(i)=>{const t=document.querySelector('.carousel-track');if(t){t.style.transition='none';t.style.transform='translateX('+(-i*420)+'px)';}}", i)
            await page.wait_for_timeout(200)
            pth = out / f"{name}-{i+1}.png"
            await page.screenshot(path=str(pth), clip={"x": 0, "y": 0, "width": 420, "height": 525})
            paths.append(pth)
        await b.close()
        return paths


def export(slides, caption, outdir, name, frame=".ig-frame"):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    html = rd_terminal.page("".join(slides), len(slides), caption)
    pngs = asyncio.run(_shoot(html, len(slides), out, name, frame))
    imgs = [Image.open(p).convert("RGB") for p in pngs]
    pdf = out / f"{name}.pdf"
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=150)
    return [str(p) for p in pngs], str(pdf)
