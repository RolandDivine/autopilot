"""Sun 8 Nov 2026 (nightly build, 6 Nov). Run from repo root:  python3 studio/days/week46a.py

Plan:
  Sun 8   No LinkedIn (weekend), no IG carousel (week 45 cap). Reels: trend-agents 07:00, ex19 inflation 10:00 (36 s cut,
          payoff first), trend-extension 13:00, trend-licensed 19:00 UTC (3 h+ apart). Stories below.
  Sat 7   ex08 moved 11:00 -> 10:00 UTC so it sits 3 h from the 07:00 and 13:00 trend Reels.
Images reused from assets/gen (no Figma credits spent).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import week45d  # noqa: E402

week45d.STORIES["2026-11-08"] = {
    "s0900": ("paper-robot.jpg", "Would you let an AI agent ==spend your money?==", "Yes or no 👇"),
    "s1100": ("jar-notes.jpg", "Your savings ==are shrinking.==", "New Reel · tap my profile"),
    "s1400": ("circuit-lock.jpg", "That extension you installed: ==who made it?==", "New Reel · tap my profile"),
    "s1700": ("jar-notes.jpg", "Where do you keep ==your savings?==", "Cash, bank or other? Reply 👇"),
    "s2100": ("twin-keys.jpg", "Is your crypto app ==licensed in your country?==", "New Reel · tap my profile"),
}

if __name__ == "__main__":
    week45d.stories("2026-11-08")
    print("built 2026-11-08 stories only")
