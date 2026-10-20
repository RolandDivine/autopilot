"""Reel first-3-seconds fix (Roland, 21 Oct 2026 Instagram review): cut the "Hey, Kobo here" greeting and open
on a big on-screen hook line for the first 3 seconds.

    python3 studio/hookcut.py <in.mp4> <out.mp4> <start_seconds> "Hook line one|line two"
"""
import subprocess
import sys
import tempfile
from pathlib import Path

FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"


def hookcut(src, out, start, hook, secs=3.0, ypos=0.40):
    lines = hook.split("|")
    filt = []
    n = len(lines)
    for i, line in enumerate(lines):
        tf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
        tf.write(line)
        tf.close()
        y = f"(h*{ypos})+{(i - (n - 1) / 2) * 120:.0f}"
        filt.append(f"drawtext=fontfile={FONT}:textfile={tf.name}:fontsize=86:fontcolor=0x07080B:"
                    f"box=1:boxcolor=0xFFD84D:boxborderw=26:x=(w-text_w)/2:y={y}:enable='lt(t,{secs})'")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{start:.2f}", "-i", str(src), "-vf", ",".join(filt),
                    "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", str(out)], check=True)
    return out


if __name__ == "__main__":
    print(hookcut(Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3]), sys.argv[4], ypos=float(sys.argv[5]) if len(sys.argv) > 5 else 0.40))
