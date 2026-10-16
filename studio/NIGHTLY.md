# Nightly build (runs in Roland's Claude conversation at 7:10 PM Lagos)

Platforms: LinkedIn (RolandDivine2) and Instagram (@defi_ring_master) both post automatically from the queue (`instagram_autopost` is true). X is off: always set `"x": {"enabled": false}`. Never post anything directly.

## Content direction (Roland, 15 Oct 2026: full rebuild after a week of near-zero reach)
Old approach is retired: no curriculum lessons, no basic explainers (what is a wallet, how to use a wallet), no daily news card, no terminal-style PDFs on LinkedIn. Those got 2–31 reach per post.
- **Topics come from tonight's search demand, nothing else.** Categories: AI, crypto, business, tech infrastructure (data centers, cloud, chips, cybersecurity). Audience is worldwide English speakers.
- **Every post makes someone's life better:** a how-to, a where-to, a tool they can use tonight, a myth corrected with real numbers. Practical and specific, real product names, real steps, what it costs, the catch.
- **Psychology on every post:** a hook that opens a curiosity gap or challenges a belief ("Does every ChatGPT chat drink a bottle of water?"), "you" language, specific numbers, and a clear payoff on the last slide. On LinkedIn end with one specific question people can answer from their own experience (never "thoughts?" or "agree?").
- Build-in-public only when there is something real and new. Klærus stays on hold (below).

## Formats (15 Oct 2026)
- **Cover image:** every post opens with a generated realistic-abstract image that makes people stop ("what is that?"): odd objects, odd materials, dramatic light, linked to the topic. Generate it with Figma (`mcp__Figma__generate_image`, planKey `team::1302716308970441796`, 1080×1350, prompt ends "no text, no logos, no people"), then run the `fetch-images` workflow with `[{"url": ..., "path": "assets/gen/<name>.jpg"}]` and `git pull`. Never use Pinterest or other people's images. Figma credits are limited: 3 images a night, reuse them for stories.
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
7. **Tell Roland (SendUserMessage):** the three titles and times, the search demand behind each topic, yesterday's Instagram numbers, the story times, and the review issue link. Send the three covers with SendUserFile. Also ask him one short question that would make a good story (something that really happened to him with AI, crypto or building). When he answers, add it to `studio/story_bank.md` (the repo is public, so only add what he's happy to post).
8. **Book tomorrow's run:** call send_later at 18:10 UTC the next day with the message:
   "Nightly build: follow /home/claude/autopilot/studio/NIGHTLY.md (clone RolandDivine/autopilot first if it's missing)."
   Don't skip this step: it is what keeps the nightly run going.
9. **Book tomorrow's posting runs** (GitHub's own timer runs hours late): call send_later at 07:01, 08:01, 10:01, 12:01, 13:01, 16:01, 18:01 and 20:01 UTC the next day, each asking to dispatch the post workflow (`gh api -X POST repos/RolandDivine/autopilot/actions/workflows/post.yml/dispatches -f ref=main -F 'inputs[dry_run]=false'`), wait for it, and check `log/posted.jsonl`. For 07:01, 12:01 and 18:01, tell Roland the links and the music pick; for the story runs, only message him if something failed.

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
