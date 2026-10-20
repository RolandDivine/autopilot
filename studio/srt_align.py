"""Make an accurate .srt from the real script, timed with Whisper segments.

Whisper mishears words but its segment timings are good. We anchor on the "Chapter N." lines and spread each
section's real sentences across that section's speech time in proportion to their length.

    python studio/srt_align.py <script.txt> <voice.json> <out.srt> <t0> <t1> ... <end>
    (one anchor time per section: intro, chapter 1..6, close, then the end time)
"""
import re
import sys
from pathlib import Path


def ts(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"


def lines(sentence, n=42):
    out, cur = [], ""
    for w in sentence.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    out.append(cur)
    return ["\n".join(out[i:i + 2]) for i in range(0, len(out), 2)]


def main(script, out, anchors):
    text = Path(script).read_text().strip()
    parts = re.split(r"(?=Chapter (?:one|two|three|four|five|six)\.)|(?=So here's the whole thing)", text)
    parts = [p.strip() for p in parts if p.strip()]
    assert len(parts) == len(anchors) - 1, (len(parts), len(anchors))
    cues = []
    for p, a, b in zip(parts, anchors, anchors[1:]):
        sents = [s for s in re.split(r"(?<=[.?!:])\s+", p.replace("\n", " ")) if s]
        pieces = [x for s in sents for x in lines(s)]
        total = sum(len(x) for x in pieces)
        t = a
        for x in pieces:
            d = (b - a - .3) * len(x) / total
            cues.append((t, t + d, x))
            t += d
    Path(out).write_text("".join(f"{i}\n{ts(a)} --> {ts(b)}\n{x}\n\n" for i, (a, b, x) in enumerate(cues, 1)))
    print(len(cues), "cues")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[3], [float(x) for x in sys.argv[4:]])
