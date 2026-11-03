"""Cut a banked voiceover down to a 30-40 s Reel (Roland, 3 Nov 2026: "Keep Reels 30-40 seconds, payoff in the first 5 s").

    python3 studio/splice.py ex15-passkeys ex15-passkeys-cut 1.7-16.5 21.5-36.2 43.5-48.3 58.1-60.9

Keeps the listed [a-b] ranges (seconds, matched to whole words) of assets/vo/<src>.mp3, joins them with a short pause,
and writes assets/vo/<dst>.mp3 + <dst>.json (word timings remapped), so explainers.py can render <dst> as usual.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO = ROOT / "assets" / "vo"
GAP = 0.18


def splice(src, dst, ranges):
    segs = json.loads((VO / f"{src}.json").read_text())
    words = [w for s in segs for w in s["words"]]
    cuts, out_segs, t = [], [], 0.0
    for a, b in ranges:
        idx = [i for i, w in enumerate(words) if w[0] >= a - 0.05 and w[0] < b]
        i0, i1 = idx[0], idx[-1]
        s = max(words[i0 - 1][1] if i0 else 0.0, words[i0][0] - 0.06)
        nxt = words[i1 + 1][0] if i1 + 1 < len(words) else words[i1][1] + 0.4
        e = min(nxt - 0.04, max(words[i1][1] + 0.35, words[i1][0] + 0.45))
        cuts.append((s, e))
        ws = [[round(w[0] - s + t, 3), round(w[1] - s + t, 3), w[2]] for w in words[i0:i1 + 1]]
        out_segs.append({"start": ws[0][0], "end": ws[-1][1], "text": "".join(w[2] for w in ws).strip(), "words": ws})
        t += (e - s) + GAP
    parts = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,apad=pad_dur={GAP}[p{i}];"
                    for i, (s, e) in enumerate(cuts))
    flt = parts + "".join(f"[p{i}]" for i in range(len(cuts))) + f"concat=n={len(cuts)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(VO / f"{src}.mp3"), "-filter_complex", flt,
                    "-map", "[o]", "-b:a", "192k", str(VO / f"{dst}.mp3")], check=True)
    (VO / f"{dst}.json").write_text(json.dumps(out_segs, indent=1))
    for sgm in out_segs:
        print(f"{sgm['start']:5.1f} {sgm['text']}")
    print(f"total {t - GAP:.1f}s")


if __name__ == "__main__":
    splice(sys.argv[1], sys.argv[2], [tuple(map(float, r.split("-"))) for r in sys.argv[3:]])
