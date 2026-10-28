"""Long-form YouTube videos (16:9). Voice: Oluwadamilare (ElevenLabs). Captions are uploaded to YouTube, not burned in.

    python studio/longform.py revoke [preview times...]
"""
import asyncio
import sys
from pathlib import Path

import viral

ROOT = Path(__file__).resolve().parent.parent
BRAND = "<div class='brand'>Roland Divine · <b>Crypto Safety</b></div>"
CSS = """
.card{left:150px;right:150px;top:150px}
.panel{padding:50px 60px}
.check{font-size:52px!important}
.card .mid{font-size:72px}
.chap{font:800 210px/1 Jakarta;color:#FFD84D;letter-spacing:-8px}
.ct{font:800 84px/1.05 Jakarta;letter-spacing:-2px;margin-top:10px}
.row{display:flex;gap:26px;margin-top:28px;align-items:stretch}
.box2{flex:1;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:28px;padding:30px 34px}
.box2 b{display:block;font:800 56px Jakarta;margin-bottom:10px}
.box2 span{font:600 40px/1.35 Jakarta;color:rgba(255,255,255,.85)}
.pill{display:inline-block;font:700 44px Jakarta;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);
 border-radius:999px;padding:12px 30px;margin:10px 12px 0 0}
.pill.y{background:#FFD84D;color:#07080B;border:0}
.tbl{width:100%;border-collapse:collapse;margin-top:24px;font:700 48px Jakarta}
.tbl th{font:700 28px Jakarta;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.6);text-align:left;padding:0 0 14px}
.tbl td{padding:20px 0;border-top:1px solid rgba(255,255,255,.12)}
.code{font:600 40px/1.5 monospace;background:#000;border-radius:24px;padding:30px 36px;margin-top:24px;border:1px solid rgba(255,216,77,.35)}
.arrow{font:800 70px Jakarta;color:#FFD84D;align-self:center}
"""


def chap(n, title):
    return f"<div class='kick'>Chapter</div><div class='chap'>0{n}</div><div class='ct'>{title}</div>"


def boxes(*bs):
    return "<div class='row'>" + "".join(f"<div class='box2'><b>{t}</b><span>{d}</span></div>" for t, d in bs) + "</div>"


def rehook(nxt, why=""):
    """Re-hook card (Roland, 28 Oct 2026 hooks research): show it every 2-3 minutes, right BEFORE a section starts.
    Most mid-video drop-off happens between sections; a tease of what's next gives people a reason to stay.
    e.g. rehook("The mistake that cost one person <span class='red'>$6.5M</span>", "in the next 60 seconds")"""
    return (f"<div class='kick'>Up next</div><div class='big' style='font-size:96px;letter-spacing:-2px'>{nxt}</div>"
            + (f"<div class='mid' style='margin-top:22px;font-size:56px'>{why}</div>" if why else ""))


def revoke_spec():
    A = ROOT / "assets" / "viral" / "howto-revoke"

    def timeline(at, dur):
        H = "html"
        bg = ROOT / "assets" / "market" / "bg-land.jpg"
        bgs = [(-1, 22.3, A / "drain.png"), (22.3, dur + 1, bg)]
        c = [
            (-1, 7.6, "<div class='kick'>Crypto safety · how to</div><div class='big' style='font-size:112px;letter-spacing:-3px'>Most drained wallets<br>"
             "<span class='yel'>never leak a seed phrase.</span></div><div class='mid' style='margin-top:24px'>The owner signs the theft. One click.</div>"),
            (7.6, 14.7, "<div class='kick'>By the end of this video</div><div class='mid' style='font-size:76px'>You'll see <span class='yel'>who can spend<br>your tokens</span> right now</div>"
             "<div class='mid' style='margin-top:24px;font-size:60px'>and cut them off in <span class='grn'>~2 minutes.</span></div>"),
            (14.7, 22.3, "<div class='kick'>Your host</div><div class='mid' style='font-size:90px'>Roland Divine</div>"
             "<div class='sm' style='margin-top:18px;font-size:42px'>DeFi builder · smart contract auditor<br>This is the first check I run on any wallet.</div>"),
            (22.3, 36.6, "<div class='kick'>Before we start</div><div class='mid'>Education, <span class='yel'>not financial advice.</span></div>"
             "<div class='sm' style='margin-top:26px;font-size:40px'>Works on Ethereum and chains like it:</div>"
             + "".join(f"<span class='pill'>{x}</span>" for x in ("Ethereum", "BNB Chain", "Base", "Arbitrum", "Polygon"))),
            (36.6, 40.1, chap(1, "What an approval<br>actually is")),
            (40.1, 52.3, "<div class='kick'>Example: a swap on Uniswap</div><div class='row'>"
             "<div class='box2'><b>You</b><span>want to swap a token</span></div><div class='arrow'>→</div>"
             "<div class='box2'><b class='yel'>Approve</b><span>wallet asks for permission</span></div><div class='arrow'>→</div>"
             "<div class='box2'><b>Contract</b><span>can now move that token</span></div></div>"),
            (52.3, 61.3, "<div class='kick'>Written on the blockchain</div><div class='mid'>What an approval says</div>"
             "<div class='code'>This contract may spend <span class='yel'>[TOKEN]</span><br>from my wallet, up to <span class='yel'>[AMOUNT]</span>.</div>"),
            (61.3, 67.7, None),
            (67.7, 76.6, None),
            (76.6, 84.9, "<div class='kick'>The risk</div><div class='mid' style='font-size:74px'>If that contract is <span class='red'>hacked</span>,<br>or was <span class='red'>malicious</span> from the start…</div>"
             "<div class='mid' style='margin-top:26px;font-size:58px'>it can move <span class='yel'>every token you approved.</span><br>No password needed.</div>"),
            (84.9, 89.1, chap(2, "How drainers<br>use this against you")),
            (89.1, 101.3, "<div class='kick'>A wallet drainer is a fake website</div><div class='mid'>It looks like…</div>"
             + "".join(f"<span class='pill'>{x}</span>" for x in ("a free airdrop", "a new mint", "a copy of a popular app", "a link in a reply on X or Telegram"))),
            (101.3, 105.6, "<div class='kick'>Then</div><div class='mid' style='font-size:90px'>Connect wallet → <span class='red'>Sign</span></div>"
             "<div class='sm' style='margin-top:20px;font-size:42px'>That signature is the trap.</div>"),
            (105.6, 118.1, "<div class='kick'>The 3 traps</div>" + boxes(("approve", "an unlimited allowance to their contract"),
                                                                     ("setApprovalForAll", "hands over a whole NFT collection"),
                                                                     ("permit", "an off-chain signature (next)"))),
            (118.1, 132.0, "<div class='kick'>Why permit works so well</div><div class='mid' style='font-size:80px'>Permit = an <span class='yel'>off-chain signature</span></div>"
             + boxes(("No gas", "so it doesn't feel like money moving"), ("No transaction", "so it doesn't look dangerous"),
                     ("They submit it", "later, and move your tokens"))),
            (132.0, 144.0, None),
            (144.0, 149.3, None),
            (149.3, 160.8, None),
            (160.8, 164.3, chap(3, "Check who can spend<br>your tokens right now")),
            (164.3, 176.0, "<div class='kick'>Free · no wallet connection needed to look</div><div class='mid'>3 steps</div>"
             + boxes(("1. Open revoke.cash", "type it yourself, don't click a link"), ("2. Paste your address", "search bar at the top"),
                     ("3. Pick the network", "Ethereum, Base, BNB…"))),
            (176.0, 184.5, "<div class='kick'>What you'll see (example)</div><table class='tbl'><tr><th>Asset</th><th>Spender</th><th>Allowance</th></tr>"
             "<tr><td>USDT</td><td>0x7a3…f19 (unknown)</td><td class='red'>Unlimited</td></tr>"
             "<tr><td>USDC</td><td>Uniswap</td><td class='red'>Unlimited</td></tr>"
             "<tr><td>WETH</td><td>App used once, 2024</td><td>50</td></tr></table>"),
            (184.5, 198.3, None),
            (198.3, 212.4, "<div class='kick'>Prefer a block explorer?</div><div class='mid' style='font-size:76px'>Etherscan <span class='yel'>Token Approval Checker</span></div>"
             "<div class='sm' style='margin-top:20px;font-size:42px'>Free. BscScan and the other explorers have their own.<br>Same idea: paste your address, read the list.</div>"),
            (212.4, 219.6, "<div class='kick'>Do this on every network you've used</div><div class='mid'>Approvals <span class='red'>don't carry across</span> chains</div>"
             + "".join(f"<span class='pill'>{x}</span>" for x in ("Ethereum", "Base", "Arbitrum", "BNB Chain", "Polygon"))),
            (219.6, 222.8, chap(4, "Revoke what<br>you don't use")),
            (222.8, 236.9, "<div class='kick'>On revoke.cash</div>" + boxes(("1. Connect", "the wallet that owns the approvals"), ("2. Revoke", "the button on each row"),
                                                                       ("3. Confirm", "allowance goes back to <b class='grn' style='display:inline;font-size:inherit'>0</b>"))),
            (236.9, 249.2, "<div class='kick'>It's a real transaction, so it costs gas</div>" + boxes(("Base · Arbitrum", "usually cents"),
                                                                                                 ("Ethereum mainnet", "can be more: start with the dangerous ones"))),
            (249.2, 262.2, None),
            (262.2, 269.0, "<div class='kick'>The safest habit</div><div class='mid' style='font-size:80px'>Revoke it anyway.<br><span class='yel'>Approve again next time.</span></div>"),
            (269.0, 286.9, "<div class='kick'>One important limit</div><div class='mid' style='font-size:76px'>Revoking stops the <span class='grn'>next</span> theft,<br>not the <span class='red'>last</span> one.</div>"
             "<div class='sm' style='margin-top:24px;font-size:42px'>Think you've been drained? Move what's left<br>to a <b class='yel'>brand-new wallet</b> straight away.</div>"),
            (286.9, 290.6, chap(5, "Read the pop-up<br>before you click")),
            (290.6, 297.1, None),
            (297.1, 309.2, "<div class='kick'>Question 1 · What type of request?</div>" + boxes(("Connect", "<span class='grn'>harmless on its own</span>"),
                                                                                            ("approve · setApprovalForAll · permit · increaseAllowance", "<span class='red'>a spending permission</span>"))),
            (309.2, 320.6, "<div class='kick'>Question 2 · Who is the spender?</div><div class='mid' style='font-size:74px'>Minting an NFT, but it wants<br>your <span class='red'>stablecoins?</span></div>"
             "<div class='big red' style='font-size:150px;margin-top:10px'>STOP.</div>"),
            (320.6, 327.8, "<div class='kick'>Question 3 · How much?</div><div class='mid' style='font-size:76px'>Swapping $100? Approve <span class='grn'>$100</span>,<br>not <span class='red'>unlimited.</span></div>"
             "<div class='sm' style='margin-top:20px;font-size:40px'>MetaMask lets you edit the spending cap.</div>"),
            (327.8, 335.7, "<div class='kick'>Can't tell what it does?</div><div class='big' style='font-size:150px'>Reject.</div>"
             "<div class='mid' style='margin-top:18px;font-size:56px'>A real app will ask again. <span class='yel'>A scam hopes you won't look.</span></div>"),
            (335.7, 339.1, chap(6, "Habits that make<br>this boring")),
            (339.1, 352.3, "<div class='kick'>Keep two wallets</div>" + boxes(("🔥 Hot wallet", "new apps, airdrops, mints.<br>Only what you can afford to lose."),
                                                                         ("🔒 Vault wallet", "ideally a hardware wallet.<br>Only talks to a few apps you trust."))),
            (352.3, 361.0, "<div class='kick'>Habit 2</div><div class='mid' style='font-size:80px'>Open apps from your <span class='yel'>bookmarks</span> only</div>"
             "<div class='sm' style='margin-top:22px;font-size:42px'>Never from a DM, a reply, or a sponsored search result.</div>"),
            (361.0, 370.3, "<div class='kick'>Habit 3 · put it in your calendar</div><div class='mid' style='font-size:84px'>Once a month:<br><span class='yel'>revoke.cash → paste → clean up</span></div>"
             "<div class='sm' style='margin-top:20px;font-size:42px'>Two minutes.</div>"),
            (370.3, 387.0, None),
            (387.0, 396.8, "<div class='kick'>Next video</div><div class='mid' style='font-size:84px'>Set up a hardware wallet <span class='yel'>properly</span></div>"
             "<div class='sm' style='margin-top:20px;font-size:42px'>…including the one mistake that makes it useless.<br>Full checklist pinned in the comments.</div>"),
            (396.8, dur + 1, "<div class='kick'>Education, not financial advice</div><div class='big yel' style='font-size:120px'>Subscribe</div>"
             "<div class='mid' style='margin-top:16px;font-size:56px'>New crypto safety how-to every week</div>"),
        ]
        special = {
            61.3: {"kind": "stat", "kick": "The problem", "value": "∞", "cls": "red", "label": "Many apps ask for an unlimited amount", "sub": "to save you fees on future swaps"},
            67.7: {"kind": "checks", "kick": "And it doesn't expire", "title": "It stays live…",
                   "items": [{"t": "after you close the app", "d": .4}, {"t": "after you disconnect your wallet", "d": 2.6}, {"t": "even years later", "d": 5.0}]},
            132.0: {"kind": "stat", "kick": "Wallet drainer phishing, 2025", "value": "$83.85M", "cls": "red", "label": "stolen from 106,106 victims", "src": "Scam Sniffer, 2025 report"},
            144.0: {"kind": "stat", "kick": "Biggest single theft of 2025", "value": "$6.5M", "cls": "red", "label": "from one permit signature", "src": "Scam Sniffer"},
            149.3: {"kind": "bars", "kick": "Losses are down, the method isn't", "title": "Drainer losses",
                    "max": 494, "bars": [{"t": "$494M", "v": 494, "q": "2024"}, {"t": "$83.85M", "v": 83.85, "q": "2025"}], "src": "Scam Sniffer"},
            184.5: {"kind": "checks", "kick": "Look for 3 things", "title": "Red flags",
                    "items": [{"t": "Anything that says <span class='red'>Unlimited</span>", "d": 1.5}, {"t": "A spender you don't recognise", "d": 4.8},
                              {"t": "Apps you used once, months ago", "d": 7.9}]},
            249.2: {"kind": "checks", "kick": "The order I use", "title": "Revoke first…",
                    "items": [{"t": "1. Unlimited → anything I don't recognise", "d": 1.8}, {"t": "2. Unlimited → apps I no longer use", "d": 5.5},
                              {"t": "3. Everything older than a few months", "d": 9.0}]},
            290.6: {"kind": "stat", "kick": "Where most money is lost", "value": "½ second", "cls": "yel", "label": "between the pop-up and the click", "sub": "Slow down. Read 3 things."},
            370.3: {"kind": "checks", "kick": "The whole video in one breath", "title": "Your checklist",
                    "items": [{"t": "Approvals let apps spend your tokens", "d": 2.8}, {"t": "Drainers trick you into signing them", "d": 5.4},
                              {"t": "Check on revoke.cash, revoke what you don't use", "d": 7.9}, {"t": "Read every pop-up", "d": 12.6},
                              {"t": "Savings in a separate wallet", "d": 14.5}]},
        }
        cards = []
        for a, b, html in c:
            card = dict(special[a]) if html is None else {"kind": H, "html": html}
            card.update({"a": a - .05, "b": b - .1})
            cards.append(card)
        return bgs, cards

    s = viral.std("howto-revoke", timeline, host=False)
    s.update({"land": True, "brand": BRAND, "nocap": True, "css": CSS})
    return s


SPECS = {"revoke": revoke_spec}

if __name__ == "__main__":
    name = sys.argv[1]
    pv = [float(x) for x in sys.argv[2:]]
    out = ROOT / "assets" / "youtube" / f"long-{name}.mp4"
    print(asyncio.run(viral.render(SPECS[name](), out, pv or None)))
