"""Roland's 150-day education plan. Day 1 = Mon 12 Oct 2026, Day 150 = Wed 10 Mar 2027.
Daily: 1 news post (morning) + 2 lessons rotating through 3 tracks -> 100 lessons per track.
Rotation by (day-1) % 3:  0 -> Crypto + AI,  1 -> AI + Builders,  2 -> Builders + Crypto.
Every 20th day (20, 40 ... 140) the news slot becomes a Klaerus spotlight.
"""
import datetime

START = datetime.date(2026, 10, 12)

CRYPTO = [
 # Phase 1: Foundations
 "What money is, and why crypto exists", "What a blockchain is, in plain words", "Bitcoin, explained for beginners",
 "Ethereum: the programmable blockchain", "What a wallet really holds: keys, not coins", "Seed phrases: the 12 words that are your money",
 "Custodial vs self-custody wallets", "Setting up your first wallet safely", "Public address vs private key",
 "What gas (transaction fees) is", "Reading a block explorer", "Exchanges: centralised vs decentralised",
 "KYC: why exchanges ask for your ID", "Buying your first crypto: a safety checklist", "P2P trading: how it works and its risks",
 "What stablecoins are", "How stablecoins hold $1: fiat-, crypto- and algorithm-backed", "USDT vs USDC: what is different",
 "Using stablecoins to save and send money", "Recap: your crypto starter kit",
 # Phase 2: Safety and how tokens work
 "The 7 most common crypto scams", "Phishing and fake websites", "Token approvals: the permission most people forget",
 "Hardware wallets: when you need one", "Storing your seed phrase backup", "How Ponzi schemes promise 'guaranteed' returns",
 "Rug pulls explained", "Pig-butchering and romance scams", "Fake support accounts", "Your security checklist",
 "Market cap vs price", "Token supply: circulating, total and max", "Tokenomics: who gets tokens and when",
 "Unlocks and vesting", "Layer 1s vs Layer 2s", "What rollups like Arbitrum do", "Bridges, and why they get hacked",
 "Gas on different chains", "What a smart contract is", "Recap: reading a token like an analyst",
 # Phase 3: Investing principles (frameworks, never picks)
 "Investing vs trading vs gambling", "Time horizon and why it matters", "Risk: only what you can afford to lose",
 "Position sizing basics", "Dollar-cost averaging explained", "Diversification in crypto",
 "Volatility: why prices swing so much", "Market cycles: bull and bear", "The bitcoin halving explained",
 "How to research a project: a checklist", "Reading a whitepaper", "Team, backers and red flags",
 "On-chain data basics", "Why most altcoins go to zero", "FOMO and FUD: emotions that cost money",
 "Taking profit: having a plan", "Keeping records for tax", "Crypto rules in Nigeria: what to know now",
 "Spot ETFs: how traditional finance holds crypto", "Recap: write your own investing rules",
 # Phase 4: DeFi and markets
 "What DeFi is", "DEXs and AMMs: how swaps work", "Slippage and price impact", "Liquidity pools and LP tokens",
 "Impermanent loss", "Lending and borrowing on-chain", "Collateral and liquidation", "Yield: where it really comes from",
 "APY traps", "Staking explained", "Liquid staking", "Oracles: how blockchains get prices", "Stablecoin depegs",
 "Real-world assets and tokenisation", "Perpetual futures explained", "Leverage: why most traders get liquidated",
 "Funding rates", "Options basics", "Prediction markets: prices as probabilities", "Recap: the DeFi risk map",
 # Phase 5: Mastery
 "Reading a smart contract audit", "How hacks happen: common exploit types", "Multisig wallets",
 "Smart wallets and account abstraction", "NFTs beyond pictures", "DAOs and governance", "MEV explained",
 "Privacy in crypto", "How different countries regulate crypto", "Event contracts: the swap-vs-bet debate",
 "A simple portfolio framework (no picks)", "Rebalancing", "Tracking a portfolio",
 "Stablecoins for business payments", "Earning in crypto: jobs and skills", "Contributing to crypto communities",
 "Spotting narratives without chasing them", "Mistakes I made building in crypto", "Your crypto playbook",
 "Graduation: what you can do now",
]

AI = [
 # Phase 1: Basics
 "What AI is (and is not)", "How AI chat assistants work, simply", "What a 'model' is",
 "What AI is good and bad at", "Hallucinations: why AI makes things up", "Your first useful prompt",
 "Prompt structure: role, task, context, format", "Giving examples in your prompt", "Asking AI to ask you questions first",
 "Iterating: the second prompt matters more", "Summarising long documents", "Writing emails with AI",
 "Learning any topic fast with AI", "Research with AI: always check sources", "Privacy: what not to paste into AI",
 "Free vs paid AI tools", "Comparing the main AI assistants", "Talking to AI: voice and image input",
 "AI on your phone", "Recap: 10 prompts worth saving",
 # Phase 2: Productivity
 "Planning your week with AI", "Turning meeting notes into actions", "AI for spreadsheets and formulas",
 "AI for slides and presentations", "AI for drafts, not final copy", "Editing your own writing with AI",
 "Translation and local languages", "Reading contracts with AI (and its limits)", "Budgeting with AI",
 "Building a personal prompt library", "Custom instructions and memory", "Projects and knowledge files",
 "Email triage with AI", "AI for social media content", "AI image tools: what is possible",
 "AI for video and audio", "Spotting AI-generated content", "AI and copyright basics",
 "Time audit: where AI saves you hours", "Recap: your AI productivity stack",
 # Phase 3: Jobs and careers
 "Which jobs AI changes most", "Skills that become more valuable", "Rewriting your CV with AI, honestly",
 "Tailoring applications to each job post", "Cover letters that don't sound like AI", "Your LinkedIn profile with AI",
 "Finding remote work", "Mock interviews with AI", "Answering 'how do you use AI?' in interviews",
 "Building a portfolio project with AI", "Freelancing with AI skills", "Pricing AI-assisted services",
 "AI skills employers ask for", "Learning to code with AI", "Data analysis for non-coders",
 "AI in customer support roles", "AI in marketing roles", "AI in operations and admin roles",
 "Preparing a salary negotiation with AI", "Recap: your AI job plan",
 # Phase 4: Automation and building
 "Automation basics: triggers and actions", "No-code automation tools", "Connecting AI to your apps",
 "AI agents explained", "Scheduled AI tasks", "A simple chatbot for a small business",
 "AI customer service for small businesses", "APIs: the basics", "What AI costs: tokens and pricing",
 "Judging AI output quality", "A knowledge-base assistant", "Automating spreadsheets",
 "AI content pipelines", "Guardrails: checking AI before it acts", "AI in crypto security audits",
 "AI in trading: hype vs reality", "AI and data-privacy laws", "Open vs closed models",
 "Running models on your own computer", "Recap: build your first automation",
 # Phase 5: Mastery
 "Thinking with AI: decision support", "AI for strategy work", "A 'second brain' with AI",
 "Teaching AI your writing style", "Multi-step AI workflows", "AI for founders: building faster",
 "AI for product design", "AI for customer research", "Bias and fairness in AI", "AI risks to watch",
 "Where AI is heading", "AI regulation basics", "AI opportunities in Africa", "Teaching others to use AI",
 "Measuring your AI productivity gains", "Keeping your own skills sharp", "Building in public with AI",
 "My personal AI workflow", "Your AI playbook", "Graduation: what you can do now",
]

BUILDERS = [
 # Phase 1: Find the problem
 "Why most products never launch", "The 150-day build challenge: how it works", "Problems vs ideas",
 "Finding problems you are close to", "Writing a problem statement", "Who exactly has this problem?",
 "Talk to users before you build", "How to run a customer interview", "Questions that don't lie",
 "Recording what you learn", "Is the problem painful enough?", "Mapping existing alternatives",
 "Picking one problem", "Your one-sentence value proposition", "Building in public: why and how",
 "Founder time management", "Solo vs co-founder", "Skills to learn, borrow or hire",
 "A tool stack for solo builders", "Recap: your problem brief",
 # Phase 2: Validate
 "What validation really means", "Smoke tests and landing pages", "Writing a landing page",
 "Collecting a waitlist", "Pre-selling before you build", "Pricing from day one", "Competitive analysis",
 "Positioning", "Defining your MVP", "Cutting scope", "User stories", "Sketching your product",
 "Wireframes with free tools", "No-code vs code", "Choosing your tech stack", "Building faster with AI",
 "Setting milestones", "Accountability: weekly updates", "Common validation mistakes",
 "Recap: your validated MVP plan",
 # Phase 3: Build and beta
 "Setting up your project", "Build the core feature first", "Design basics for non-designers",
 "Onboarding: the first 60 seconds", "Accounts and sign-in", "Taking payments in Nigeria and abroad",
 "Data and privacy basics", "Security basics for builders", "Analytics: what to measure",
 "Testing with real users", "Fixing what users actually hit", "Shipping every week",
 "Handling burnout while building", "Documentation basics", "Customer support from day one",
 "Feedback loops", "Running a beta", "Beta metrics", "Iterating on feedback", "Recap: beta checklist",
 "Naming and branding basics", "Writing product copy", "Making a demo video", "Building an email list",
 "Content marketing for products", "Community before launch", "Partnerships",
 "Registering your business (CAC and beyond)", "Terms and privacy policy", "Recap: launch-ready checklist",
 # Phase 4: Launch
 "Planning your launch", "Choosing launch channels", "Launch platforms like Product Hunt",
 "Your launch-day timeline", "Launch posts that work", "Asking your network for help",
 "LAUNCH DAY: ship it and show us", "Post-launch review", "Your first 10 customers", "Activation",
 "Retention", "Talking to users who left", "Iterating on pricing", "Sales basics for founders",
 "Respectful cold outreach", "Referrals", "SEO basics", "Social media for your product",
 "A simple metrics dashboard", "Recap: your first 30 days after launch",
 # Phase 5: Grow
 "Unit economics basics", "When to raise money, and when not to", "Bootstrapping", "Pitch basics",
 "Hiring your first help", "Systems and delegation", "Founder mental health",
 "Lessons from my own builds", "Your next 150 days", "Graduation: show what you launched",
]

assert len(CRYPTO) == len(AI) == len(BUILDERS) == 100, (len(CRYPTO), len(AI), len(BUILDERS))

TRACKS = {"Crypto": (CRYPTO, {0, 2}), "AI": (AI, {0, 1}), "Builders": (BUILDERS, {1, 2})}
PAIR = {0: ("Crypto", "AI"), 1: ("AI", "Builders"), 2: ("Builders", "Crypto")}


def lesson_no(track, day):
    s = TRACKS[track][1]
    return sum(1 for k in range(1, day + 1) if (k - 1) % 3 in s)


def plan(day):
    a, b = PAIR[(day - 1) % 3]
    date = START + datetime.timedelta(days=day - 1)
    out = {"day": day, "date": date, "slot1": "Klaerus spotlight" if day % 20 == 0 else "News", "lessons": []}
    for t in (a, b):
        n = lesson_no(t, day)
        out["lessons"].append((t, n, TRACKS[t][0][n - 1]))
    return out


if __name__ == "__main__":
    for d in (1, 2, 3, 20, 115, 150):
        print(plan(d))
