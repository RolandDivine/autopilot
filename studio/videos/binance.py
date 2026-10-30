"""YouTube long-form: The $6B Binance hack explained (Roland's own voice, ElevenLabs voice isolation). Facts on screen are
the verified ones (CoinDesk, Euronews, Cointelegraph, The Block; 30 Oct 2026), whatever the voice says."""
OUT = "long-binance-hack.mp4"


def chk(t, at, x=False):
    return f"<div class='chk' data-at='{at}'><i class='{'x' if x else ''}'>{'✕' if x else '✓'}</i><div>{t}</div></div>"


def chapter(n, t):
    return f"<div class='chap'><div class='n' data-at='0'>{n:02d}</div><div class='t' data-at='0.25'>{t}</div></div>"


def bar(name, year, w, lab, color="#3a3f4a", at=0.3):
    return (f"<div class='bar' data-at='{at}'><div class='n'>{name}<span>{year}</span></div>"
            f"<div class='t' data-w='{w}' data-at='{at}' style='background:{color}'><div class='v'>{lab}</div></div></div>")


S = []


def sc(a, b, img, html, tint=None):
    S.append({"a": a, "b": b, "img": img, "html": html, "tint": tint})


# ---------------------------------------------------------------- intro
sc(0.0, 4.6, "black-cube.jpg", "<div class='L' style='top:300px'><div class='k' data-at='0.1'>Overnight</div>"
   "<div class='h yel' data-count='6000000000' data-pre='$' data-at='0.2' data-dur='2.4'>$0</div>"
   "<div class='sub' data-at='2.8'>Gone.</div></div>")
sc(4.6, 11.0, "ice-server.jpg", "<div class='L'><div class='k' data-at='0.1'>The world's biggest crypto exchange</div>"
   "<div class='h' data-at='0.3'>Binance.</div><div class='h red' data-at='1.6'>In one night.</div></div>")
sc(11.0, 17.2, "circuit-lock.jpg", "<div class='L'><div class='h2' data-at='0.2'>They didn't break the code.</div>"
   "<div class='h yel pop' data-at='3.4' style='margin-top:40px'>They got one key.</div></div>")
sc(17.2, 21.8, "phone-glow.jpg", "<div class='L' style='top:320px'><div class='h' data-at='0.2'>Money on <span class='yel'>any</span> exchange?</div>"
   "<div class='sub' data-at='1.8'>This affects you.</div></div>")
sc(21.8, 28.9, "chrome-hourglass.jpg", "<div class='L'><div class='k' data-at='0.1'>In the next few minutes</div>"
   + chk("What actually happened", 0.4) + chk("Is your money safe?", 1.6) + chk("What to do today", 2.8) + "</div>")
sc(28.9, 35.7, "arrow-hourglass.png", "<div class='L' style='top:300px'><div class='k' data-at='0.1'>Your host</div>"
   "<div class='h2' data-at='0.3'>Roland Divine</div><div class='sub' data-at='0.9'>DeFi builder · smart contract auditor</div>"
   "<div class='row' data-at='3.0' style='border-color:#FFD84D;margin-top:40px'>Education, not financial advice.</div></div>")
# ---------------------------------------------------------------- 01 what happened
sc(35.7, 37.0, None, chapter(1, "What happened"))
sc(37.0, 39.0, "hourglass-half.jpg", "<div class='L'><div class='k' data-at='0'>Thursday night</div>"
   "<div class='h2' style='font-family:SpaceG' data-at='0.2' data-type='29 OCT 2026 · 20:24 UTC' data-dur='0.9'></div>"
   "<div class='sub' data-at='1.0'>Money starts leaving Binance's hot wallets.</div></div>")
sc(39.0, 42.4, "coin-siphon.jpg", "<div class='L'><div class='k' data-at='0'>On-chain · outflows</div>"
   "<div class='row' data-at='0.2'><b>−167,464 ETH</b> &nbsp;leaves wallet “Binance 14”</div>"
   "<div class='row' data-at='0.9'><b>−28,005 ETH</b> &nbsp;leaves wallet “Binance 16”</div>"
   "<div class='row' data-at='1.6'><b>→</b> forwarded to a new address ~15 min later</div>"
   "<div class='src' data-at='1.6'>Source: CoinDesk, 30 Oct 2026</div></div>")
sc(42.4, 44.7, "circuit-lock.jpg", "<div class='L'><div class='k' data-at='0'>Within hours</div><div class='h' data-at='0.1'>Binance confirms…</div>"
   "<div class='stamp' data-at='1.4' style='margin-top:40px'>HACKED</div></div>", tint="red")
sc(44.7, 47.8, "black-cube.jpg", "<div class='L' style='top:300px'><div class='k' data-at='0'>Total impact (estimate)</div>"
   "<div class='h yel' data-count='6300000000' data-pre='≈$' data-at='0.1' data-dur='2.0'>$0</div>"
   "<div class='sub' data-at='2.2'>The biggest crypto hack ever recorded.</div></div>")
sc(47.8, 56.1, "coin-collapse.jpg", "<div class='L' style='width:1250px'><div class='k' data-at='0'>Biggest crypto hacks ever</div>"
   + bar("Mt. Gox", "2014", 63, "$0.46B", at=0.2) + bar("Ronin", "2022", 85, "$0.62B", at=0.4)
   + bar("Bybit", "2025", 205, "$1.5B", "#FFD84D", at=0.6) + bar("Binance", "2026", 860, "≈ $6.3B", "#FF4D4D", at=1.0)
   + "<div class='src' data-at='2.5'>Value at the time of theft. Binance figure is an early estimate.</div></div>")
sc(56.1, 58.8, "arrow-hourglass.png", "<div class='L' style='top:250px'><div class='pop' data-at='0.3' style='font:800 360px/1 Jakarta;letter-spacing:-14px;color:#FFD84D'>4×</div>"
   "<div class='h2' data-at='0.8'>bigger than the old record.</div></div>")
sc(58.8, 63.6, "ice-server.jpg", "<div class='L'><div class='k' data-at='0'>Suspected</div><div class='h2' data-at='0.2'>North Korea-linked hackers</div>"
   "<div class='sub' data-at='1.2'>Investigators point to the TraderTraitor group.</div><div class='src' data-at='1.2'>Source: Cointelegraph, 30 Oct 2026</div></div>", tint="red")
sc(63.6, 69.2, "anchor-coin.jpg", "<div class='L'><div class='k' data-at='0'>Markets react</div>"
   "<div class='row' data-at='0.3'>Bitcoin &nbsp;<b>slides below $77,000</b></div><div class='row' data-at='1.3'>BNB &nbsp;<b>−7% in a day</b></div>"
   "<div class='src' data-at='1.3'>Sources: The Block, Cointelegraph</div></div>")
sc(69.2, 75.2, "glass-pen-coins.jpg", "<div class='L' style='top:300px'><div class='k' data-at='0'>Leveraged traders wiped out</div>"
   "<div class='h red' data-count='1.5' data-dec='1' data-pre='$' data-suf='B+' data-at='0.2' data-dur='1.6'>$0</div>"
   "<div class='sub' data-at='1.9'>in liquidations</div><div class='src' data-at='1.9'>Source: crypto.news</div></div>")
sc(75.2, 82.2, "hourglass-half.jpg", "<div class='L' style='top:320px'><div class='k' data-at='0.1'>Before you panic</div>"
   "<div class='h2' data-at='0.4'>Next: how <span class='yel'>one key</span><br>moved billions</div></div>")
# ---------------------------------------------------------------- 02 one key
sc(82.2, 85.2, None, chapter(2, "How one key<br>moved billions"))
sc(85.2, 98.7, "ice-server.jpg", "<div class='L' style='width:1100px'><div class='k' data-at='0'>Every exchange has two kinds of wallet</div>"
   "<div class='box' data-at='1.8'><div class='t'>❄️ Cold</div><div class='d'>Offline. Like a vault.</div></div>"
   "<div class='box' data-at='4.0'><div class='t'>🔥 Hot</div><div class='d'>Online. Pays out withdrawals fast.</div></div>"
   "<div class='h2 red pop' data-at='11.8' style='margin-top:50px'>Hot wallets = the target.</div></div>")
sc(98.7, 104.8, "glass-keys.jpg", "<div class='L'><div class='k' data-at='0'>According to early reports</div>"
   "<div class='h2' data-at='0.3'>The attacker got the <span class='yel'>signing key</span> to a Binance hot wallet.</div></div>")
sc(104.8, 117.5, "circuit-lock.jpg", "<div class='L' style='width:1150px'><div class='k' data-at='0'>Then</div>"
   "<div class='h2' style='font-size:62px' data-at='0.3'>A newer Ethereum feature lets a wallet hand control to software.</div>"
   "<div class='flow'><div class='node' data-at='3.0' style='left:0'>Hot wallet<small>Binance</small></div>"
   "<div class='line' data-at='4.2' style='left:330px;width:290px'></div>"
   "<div class='node' data-at='4.6' style='left:650px'>Software<small>EIP-7702</small></div></div></div>")
sc(117.5, 125.0, "coin-siphon.jpg", "<div class='L' style='width:1150px'><div class='k' data-at='0'>They turned it into a</div>"
   "<div class='h red pop' data-at='0.4'>Sweeper</div>"
   "<div class='flow'><div class='node' data-at='1.0' style='left:0'>Hot wallet<small>funds land here</small></div>"
   "<div class='line' data-at='1.4' style='left:330px;width:290px'></div>"
   "<div class='node' data-at='1.6' style='left:650px;border-color:#FF4D4D'>Attacker<small>new address</small></div>"
   "<div class='dot' data-at0='2.0' data-x0='320' data-x1='610' data-p='1.0'></div></div></div>")
sc(125.0, 132.0, "black-cube.jpg", "<div class='L'>" + chk("No code exploit", 0.3, True) + chk("No smart contract bug", 1.6, True)
   + "<div class='h yel pop' data-at='4.6' style='margin-top:50px'>One key.</div></div>")
sc(132.0, 150.6, "glass-house.jpg", "<div class='L'><div class='k' data-at='0'>The lesson for builders</div>"
   "<div class='h2' data-at='0.3'>Your security is only as strong as your <span class='yel'>key management.</span></div>"
   "<div class='sub' data-at='9.6'>You can audit every line of code. If one key controls the vault, that key is the whole game.</div></div>")
# ---------------------------------------------------------------- 03 is your money safe
sc(150.6, 153.7, None, chapter(3, "Is your money safe?"))
sc(153.7, 165.6, "jar-notes.jpg", "<div class='L'><div class='k' data-at='0'>What Binance says</div>"
   + chk("User funds are safe", 3.4) + chk("It will cover the losses", 6.5) + chk("Emergency fund (SAFU): ~$1B in bitcoin", 8.3)
   + "<div class='src' data-at='8.3'>Sources: Binance statements via CoinDesk, Euronews</div></div>")
sc(165.6, 170.3, "ice-server.jpg", "<div class='L'><div class='k' data-at='0'>For now</div>"
   "<div class='h2' data-at='0.2'>Deposits and withdrawals: <span class='red'>paused</span></div>"
   "<div class='sub' data-at='1.2'>While Binance locks things down and investigates.</div></div>")
sc(170.3, 180.5, "glass-pen-coins.jpg", "<div class='L' style='top:280px'><div class='k' data-at='0'>Frozen by Tether + Circle</div>"
   "<div class='h yel' data-count='2.4' data-dec='1' data-pre='$' data-suf='B+' data-at='0.2' data-dur='1.6'>$0</div>"
   "<div class='sub' data-at='5.5'>Good for victims. Also a reminder: a few companies can freeze crypto.</div></div>")
sc(180.5, 195.3, "phone-glow.jpg", "<div class='L'><div class='k' data-at='0'>If your money is on Binance</div>"
   + chk("Don't panic-sell at the bottom", 0.3) + chk("Don't act on rumours", 3.2) + chk("Wait for updates in the official app", 7.6) + "</div>")
# ---------------------------------------------------------------- 04 scam wave
sc(195.3, 197.6, None, chapter(4, "The scam wave"))
sc(197.6, 214.2, "glass-keys.jpg", "<div class='L' style='width:1000px'><div class='k' data-at='0'>Coming to your DMs</div>"
   "<div class='bub' data-at='2.5'><small>“BINANCE SUPPORT”</small>Binance compensation: claim your refund now 🎁<div class='fake' data-at='3.7'>FAKE</div></div>"
   "<div class='bub' data-at='6.2'><small>“SECURITY TEAM”</small>Your account is at risk. Verify now ⚠️<div class='fake' data-at='7.4'>FAKE</div></div>"
   "<div class='bub' data-at='9.3'><small>“BINANCE VIP”</small>Move your funds to this safe wallet 🔐<div class='fake' data-at='10.5'>FAKE</div></div></div>", tint="red")
sc(214.2, 237.9, "circuit-lock.jpg", "<div class='L'><div class='k' data-at='0'>The rule</div>"
   + chk("Binance won't DM you first", 0.5) + chk("No agent will ever ask for your password, 2FA code or seed phrase", 3.3)
   + chk("Updates only in the official app, or a site you type in yourself", 8.0) + "</div>")
sc(237.9, 242.8, "hourglass-half.jpg", "<div class='L' style='top:330px'><div class='h' data-at='0.2'>Rushing you?</div>"
   "<div class='h red pop' data-at='1.8'>Urgency is the scam.</div></div>", tint="red")
# ---------------------------------------------------------------- 05 exchange vs own wallet
sc(242.8, 246.6, None, chapter(5, "Exchange or your<br>own wallet?"))
sc(246.6, 257.0, "twin-keys.jpg", "<div class='L' style='top:320px'><div class='k' data-at='0.2'>Everyone's asking</div>"
   "<div class='h' data-at='0.5'>Where is my crypto <span class='yel'>actually safe?</span></div></div>")
sc(257.0, 269.6, "ice-server.jpg", "<div class='L'><div class='k' data-at='0'>On an exchange</div>"
   + chk("They hold the keys", 0.4) + chk("Easy, and big ones can cover losses", 2.6) + chk("Hacked or frozen? You wait", 5.4, True) + "</div>")
sc(269.6, 284.1, "glass-house.jpg", "<div class='L'><div class='k' data-at='0'>My take</div>"
   "<div class='h2' data-at='0.3'>Big exchanges are convenient, and they have backup funds.</div>"
   "<div class='sub' data-at='8.0'>But always know who holds your keys.</div></div>")
sc(284.1, 293.5, "twin-keys.jpg", "<div class='L' style='width:1100px'><div class='k' data-at='0'>The smart split</div>"
   "<div class='box' data-at='0.6'><div class='t'>📈 Trading</div><div class='d'>Small, active money on the exchange.</div></div>"
   "<div class='box' data-at='3.6' style='border-color:#3DDC97'><div class='t grn'>🔐 Savings</div><div class='d'>Large amounts in your own wallet.</div></div></div>")
sc(293.5, 298.4, "black-cube.jpg", "<div class='L' style='top:320px'><div class='k' data-at='0'>Crypto safety, explained straight</div>"
   "<div class='h yel pop' data-at='0.4'>Subscribe</div><div class='sub' data-at='1.2'>Checklist pinned in the comments.</div></div>")

CAPS = [
    (0.0, 4.6, "$6 billion. Gone."),
    (4.6, 11.0, "From the world's biggest exchange, in one night."),
    (11.0, 17.2, "They didn't break the code. They got one key."),
    (17.2, 21.8, "If your money is on any exchange, this affects you."),
    (21.8, 28.9, "What happened, is your money safe, and what to do."),
    (28.9, 35.7, "Education, not financial advice. Let's get started."),
    (37.0, 42.4, "Money started leaving Binance. Fast. Within hours."),
    (42.4, 44.7, "Binance confirmed it had been hacked."),
    (44.7, 47.8, "Total impact: around $6 billion."),
    (47.8, 50.2, "The biggest hack in the industry."),
    (50.2, 56.1, "The previous record: Bybit, 2025. About $1.5 billion."),
    (56.1, 58.8, "This one is roughly 4 times bigger."),
    (58.8, 63.6, "North Korea-linked hackers are suspected."),
    (63.6, 69.2, "Bitcoin and BNB dropped fast."),
    (69.2, 75.2, "Billions in leveraged trades were wiped out."),
    (75.2, 82.2, "Before you panic, the next part matters more."),
    (85.2, 92.9, "Cold wallets are offline. Hot wallets are online."),
    (92.9, 98.7, "Hot wallets are convenient. They're also the target."),
    (98.7, 104.8, "The attacker got the signing key to a hot wallet."),
    (104.8, 117.5, "A newer Ethereum feature lets a wallet hand control to software."),
    (117.5, 125.0, "They turned it into a sweeper. Everything got forwarded."),
    (125.0, 132.0, "No exploit. No bug. One key."),
    (132.0, 141.7, "Your security is only as strong as your key management."),
    (141.7, 150.6, "Audit every line of code. One key can still decide everything."),
    (153.7, 165.6, "Binance says user funds are safe and it will cover the losses."),
    (165.6, 170.3, "Deposits and withdrawals are paused for now."),
    (170.3, 180.5, "Tether and Circle froze over $2.4 billion."),
    (180.5, 195.3, "Don't panic-sell. Don't act on rumours. Wait for official updates."),
    (197.6, 214.2, "Compensation, verify now, move your funds: all fake."),
    (214.2, 228.0, "Binance won't DM you first. No agent asks for your seed phrase."),
    (228.0, 237.9, "Updates come in the official app, or a site you type yourself."),
    (237.9, 242.8, "If a message makes you rush, stop."),
    (246.6, 257.0, "Where is my crypto actually safe?"),
    (257.0, 269.6, "On an exchange, they hold the keys. Hacked? You wait."),
    (269.6, 284.1, "Exchanges are convenient. Know who holds your keys."),
    (284.1, 293.5, "Trade on the exchange. Store large amounts in your own wallet."),
    (293.5, 298.4, "Thanks for watching. See you in the next one."),
]

SPEC = {"audio": "/home/claude/money_audio/roland-binance-iso.wav", "t0": 0.0, "t1": 298.4,
        "label": "THE $6B BINANCE HACK", "scenes": S, "captions": CAPS}
