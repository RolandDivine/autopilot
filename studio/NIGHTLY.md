# Nightly build (runs in Roland's Claude conversation at 7:10 PM Lagos)

Platforms: LinkedIn (RolandDivine2) and Instagram (@defi_ring_master) both post automatically from the queue (`instagram_autopost` is true). X is off: always set `"x": {"enabled": false}`. Never post anything directly.

> **Read `studio/STORY_GUIDE.md` first (Roland, 24 Oct 2026).** Every piece is designed with ABC (Act, Believe, Care) and delivered with STORY (Stage, Tension, Opportunity, Resolution, Yes), selling the audience's real desire. Run its checklist before anything ships.

## POSTING CHANGE (Roland, 29 Oct 2026: "Stop letting GitHub do that")
GitHub cron is OFF for post.yml and videos.yml (commit 4aca114). Posting runs are now send_later reminders in Roland's main
Claude session (07, 08, 10, 11, 13, 16, 17, 20 UTC; the Sat 31 Oct 20:00 run books the next 3 days). The nightly build does NOT
book, cancel or edit those reminders; it only reconciles the logs and reports any gap. Step 9 below is out of date on this point.

## STATUS (28 Oct 2026, 19:40 Lagos nightly): Wed 28 Oct – Mon 2 Nov are fully built and pushed
Do NOT rebuild queue/2026-10-29..2026-11-02 or queue/vo/posts-2026-10-29..2026-11-02.json (built by studio/days/week44.py and
studio/days/week45.py). Next nightly: reconcile, then build Tue 3 Nov (+ Wed 4). Reels left in the Fish ELITE bank for the 12:00 slot,
in order: ex15 passkeys, ex07 gas fees, ex06 Mt Gox, ex08 ETF, ex19 inflation, ex11 hallucination, ex12 LLM, ex13 CrowdStrike,
ex16 business, howto-* clips. Kobo Season 2 is finished (kobo15 on Sun 1 Nov), so the 18:00 video slot is free from Mon 2 Nov.
Carousels: Tue 3 Nov can be the LinkedIn PDF day (reuse a week-45 Instagram carousel; none built yet). **Never skip (Roland, 28 Oct 2026: "don't skip anything... push as much as possible"):** slots and stories now post up to
24 h late (config slot_grace_minutes / story_grace_minutes = 1440) and videos.yml also retries yesterday's file. Every nightly:
if anything due today is still missing from log/posted.jsonl or log/videos.jsonl, dispatch post.yml (dry_run false) or
videos.yml right away. Instagram can answer HTTP 500 and still publish: check recent media before re-posting.

## Content direction (Roland, 15 Oct 2026: full rebuild after a week of near-zero reach)
Old approach is retired: no curriculum lessons, no basic explainers (what is a wallet, how to use a wallet), no daily news card, no terminal-style PDFs on LinkedIn. Those got 2–31 reach per post.
- **Topics come from tonight's search demand, nothing else.** Categories: AI, crypto, business, tech infrastructure (data centers, cloud, chips, cybersecurity). Audience is worldwide English speakers.
- **Every post makes someone's life better:** a how-to, a where-to, a tool they can use tonight, a myth corrected with real numbers. Practical and specific, real product names, real steps, what it costs, the catch.
- **Psychology on every post:** a hook that opens a curiosity gap or challenges a belief ("Does every ChatGPT chat drink a bottle of water?"), "you" language, specific numbers, and a clear payoff on the last slide. On LinkedIn end with one specific question people can answer from their own experience (never "thoughts?" or "agree?").
- Build-in-public only when there is something real and new. Klærus stays on hold (below).

## Instagram rules (Roland, 21 Oct 2026, after the Instagram review: 0 shares and 1 save in 39 posts, reach per post falling as volume rose)
- **Two lanes on Instagram only:** crypto safety & money, and AI tools. Off-lane topics (small-business how-tos, Google Maps, careers) go to LinkedIn only.
- **Per day on Instagram: 1 carousel + 1 Reel + 3–4 stories.** The 0800 slot is the Instagram carousel; set `instagram.enabled = false` on 1300 and 1900 (they stay on LinkedIn). The 9 PM "Do you know…?" teaser is a **story only** (2100.json has Instagram off; keep s2100 in stories.json).
- **Videos:** one Reel a day on Instagram (the explainer, or Kobo on days with no explainer). The second video gets `"instagram_reel": false` in posts-<date>.json: it still goes to LinkedIn, Stories (auto-split) and YouTube if crypto.
- **First seconds = ONE clean text hook (upgraded 28 Oct 2026):** every Reel opens on its hook, never on "Hey, Kobo here". After rendering, run `python3 studio/hookcut.py <in.mp4> <in>-hook.mp4 <seconds where the first real sentence starts> "Hook line|payoff line"` and post the -hook file. For the first 2 s the frame is blurred so only the hook shows (white line + yellow payoff line, auto-sized). ≤7 words. Write 3 versions per Reel in `queue/hooks.json` (style tags: stake, mistake, number, myth, warning, curiosity, nigeria), cut the strongest, and make each `reel_caption` start with that entry's `caption_start`. Rotate styles; the Sunday research file's `hook_scoreboard` ranks styles by average watch time: after 3–4 weeks, drop the weak styles.
- **Search-first captions:** the first sentence starts with the words people search ("How to revoke token approvals…", "Bitcoin halving explained:"), then the hook. 3–5 hashtags.
- **Alt text:** every Instagram image gets alt text (`instagram.alt` = one line per image: what it shows + the slide's words). ig_client sends it and falls back if Instagram rejects it.
- **Real Roland beats everything:** his voice-note stories (no camera needed) become Reels with captions; build one whenever he sends a recording.

## Reel formula (data, 24 Oct 2026: Roland asked "6 views, how? analyze it, retarget")
Evidence: address poisoning Reel = 1,410 views, 1,182 reach, 19 saves, 9 shares, **16.3 s average watch**. Every other Reel = 6–34 views with **3–6 s average watch** (people swipe in the first 3 seconds). Carousels = 1–7 reach each.
- **Topic formula that won:** a money-loss threat the viewer didn't know about + a surprising mechanism ("needs zero clicks") + 3 protect-yourself steps. **Mix (Roland, 24 Oct: "we can't keep talking about only scams"):** the winning ingredient is the structure, not the topic. Each week: ~40% PROTECT (scams, safety, privacy), ~40% EARN & ADVANCE (AI tools that save time or make money, tech skills that pay, career moves for young Nigerians, framed as a specific gain: "This free AI tool does your CV in 2 minutes"), ~20% BUILDER & TRUTH (Roland's own work and hard lessons, from his voice notes). Every Reel uses the same structure: viewer's stake in the first sentence, a surprising twist, 3 concrete steps, a send-to-a-friend ending. Compare average watch time and shares weekly and shift the mix toward what wins. Prefer scams young Nigerians actually meet (fake bank/POS alerts, P2P crypto scams, "account blocked" SMS, Ponzi apps, fake giveaways, SIM swap).
- **First 3 seconds:** the threat in ≤7 words, on screen AND spoken in the first sentence, about the VIEWER ("Your…", "This scam…"). No greeting, no history/date opener, no mascot intro. Hook overlay must be a personal stake ("Your 'stable' coin can go to zero"), not a headline ("The $1 coin that went to zero").
- **Length 30–45 s** for new scripts (one idea). End on "send this to someone who…" — shares drove the breakout.
- **Double down on winners within 48 h:** a Part 2 / follow-up Reel on the same topic, the winner shared to stories, Roland pins it and replies to every comment.
- **Explainer order from 25 Oct (Roland: "continue with this pattern"):** alternate PROTECT explainers with EARN/AI Reels; history topics last. Use the audio bank in this order regardless of the old Notion dates (move the rows to match): ex14 SIM swap, ex20 fake giveaway, ex17 quishing (QR scams), ex09 voice clone, ex18 rug pull, ex10 Arup deepfake, ex15 passkeys, ex07 gas fees, ex06 Mt Gox, ex08 ETF, ex19 inflation, ex11 hallucination, ex12 LLM, ex13 CrowdStrike, ex16 business. Each one: personal-stake hook overlay + "send this to someone who…" caption.
- **Carousels:** max 2 a week on Instagram (save-worthy checklists only, ABSTRACT Figma cover). The daily 0800 slot becomes a Reel or carousel depending on the week's plan; never more than 1 carousel a day.

## LinkedIn rules (Roland, 21 Oct 2026: "go with your recommended fix... one daily, 5 a week")
Supersedes earlier LinkedIn cadence lines. Why: 4-6 LinkedIn posts a day split every golden hour; posts read as generic explainers, not a founder.
- **1 post a day, Monday to Friday only, at 0800 Lagos (07:00 UTC)** — the 0800 slot. Every other slot has `"linkedin": {"enabled": false}`. No LinkedIn on Sat/Sun.
- Videos (`post_video.py`) skip LinkedIn unless the entry sets `"linkedin": true` (use it for the Thursday clip). Kobo cartoons and teasers never go to LinkedIn.
- **Weekly plan:**
  - **Mon — what I built or broke this week:** Community Square, Autopilot, Klærus, Farm Ledger (farm manager); Gabriel only if it fits. Not Nebula-Q. Klærus posts are builder updates only (no "house edge" terms, no product pitches).
  - **Tue — PDF carousel:** reuse that week's Instagram carousel as a LinkedIn document post.
  - **Wed — AI or crypto explainer with Roland's own take** ("here's what I'd do"), not a neutral summary.
  - **Thu — native video clip** from that week's YouTube long-form (≤90 s, captions on).
  - **Fri — Nigeria innovating + motivation:** inspiring and educating young Nigerians (not Edo only); hard truths about life, discipline, consistency, building together.
- **Voice:** first person, Roland's real work and real opinions. **Never invent stories, results, or "I did X this week" claims.** If a Mon/Fri post needs a real moment, ask Roland for two lines in the evening message; if none arrives, write a principle-led post with no fake anecdote.
- **Ending:** the last line is a specific question people want to answer. Sources and links go in `"first_comment"` (post.py posts it). "Education, not financial advice" goes above the question on crypto posts.
- Two lanes only: building tech (AI + crypto infrastructure) and Nigeria innovation/motivation. Drop CV tips, local SEO, generic small-business tips on LinkedIn (they can stay on Instagram).
- Roland does live engagement himself (reply to every comment in the first hour; 5 comments/day on 10-15 bigger AI/Web3/African tech accounts). If he asks, draft comments; never post them automatically.

## Zero to One series (Roland, 23 Oct 2026: "extra posts, not the already scheduled ones")
- Fri 23 – Mon 26 Oct: `queue/<date>/1300.json` already holds a "Zero to One, decoded" Instagram carousel + LinkedIn PDF (built by `studio/days/zto1.py`, then `zto1_li.py` (LinkedIn people-photo design) and `zto1_ig.py` (Instagram conversational chat). Re-running zto1.py alone would undo the last two). **Never overwrite or disable those four 1300 slots**, and keep 12:01 UTC posting runs booked for them. They are extra to the normal plan (so LinkedIn gets 2 posts on those days, including Sat/Sun).
- Not on YouTube (crypto only). Lessons are paraphrased; at most one short attributed quote per post.

## Formats (15 Oct 2026)
- **ABSTRACT COVERS ONLY (Roland, 27 Oct 2026: "return to abstract designs")** on Instagram (posts and stories). LinkedIn: Roland chose the people photo for the 28 Oct Klærus post, so ask him or follow his latest call for LinkedIn. Spare abstract image: assets/gen/arrow-hourglass.png (direction vs timing), reuse it.
- **Cover image:** every post opens with a generated realistic-abstract image that makes people stop ("what is that?"): odd objects, odd materials, dramatic light, linked to the topic. Generate it with Figma (`mcp__Figma__generate_image`, planKey `team::1302716308970441796`, 1080×1350, prompt ends "no text, no logos, no people"), then run the `fetch-images` workflow with `[{"url": ..., "path": "assets/gen/<name>.jpg"}]` and `git pull`. Never use Pinterest or other people's images. Figma credits are limited: 3 images a night, reuse them for stories. (17 Oct: `generate_image` now needs a `fileKey`; make one with `create_new_file`, then `download_assets` for the raw image URL and pass it to `fetch-images` with `gh api .../fetch-images.yml/dispatches -f "inputs[items]=..."`, because this machine can't reach figma.com directly. Credits reset at 00:00 UTC; if they run out, never build the day on Canva thumbnails. Generate the images first so the queue is never left waiting on them.)
- **Hook overlay:** `studio/cover.py` → `cover(img, hook, out, kicker=...)`. Hook 4–10 words with one ==highlight==.
- **Instagram:** carousel = cover + Chat Bubbles slides (`ig_chat.carousel(..., offset=1)`), 5–7 slides after the cover. The chat slides do the teaching (people won't read long captions), so the full lesson lives in the bubbles. Captions stay short: hook, one line of payoff, 📌 save / 📤 send, 3–5 hashtags.
- **LinkedIn: three posts a day (8 AM, 1 PM, 7 PM), Roland's decision 15 Oct.** Mix the formats across the day:
  - **PDF** for step-by-step guides: page 1 is the generated cover (handle "Roland Divine"), then the Chat Bubbles slides (`carousel(..., handle="Roland Divine")`), with a LinkedIn signoff slide (save, repost, follow Roland Divine). See the 1300 slot in `day5.py`.
  - **Single image** (the cover with `swipe=False`) for myth checks, opinions and news.
- **LinkedIn writing pattern (every post):**
  - Line 1 is the hook, under ~12 words: a surprising claim, a question people argue about, or a pain ("Your customers are messaging you at 2 AM."). Line 2 re-hooks and promises the payoff. Both must land before "…see more".
  - Short lines and paragraphs of 1–2 sentences, lots of white space. Numbered steps or → bullets for the value.
  - Specific numbers, real product names, the catch nobody mentions, and one opinionated line of Roland's own ("The mistake I'd avoid: …").
  - End with one specific question people can answer from their own experience. Never "thoughts?", "agree?" or the other banned phrases.
  - 900–1,600 characters, no hashtags or emoji, sources named at the end.
- **Stories:** 5 a day made with `cover(..., size=(1080, 1920), pos="top", swipe=False)` from the same images: two "new post · tap my profile" teasers, and three questions people can reply to.
- **Daily 9 PM teaser (Roland, 15 Oct):** one "Do you know…?" question on a generated image, posted as an Instagram feed post (slot `2100.json`, Instagram only) and as the 9 PM story. It teases tomorrow's 8 AM post, so pick tomorrow's 8 AM topic first. Rules and the log are in `studio/teasers.md`: before writing the 8 AM post, check what yesterday's teaser promised and answer it exactly.
- Template: `studio/days/day5.py` (builds slots, covers, carousels and stories in one go).

## Notion HQ and messages (Roland, 16 Oct 2026: "too scattered, organize it")
- Everything lives in Notion: page "Autopilot HQ" (https://app.notion.com/p/3fb0e9f9cf9f813b9c55eecc3f91555b) with the **Content Calendar** database (data source `collection://f324bb97-ecd6-48da-81dd-1d766c61fbc0`; columns Post, When, Platforms, Format, Pillar, Status, Instagram, LinkedIn, YouTube, Notes).
- Nightly build: add a row (Status = Scheduled) for every post and video booked for tomorrow.
- Every posting run: update that row (Status Posted/Failed + links). **Do not message Roland after a posting run unless something failed.**
- The nightly build sends ONE evening message: tomorrow's plan (titles + times), today's results in one line, and the Notion link.

## Steps
0. **Fresh-session setup (each nightly is a new session):** if `/home/claude/fonts/node_modules/@fontsource` is missing, run `mkdir -p /home/claude/fonts && cd /home/claude/fonts && npm i -s @fontsource/plus-jakarta-sans @fontsource/archivo-black @fontsource/dm-serif-display @fontsource/caveat @fontsource/instrument-serif @fontsource/space-grotesk @fontsource/bricolage-grotesque`; `pip install --break-system-packages -r requirements.txt soundfile numpy pillow playwright cryptography` if imports fail. Load studio/STORY_GUIDE.md before writing anything.
1. **Repo:** if `/home/claude/autopilot` is missing, call add_repo (RolandDivine/autopilot, push), clone it there, and call register_repo_root. Run `git pull`.
2. **Tomorrow:** N = (tomorrow − 2026-10-12) + 1. If `queue/<tomorrow>/` already has 3 slot files, skip to step 7. After Day 150 (10 Mar 2027), tell Roland the plan has ended and stop.
3. **Research (do this before writing anything):**
   - Dispatch the `research` workflow (`gh api -X POST repos/RolandDivine/autopilot/actions/workflows/research.yml/dispatches -f ref=main`), wait for it, `git pull`, and read `research/<today>.json`: Google Trends (US, GB, NG, IN), Hacker News, Google autocomplete questions per topic, and Instagram stats per post.
   - Run 3–5 WebSearches for what people are asking this week in the four categories (Reddit and X threads, new product launches, "how to" questions). Reddit blocks the workflow, so search it.
   - Pick 3 topics with clear demand. Verify every fact in primary or reputable sources; name sources.
   - Look at the Instagram stats: what got reach, saves and shares? Do more of that. Report it in step 7.
4. **Content:** copy `studio/days/day5.py` to `dayN.py`, generate 3 cover images, rewrite the copy, run it.
5. **Check:** build contact sheets and look at every slide and story. Fix any overflow, clipped text or wrong counter.
6. **Slots:** `dayN.py` writes `queue/<tomorrow>/{0800,1300,1900,2100}.json` and `stories.json`. LinkedIn and Instagram both on in all three slots. Instagram caption: 3–5 hashtags and a 📌 save / 📤 send line. Lint all slots and stories (`autopilot.lint.lint_stories(folder)`), fix every FAIL. Commit "Day N queue" and push. Confirm the review issue opened.
7. **Tell Roland (one SendUserMessage, the only routine message of the day; also add tomorrow's rows to the Notion Content Calendar):** the three titles and times, the search demand behind each topic, yesterday's Instagram numbers, the story times, and the review issue link. Send the three covers with SendUserFile. Also ask him one short question that would make a good story (something that really happened to him with AI, crypto or building). When he answers, add it to `studio/story_bank.md` (the repo is public, so only add what he's happy to post).
8. **YouTube (21 Oct 2026):** no daily Market Read. Follow the weekly loop in `studio/YOUTUBE.md` (long-form: script Mon, voice + render by Thu, publish Thu).
9. **Posting runs need NO Claude session (27 Oct 2026, after a usage-limit outage froze everything for 3 days):**
   - GitHub posts the slot files and stories on its own (`post.yml` runs every hour 06–22 UTC) and posts the day's videos on time
     (`videos.yml` runs hourly, reads `queue/vo/posts-<date>.json`; each entry may set `"at": "HH:MM"` UTC, defaults ex* 11:00, kobo* 17:00, liclip* 07:00).
   - **Never book send_later posting or video runs again.** They woke a huge conversation 8–10 times a day and burned Roland's usage.
   - This nightly build runs as its own fresh scheduled session (one a day). It also **reconciles yesterday**: read `log/posted.jsonl` and
     `log/videos.jsonl`, set each Notion row to Posted (with links) or Failed, and mention failures in the evening message.
10. **Stay 2 days ahead:** if the queue for tomorrow AND the day after doesn't exist, build both tonight (videos rendered, slots, stories).
    A missed night must never leave a day empty.

## Music (Roland's request, 13 Oct 2026)
The Instagram API can't attach music to carousels (only to Reels, and only with Facebook Login), so Roland adds it in the app after each post goes out.
For every Instagram slot, set `"music"` to one old-school track that fits the mood. Rotate through Sade, Phil Collins and Michael Bolton, plus similar artists (Anita Baker, Luther Vandross, Lionel Richie, Whitney Houston, Tracy Chapman, George Michael). Don't repeat the same song within a week.
Example: `"music": "Sade – Smooth Operator"`.

## Klærus content: on hold (Roland, 15 Oct 2026)
Do not post anything about Klærus. The 15 Oct drafts are in archive/klaerus-2026-10-15 and are
outdated: Klærus was restructured and terms like "house edge" are no longer used. Wait for Roland's
restructured document before writing any Klærus content.

## Kobo videos (Roland, 15 Oct 2026)
Kobo animated videos are strictly for storytelling content: story-led videos like Kobo's Money Story.
They can go out as Instagram Reels and as LinkedIn videos, but are never used for news or plain how-tos.
Kobo alone for a solo script; Kobo and Babe together for a duo script.
Exception (Roland, 16 Oct 2026): Kobo is the brand host of the viral explainer videos (`studio/viral.py`): he opens with "Hey, Kobo here" and appears lip-synced in the corner.

## Viral explainer videos (Roland, 16 Oct 2026)
Trend-led 40-65s Reels with on-screen evidence, one each across founders/building products, crypto and AI.
Pipeline: research a trending story and verify facts in reputable sources → ElevenLabs voice (Oluwadamilare, VzScgb5Pi0A6lafMNQpm) → 1-2 Figma images → `python studio/viral_pull.py <name> <voice_url> <img_url>=<file>` → add a spec to `studio/viral.py` (cards name their sources) → preview frames, fix, render → captions in `queue/kobo/viral.json` (LinkedIn text short: a powerful hook + 1-2 lines + sources).
Posting a video (Roland, 16 Oct 2026): `python3 studio/post_video.py <json> <key> [story]` posts the Instagram Reel, the LinkedIn video, the YouTube Short (channel "Building Gen12 with Roland", via youtube-publish) and, with `story`, an Instagram video story (only for videos up to 60s).

## YouTube: "Trade Like an Institution" (Roland, 16 Oct 2026)
- **21 Oct 2026 overhaul: `studio/YOUTUBE.md` now leads.** Daily Market Read Shorts are stopped (no more 06:00 runs; the nightly build must not book them). One long-form how-to a week plus Shorts cut from it, and one weekly Sunday market video. Where the lines below disagree with YOUTUBE.md, YOUTUBE.md wins.
- **Crypto only.** Non-crypto videos never go to YouTube (`"youtube": true` only on crypto entries; `post_video.py` skips the rest). Instagram and LinkedIn are unchanged.
- ~~Shorts = Daily Market Read~~ (stopped 21 Oct, see YOUTUBE.md), formerly every day: `market` workflow (05:15 UTC, CoinGecko) → `python studio/market_short.py script <date>` → ElevenLabs voice → `viral_pull.py market-<date> <url>` → `market_short.py render <date>`. Playlist "Daily Market Read".
- ~~Daily run~~ (stopped 21 Oct 2026) (Roland, 17 Oct 2026: "start the YouTube daily crypto market read shorts"):** every morning at 06:00 UTC a scheduled task dispatches `market`, waits, runs `market_short.py script`, voices it with ElevenLabs (Oluwadamilare, model `eleven_flash_v2_5`, half the credits), `viral_pull.py market-<date> <url>`, renders, checks frames, then posts YouTube only: `python3 studio/post_video.py queue/market/<date>/post.json market ytonly` (playlist "Daily Market Read"), and adds/updates its Notion row. The nightly build books the next morning's run (step 8).
- **Landscape how-tos (Roland, 17 Oct: "landscape videos of how to use trading platforms"):** `studio/howto.py` (1920x1080, same engine). Scripts in `queue/howto/<name>.txt`. One or two a week, playlist "How To: Crypto Apps & Tools". Platform steps are shown as our own step cards, keycaps and charts, never copied screenshots or logos; verify every click and shortcut in the platform's own docs first. When Roland sends screen recordings, cut them in instead.
- **ElevenLabs credits (Roland paid for Starter, 18 Oct 2026):** 30,000 credits a month, and Flash costs about 1 credit per character on this plan. Budget: Daily Market Read script under 650 characters (~20k a month), how-tos ~1,700 each. Check the cost in each generation result; if a call fails on quota, don't retry: set the Notion row to Failed ("ElevenLabs credits") and mention it once in the evening message. Fish Audio: Roland's 250k credits are app credits (API balance is 0), so they only work inside fish.audio itself; the `fish-tts` workflow is ready if he ever adds API credit (FISH_API_KEY secret is set). **Fish via the website (Roland, 18 Oct: "use no 1")**: when his computer is online, use the built-in browser (signed in at fish.audio): open `https://fish.audio/app/text-to-speech/?modelId=<voice id>`, wrap `window.fetch` to collect ids from `api.fish.audio/task/<32-hex id>` calls, insert the script into the contenteditable box, click Generate Speech (it makes 2 takes), then fetch `https://platform.r2.fish.audio/tasks/<UTC date>/<id>.mp3` into the repo with the fetch-images workflow. Never call Fish's internal task API directly (it is reCAPTCHA-protected). Samples: assets/voices/fish-{elite,ethan,slax}.mp3.
- **Scenario analysis only:** levels, "if it closes above X, next level Y; lose Z and the idea is wrong". Never "buy/sell", never leverage or position size advice. Always "Scenarios, not signals. Education, not financial advice." Post a weekly recap of which setups played out and which failed.
- **Landscape videos = how-tos** (apps, exchanges, wallets, TradingView), trading like an institution (risk, sizing, funding, open interest), crypto terms explained. Roland will also send screen recordings (Google Drive or the desktop link) for editing.
- **Voice (Roland, 17 Oct 2026, final):** ElevenLabs "Oluwadamilare" `VzScgb5Pi0A6lafMNQpm`, the voice in the FTX and hardware-wallet videos, for every new video on every platform. Don't switch voices or ask again.
- Playlists: Daily Market Read, How To: Crypto Apps & Tools, Trade Like an Institution, Crypto Terms Explained, Crypto Safety. Manage the channel with `youtube-admin` (never delete; set private instead).

- **VOICE FOR INSTAGRAM REELS (Roland, 27 Oct 2026): the American Fish ELITE voice, the one from the viral address-poisoning Reel.** Use the voiced bank in assets/vo (ex*.mp3) first. Never voice an Instagram Reel with ElevenLabs Oluwadamilare. New Reel scripts need Fish ELITE (via fish.audio in the built-in browser, see below); if that isn't possible, use a banked explainer instead. Oluwadamilare is for YouTube long-form only. assets/vo/ex21-poison2.mp3 (Oluwadamilare) is NOT to be posted; re-voice that script in Fish ELITE.

## Audio bank (voiced 18 Oct 2026, before Fish plan ends 22 Oct)
- 30 Fish ELITE voiceovers in assets/vo/: kobo06–kobo15 (Kobo S2) + ex01–ex20 explainers. Each has an alt take (<name>-b.mp3) and Whisper word timings (<name>.json). Index: queue/vo/index.json.
- 5 ElevenLabs how-to voiceovers: assets/vo/howto-*.mp3 (scripts in queue/howto/).
- Notion rows exist, 2 a day at 12:00 (explainer) and 18:00 (Kobo) WAT, shifted to 20 Oct–3 Nov after the missed 19 Oct build. Order: ex01+kobo06 (20 Oct, posted), ex02+kobo07 (21 Oct), then ex03+kobo08 (22 Oct) … ex10+kobo15 (29 Oct), then two explainers a day ex11–ex20 (30 Oct–3 Nov). The Notion row's When is the source of truth.
- **Nightly video step (every night, before step 7):** build tomorrow's two videos.
  - Kobo part N: add `duo.CARDS[N]` in `studio/money2.py` (5–8 cards timed from `assets/vo/koboNN.json`), preview with `python3 studio/money2.py N 3 20 40 60`, look at the frames, then render `python3 studio/money2.py N`.
  - Explainer exNN: add a `*_spec()` to `studio/explainers.py` (cards anchored on words with `at()`, one generated vertical background image in assets/gen), preview, look, render.
  - Write `queue/vo/posts-<date>.json` (video, title, youtube true only for crypto, playlist, reel_caption, li_text) like `posts-2026-10-21.json`, commit the mp4s, set both Notion rows to Scheduled.
  - Don't book runs: the `videos` workflow posts them at 11:00 / 17:00 UTC (or the entry's "at"). Next night, reconcile `log/videos.jsonl` into Notion. post_video.py also posts the video to Instagram Stories by default, cut into parts of 60 s or less at natural pauses (Roland, 20 Oct 2026: always do this, every video).
