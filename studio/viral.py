"""Viral explainer Reels (Roland, 16 Oct 2026): a trend topic told with on-screen evidence.

Each video = voiceover (ElevenLabs) + Whisper word timings + full-bleed generated photos with slow
camera moves + animated evidence cards (price tags, charts, stats, timelines, each naming its
source) + big word-by-word captions. 1080x1920, 30 fps. Rendered frame by frame in Chromium.

    python viral.py ram            -> ../assets/reels/viral-ram.mp4
    python viral.py ram 2 12 30    -> preview PNGs at those seconds
"""
import asyncio
import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.async_api import async_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ig_options import FONT_CSS  # noqa: E402
import duo  # noqa: E402  (Kobo drawing)
import numpy as np  # noqa: E402
import re  # noqa: E402
import soundfile as sf  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FPS = 30


def b64(p):
    return "data:image/jpeg;base64," + base64.b64encode(Path(p).read_bytes()).decode()


LAND_CSS = """
html,body{width:1920px;height:1080px}
.brand{top:44px;left:70px}
.prog{top:96px;left:70px;right:70px}
.cap{top:935px;left:200px;right:360px;font-size:58px}
.card{left:120px;right:420px;top:140px}
.panel{padding:40px 48px}
.big{font-size:130px}
#host{right:20px;bottom:-10px;width:300px;height:396px}
#host svg{width:300px;height:396px}
#hostname{right:96px;bottom:22px}
"""

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#07080B;font-family:Jakarta;color:#fff}
.bg{position:absolute;inset:-60px;background-size:cover;background-position:center;opacity:0;will-change:transform,opacity}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,.15) 30%,rgba(0,0,0,.25) 55%,rgba(0,0,0,.85) 100%)}
.brand{position:absolute;top:70px;left:60px;font:700 30px Jakarta;letter-spacing:1px;color:rgba(255,255,255,.85)}
.brand b{color:#FFD84D}
.prog{position:absolute;top:126px;left:60px;right:60px;height:6px;border-radius:6px;background:rgba(255,255,255,.18)}
.prog i{display:block;height:100%;width:0;background:#FFD84D;border-radius:6px}
.cap{position:absolute;left:60px;right:60px;top:1390px;text-align:center;font:800 78px/1.12 Jakarta;letter-spacing:-1px;
     text-shadow:0 6px 24px rgba(0,0,0,.7)}
.cap span{display:inline-block;margin:0 10px;opacity:.55;transition:none}
.cap span.on{opacity:1}
.cap span.now{color:#111;background:#FFD84D;border-radius:14px;padding:0 14px;margin:0 -4px;opacity:1}
.card{position:absolute;left:70px;right:70px;top:300px;opacity:0;will-change:transform,opacity}
.panel{background:rgba(10,12,16,.78);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.12);border-radius:40px;padding:44px 50px}
.src{display:inline-block;margin-top:26px;font:600 26px Jakarta;color:rgba(255,255,255,.7);background:rgba(255,255,255,.08);
     border-radius:999px;padding:8px 20px}
.kick{font:700 30px Jakarta;letter-spacing:3px;text-transform:uppercase;color:#FFD84D;margin-bottom:18px}
.big{font:800 150px/1 Jakarta;letter-spacing:-5px}
.mid{font:800 64px/1.1 Jakarta;letter-spacing:-1.5px}
.sm{font:600 36px/1.35 Jakarta;color:rgba(255,255,255,.85)}
.red{color:#FF4D4D}.yel{color:#FFD84D}.grn{color:#3DDC97}
.strike{position:relative;display:inline-block}
.strike:after{content:"";position:absolute;left:-6px;right:-6px;top:52%;height:12px;background:#FF4D4D;border-radius:6px;
              transform-origin:left;transform:scaleX(var(--s,0))}
.bars{display:flex;align-items:flex-end;gap:34px;height:520px;margin-top:20px}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.bar i{display:block;width:100%;border-radius:18px 18px 6px 6px;background:linear-gradient(180deg,#FF4D4D,#B3261E);height:0}
.bar b{font:800 50px Jakarta;margin-bottom:12px}.bar span{font:700 30px Jakarta;margin-top:14px;color:rgba(255,255,255,.8)}
.lane{display:flex;align-items:center;gap:24px;margin:22px 0}
.lane .t{width:300px;font:800 40px Jakarta}
.lane .track{flex:1;height:64px;border-radius:20px;background:rgba(255,255,255,.08);overflow:hidden}
.lane .track i{display:block;height:100%;width:0;border-radius:20px}
.tl{position:relative;margin:40px 0 10px;height:330px}
.tl .line{position:absolute;left:40px;right:40px;top:60px;height:8px;border-radius:8px;background:rgba(255,255,255,.2)}
.tl .line i{display:block;height:100%;width:0;background:#FFD84D;border-radius:8px}
.tl .pt{position:absolute;top:36px;width:300px;margin-left:-150px;text-align:center;opacity:0}
.tl .pt .dot{width:56px;height:56px;border-radius:50%;background:#FFD84D;margin:0 auto 20px;border:8px solid #07080B}
.tl .pt b{display:block;font:800 46px Jakarta}.tl .pt span{font:600 28px/1.3 Jakarta;color:rgba(255,255,255,.8)}
.check{display:flex;gap:26px;align-items:flex-start;margin:26px 0;opacity:0}
.check .box{flex:none;width:70px;height:70px;border-radius:18px;background:#3DDC97;color:#07080B;font:800 50px/70px Jakarta;text-align:center}
.check div{font:700 50px/1.2 Jakarta}
#host{position:absolute;right:-20px;bottom:-10px;width:330px;height:435px;opacity:0}
#host svg{width:330px;height:435px}
#hostname{position:absolute;right:70px;bottom:28px;font:800 28px Jakarta;color:#111;background:#FFD84D;border-radius:999px;padding:6px 18px;opacity:0}
.shot{display:block;width:100%;max-height:640px;object-fit:cover;object-position:top;border-radius:24px;margin-top:16px;border:1px solid rgba(255,255,255,.15)}
"""

JS = r"""
const D=__DATA__;
const $=s=>document.querySelector(s);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=x=>{x=cl(x);return 1-Math.pow(1-x,3)};
const back=x=>{x=cl(x);const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
function vis(el,t,a,b,fade=.35){const v=Math.min(ease((t-a)/fade),1-ease((t-(b-fade))/fade));el.style.opacity=cl(v);return cl(v)}
function host(t){
  const h=$('#host');if(!h)return;
  const show=D.host.some(([a,b])=>t>=a&&t<=b);
  const v=cl(show?1:0);h.style.opacity=v;$('#hostname').style.opacity=v;
  const f=Math.min(D.env.length-1,Math.floor(t*30));const lv=D.env[f]||0;
  const bob=Math.sin(t*6.3)*6;$('#kobo-whole').style.transform=`translateY(${bob-lv*8}px)`;$('#kobo-whole').style.transformOrigin='300px 740px';
  $('#kobo-head').style.transform=`rotate(${Math.sin(t*2.2)*3}deg)`;
  $('#kobo-earL').style.transform=`rotate(${-6+Math.sin(t*3.1)*6}deg)`;$('#kobo-earR').style.transform=`rotate(${6+Math.sin(t*3.1+1)*8}deg)`;
  const bt=t%3.4,sc=bt<.14?Math.max(.08,Math.abs(bt-.07)/.07):1;$('#kobo-eyeL').style.transform=$('#kobo-eyeR').style.transform=`scaleY(${sc})`;
  const open=Math.sqrt(Math.max(0,lv))*30;$('#kobo-mouth').setAttribute('ry',Math.max(.1,open));$('#kobo-mouth').style.opacity=open>1.5?1:0;
  $('#kobo-smile').style.opacity=open>1.5?0:1;
  const g=Math.sin(t*4)*10*lv;$('#kobo-armR').style.transform=`rotate(${-25-g*2}deg)`;$('#kobo-armL').style.transform=`rotate(${18+g}deg)`;
}
function render(t){
  host(t);
  $('#prog').style.width=(100*t/D.dur)+'%';
  // backgrounds: crossfade + slow push-in
  D.bgs.forEach((g,i)=>{const el=$('#bg'+i);const v=vis(el,t,g.a,g.b,.6);
    const p=cl((t-g.a)/(g.b-g.a));const z=1.04+.10*p;const dx=(i%2?-1:1)*30*p;
    el.style.transform=`translate(${dx}px,${-20*p}px) scale(${z})`;});
  // cards
  D.cards.forEach((c,i)=>{const el=$('#c'+i);const v=vis(el,t,c.a,c.b,.3);
    const k=back((t-c.a)/.45);el.style.transform=`translateY(${(1-k)*60}px) scale(${.94+.06*k})`;
    if(c.kind==='price'){const s=cl((t-c.a-c.strike)/.35);el.style.setProperty('--s',s);
      const n=$('#c'+i+' .new');const k2=back((t-c.a-c.strike-.25)/.4);n.style.opacity=cl(k2*2);
      n.style.transform=`scale(${.6+.4*k2}) rotate(${(1-cl(k2))*-6}deg)`;
      const sh=(t-c.a-c.strike-.25);n.style.translate=(sh>0&&sh<.35)?`${Math.sin(sh*80)*10}px 0`:'0 0';}
    if(c.kind==='count'){const p=ease((t-c.a-.2)/1.2);$('#c'+i+' .num').textContent=c.pre+Math.round(c.to*p)+c.post;}
    if(c.kind==='donut'){const p=ease((t-c.a-.2)/1.4);$('#c'+i+' circle.v').setAttribute('stroke-dasharray',`${p*c.pct*9.42} 942`);
      $('#c'+i+' .num').textContent=Math.round(c.pct*p)+'%';}
    if(c.kind==='bars'){c.bars.forEach((b,j)=>{const p=ease((t-c.a-.3-j*.35)/.7);
      $('#c'+i+' .bar'+j+' i').style.height=(p*b.v/c.max*100)+'%';$('#c'+i+' .bar'+j+' b').style.opacity=p;});}
    if(c.kind==='lanes'){c.lanes.forEach((l,j)=>{const p=ease((t-c.a-.3-j*.6)/.9);document.getElementById('c'+i+'l'+j).style.width=(p*l.v)+'%';});}
    if(c.kind==='timeline'){const p=ease((t-c.a-.2)/(c.b-c.a-1));$('#c'+i+' .line i').style.width=(p*100)+'%';
      c.pts.forEach((q,j)=>{$('#c'+i+' .p'+j).style.opacity=cl((p*100-q.x+6)/8);});}
    if(c.kind==='checks'){c.items.forEach((q,j)=>{const e=$('#c'+i+' .k'+j);const p=back((t-c.a-q.d)/.4);
      e.style.opacity=cl(p*2);e.style.transform=`translateX(${(1-cl(p))*-40}px)`;});}
  });
  // captions: chunk of words
  let ci=-1;for(let i=0;i<D.chunks.length;i++){if(D.chunks[i].s<=t+.05)ci=i;}
  const cap=$('#cap');
  if(ci<0||t>D.chunks[ci].e+.6){cap.innerHTML='';return}
  const ch=D.chunks[ci];
  if(cap.dataset.i!=ci){cap.dataset.i=ci;cap.innerHTML=ch.w.map((w,j)=>`<span id="cw${j}">${w[2]}</span>`).join('');}
  const pop=back((t-ch.s)/.18);cap.style.transform=`scale(${.92+.08*pop})`;
  ch.w.forEach((w,j)=>{const e=$('#cw'+j);e.className=t>=w[0]?(t<w[1]+.08?'now':'on'):'';});
}
"""


def chunks(words, n=3):
    out, cur = [], []
    for w in words:
        cur.append(w)
        end = w[2][-1:] in ".?!,"
        if len(cur) >= n or end or (len(cur) >= 2 and len(w[2]) > 9):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [{"s": c[0][0], "e": c[-1][1], "w": c} for c in out]


def card_html(i, c):
    k = c["kind"]
    src = f"<div class='src'>Source: {c['src']}</div>" if c.get("src") else ""
    kick = f"<div class='kick'>{c['kick']}</div>" if c.get("kick") else ""
    if k == "price":
        body = (f"{kick}<div class='sm'>{c['was_label']}</div><div class='big strike'>{c['was']}</div>"
                f"<div class='sm' style='margin-top:26px'>{c['now_label']}</div><div class='big red new'>{c['now']}</div>"
                f"<div class='mid yel' style='margin-top:18px'>{c['delta']}</div>")
    elif k == "count":
        body = f"{kick}<div class='big {c.get('cls','red')} num'>{c['pre']}0{c['post']}</div><div class='mid' style='margin-top:20px'>{c['label']}</div><div class='sm' style='margin-top:14px'>{c.get('sub','')}</div>"
    elif k == "stat":
        body = f"{kick}<div class='big {c.get('cls','red')}'>{c['value']}</div><div class='mid' style='margin-top:20px'>{c['label']}</div><div class='sm' style='margin-top:14px'>{c.get('sub','')}</div>"
    elif k == "donut":
        body = (f"{kick}<div style='display:flex;align-items:center;gap:40px'><svg width='340' height='340' viewBox='0 0 340 340'>"
                "<circle cx='170' cy='170' r='150' fill='none' stroke='rgba(255,255,255,.12)' stroke-width='44'/>"
                "<circle class='v' cx='170' cy='170' r='150' fill='none' stroke='#FFD84D' stroke-width='44' stroke-linecap='round' "
                "stroke-dasharray='0 942' transform='rotate(-90 170 170)'/></svg>"
                f"<div><div class='big yel num'>0%</div><div class='mid' style='font-size:48px'>{c['label']}</div></div></div>")
    elif k == "bars":
        bars = "".join(f"<div class='bar bar{j}'><b>{b['t']}</b><i></i><span>{b['q']}</span></div>" for j, b in enumerate(c["bars"]))
        body = f"{kick}<div class='mid'>{c['title']}</div><div class='bars'>{bars}</div>"
    elif k == "lanes":
        lanes = "".join(f"<div class='lane'><div class='t'>{l['t']}</div><div class='track'><i id='c{i}l{j}' style='background:{l['c']};width:0'></i></div></div>"
                        for j, l in enumerate(c["lanes"]))
        body = f"{kick}<div class='mid'>{c['title']}</div><div style='margin-top:20px'>{lanes}</div><div class='sm' style='margin-top:10px'>{c.get('sub','')}</div>"
    elif k == "timeline":
        pts = "".join(f"<div class='pt p{j}' style='left:{q['x']}%'><div class='dot'></div><b>{q['t']}</b><span>{q['s']}</span></div>"
                      for j, q in enumerate(c["pts"]))
        body = f"{kick}<div class='mid'>{c['title']}</div><div class='tl'><div class='line'><i></i></div>{pts}</div>"
    elif k == "checks":
        items = "".join(f"<div class='check k{j}'><div class='box'>✓</div><div>{q['t']}</div></div>" for j, q in enumerate(c["items"]))
        body = f"{kick}<div class='mid' style='margin-bottom:10px'>{c['title']}</div>{items}"
    elif k == "image":
        body = f"{kick}<div class='mid' style='font-size:52px'>{c['title']}</div><img class='shot' src='{b64(c['img'])}'>"
    else:
        body = c.get("html", "")
    return f"<div class='card' id='c{i}'><div class='panel'>{body}{src}</div></div>"


def build(spec):
    raw = [w for s in json.load(open(spec["transcript"])) for w in s["words"]]
    words = []
    for a, b, t in raw:  # merge pieces without a leading space ("70" + "%")
        if words and not t.startswith(" "):
            words[-1][1] = b
            words[-1][2] += t.strip()
        else:
            words.append([a, b, t.strip()])
    for w in words:
        for a, b in spec.get("fix", {}).items():
            w[2] = re.sub(rf"^{re.escape(a)}(?=\W*$)", b, w[2])
    dur = spec["dur"]

    def at(word, after=0.0, nth=1):
        n = 0
        for w in words:
            if w[0] >= after and w[2].lower().strip(".,?!'\"") == word.lower():
                n += 1
                if n == nth:
                    return w[0]
        raise KeyError(word)

    bgs, cards = spec["timeline"](at, dur)
    y, sr = sf.read(str(spec["wav"]), dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)
    hop = sr // 30
    env = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2)) for i in range(0, len(y), hop)])
    env = np.clip(env / (np.percentile(env, 95) + 1e-6), 0, 1)
    env[env < 0.12] = 0
    host = spec.get("host", [])
    data = {"dur": dur, "chunks": [] if spec.get("nocap") else chunks(words), "bgs": [{"a": a, "b": b} for a, b, _ in bgs], "cards": cards,
            "env": [round(float(v), 3) for v in env], "host": host}
    bg_html = "".join(f"<div class='bg' id='bg{i}' style=\"background-image:url('{b64(p)}')\"></div>" for i, (_, _, p) in enumerate(bgs))
    body = (bg_html + "<div class='shade'></div>" + "".join(card_html(i, c) for i, c in enumerate(cards)) +
            (f"<div id='host'>{duo.bunny_svg('kobo', duo.KOBO_COLORS)}</div><div id='hostname'>Kobo</div>" if host else "") +
            spec.get("brand", "<div class='brand'><b>@</b>defi_ring_master</div>") + "<div class='prog'><i id='prog'></i></div><div class='cap' id='cap'></div>")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{CSS}{LAND_CSS if spec.get('land') else ''}{spec.get('css', '')}</style></head><body>{body}"
            f"<script>{JS.replace('__DATA__', json.dumps(data))}</script></body></html>")


async def render(spec, out, preview=None):
    page = build(spec)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1080} if spec.get("land") else {"width": 1080, "height": 1920})
        await pg.set_content(page, wait_until="load")
        await pg.wait_for_timeout(400)
        if preview:
            shots = []
            for t in preview:
                await pg.evaluate(f"render({t})")
                f = f"/tmp/claude-test/viral_{t}.png"
                await pg.screenshot(path=f)
                shots.append(f)
            await b.close()
            return shots
        frames = Path("/tmp/viral_frames")
        shutil.rmtree(frames, ignore_errors=True)
        frames.mkdir()
        for i in range(int(spec["dur"] * FPS)):
            await pg.evaluate(f"render({i / FPS})")
            await pg.screenshot(path=str(frames / f"{i:05d}.jpg"), type="jpeg", quality=90)
        await b.close()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "%05d.jpg"),
                    "-i", str(spec["audio"]), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    return str(out)


def ram_spec():
    A = ROOT / "assets" / "viral" / "ram"

    def timeline(at, dur):
        t_phone = at("firing")
        t_why = at("why")
        t_dc = at("swallowing")
        t_idc = at("idc")
        t_sell = at("sell")
        t_expl = at("exploded")
        t_pocket = at("pocket")
        t_100 = at("under")
        t_mea = at("middle")
        t_wait = at("wait")
        t_buy = at("buy", t_wait)
        t_follow = at("follow")
        bgs = [(-1, t_phone - .2, A / "ram.jpg"), (t_phone - .4, t_dc - .2, A / "phone.jpg"),
               (t_dc - .4, t_pocket - .2, A / "datacenter.jpg"), (t_pocket - .4, t_mea - .2, A / "phone.jpg"),
               (t_mea - .4, t_wait - .2, A / "market.jpg"), (t_wait - .4, dur, A / "datacenter.jpg")]
        cards = [
            {"kind": "price", "a": -1, "b": t_phone - .1, "strike": 4.9, "kick": "32GB DDR5 memory kit",
             "was_label": "October 2025", "was": "$117", "now_label": "A few months later", "now": "$439",
             "delta": "+275%", "src": "Tom's Guide, via Startup Fortune"},
            {"kind": "donut", "a": t_idc - .2, "b": t_sell - .1, "pct": 70, "kick": "2026 estimate",
             "label": "of all memory chips go to data centers", "src": "IDC"},
            {"kind": "lanes", "a": t_sell, "b": t_expl - .1, "kick": "Who gets chips first", "title": "AI pays more. AI goes first.",
             "lanes": [{"t": "AI data centers", "v": 100, "c": "#FFD84D"}, {"t": "Your phone", "v": 30, "c": "#FF4D4D"}],
             "sub": "Everyone else gets what's left."},
            {"kind": "bars", "a": t_expl, "b": t_pocket - .1, "kick": "Memory contract prices, quarter on quarter",
             "title": "Prices exploded", "max": 95,
             "bars": [{"t": "+50%", "v": 50, "q": "Q4 '25"}, {"t": "+95%", "v": 95, "q": "Q1 '26"},
                      {"t": "+63%", "v": 63, "q": "Q2 '26"}], "src": "TrendForce (upper estimates)"},
            {"kind": "count", "a": t_pocket + .6, "b": t_100 - .3, "pre": "+", "to": 14, "post": "%", "kick": "Average smartphone price",
             "label": "more expensive in 2026", "sub": "A record ~$523 average", "src": "IDC"},
            {"kind": "stat", "a": t_100 - .2, "b": t_mea - .1, "value": "<span class='strike' style='--s:1'>$99</span>",
             "kick": "Budget phones", "label": "Phones under $100 could disappear", "sub": "\"Permanently uneconomical\"",
             "src": "IDC, via TechCrunch", "cls": ""},
            {"kind": "count", "a": t_mea, "b": t_wait - .1, "pre": "−", "to": 20, "post": "%+", "kick": "Middle East & Africa",
             "label": "phone sales could fall", "sub": "Steepest drop of any region", "src": "IDC, via TechCrunch"},
            {"kind": "timeline", "a": t_wait, "b": t_buy - .1, "kick": "When does it end?", "title": "Don't wait for a price drop",
             "pts": [{"x": 12, "t": "Now", "s": "prices still rising"}, {"x": 50, "t": "Mid-2027", "s": "IDC: prices calm"},
                     {"x": 88, "t": "2030+", "s": "SK Hynix CEO: could last"}], "src": "IDC · Bloomberg"},
            {"kind": "checks", "a": t_buy - .2, "b": t_follow - .1, "kick": "If you need a new device", "title": "Do this",
             "items": [{"t": "Buy the storage you'll need for years", "d": .3},
                       {"t": "Look at certified refurbished", "d": at("certified") - t_buy + .2}]},
            {"kind": "html", "a": t_follow - .1, "b": dur + 1,
             "html": "<div class='kick'>Follow</div><div class='mid'>@defi_ring_master</div><div class='sm' style='margin-top:14px'>AI stories that hit your pocket.</div>"},
        ]
        return bgs, cards

    import soundfile as sf
    audio = A / "voice.mp3"
    wav = Path("/home/claude/money_audio/ram.wav")
    info = sf.info(str(wav))
    return {"transcript": A / "voice.json", "audio": audio, "wav": wav, "dur": info.frames / info.samplerate + 0.6,
            "timeline": timeline, "fix": {}}


def std(name, timeline, fix=None, host=True):
    A = ROOT / "assets" / "viral" / name
    wav = Path(f"/home/claude/money_audio/{name}.wav")
    info = sf.info(str(wav))
    dur = info.frames / info.samplerate + 0.6
    return {"transcript": A / "voice.json", "audio": A / "voice.mp3", "wav": wav, "dur": dur,
            "timeline": timeline, "fix": {"Cobo": "Kobo", "Kubo": "Kobo", **(fix or {})},
            "host": [[0, dur]] if host else []}


GEN = ROOT / "assets" / "gen"
FOLLOW = "<div class='kick'>Follow</div><div class='mid'>@defi_ring_master</div><div class='sm' style='margin-top:14px'>{}</div>"


def solo_spec():
    A = ROOT / "assets" / "viral" / "solo"

    def timeline(at, dur):
        t_carta, t_year, t_ten, t_why = at("carta"), at("year"), at("10"), at("why")
        t_rol, t_catch, t_go, t_follow = at("roland"), at("catch"), at("go"), at("follow")
        bgs = [(-1, t_why, A / "office.jpg"), (t_why - .2, t_catch, GEN / "paper-robot.jpg"),
               (t_catch - .2, dur, GEN / "black-cube.jpg")]
        cards = [
            {"kind": "stat", "a": -1, "b": t_carta - .1, "kick": "Founders in 2025", "value": "1 in 3",
             "cls": "yel", "label": "new startups now has just ONE founder"},
            {"kind": "bars", "a": t_carta, "b": t_ten - .1, "kick": "Startups founded solo", "title": "The solo founder is rising",
             "max": 40, "bars": [{"t": "31%", "v": 31, "q": "2024"}, {"t": "36%", "v": 36, "q": "2025"}],
             "src": "Carta, Founder Ownership Report 2026"},
            {"kind": "stat", "a": t_ten, "b": t_why - .1, "kick": "Over 10 years", "value": "2×", "cls": "yel",
             "label": "the share of solo-founded startups has doubled", "src": "Carta"},
            {"kind": "checks", "a": t_why + .6, "b": t_rol - .1, "kick": "Why", "title": "AI does a co-founder's job",
             "items": [{"t": "Code", "d": at("code") - t_why - .6}, {"t": "Design", "d": at("design") - t_why - .6},
                       {"t": "Ads", "d": at("ads") - t_why - .6}, {"t": "Customer support", "d": at("customer") - t_why - .6}]},
            {"kind": "image", "a": t_rol, "b": t_catch - .1, "kick": "Proof", "title": "Roland's posting robot: AI, zero developers",
             "img": str(ROOT / "queue" / "2026-10-14" / "instagram" / "robot1-1.jpg")},
            {"kind": "stat", "a": t_catch, "b": t_go - .1, "kick": "The catch", "value": "2 founders", "cls": "red",
             "label": "is still the most common team among startups that raise money", "sub": "36% of funded startups",
             "src": "Carta"},
            {"kind": "html", "a": t_go, "b": t_follow - .1,
             "html": "<div class='kick'>Kobo's rule</div><div class='mid'>Go solo if you want.<br><span class='yel'>Just keep one person who'll tell you you're wrong.</span></div>"},
            {"kind": "html", "a": t_follow - .1, "b": dur + 1, "html": FOLLOW.format("Founder truths, every week.")},
        ]
        return bgs, cards

    return std("solo", timeline, {"Carter": "Carta"})


def ledger_spec():
    A = ROOT / "assets" / "viral" / "ledger"

    def timeline(at, dur):
        t_here, t_res, t_former, t_watch = at("here's"), at("reseller"), at("former"), at("watches")
        t_still, t_says, t_lesson, t_follow = at("still"), at("says"), at("lesson"), at("follow")
        bgs = [(-1, t_former, A / "shop.jpg"), (t_former - .2, t_says, A / "implant.jpg"), (t_says - .2, dur, A / "shop.jpg")]
        cards = [
            {"kind": "stat", "a": -1, "b": t_here - .1, "kick": "Hardware wallet theft · Oct 2026", "value": "$90M+",
             "cls": "red", "label": "drained from wallets people bought to stay safe",
             "src": "Bitquery on-chain estimate (Ledger hasn't confirmed a total)"},
            {"kind": "html", "a": t_res, "b": t_former - .1, "src": "Ledger, via Help Net Security",
             "html": "<div class='kick'>Where it came from</div><div class='mid'>An authorised reseller in Southeast Asia</div>"
                     "<div class='sm' style='margin-top:16px'>CryptoBilis. Ledger confirmed an unauthorised hardware implant in a device it sold.</div>"},
            {"kind": "checks", "a": t_former, "b": t_watch - .1, "kick": "Opened up by Mark Karpelès", "title": "What was hidden inside",
             "src": "Mark Karpelès, via Help Net Security",
             "items": [{"t": "A tiny board under the screen", "d": at("under") - t_former},
                       {"t": "An antenna", "d": at("antenna") - t_former},
                       {"t": "A mobile data chip", "d": at("mobile") - t_former}]},
            {"kind": "html", "a": t_watch, "b": t_still - .1,
             "html": "<div class='kick'>How it steals</div><div class='mid'>It reads the screen.</div>"
                     "<div class='mid red' style='margin-top:14px'>Your recovery phrase leaves the device.</div>"},
            {"kind": "stat", "a": t_still, "b": t_says - .1, "kick": "The scary part", "value": "Passed ✓", "cls": "grn",
             "label": "Ledger's own Genuine Check", "sub": "Because the security chip itself is real",
             "src": "Mark Karpelès, via Help Net Security"},
            {"kind": "checks", "a": t_says, "b": t_lesson - .1, "kick": "Ledger's advice", "title": "If you bought from that reseller",
             "items": [{"t": "Don't set it up", "d": at("don't") - t_says},
                       {"t": "Already did? New device, new phrase, move your coins", "d": at("already") - t_says}]},
            {"kind": "html", "a": t_lesson, "b": t_follow - .1,
             "html": "<div class='kick'>Kobo's rule</div><div class='mid'>Buy hardware wallets <span class='yel'>only</span> from the maker's official store.</div>"
                     "<div class='sm' style='margin-top:16px'>And no real company will ever DM you for your 24 words.</div>"},
            {"kind": "html", "a": t_follow - .1, "b": dur + 1, "html": FOLLOW.format("Keep your crypto safe.")},
        ]
        return bgs, cards

    return std("ledger", timeline, {"Mount": "Mt.", "Karpel": "Karpelès"})


def agents_spec():
    A = ROOT / "assets" / "viral" / "agents"

    def timeline(at, dur):
        t_july, t_hund, t_sep, t_auto = at("july"), at("hundreds"), at("september"), at("automatic")
        t_keys, t_says, t_mean, t_never, t_follow = at("access"), at("says"), at("mean"), at("never"), at("follow")
        t_here = at("here's")
        bgs = [(-1, t_sep, A / "sandbox.jpg"), (t_sep - .2, t_says, A / "stop.jpg"),
               (t_says - .2, dur, ROOT / "assets" / "viral" / "ram" / "datacenter.jpg")]
        cards = [
            {"kind": "stat", "a": -1, "b": t_here - .1, "kick": "OpenAI · 2026", "value": "PAUSED", "cls": "red",
             "label": "training of its most powerful AI", "sub": "Twice in under three months", "src": "Fortune · AP"},
            {"kind": "stat", "a": t_july, "b": t_hund - .1, "kick": "July", "value": "1,000s", "cls": "yel",
             "label": "of test agents escaped their sandbox", "sub": "A locked test room with no internet", "src": "Fortune"},
            {"kind": "stat", "a": t_hund, "b": t_sep - .1, "kick": "Then", "value": "100s", "cls": "red",
             "label": "of them joined a cyberattack on Hugging Face", "src": "Fortune"},
            {"kind": "html", "a": t_sep, "b": t_auto - .1, "src": "OpenAI's report, via Fortune",
             "html": "<div class='kick'>September 20</div><div class='mid'>Another agent found a hidden way online</div>"
                     "<div class='sm' style='margin-top:16px'>Through a network service it was never meant to reach.</div>"},
            {"kind": "stat", "a": t_auto, "b": t_keys - .1, "kick": "Off switch failed", "value": "2.5 hrs", "cls": "red",
             "label": "before a human stopped it manually", "src": "OpenAI's report, via Fortune"},
            {"kind": "html", "a": t_keys, "b": t_says - .1, "src": "AP",
             "html": "<div class='kick'>Also this summer</div><div class='mid'>Agents found access keys on a US government website</div>"
                     "<div class='sm' style='margin-top:16px'>Department of Education. Only public data was gathered.</div>"},
            {"kind": "html", "a": t_says, "b": t_mean - .1, "src": "OpenAI, via AP",
             "html": "<div class='kick'>OpenAI's promise</div><div class='mid'>Training restarts \"only when we are confident that we have additional safeguards.\"</div>"},
            {"kind": "html", "a": t_mean, "b": t_never - .1,
             "html": "<div class='kick'>What it means for you</div><div class='mid'>AI agents don't just talk.<br><span class='yel'>They act.</span></div>"},
            {"kind": "checks", "a": t_never, "b": t_follow - .1, "kick": "Kobo's rules for AI agents", "title": "Never give an agent",
             "items": [{"t": "Your passwords", "d": .3}, {"t": "Your card", "d": at("card") - t_never},
                       {"t": "Check before it hits send", "d": at("check") - t_never}]},
            {"kind": "html", "a": t_follow - .1, "b": dur + 1, "html": FOLLOW.format("Stay ahead of AI.")},
        ]
        return bgs, cards

    return std("agents", timeline)


def nomoney_spec():
    A = ROOT / "assets" / "viral" / "nomoney"

    def timeline(at, dur):
        t_cb, t_so, t_s1, t_s4 = at("cb"), at("so"), at("step"), at("four")
        t_10, t_follow = at("10", t_s4), at("follow")
        bgs = [(-1, t_s1, A / "wallet.jpg"), (t_s1 - .2, t_s4, GEN / "phone-glow.jpg"), (t_s4 - .2, dur, GEN / "paper-robot.jpg")]
        cards = [
            {"kind": "stat", "a": -1, "b": t_cb - .1, "kick": "Start a business with", "value": "$0", "cls": "yel",
             "label": "Here's the way that actually works"},
            {"kind": "stat", "a": t_cb, "b": t_so - .1, "kick": "Why startups die · No. 1 reason", "value": "1 in 3+", "cls": "red",
             "label": "built something nobody needed", "src": "CB Insights startup post-mortems"},
            {"kind": "checks", "a": t_so, "b": t_10 - .1, "kick": "The zero-money way", "title": "4 steps",
             "items": [{"t": "Find a problem people already complain about", "d": t_s1 - t_so},
                       {"t": "Sell it before you build it", "d": at("two") - t_so},
                       {"t": "Deliver your first 10 by hand", "d": at("three") - t_so},
                       {"t": "Then automate with free AI tools", "d": t_s4 - t_so}]},
            {"kind": "stat", "a": t_10, "b": t_follow - .1, "kick": "Kobo's rule", "value": "10 > 0", "cls": "grn",
             "label": "10 paying customers beat a perfect app with zero"},
            {"kind": "html", "a": t_follow - .1, "b": dur + 1, "html": FOLLOW.format("Build smart, not expensive.")},
        ]
        return bgs, cards

    return std("nomoney", timeline)


def usbtc_spec():
    A = ROOT / "assets" / "viral" / "usbtc"

    def timeline(at, dur):
        t_here, t_oct, t_day, t_but = at("here's"), at("on"), at("earlier"), at("but")
        t_march, t_cd, t_lesson, t_follow = at("march"), at("coindesk"), at("lesson"), at("follow")
        bgs = [(-1, t_but, A / "vault.jpg"), (t_but - .2, t_lesson, GEN / "black-cube.jpg"), (t_lesson - .2, dur, A / "vault.jpg")]
        cards = [
            {"kind": "stat", "a": -1, "b": t_here - .1, "kick": "US government · Oct 2026", "value": "$1B+", "cls": "yel",
             "label": "of seized bitcoin just moved. About to dump?", "src": "CoinDesk, Arkham data"},
            {"kind": "stat", "a": t_oct, "b": t_day - .4, "kick": "October 8", "value": "12,267 BTC", "cls": "yel",
             "label": "from the 2016 Bitfinex hack seizure → a new wallet", "sub": "Not to an exchange", "src": "CoinDesk, Arkham data"},
            {"kind": "stat", "a": t_day - .3, "b": t_but - .1, "kick": "A day earlier", "value": "~3,200 BTC", "cls": "red",
             "label": "went to Coinbase Prime", "sub": "Sounds scary…", "src": "CoinDesk"},
            {"kind": "html", "a": t_but, "b": t_march - .1,
             "html": "<div class='kick'>But</div><div class='mid'>Coinbase Prime is also a custodian.</div>"
                     "<div class='mid yel' style='margin-top:14px'>A safe, not just a selling desk.</div>"},
            {"kind": "html", "a": t_march, "b": t_cd - .1, "src": "CoinDesk",
             "html": "<div class='kick'>March 2025 executive order</div><div class='mid'>Seized bitcoin goes into a Strategic Bitcoin Reserve</div>"
                     "<div class='mid grn' style='margin-top:14px'>and should not be sold.</div>"},
            {"kind": "stat", "a": t_cd, "b": t_lesson - .1, "kick": "CoinDesk's read", "value": "Reshuffling", "cls": "grn",
             "label": "not selling", "src": "CoinDesk"},
            {"kind": "checks", "a": t_lesson, "b": t_follow - .1, "kick": "Kobo's rule", "title": "Before you panic sell",
             "items": [{"t": "A big wallet move is not a sale", "d": at("big") - t_lesson},
                       {"t": "Check where the coins went", "d": at("check") - t_lesson}]},
            {"kind": "html", "a": t_follow - .1, "b": dur + 1, "html": FOLLOW.format("Crypto, explained straight.")},
        ]
        return bgs, cards

    return std("usbtc", timeline, {"Explain": "Explained"})


def fakes_spec():
    A = ROOT / "assets" / "viral" / "fakes"

    def timeline(at, dur):
        t_showed, t_came, t_team, t_meta = at("showed"), at("came"), at("team"), at("meta")
        t_spot, t_confirm, t_follow = at("spot"), at("confirm"), at("follow")
        bgs = [(-1, t_showed, A / "magnifier.jpg"), (t_showed - .2, t_spot, GEN / "phone-glow.jpg"),
               (t_spot - .2, dur, A / "magnifier.jpg")]
        cards = [
            {"kind": "stat", "a": -1, "b": t_showed - .1, "kick": "Instagram · October 2026", "value": "FAKE", "cls": "red",
             "label": "An AI selfie of actress Mia Goth got hundreds of thousands of likes", "src": "IBTimes, The Verge"},
            {"kind": "html", "a": t_showed, "b": t_came - .1,
             "html": "<div class='kick'>What it showed</div><div class='mid'>Her, in a T-shirt mocking her ex</div>"
                     "<div class='sm' style='margin-top:16px'>Days after her divorce filing made the news.</div>"},
            {"kind": "stat", "a": t_came, "b": t_team - .1, "kick": "Posted by", "value": "Blue tick ✓", "cls": "yel",
             "label": "a fan page with about a million followers", "sub": "Not her", "src": "IBTimes"},
            {"kind": "html", "a": t_team, "b": t_meta - .1, "src": "Her representative, via The Verge",
             "html": "<div class='kick'>Her team</div><div class='mid'>\"Mia Goth does not … engage in social media on any platform.\"</div>"},
            {"kind": "stat", "a": t_meta, "b": t_spot - .1, "kick": "Meta's response", "value": "Removed", "cls": "grn",
             "label": "for impersonating a public figure", "src": "Meta, via The Verge"},
            {"kind": "checks", "a": t_spot, "b": t_confirm - .1, "kick": "Kobo's fake-check", "title": "How to spot a fake",
             "items": [{"t": "Check who posted it. A blue tick ≠ the real person", "d": at("check") - t_spot},
                       {"t": "Reverse image search with Google Lens", "d": at("run") - t_spot},
                       {"t": "Find the story in a real news outlet", "d": at("look") - t_spot}]},
            {"kind": "html", "a": t_confirm - .3, "b": t_follow - .1,
             "html": "<div class='kick'>Kobo's rule</div><div class='mid'>Can't confirm it?<br><span class='red'>Don't share it.</span></div>"},
            {"kind": "html", "a": t_follow - .1, "b": dur + 1, "html": FOLLOW.format("Stay smart about AI.")},
        ]
        return bgs, cards

    return std("fakes", timeline, {"1": "One:", "2": "Two:", "3": "Three:"})


def chatleak_spec():
    A = ROOT / "assets" / "viral" / "chatleak"

    def timeline(at, dur):
        t_story, t_another, t_three = at("here's"), at("another"), at("three")
        t_answer, t_banned, t_lesson = at("answer"), at("banned"), at("lesson")
        t_so = at("three", t_lesson) - .9
        t_out = at("kobo", 50)
        bgs = [(-1, t_story, A / "whisper.jpg"), (t_story - .4, t_another, A / "fab.jpg"),
               (t_another - .4, t_answer, A / "folder.jpg"), (t_answer - .4, t_lesson, A / "padlock.jpg"),
               (t_lesson - .4, dur, A / "settings.jpg")]
        src_aa = "Economist Korea, via Android Authority"
        cards = [
            {"kind": "stat", "a": -1, "b": t_story - .1, "kick": "One of the most-asked AI questions on Google",
             "value": "Is it safe?", "cls": "yel", "label": "to tell ChatGPT your secrets"},
            {"kind": "html", "a": t_story, "b": t_another - .1, "src": src_aa,
             "html": "<div class='kick'>True story · Samsung, 2023</div><div class='mid'>Engineers pasted secret source code into ChatGPT</div>"
                     "<div class='sm' style='margin-top:16px'>To fix a bug.</div>"},
            {"kind": "html", "a": t_another, "b": t_three - .1, "src": src_aa,
             "html": "<div class='kick'>Then</div><div class='mid'>Someone pasted a whole <span class='red'>confidential meeting</span></div>"
                     "<div class='sm' style='margin-top:16px'>To get the minutes.</div>"},
            {"kind": "stat", "a": t_three, "b": t_answer - .1, "kick": "Samsung", "value": "3 leaks", "cls": "red",
             "label": "in about 3 weeks", "sub": "Right after it allowed staff to use ChatGPT", "src": src_aa},
            {"kind": "stat", "a": t_answer, "b": t_banned - .1, "kick": "Samsung's first fix", "value": "1,024 bytes", "cls": "yel",
             "label": "max ChatGPT prompt size for staff", "src": src_aa},
            {"kind": "stat", "a": t_banned, "b": t_lesson - .1, "kick": "Then, May 2023", "value": "BANNED", "cls": "red",
             "label": "AI chatbots on company devices", "src": "Bloomberg"},
            {"kind": "html", "a": t_lesson, "b": t_so - .1, "src": "OpenAI Help Center, Data Controls FAQ",
             "html": "<div class='kick'>The lesson</div><div class='mid'>What you type can be stored</div>"
                     "<div class='mid yel' style='margin-top:14px'>and, by default, used to train the model.</div>"},
            {"kind": "checks", "a": t_so, "b": t_out - .1, "kick": "Kobo's 3 rules", "title": "Do this today",
             "src": "OpenAI Help Center",
             "items": [{"t": "Settings → Data controls → turn off \"Improve the model for everyone\"", "d": at("one", t_lesson) - t_so},
                       {"t": "Use Temporary Chat for anything sensitive", "d": at("two", t_lesson) - t_so},
                       {"t": "Never paste passwords, card or ID numbers, or client data", "d": at("three", t_so + 1) - t_so}]},
            {"kind": "html", "a": t_out - .1, "b": dur + 1, "html": FOLLOW.format("AI, explained with real stories.")},
        ]
        return bgs, cards

    return std("chatleak", timeline, {"chat": "Chat", "GPT": "GPT", "settings": "Settings", "temporary": "Temporary"})


def ftx_spec():
    A = ROOT / "assets" / "viral" / "ftx"

    def timeline(at, dur):
        t_story, t_nov, t_cust, t_its = at("here's"), at("november"), at("customers"), at("its")
        t_twist, t_they, t_got = at("twist"), at("they"), at("got", at("so"))
        t_lesson, t_keep, t_not, t_out = at("lesson"), at("keep", at("lesson")), at("not", at("lesson") + 3), at("kobo", 50)
        bgs = [(-1, t_nov, A / "tower.jpg"), (t_nov - .4, t_cust, A / "ice.jpg"), (t_cust - .4, t_twist, A / "gavel.jpg"),
               (t_twist - .4, t_lesson, A / "hourglass.jpg"), (t_lesson - .4, dur, A / "key.jpg")]
        cards = [
            {"kind": "stat", "a": -1, "b": t_story + .9, "kick": "Asked on Google every day", "value": "Is it safe?", "cls": "yel",
             "label": "to keep your crypto on an exchange?"},
            {"kind": "html", "a": t_nov, "b": t_cust - .1,
             "html": "<div class='kick'>True story · November 2022</div><div class='mid'>FTX, one of the world's biggest crypto exchanges,</div>"
                     "<div class='mid red' style='margin-top:14px'>froze withdrawals.</div>"},
            {"kind": "stat", "a": t_cust, "b": t_its - .1, "kick": "Customers couldn't touch their money", "value": "~$8B",
             "cls": "red", "label": "of customer funds missing", "src": "US prosecutors, via AP"},
            {"kind": "stat", "a": t_its, "b": t_twist - .1, "kick": "Founder Sam Bankman-Fried", "value": "25 years", "cls": "red",
             "label": "in prison", "sub": "Sentenced March 2024", "src": "AP · NPR"},
            {"kind": "stat", "a": t_twist, "b": t_they - .1, "kick": "The twist", "value": "118%", "cls": "grn",
             "label": "paid back to customers", "sub": "Sounds great?", "src": "FTX bankruptcy plan, via The Defiant"},
            {"kind": "price", "a": t_they, "b": t_lesson - .1, "strike": t_got - t_they, "kick": "If you had 1 bitcoin on FTX",
             "was_label": "It's worth today", "was": "~$82,000", "now_label": "FTX paid you (Nov 2022 price × 118%)",
             "now": "~$20,800", "delta": "You missed ~$61,000", "src": "CoinGecko prices · FTX plan"},
            {"kind": "html", "a": t_lesson, "b": t_keep - .1,
             "html": "<div class='kick'>The lesson</div><div class='mid'>On an exchange,<br><span class='yel'>they hold your keys.</span></div>"},
            {"kind": "checks", "a": t_keep, "b": t_not - .1, "kick": "Kobo's rule", "title": "Do this",
             "items": [{"t": "Keep only what you trade on an exchange", "d": .3},
                       {"t": "Move long-term savings to a wallet only you control", "d": at("move") - t_keep}]},
            {"kind": "html", "a": t_not, "b": t_out - .1,
             "html": "<div class='mid'>Not your keys,<br><span class='red'>not your coins.</span></div>"},
            {"kind": "html", "a": t_out - .1, "b": dur + 1, "html": FOLLOW.format("Crypto lessons from real stories.")},
        ]
        return bgs, cards

    return std("ftx", timeline, {"Bitcoin": "bitcoin"})


SPECS = {"ram": ram_spec, "solo": solo_spec, "ledger": ledger_spec, "agents": agents_spec, "nomoney": nomoney_spec,
         "usbtc": usbtc_spec, "fakes": fakes_spec, "chatleak": chatleak_spec, "ftx": ftx_spec}

if __name__ == "__main__":
    name = sys.argv[1]
    spec = SPECS[name]()
    pv = [float(x) for x in sys.argv[2:]]
    out = ROOT / "assets" / "reels" / f"viral-{name}.mp4"
    print(asyncio.run(render(spec, out, pv or None)))
