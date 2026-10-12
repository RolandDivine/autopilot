"""Render 7 Instagram style options (cover, teaching slide, closing slide) for Roland to pick from."""
import asyncio
import base64
from pathlib import Path

from playwright.async_api import async_playwright

FONTS = Path("/home/claude/fonts/node_modules/@fontsource")
OUT = Path("/tmp/claude-test/igopts")
HANDLE = "@defi_ring_master"
NAME = "Roland Divine"


def face(family, pkg, weights=(400, 700)):
    css = ""
    for w in weights:
        f = FONTS / pkg / "files" / f"{pkg}-latin-{w}-normal.woff2"
        if f.exists():
            b = base64.b64encode(f.read_bytes()).decode()
            css += f"@font-face{{font-family:'{family}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
    return css


FONT_CSS = (face("DMSerif", "dm-serif-display", (400,)) + face("Caveat", "caveat", (500, 700)) +
            face("ArchivoBlack", "archivo-black", (400,)) + face("Jakarta", "plus-jakarta-sans", (400, 500, 700, 800)) +
            face("Instrument", "instrument-serif", (400,)) + face("SpaceG", "space-grotesk", (400, 500, 700)) +
            face("Bricolage", "bricolage-grotesque", (400, 600, 800)))

BASE = ("*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden}"
        ".s{position:relative;width:1080px;height:1350px;overflow:hidden}")


def page(css, body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{BASE}{css}</style></head><body>{body}</body></html>"


# Shared copy: AI lesson 2, written for complete beginners
C = dict(
    kicker="AI lesson 2",
    title="How AI chatbots actually work",
    sub="3 simple steps. No tech words.",
    step="Step 3",
    step_title="It guesses the next word",
    prompt="The capital of Nigeria is…",
    good="Abuja", bad="Lagos",
    explain="It writes your answer one word at a time, always picking the word that is most likely to come next.",
    save="Save this so you remember it",
    share="Send it to a friend who uses ChatGPT",
    follow="1 easy lesson a day on AI, crypto & building",
)

OPTIONS = {}


def option(key, label, why):
    def deco(fn):
        OPTIONS[key] = (label, why, fn)
        return fn
    return deco


@option("1", "Notebook", "Warm paper, a teacher's handwriting and your yellow highlighter. Feels like a friend's study notes.")
def notebook(i):
    css = (".s{background:#FBF7EE;font-family:Jakarta;color:#1A1A1A;padding:110px 96px}"
           ".s:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(#FBF7EE 0 58px,#EAE3D2 58px 60px);opacity:.55}"
           ".s>*{position:relative}.hand{font-family:Caveat;font-weight:700;color:#B98100}"
           ".hl{background:linear-gradient(transparent 55%,#FFD84D 55%);padding:0 6px}"
           "h1{font-family:DMSerif;font-weight:400;font-size:112px;line-height:1.02;margin:28px 0 40px}"
           "h2{font-family:DMSerif;font-weight:400;font-size:84px;line-height:1.05;margin:16px 0 50px}"
           "p{font-size:40px;line-height:1.45}.foot{position:absolute;left:96px;right:96px;bottom:70px;display:flex;justify-content:space-between;font-size:30px;color:#7A7468}")
    foot = f"<div class='foot'><span>{HANDLE}</span><span>{i+1}/3</span></div>"
    if i == 0:
        b = (f"<div class='hand' style='font-size:56px'>{C['kicker']} ✎</div><h1>How <span class='hl'>AI chatbots</span> actually work</h1>"
             f"<p>{C['sub']}</p><div class='hand' style='font-size:64px;margin-top:150px'>swipe →</div>")
    elif i == 1:
        b = (f"<div class='hand' style='font-size:56px'>{C['step']}</div><h2>{C['step_title']}</h2>"
             f"<p style='font-size:46px;margin-bottom:34px'>\"{C['prompt']}\"</p>"
             f"<p style='font-size:52px'>✓ <b class='hl'>{C['good']}</b> <span class='hand' style='font-size:44px'>← most likely</span></p>"
             f"<p style='font-size:52px;color:#9A9384;margin:18px 0 60px'>✗ <s>{C['bad']}</s></p><p>{C['explain']}</p>")
    else:
        b = (f"<div class='hand' style='font-size:60px'>before you go…</div><h2><span class='hl'>{C['save']}</span></h2>"
             f"<p style='margin-bottom:28px'>↗ {C['share']}</p><p style='margin-bottom:90px'>＋ Follow {HANDLE}<br>for {C['follow']}</p>"
             f"<div class='hand' style='font-size:54px'>— {NAME}</div>")
    return page(css, f"<div class='s'>{b}{foot}</div>")


@option("2", "Bold Yellow", "Your brand yellow as the whole background, with huge black words. Stops the scroll and is easy to spot in a feed.")
def yellow(i):
    css = (".s{background:#FFD84D;font-family:Jakarta;color:#111;padding:110px 92px}"
           "h1{font-family:ArchivoBlack;font-size:128px;line-height:.98;letter-spacing:-2px;margin:34px 0 46px;text-transform:uppercase}"
           "h2{font-family:ArchivoBlack;font-size:92px;line-height:1;margin:20px 0 56px;text-transform:uppercase}"
           ".pill{display:inline-block;background:#111;color:#FFD84D;font-weight:800;font-size:34px;padding:14px 30px;border-radius:999px}"
           "p{font-size:42px;line-height:1.4;font-weight:500}.card{background:#fff;border-radius:36px;padding:44px 48px;margin:0 0 48px;box-shadow:0 10px 0 #111}"
           ".foot{position:absolute;left:92px;right:92px;bottom:70px;display:flex;justify-content:space-between;font-size:30px;font-weight:700}")
    foot = f"<div class='foot'><span>{HANDLE}</span><span>{i+1}/3</span></div>"
    if i == 0:
        b = (f"<span class='pill'>{C['kicker'].upper()}</span><h1>How AI chatbots actually work</h1>"
             f"<p style='font-size:48px'>{C['sub']}</p><div style='font-family:ArchivoBlack;font-size:60px;margin-top:150px'>SWIPE →</div>")
    elif i == 1:
        b = (f"<span class='pill'>{C['step'].upper()}</span><h2>{C['step_title']}</h2>"
             f"<div class='card'><p style='font-size:44px;margin-bottom:26px'>\"{C['prompt']}\"</p>"
             f"<p style='font-size:54px;font-weight:800'>✓ {C['good']}</p><p style='font-size:44px;color:#999'>✗ {C['bad']}</p></div>"
             f"<p>{C['explain']}</p>")
    else:
        b = (f"<span class='pill'>BEFORE YOU GO</span><h2>Save this so you remember it</h2>"
             f"<div class='card'><p>↗ {C['share']}</p></div><p style='font-size:44px'>Follow <b>{HANDLE}</b><br>{C['follow']}</p>")
    return page(css, f"<div class='s'>{b}{foot}</div>")


@option("3", "Clean Editorial", "Magazine-style: big elegant serif headline, lots of white space. Looks premium and trustworthy.")
def editorial(i):
    css = (".s{background:#FFFFFF;font-family:Jakarta;color:#141414;padding:120px 100px}"
           ".k{font-size:28px;letter-spacing:6px;text-transform:uppercase;color:#B98100;font-weight:700}"
           "h1{font-family:Instrument;font-weight:400;font-size:136px;line-height:.98;margin:40px 0 50px}"
           "h2{font-family:Instrument;font-weight:400;font-size:100px;line-height:1;margin:26px 0 60px}"
           "em{font-style:italic;background:linear-gradient(transparent 60%,#FFD84D 60%)}"
           "p{font-size:40px;line-height:1.5;color:#333}.rule{height:2px;background:#141414;margin:50px 0}"
           ".foot{position:absolute;left:100px;right:100px;bottom:70px;display:flex;justify-content:space-between;font-size:28px;color:#888;border-top:2px solid #eee;padding-top:26px}")
    foot = f"<div class='foot'><span>{NAME} · {HANDLE}</span><span>{i+1} / 3</span></div>"
    if i == 0:
        b = (f"<div class='k'>{C['kicker']}</div><h1>How AI chatbots <em>actually</em> work</h1>"
             f"<p>{C['sub']}</p><p style='margin-top:170px;font-size:36px;color:#888'>Swipe to learn →</p>")
    elif i == 1:
        b = (f"<div class='k'>{C['step']}</div><h2>It <em>guesses</em> the next word</h2>"
             f"<p style='font-size:46px;color:#141414'>\"{C['prompt']}\"</p><div class='rule'></div>"
             f"<p style='font-size:50px;color:#141414'><b>{C['good']}</b> — most likely &nbsp;·&nbsp; <span style='color:#bbb'>{C['bad']}</span></p>"
             f"<div class='rule'></div><p>{C['explain']}</p>")
    else:
        b = (f"<div class='k'>Before you go</div><h2>Save this so you <em>remember</em> it</h2>"
             f"<p style='margin-bottom:30px'>{C['share']}.</p><p>Follow {HANDLE} for {C['follow']}.</p>")
    return page(css, f"<div class='s'>{b}{foot}</div>")


@option("4", "Tweet Card", "Looks like a post from a person, with your photo, name and handle on top. Very familiar on Instagram and feels personal.")
def tweet(i):
    css = (".s{background:#F2F2F2;font-family:Jakarta;color:#0F1419;display:flex;align-items:center;justify-content:center;padding:70px}"
           ".c{background:#fff;border-radius:44px;padding:70px 70px 60px;width:100%;box-shadow:0 2px 0 #e5e5e5}"
           ".hd{display:flex;align-items:center;gap:26px;margin-bottom:46px}.av{width:120px;height:120px;border-radius:50%;background:#FFD84D;display:flex;align-items:center;justify-content:center;font:800 54px Jakarta}"
           ".nm{font-weight:800;font-size:40px}.hn{font-size:32px;color:#6b7280}"
           "p{font-size:50px;line-height:1.38;margin-bottom:30px}.hl{background:#FFD84D;padding:0 8px;border-radius:6px}"
           ".ft{display:flex;justify-content:space-between;color:#9ca3af;font-size:28px;margin-top:30px;border-top:2px solid #f0f0f0;padding-top:26px}")
    hd = f"<div class='hd'><div class='av'>RD</div><div><div class='nm'>{NAME}</div><div class='hn'>{HANDLE}</div></div></div>"
    ft = f"<div class='ft'><span>{C['kicker']}</span><span>{i+1}/3 {'→' if i < 2 else ''}</span></div>"
    if i == 0:
        b = (f"<p style='font-size:64px;font-weight:800;line-height:1.15'>How AI chatbots actually work.</p>"
             f"<p>3 simple steps. No tech words. I'll explain it like I'm explaining it to my little sister.</p><p style='color:#6b7280'>Swipe →</p>")
    elif i == 1:
        b = (f"<p style='font-weight:800'>Step 3: it guesses the next word.</p>"
             f"<p>You type: \"{C['prompt']}\"</p><p>It picks <span class='hl'>{C['good']}</span>, because that's the most likely next word. Not {C['bad']}.</p>"
             f"<p>That's all it does, one word at a time, until your answer is done.</p>")
    else:
        b = (f"<p style='font-weight:800'>Save this so you remember it.</p><p>Send it to a friend who uses ChatGPT every day but has no idea how it works.</p>"
             f"<p>I post {C['follow']}. Follow so you don't miss tomorrow's.</p>")
    return page(css, f"<div class='s'><div class='c'>{hd}{b}{ft}</div></div>")


@option("5", "Chat Bubbles", "The lesson as a WhatsApp-style chat: someone asks, you answer. Feels like texting a friend who knows things.")
def chat(i):
    css = (".s{background:#EFE7DE;font-family:Jakarta;color:#111;padding:90px 70px}"
           ".top{display:flex;align-items:center;gap:22px;background:#fff;border-radius:30px;padding:26px 32px;margin-bottom:56px}"
           ".av{width:84px;height:84px;border-radius:50%;background:#FFD84D;display:flex;align-items:center;justify-content:center;font:800 36px Jakarta}"
           ".b{max-width:80%;padding:30px 36px;border-radius:34px;font-size:42px;line-height:1.38;margin-bottom:28px}"
           ".me{background:#fff;border-top-left-radius:8px}.r{background:#D9FDD3;margin-left:auto;border-top-right-radius:8px}"
           ".hl{background:#FFD84D;padding:0 8px;border-radius:6px;font-weight:800}"
           ".foot{position:absolute;left:70px;right:70px;bottom:60px;display:flex;justify-content:space-between;font-size:28px;color:#6b6257}")
    top = f"<div class='top'><div class='av'>RD</div><div><b style='font-size:36px'>{NAME}</b><div style='font-size:28px;color:#6b7280'>{C['kicker']} · online</div></div></div>"
    foot = f"<div class='foot'><span>{HANDLE}</span><span>{i+1}/3</span></div>"
    if i == 0:
        b = ("<div class='b me'>Roland, how does ChatGPT actually work? 🤔</div>"
             "<div class='b r'>Easier than you think. <b>3 simple steps.</b> No tech words, I promise.</div>"
             "<div class='b me'>Ok, explain like I'm 10</div><div class='b r'>Swipe → 👇</div>")
    elif i == 1:
        b = ("<div class='b r'><b>Step 3: it guesses the next word.</b></div>"
             f"<div class='b r'>If you type \"{C['prompt']}\" it picks <span class='hl'>{C['good']}</span>. Not {C['bad']}. Because that's the most likely next word.</div>"
             "<div class='b me'>So it's just guessing?? 😮</div><div class='b r'>Very smart guessing, one word at a time. That's why it can sound sure and still be wrong.</div>")
    else:
        b = ("<div class='b me'>This was actually easy to understand</div>"
             "<div class='b r'><b>Save it</b> so you remember 📌</div>"
             f"<div class='b r'>And send it to a friend who uses ChatGPT every day 😄</div>"
             f"<div class='b r'>New lesson tomorrow. Follow <b>{HANDLE}</b></div>")
    return page(css, f"<div class='s'>{top}{b}{foot}</div>")


@option("6", "Step Cards", "Big numbers and one idea per card, like a recipe. Very easy to follow and great for saving.")
def steps(i):
    css = (".s{background:#FFFFFF;font-family:SpaceG;color:#121212;padding:110px 92px}"
           ".band{position:absolute;left:0;top:0;bottom:0;width:26px;background:#FFD84D}"
           ".k{font-size:32px;font-weight:700;color:#B98100;letter-spacing:2px;text-transform:uppercase}"
           "h1{font-family:Bricolage;font-weight:800;font-size:116px;line-height:1;margin:30px 0 50px;letter-spacing:-2px}"
           ".big{font-family:Bricolage;font-weight:800;font-size:300px;line-height:.8;color:#FFD84D;-webkit-text-stroke:4px #121212}"
           "h2{font-family:Bricolage;font-weight:800;font-size:82px;line-height:1.02;margin:30px 0 50px}"
           "p{font-size:42px;line-height:1.42}.row{display:flex;gap:24px;align-items:center;font-size:44px;margin:16px 0}"
           ".n{width:84px;height:84px;border-radius:22px;background:#121212;color:#FFD84D;display:flex;align-items:center;justify-content:center;font-weight:700}"
           ".foot{position:absolute;left:92px;right:92px;bottom:70px;display:flex;justify-content:space-between;font-size:30px;color:#777}")
    foot = f"<div class='band'></div><div class='foot'><span>{HANDLE}</span><span>{i+1}/3 →</span></div>"
    if i == 0:
        b = (f"<div class='k'>{C['kicker']}</div><h1>How AI chatbots actually work</h1>"
             "<div class='row'><div class='n'>1</div>It read a huge library</div>"
             "<div class='row'><div class='n'>2</div>Your words become pieces</div>"
             "<div class='row'><div class='n'>3</div>It guesses the next word</div>"
             "<p style='margin-top:90px;color:#777'>Swipe for each step →</p>")
    elif i == 1:
        b = (f"<div class='big'>3</div><h2>{C['step_title']}</h2>"
             f"<p style='margin-bottom:28px'>\"{C['prompt']}\"</p><p style='font-size:54px;font-weight:700'>→ {C['good']} ✓</p>"
             f"<p style='margin-top:40px'>{C['explain']}</p>")
    else:
        b = (f"<div class='k'>Before you go</div><h2>Save this so you remember it</h2>"
             f"<div class='row'><div class='n'>↗</div>{C['share']}</div><div class='row'><div class='n'>＋</div>Follow {HANDLE}</div>"
             f"<p style='margin-top:40px;color:#555'>{C['follow']}.</p>")
    return page(css, f"<div class='s'>{b}{foot}</div>")


@option("7", "Soft Cards", "Calm cream background with rounded cards and small icons, like a friendly learning app. Easy on the eyes.")
def soft(i):
    css = (".s{background:linear-gradient(160deg,#FFF8E1 0%,#FFFDF7 60%);font-family:Jakarta;color:#1E1B16;padding:100px 84px}"
           ".tag{display:inline-flex;gap:14px;align-items:center;background:#fff;border:2px solid #F1E3B4;border-radius:999px;padding:14px 30px;font-size:32px;font-weight:700}"
           ".dot{width:22px;height:22px;border-radius:50%;background:#FFD84D;border:3px solid #1E1B16}"
           "h1{font-family:Bricolage;font-weight:800;font-size:110px;line-height:1.02;margin:44px 0 40px;letter-spacing:-1px}"
           "h2{font-family:Bricolage;font-weight:800;font-size:80px;line-height:1.05;margin:34px 0 44px}"
           "p{font-size:41px;line-height:1.45}.card{background:#fff;border-radius:40px;padding:44px;margin-bottom:30px;border:2px solid #F3EBD3}"
           ".ic{font-size:60px;margin-bottom:10px}.y{background:#FFD84D;border-radius:10px;padding:0 10px;font-weight:800}"
           ".foot{position:absolute;left:84px;right:84px;bottom:66px;display:flex;justify-content:space-between;font-size:30px;color:#8A8170}")
    foot = f"<div class='foot'><span>{HANDLE}</span><span>{'●' * (i + 1)}{'○' * (2 - i)}</span></div>"
    if i == 0:
        b = (f"<span class='tag'><span class='dot'></span>{C['kicker']}</span><h1>How AI chatbots actually work</h1>"
             f"<div class='card'><p>🧠 &nbsp;3 simple steps<br>🙅 &nbsp;No tech words<br>⏱ &nbsp;2-minute read</p></div><p style='color:#8A8170'>Swipe →</p>")
    elif i == 1:
        b = (f"<span class='tag'><span class='dot'></span>{C['step']}</span><h2>{C['step_title']}</h2>"
             f"<div class='card'><p style='color:#8A8170'>You type</p><p style='font-size:48px;font-weight:700'>\"{C['prompt']}\"</p></div>"
             f"<div class='card'><p style='color:#8A8170'>AI picks the most likely word</p><p style='font-size:54px'><span class='y'>{C['good']}</span> ✓</p></div>"
             f"<p>{C['explain']}</p>")
    else:
        b = (f"<span class='tag'><span class='dot'></span>Before you go</span><h2>Save this so you remember it 📌</h2>"
             f"<div class='card'><p>📤 &nbsp;{C['share']}</p></div><div class='card'><p>➕ &nbsp;Follow <b>{HANDLE}</b><br>{C['follow']}</p></div>")
    return page(css, f"<div class='s'>{b}{foot}</div>")


async def render():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for key, (label, why, fn) in OPTIONS.items():
            for i in range(3):
                await pg.set_content(fn(i), wait_until="load")
                await pg.wait_for_timeout(300)
                await pg.screenshot(path=str(OUT / f"opt{key}-{i+1}.png"))
        await b.close()


if __name__ == "__main__":
    asyncio.run(render())
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", 44)
    small = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf", 26)
    for key, (label, why, fn) in OPTIONS.items():
        W, H = 3 * 540 + 4 * 30, 675 + 190
        sheet = Image.new("RGB", (W, H), "#E9E9E9")
        d = ImageDraw.Draw(sheet)
        d.text((30, 30), f"Option {key} · {label}", font=font, fill="#111")
        d.text((30, 98), why, font=small, fill="#444")
        for i in range(3):
            im = Image.open(OUT / f"opt{key}-{i+1}.png").resize((540, 675))
            sheet.paste(im, (30 + i * 570, 160))
        sheet.save(OUT / f"option-{key}-{label.replace(' ', '-').lower()}.png")
    print("done")
