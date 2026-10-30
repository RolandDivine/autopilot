"""Binance hack trend (30 Oct 2026, Roland: "ride on it... now"). Facts from CoinDesk, Euronews, Cointelegraph (30 Oct).
Not confirmed anywhere: "7 other banks" hit, so it is left out. Run from studio/: python days/binance.py"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cover import cover  # noqa: E402
from ig_chat import carousel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "queue" / "live" / "2026-10-30-binance"
GEN = ROOT / "assets" / "gen"

LI = """Binance didn't lose billions to a bug in its code. It lost them to one key.

Overnight, Binance suffered what's being called the biggest crypto hack in history, with around $6 billion impacted. North Korea-linked hackers are suspected.

As someone who audits smart contracts, here's the part that should keep every builder up at night.

Early reports say the attackers got the signing key to one of Binance's hot wallets. Then they used an Ethereum feature called EIP-7702 to turn that wallet into a "sweeper", quietly forwarding funds to their own address.

No exotic exploit. One key.

Three lessons:

1. Your security is only as strong as your key management. Audited code doesn't help if one key controls the vault.

2. "Decentralised" is a spectrum. Tether and Circle froze more than $2.4 billion of the stolen stablecoins within hours. Good for the victims. Also a reminder of who really holds the switch.

3. Users carry the risk either way. On an exchange, you trust their security team. In your own wallet, you are the security team.

Binance says user funds are safe and it will cover the losses. Deposits and withdrawals are paused while it investigates.

For builders: how many single keys can move money in your system today?
For everyone else: where is your crypto right now, and who holds the key?

Education, not financial advice."""
LI_SRC = "Sources: CoinDesk (30 Oct 2026, reserve wallets and EIP-7702), Euronews (amounts frozen, withdrawals paused), Cointelegraph live updates (North Korea's TraderTraitor suspected). Figures are early estimates and may change."

HOOK = "Binance got hacked. ==Is your money safe?=="
SLIDES = [
    [("q", "Roland, I heard Binance got hacked 😱 Is my money gone?"),
     ("r", "Breathe 🙏🏾 Let's go through it calmly."),
     ("r", "Binance says ==user funds are safe== and that it will cover the losses.")],
    [("r", "**What happened** ⚡"),
     ("r", "Hackers got the key to one of Binance's hot wallets, the online wallet it uses to pay out withdrawals."),
     ("r", "Around ==$6 billion== was hit. The biggest crypto hack ever. North Korea-linked hackers are suspected.")],
    [("q", "So why can't I withdraw?"),
     ("r", "Deposits and withdrawals are paused while Binance locks things down and works with investigators."),
     ("r", "Tether and Circle have frozen ==over $2.4 billion== of the stolen stablecoins.")],
    [("r", "**The scam wave is coming** 🚩"),
     ("r", "\"Claim your Binance refund\"\n\"Verify your account now\""),
     ("r", "\"Move your funds to this safe wallet\"\n==All fake. Don't click.==")],
    [("r", "**Do this today** ✅"),
     ("r", "Don't panic-sell. Use an authenticator app for 2FA, not SMS."),
     ("r", "Only use the official app or a site you type in yourself. ==Binance won't DM you first.==")],
    [("q", "Should I even keep coins on an exchange?"),
     ("r", "Keep only what you actively trade there."),
     ("r", "Long-term savings: ==a wallet you control==. Seed phrase on paper, never online.")],
    [("r", "Your turn 👇"),
     ("r", "Where do you keep your crypto: ==exchange, own wallet, or both?=="),
     ("r", "Tell me in the comments and I'll help you think it through. 💬")],
    [("r", "📌 Save this · 📤 Send it to a friend on Binance"),
     ("r", "Follow **@defi_ring_master** for crypto safety, explained straight."),
     ("r", "Education, not financial advice.")],
]
CAP = """Binance hack explained: what happened, and what to do now 🚨

Around $6 billion hit in the biggest crypto hack ever. Is your money safe, why withdrawals are paused, and the fake "refund" scams to ignore. Swipe →

💬 Comment: exchange, own wallet, or both?
📌 Save it · 📤 Send it to a friend on Binance
🔔 Follow @defi_ring_master
Education, not financial advice.

#binance #crypto #cryptonews #nigeria"""

STORIES = {
    "s1100": ("black-cube.jpg", "Binance was hacked overnight. ==Is your money safe?==", "Full breakdown · tap my profile"),
    "s1400": ("glass-keys.jpg", "\"Claim your Binance refund\"? ==It's a scam.==", "New Reel · tap my profile"),
    "s1700": ("twin-keys.jpg", "Exchange or your own wallet: ==which is safer?==", "New Reel · tap my profile"),
    "s2100": ("black-cube.jpg", "Where do you keep your crypto? ==Reply 👇==", "I'll help you think it through"),
}


def build():
    D.mkdir(parents=True, exist_ok=True)
    (D / "li.txt").write_text(LI)
    (D / "li_src.txt").write_text(LI_SRC)
    cover(GEN / "people-trader-night.png", "One key. ==Billions gone.==", D / "li.jpg", kicker="Binance hack · lessons", handle="Roland Divine", swipe=False)
    cover(GEN / "black-cube.jpg", HOOK, D / "ig-0.jpg", kicker="Crypto · breaking")
    rest = carousel(SLIDES, "Crypto · breaking", D, "ig", offset=1)
    (D / "ig_paths.txt").write_text(" ".join(["queue/live/2026-10-30-binance/ig-0.jpg"] + [f"queue/live/2026-10-30-binance/{Path(p).name}" for p in rest]))
    (D / "ig_cap.txt").write_text(CAP)
    Q = ROOT / "queue" / "2026-10-30" / "stories"
    for at, (img, text, foot) in STORIES.items():
        cover(GEN / img, text, Q / f"{at}.jpg", kicker=foot, size=(1080, 1920), pos="top", swipe=False)
    print("built", D)


if __name__ == "__main__":
    build()
