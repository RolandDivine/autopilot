# Nightly build (runs in Roland's Claude conversation at 7:10 PM Lagos)

Platforms: LinkedIn (RolandDivine2) and Instagram (@defi_ring_master) both post automatically from the queue (`instagram_autopost` is true). X is off: always set `"x": {"enabled": false}`. Never post anything directly.

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
- **First 3 seconds:** every Reel opens on its hook, never on "Hey, Kobo here". After rendering, run `python3 studio/hookcut.py <in.mp4> <in>-hook.mp4 <seconds where the first real sentence starts> "Hook line|line two" [y 0.40–0.62 to avoid cards]` and post the -hook file.
- **Search-first captions:** the first sentence starts with the words people search ("How to revoke token approvals…", "Bitcoin halving explained:"), then the hook. 3–5 hashtags.
- **Alt text:** every Instagram image gets alt text (`instagram.alt` = one line per image: what it shows + the slide's words). ig_client sends it and falls back if Instagram rejects it.
- **Real Roland beats everything:** his voice-note stories (no camera needed) become Reels with captions; build one whenever he sends a recording.

## Formats (15 Oct 2026)
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
8. **Book tomorrow's run:** also book the Daily Market Read run at 06:00 UTC the next day (send_later: "Daily Market Read: follow the Daily run section in /home/claude/autopilot/studio/NIGHTLY.md for <date>.").
   Then: call send_later at 18:10 UTC the next day with the message:
   "Nightly build: follow /home/claude/autopilot/studio/NIGHTLY.md (clone RolandDivine/autopilot first if it's missing)."
   Don't skip this step: it is what keeps the nightly run going.
9. **Book tomorrow's posting runs** (GitHub's own timer runs hours late): call send_later at 07:01, 08:01, 10:01, 12:01, 13:01, 16:01, 18:01 and 20:01 UTC the next day, each asking to dispatch the post workflow (`gh api -X POST repos/RolandDivine/autopilot/actions/workflows/post.yml/dispatches -f ref=main -F 'inputs[dry_run]=false'`), wait for it, and check `log/posted.jsonl`. After each run, update the post's row in the Notion Content Calendar (Status + links). Only message Roland if something failed.

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
- **Crypto only.** Non-crypto videos never go to YouTube (`"youtube": true` only on crypto entries; `post_video.py` skips the rest). Instagram and LinkedIn are unchanged.
- **Shorts = Daily Market Read**, every day: `market` workflow (05:15 UTC, CoinGecko) → `python studio/market_short.py script <date>` → ElevenLabs voice → `viral_pull.py market-<date> <url>` → `market_short.py render <date>`. Playlist "Daily Market Read".
- **Daily run (Roland, 17 Oct 2026: "start the YouTube daily crypto market read shorts"):** every morning at 06:00 UTC a scheduled task dispatches `market`, waits, runs `market_short.py script`, voices it with ElevenLabs (Oluwadamilare, model `eleven_flash_v2_5`, half the credits), `viral_pull.py market-<date> <url>`, renders, checks frames, then posts YouTube only: `python3 studio/post_video.py queue/market/<date>/post.json market ytonly` (playlist "Daily Market Read"), and adds/updates its Notion row. The nightly build books the next morning's run (step 8).
- **Landscape how-tos (Roland, 17 Oct: "landscape videos of how to use trading platforms"):** `studio/howto.py` (1920x1080, same engine). Scripts in `queue/howto/<name>.txt`. One or two a week, playlist "How To: Crypto Apps & Tools". Platform steps are shown as our own step cards, keycaps and charts, never copied screenshots or logos; verify every click and shortcut in the platform's own docs first. When Roland sends screen recordings, cut them in instead.
- **ElevenLabs credits (Roland paid for Starter, 18 Oct 2026):** 30,000 credits a month, and Flash costs about 1 credit per character on this plan. Budget: Daily Market Read script under 650 characters (~20k a month), how-tos ~1,700 each. Check the cost in each generation result; if a call fails on quota, don't retry: set the Notion row to Failed ("ElevenLabs credits") and mention it once in the evening message. Fish Audio: Roland's 250k credits are app credits (API balance is 0), so they only work inside fish.audio itself; the `fish-tts` workflow is ready if he ever adds API credit (FISH_API_KEY secret is set). **Fish via the website (Roland, 18 Oct: "use no 1")**: when his computer is online, use the built-in browser (signed in at fish.audio): open `https://fish.audio/app/text-to-speech/?modelId=<voice id>`, wrap `window.fetch` to collect ids from `api.fish.audio/task/<32-hex id>` calls, insert the script into the contenteditable box, click Generate Speech (it makes 2 takes), then fetch `https://platform.r2.fish.audio/tasks/<UTC date>/<id>.mp3` into the repo with the fetch-images workflow. Never call Fish's internal task API directly (it is reCAPTCHA-protected). Samples: assets/voices/fish-{elite,ethan,slax}.mp3.
- **Scenario analysis only:** levels, "if it closes above X, next level Y; lose Z and the idea is wrong". Never "buy/sell", never leverage or position size advice. Always "Scenarios, not signals. Education, not financial advice." Post a weekly recap of which setups played out and which failed.
- **Landscape videos = how-tos** (apps, exchanges, wallets, TradingView), trading like an institution (risk, sizing, funding, open interest), crypto terms explained. Roland will also send screen recordings (Google Drive or the desktop link) for editing.
- **Voice (Roland, 17 Oct 2026, final):** ElevenLabs "Oluwadamilare" `VzScgb5Pi0A6lafMNQpm`, the voice in the FTX and hardware-wallet videos, for every new video on every platform. Don't switch voices or ask again.
- Playlists: Daily Market Read, How To: Crypto Apps & Tools, Trade Like an Institution, Crypto Terms Explained, Crypto Safety. Manage the channel with `youtube-admin` (never delete; set private instead).

## Audio bank (voiced 18 Oct 2026, before Fish plan ends 22 Oct)
- 30 Fish ELITE voiceovers in assets/vo/: kobo06–kobo15 (Kobo S2) + ex01–ex20 explainers. Each has an alt take (<name>-b.mp3) and Whisper word timings (<name>.json). Index: queue/vo/index.json.
- 5 ElevenLabs how-to voiceovers: assets/vo/howto-*.mp3 (scripts in queue/howto/).
- Notion rows exist, 2 a day at 12:00 (explainer) and 18:00 (Kobo) WAT, shifted to 20 Oct–3 Nov after the missed 19 Oct build. Order: ex01+kobo06 (20 Oct, posted), ex02+kobo07 (21 Oct), then ex03+kobo08 (22 Oct) … ex10+kobo15 (29 Oct), then two explainers a day ex11–ex20 (30 Oct–3 Nov). The Notion row's When is the source of truth.
- **Nightly video step (every night, before step 7):** build tomorrow's two videos.
  - Kobo part N: add `duo.CARDS[N]` in `studio/money2.py` (5–8 cards timed from `assets/vo/koboNN.json`), preview with `python3 studio/money2.py N 3 20 40 60`, look at the frames, then render `python3 studio/money2.py N`.
  - Explainer exNN: add a `*_spec()` to `studio/explainers.py` (cards anchored on words with `at()`, one generated vertical background image in assets/gen), preview, look, render.
  - Write `queue/vo/posts-<date>.json` (video, title, youtube true only for crypto, playlist, reel_caption, li_text) like `posts-2026-10-21.json`, commit the mp4s, set both Notion rows to Scheduled.
  - Book send_later at 11:01 UTC (explainer) and 17:01 UTC (Kobo): `python3 studio/post_video.py queue/vo/posts-<date>.json <key>`, then update the Notion row. post_video.py also posts the video to Instagram Stories by default, cut into parts of 60 s or less at natural pauses (Roland, 20 Oct 2026: always do this, every video).
