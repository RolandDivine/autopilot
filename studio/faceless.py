"""Faceless documentary-style explainer engine (Roland, 30 Oct 2026: "think as a professional video editor who does
faceless content... CapCut and Premiere Pro"). 16:9, 1920x1080, 30 fps, over Roland's own (enhanced) voice.

Editing grammar: a new visual every 2-4 s; image panels with slow push-in (Ken Burns) blended into a dark stage;
motion graphics carry the numbers (counters, bar charts, on-chain ticker); kinetic captions word by word;
whip-flash transitions; vignette + film grain; a sound effect on every cut (whoosh / impact / ticks) and a low drone bed.

    python studio/faceless.py sample       -> assets/youtube/faceless-sample.mp4
"""
import base64
import json
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ig_options import face  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "assets" / "gen"
W, H, FPS = 1920, 1080, 30
FONTS = face("Jakarta", "plus-jakarta-sans", (500, 700, 800)) + face("SpaceG", "space-grotesk", (500, 700))


def b64(p):
    p = Path(p)
    mime = "png" if p.suffix == ".png" else "jpeg"
    return f"data:image/{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def grain_png(path):
    from PIL import Image
    random.seed(7)
    im = Image.new("L", (512, 512))
    im.putdata([random.randint(0, 255) for _ in range(512 * 512)])
    im.save(path)
    return path


# ---------------------------------------------------------------- sample: 37.0-58.45 s of Roland's recording
SAMPLE = {
    "audio": "/home/claude/money_audio/roland-binance-enh.wav",
    "t0": 36.95, "t1": 58.55,
    "label": "THE $6B BINANCE HACK",
    "scenes": [
        {"a": 0.0, "b": 2.05, "kind": "date", "img": "hourglass-half.jpg"},
        {"a": 2.05, "b": 5.35, "kind": "ticker", "img": "coin-siphon.jpg"},
        {"a": 5.35, "b": 7.75, "kind": "stamp", "img": "circuit-lock.jpg"},
        {"a": 7.75, "b": 10.75, "kind": "counter", "img": "black-cube.jpg"},
        {"a": 10.75, "b": 19.1, "kind": "chart", "img": "coin-collapse.jpg"},
        {"a": 19.1, "b": 21.6, "kind": "times", "img": "arrow-hourglass.png"},
    ],
    "captions": [
        (0.05, 4.1, "Money started leaving Binance's wallets"),
        (4.1, 5.3, "fast. Within hours."),
        (5.35, 7.7, "Binance confirmed it had been hacked."),
        (7.75, 10.7, "Total impact: around $6 billion."),
        (10.75, 13.25, "The biggest crypto hack in history."),
        (13.3, 19.05, "Previous record: Bybit, 2025. About $1.5 billion."),
        (19.1, 21.5, "Roughly four times bigger."),
    ],
    "sfx": [("whoosh", 2.0), ("tick", 2.35), ("tick", 3.05), ("tick", 3.75), ("riser", 5.0), ("impact", 6.9),
            ("whoosh", 7.7), ("ticks", 8.0), ("impact", 9.8), ("whoosh", 10.7), ("whoosh", 19.05), ("impact", 19.4)],
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1920px;height:1080px;overflow:hidden;background:#07080B;font-family:Jakarta;color:#fff}
#stage{position:absolute;inset:0;overflow:hidden}
.scene{position:absolute;inset:0;opacity:0}
.panel{position:absolute;top:0;right:0;width:1100px;height:1080px;overflow:hidden;
 -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 38%);mask-image:linear-gradient(90deg,transparent 0,#000 38%)}
.panel img{position:absolute;width:100%;height:auto;top:50%;left:0;transform-origin:50% 50%}
.glow{position:absolute;inset:0;background:radial-gradient(1200px 700px at 75% 45%,rgba(255,216,77,.10),transparent 60%)}
.kick{font:700 30px SpaceG;letter-spacing:6px;text-transform:uppercase;color:#FFD84D}
.big{font:800 140px/1 Jakarta;letter-spacing:-5px}
.left{position:absolute;left:120px;top:250px;width:900px}
.red{color:#FF4D4D}.yel{color:#FFD84D}
.row{font:500 34px SpaceG;color:#d9dde5;background:rgba(255,255,255,.06);border-left:4px solid #FF4D4D;padding:18px 24px;margin-top:18px;border-radius:6px}
.row b{color:#FF4D4D;font-weight:700}
.stamp{position:absolute;left:120px;top:330px;font:800 190px/1 Jakarta;letter-spacing:-6px;color:#FF4D4D;
 border:12px solid #FF4D4D;padding:10px 40px;border-radius:18px;transform-origin:30% 50%}
.bars{position:absolute;left:120px;top:250px;width:1180px}
.bar{display:flex;align-items:center;margin:26px 0}
.bar .n{width:300px;font:700 34px Jakarta;color:#cfd3db}.bar .n span{display:block;font:500 24px SpaceG;color:#8a909c}
.bar .t{height:74px;border-radius:8px;background:#3a3f4a;position:relative}
.bar .v{position:absolute;left:100%;margin-left:22px;top:50%;transform:translateY(-50%);font:800 40px Jakarta;white-space:nowrap}
.note{position:absolute;left:120px;bottom:210px;font:500 22px SpaceG;color:#7d8390}
#cap{position:absolute;left:0;right:0;bottom:90px;text-align:center;font:800 54px Jakarta;letter-spacing:-1px}
#cap span{display:inline-block;margin:0 9px;opacity:0;text-shadow:0 4px 24px rgba(0,0,0,.8)}
#cap span.on{opacity:1}#cap span.hot{color:#FFD84D}
#top{position:absolute;left:120px;top:70px;font:700 24px SpaceG;letter-spacing:5px;color:#fff;opacity:.85}
#top i{display:inline-block;width:12px;height:12px;border-radius:50%;background:#FF4D4D;margin-right:14px;vertical-align:middle}
#prog{position:absolute;left:0;top:0;height:6px;background:#FFD84D}
#flash{position:absolute;inset:0;background:#fff;opacity:0;mix-blend-mode:screen}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,.65) 100%);pointer-events:none}
#grain{position:absolute;inset:-50%;opacity:.07;mix-blend-mode:overlay;pointer-events:none}
#rec{position:absolute;right:120px;top:66px;font:700 24px SpaceG;letter-spacing:3px;color:#8a909c}
"""

JS = r"""
const E=(t,a,b)=>Math.min(1,Math.max(0,(t-a)/(b-a)));
const OUT=x=>1-Math.pow(1-x,3), INOUT=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const BACK=x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
function fmt(n){return n.toLocaleString('en-US')}
function render(t){
  const S=window.SPEC; const total=S.t1-S.t0;
  document.getElementById('prog').style.width=(100*t/total)+'%';
  document.getElementById('grain').style.transform=`translate(${(Math.sin(t*91)*6).toFixed(1)}%,${(Math.cos(t*77)*6).toFixed(1)}%)`;
  let flash=0;
  S.scenes.forEach((s,i)=>{
    const el=document.getElementById('s'+i);
    const fin=E(t,s.a-0.12,s.a+0.18), fout=1-E(t,s.b-0.12,s.b+0.12);
    const vis=(t>=s.a-0.15&&t<s.b+0.15)?Math.min(fin,fout):0;
    el.style.opacity=vis;
    const p=E(t,s.a,s.b);
    const img=el.querySelector('.panel img');
    if(img){const sc=1.06+0.12*INOUT(p); const dx=(i%2?-1:1)*30*p;
      img.style.transform=`translate(${dx}px,-50%) scale(${sc})`;
      img.style.filter=s.kind=='stamp'?`saturate(.3) sepia(1) hue-rotate(-50deg) saturate(4) brightness(${.55+.25*Math.abs(Math.sin(t*14))})`:'brightness(.85)';}
    const lt=t-s.a;
    // whip-in offset
    const whip=(1-OUT(E(t,s.a-0.05,s.a+0.35)))*140;
    el.querySelectorAll('.left,.bars,.stamp').forEach(x=>x.style.translate=`${-whip}px 0`);
    if(Math.abs(t-s.a)<0.12&&i>0) flash=Math.max(flash,0.55*(1-Math.abs(t-s.a)/0.12));
    if(s.kind=='date'){
      el.querySelector('#d1').style.opacity=OUT(E(lt,0.05,0.4));
      const txt='29 OCT 2026  ·  20:24 UTC'; const k=Math.floor(txt.length*E(lt,0.25,1.1));
      el.querySelector('#d2').textContent=txt.slice(0,k)+(k<txt.length&&Math.floor(t*6)%2?'▍':'');
      el.querySelector('#d3').style.opacity=OUT(E(lt,1.1,1.5));
    }
    if(s.kind=='ticker'){
      el.querySelector('.left .kick').style.opacity=OUT(E(lt,0,0.3));
      el.querySelectorAll('.row').forEach((r,j)=>{const q=OUT(E(lt,0.3+j*0.7,0.6+j*0.7));r.style.opacity=q;r.style.transform=`translateX(${(1-q)*-60}px)`;});
    }
    if(s.kind=='stamp'){
      const q=E(lt,1.5,1.62); const st=el.querySelector('.stamp');
      st.style.opacity=q>0?1:0; st.style.transform=`rotate(-6deg) scale(${q>0?1+1.4*(1-OUT(E(lt,1.5,1.75))):3})`;
      const shake=lt>1.5&&lt<1.9?(Math.sin(t*120)*10*(1.9-lt)):0; el.style.transform=`translate(${shake}px,${shake*.6}px)`;
      el.querySelector('.left').style.opacity=OUT(E(lt,0.05,0.4))*(1-E(lt,1.45,1.5));
      if(Math.abs(lt-1.55)<0.1) flash=Math.max(flash,.8*(1-Math.abs(lt-1.55)/0.1));
    }
    if(s.kind=='counter'){
      const q=INOUT(E(lt,0.25,2.05)); const v=Math.round(6e9*q/1e6)*1e6;
      el.querySelector('#cnt').textContent='$'+fmt(v);
      el.querySelector('#cnt').style.transform=`scale(${1+0.06*Math.max(0,1-Math.abs(lt-2.1)/0.25)})`;
      el.querySelector('#csub').style.opacity=OUT(E(lt,2.1,2.5));
    }
    if(s.kind=='chart'){
      el.querySelector('.bars .kick').style.opacity=OUT(E(lt,0,0.3));
      const data=S.chart; const max=6.3;
      el.querySelectorAll('.bar').forEach((b,j)=>{
        const d=data[j]; const st=d.last?0.5:0.15+j*0.12, en=d.last?1.9:0.6+j*0.12;
        const q=OUT(E(lt,st,en)); b.style.opacity=OUT(E(lt,st-0.1,st+0.15));
        const bar=b.querySelector('.t'); bar.style.width=(860*d.v/max*q)+'px';
        b.querySelector('.v').textContent=d.lab; b.querySelector('.v').style.opacity=E(lt,en-0.2,en);
        const hi=(d.hi&&lt>2.55)?1:0;
        bar.style.background=d.last?'#FF4D4D':(hi?'#FFD84D':'#3a3f4a');
        b.querySelector('.n').style.color=d.last?'#fff':(hi?'#FFD84D':'#cfd3db');
        b.style.transform=hi?`scale(${1+0.04*Math.max(0,1-Math.abs(lt-2.7)/0.3)})`:'none'; b.style.transformOrigin='0 50%';
      });
      el.querySelector('.note').style.opacity=OUT(E(lt,2.2,2.6));
    }
    if(s.kind=='times'){
      const q=E(lt,0.3,0.55); const x=el.querySelector('#x4');
      x.style.opacity=q>0?1:0; x.style.transform=`scale(${q>0?1+0.9*(1-OUT(E(lt,0.3,0.6))):2})`;
      el.querySelector('#x4s').style.opacity=OUT(E(lt,0.7,1.0));
      if(Math.abs(lt-0.32)<0.1) flash=Math.max(flash,.7*(1-Math.abs(lt-0.32)/0.1));
    }
  });
  document.getElementById('flash').style.opacity=flash;
  // captions
  const cap=document.getElementById('cap'); let html='';
  S.captions.forEach(c=>{ if(t>=c[0]&&t<c[1]){ const w=c[2].split(' '); const span=Math.min(c[1]-c[0],Math.max(0.9,w.length*0.32));
    html=w.map((x,i)=>{const on=t>=c[0]+span*i/w.length; const hot=/\$|\d|hack|billion|bigger|fast|Bybit/i.test(x);
      return `<span class="${on?'on':''} ${hot?'hot':''}">${x}</span>`}).join('');}});
  cap.innerHTML=html;
}
"""


def html(spec):
    sc = []
    for i, s in enumerate(spec["scenes"]):
        k = s["kind"]
        panel = f"<div class='panel'><img src='{b64(GEN / s['img'])}'></div><div class='glow'></div>"
        if k == "date":
            body = ("<div class='left'><div class='kick' id='d1'>Thursday night</div>"
                    "<div class='big' style='font-size:96px;margin-top:26px;font-family:SpaceG;letter-spacing:-2px' id='d2'></div>"
                    "<div style='font:600 40px Jakarta;color:#aab0bb;margin-top:30px' id='d3'>Money starts leaving Binance's hot wallets.</div></div>")
        elif k == "ticker":
            body = ("<div class='left' style='top:230px'><div class='kick'>On-chain · outflows</div>"
                    "<div class='row'><b>−167,464 ETH</b> &nbsp;leaves wallet “Binance 14”</div>"
                    "<div class='row'><b>−28,005 ETH</b> &nbsp;leaves wallet “Binance 16”</div>"
                    "<div class='row'><b>→</b> forwarded to a new address ~15 min later</div>"
                    "<div style='font:500 22px SpaceG;color:#7d8390;margin-top:22px'>Source: CoinDesk, 30 Oct 2026</div></div>")
        elif k == "stamp":
            body = ("<div class='left'><div class='kick'>Within hours</div><div class='big' style='font-size:110px;margin-top:20px'>Binance<br>confirms…</div></div>"
                    "<div class='stamp'>HACKED</div>")
        elif k == "counter":
            body = ("<div class='left' style='top:300px'><div class='kick'>Total impact (estimate)</div>"
                    "<div class='big yel' id='cnt' style='font-size:150px;margin-top:24px;transform-origin:0 50%'>$0</div>"
                    "<div id='csub' style='font:600 40px Jakarta;color:#aab0bb;margin-top:26px'>The biggest crypto hack ever recorded.</div></div>")
        elif k == "chart":
            bars = "".join(f"<div class='bar'><div class='n'>{d['name']}<span>{d['year']}</span></div><div class='t'><div class='v'></div></div></div>"
                           for d in spec["chart"])
            body = (f"<div class='bars'><div class='kick'>Biggest crypto hacks ever</div>{bars}</div>"
                    "<div class='note'>Value at the time of theft. Binance figure is an early estimate.</div>")
        elif k == "times":
            body = ("<div class='left' style='top:230px'><div id='x4' style='font:800 360px/1 Jakarta;letter-spacing:-14px;color:#FFD84D;transform-origin:20% 60%'>4×</div>"
                    "<div id='x4s' style='font:700 54px Jakarta;margin-top:10px'>bigger than the old record.</div></div>")
        sc.append(f"<div class='scene' id='s{i}'>{panel}{body}</div>")
    grain = b64(grain_png(Path("/tmp/claude-0/-home-claude/7bf7680f-a27b-5721-8432-9f712c0cf377/scratchpad/grain.png")))
    return (f"<html><head><style>{FONTS}{CSS}</style></head><body><div id='stage'>{''.join(sc)}</div>"
            f"<img id='grain' src='{grain}' style='width:200%;height:200%;image-rendering:pixelated'>"
            f"<div id='vig'></div><div id='flash'></div><div id='prog'></div>"
            f"<div id='top'><i></i>{spec['label']}</div><div id='rec'>ROLAND DIVINE</div><div id='cap'></div>"
            f"<script>window.SPEC={json.dumps({k: v for k, v in spec.items() if k != 'audio'})};{JS}</script></body></html>")


def sfx(spec, out, dur):
    """Synthesised sound design: whoosh, impact, tick(s), riser, plus a low drone bed. All generated, no licensing."""
    tmp = Path(out).parent / "sfx"
    tmp.mkdir(exist_ok=True)
    gen = {
        "whoosh": "anoisesrc=color=pink:d=0.55:a=0.5,bandpass=f=1800:w=1600,afade=t=in:d=0.3,afade=t=out:st=0.3:d=0.25,volume=0.55",
        "impact": "sine=f=48:d=0.9,volume=1.6,afade=t=out:st=0.05:d=0.85[a];anoisesrc=color=brown:d=0.25:a=0.6,lowpass=f=900,afade=t=out:d=0.25[b];[a][b]amix=2",
        "tick": "sine=f=2200:d=0.04,afade=t=out:d=0.04,volume=0.35",
        "ticks": "aevalsrc=0.25*sin(2*PI*2400*t)*lt(mod(t\\,0.09)\\,0.012):d=2.0:s=44100,afade=t=out:st=1.7:d=0.3",
        "riser": "anoisesrc=color=white:d=1.9:a=0.08,highpass=f=3000,afade=t=in:d=1.8,afade=t=out:st=1.75:d=0.15,volume=0.4",
    }
    for k, f in gen.items():
        if "[" in f:
            cmd = ["ffmpeg", "-loglevel", "error", "-y", "-filter_complex", f, str(tmp / f"{k}.wav")]
        else:
            cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f, str(tmp / f"{k}.wav")]
        subprocess.run(cmd, check=True)
    # drone bed: two low sines with slow tremolo
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-filter_complex",
                    f"sine=f=55:d={dur}[a];sine=f=82.4:d={dur}[b];[a][b]amix=2,tremolo=f=0.25:d=0.4,volume=0.35,afade=t=in:d=1,afade=t=out:st={dur-1.2}:d=1.2",
                    str(tmp / "drone.wav")], check=True)
    ins, filt = ["-i", str(tmp / "drone.wav")], ["[0:a]volume=0.5[d]"]
    mix = ["[d]"]
    for j, (k, at) in enumerate(spec["sfx"], 1):
        ins += ["-i", str(tmp / f"{k}.wav")]
        ms = int(at * 1000)
        filt.append(f"[{j}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,adelay={ms}|{ms}[x{j}]")
        mix.append(f"[x{j}]")
    filt.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,atrim=0:{dur}[out]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[out]",
                    "-ar", "48000", "-ac", "1", str(out)], check=True)


def render(spec, out, preview=None):
    dur = spec["t1"] - spec["t0"]
    work = Path("/tmp/claude-0/-home-claude/7bf7680f-a27b-5721-8432-9f712c0cf377/scratchpad/faceless")
    frames = work / "frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir(parents=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(html(spec))
        pg.wait_for_timeout(600)
        ts = preview or [i / FPS for i in range(int(dur * FPS))]
        for i, t in enumerate(ts):
            pg.evaluate(f"render({t})")
            pg.screenshot(path=str(frames / f"f{i:05d}.jpg"), type="jpeg", quality=90)
        b.close()
    if preview:
        return [str(frames / f"f{i:05d}.jpg") for i in range(len(ts))]
    sfx(spec, work / "sfx.wav", dur)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(spec["t0"]), "-t", str(dur), "-i", spec["audio"],
                    str(work / "voice.wav")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg"),
                    "-i", str(work / "voice.wav"), "-i", str(work / "sfx.wav"), "-filter_complex",
                    "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,afade=t=in:d=0.08[v];"
                    "[2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,volume=0.45[s];"
                    "[v][s]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
    return out


SAMPLE["chart"] = [
    {"name": "Mt. Gox", "year": "2014", "v": 0.46, "lab": "$0.46B"},
    {"name": "Ronin", "year": "2022", "v": 0.62, "lab": "$0.62B"},
    {"name": "Bybit", "year": "2025", "v": 1.5, "lab": "$1.5B", "hi": True},
    {"name": "Binance", "year": "2026", "v": 6.3, "lab": "≈ $6.3B", "last": True},
]

if __name__ == "__main__":
    out = ROOT / "assets" / "youtube" / "faceless-sample.mp4"
    pv = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None
    print(render(SAMPLE, out, pv))
