"""Reel opening: cut the greeting and open on ONE clean text hook (Roland, 28 Oct 2026: "upgrade the tool that cuts
reels into opening").

Research (text hooks, Oct 2026): the first second decides watch-or-swipe; one message only; 5-8 words; big, centered,
high contrast; the voice says the same promise. Our first frames used to show three texts at once (card + hook + captions).
Now, for the first `secs` seconds, the whole frame is blurred and dimmed so only the hook is readable; then the normal
video (cards, captions) takes over.

    python3 studio/hookcut.py <in.mp4> <out.mp4> <start_seconds> "Hook line one|line two" [ypos 0.30-0.60] [secs]

The last line is drawn black on the yellow highlight (the payoff words); earlier lines are white.
Keep it to 7 words or fewer in total. Log the hook and its style in queue/hooks.json.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"


def hookcut(src, out, start, hook, secs=2.0, ypos=0.46):
    lines = [x.strip() for x in hook.split("|") if x.strip()]
    words = sum(len(x.split()) for x in lines)
    if words > 8:
        print(f"warning: hook has {words} words; keep it to 7 or fewer", file=sys.stderr)
    n = len(lines)
    size = min(104, int(850 / (0.56 * max(len(x) for x in lines))))  # keep every line inside ~850 px
    draws = []
    for i, line in enumerate(lines):
        tf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
        tf.write(line)
        tf.close()
        last = i == n - 1
        y = f"(h*{ypos})+{(i - (n - 1) / 2) * size * 1.45:.0f}-text_h/2"
        style = ("fontcolor=0x07080B:box=1:boxcolor=0xFFD84D:boxborderw=24" if last
                 else "fontcolor=white:shadowcolor=0x000000AA:shadowx=0:shadowy=4")
        draws.append(f"drawtext=fontfile={FONT}:textfile={tf.name}:fontsize={size}:{style}:"
                     f"x=(w-text_w)/2:y={y}:enable='lt(t,{secs})'")
    filt = (f"[0:v]split[a][b];[b]boxblur=22:2,eq=brightness=-0.16:saturation=0.8[bl];"
            f"[a][bl]overlay=enable='lt(t,{secs})'," + ",".join(draws) + "[v]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{start:.2f}", "-i", str(src), "-filter_complex", filt,
                    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], check=True)
    return out


if __name__ == "__main__":
    a = sys.argv
    print(hookcut(Path(a[1]), Path(a[2]), float(a[3]), a[4],
                  ypos=float(a[5]) if len(a) > 5 else 0.46, secs=float(a[6]) if len(a) > 6 else 2.0))
