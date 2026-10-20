# YouTube playbook (Roland, 21 Oct 2026: "complete overhaul on YouTube... do it now")

Supersedes the daily-Shorts plan. Why: 28 days of daily Shorts got ~19 views and 0 subscribers; the channel's best video
ever is a 2024 long-form wallet-safety how-to (158 views). Search-driven long-form how-tos are the lane.

## Identity
- Name **Roland Divine | Crypto Safety & AI**, handle **@rolanddivine** (Roland changes these in Studio; the API can't).
- Promise: keep your crypto safe and use AI like a pro, step by step, without the hype. Country NG, audience worldwide English.
- Banner: `studio/yt_banner.py` → `assets/youtube/banner.jpg` (upload with the `banner` op). Description and keywords are set
  with `update_channel`; keep them in sync with this file.

## Voice (Roland, 21 Oct: "my phone is bad... I can't do recordings. So you create those voiceovers")
- Every video uses ElevenLabs **Oluwadamilare** (`VzScgb5Pi0A6lafMNQpm`, `eleven_flash_v2_5`) until Roland says he can record.
- Scripts may say "I'm Roland" and state his real background (DeFi builder, smart contract auditor, Lagos). **Never invent
  personal stories, results or anecdotes.** Teach; don't narrate a life.
- One TTS call takes at most **5,000 characters**: split long scripts at a chapter line, then join the halves with
  0.8 s of silence (see `assets/vo/revoke-a.mp3` + `-b.mp3` → `assets/viral/howto-revoke/voice.mp3`).

## Weekly loop (the "Roland agent")
1. **Monday, pick the topic:** a question people actually search (crypto safety first, AI tools second). Check YouTube
   search suggestions/vidIQ when available; prefer "how to …" phrasing with a clear outcome.
2. **Research:** every number from a named, recent source (put it on screen and in the description).
3. **Script** `queue/youtube/<slug>.txt`, 6-10 minutes (≈1,000-1,500 words):
   - 0:00-0:20 hook: the surprising fact + what they'll be able to do by the end. No greeting first.
   - one line of who's talking + "Education, not financial advice".
   - 4-6 chapters, each starting with the line "Chapter one." etc. (anchors for visuals and captions).
   - one-breath summary, then tease the next video and "checklist pinned in the comments".
4. **Voice** (above), then transcribe for timings (`kobo-audio-2` branch + `transcribe` workflow, as `viral_pull.py` does).
5. **Visuals** `studio/longform.py` spec (16:9, `nocap: True`): a new card every 5-15 s; our own diagrams, tables and
   stat cards; sources named on stat cards. No copied screenshots, logos, Pinterest or other people's images.
   Preview frames, look at them, fix, then render (`python studio/longform.py <name>`, ~20 min).
6. **Captions:** `studio/srt_align.py` builds a correct .srt from the real script (Whisper mishears words; its timing is
   fine). Upload with the `caption` op. Never burn Whisper text into a long video.
7. **Package:** title = the search phrase + the outcome (≤70 chars). Thumbnail `studio/yt_thumb.py`: one strong image,
   **3 words or fewer**, high contrast. Description: 2-line summary, chapters (0:00 first), checklist, sources, links,
   "Education, not financial advice". 8-12 tags.
8. **Publish** a regular (non-Short) video via `youtube-publish`, then `youtube-admin`: thumbnail, caption, playlist,
   own checklist comment (Roland pins it in Studio). New best video becomes the channel trailer.
9. **Cut 2-3 Shorts / Reels** from the long video's best 30-50 s moments, each ending "full video on the channel".
   Crypto only on YouTube Shorts. Instagram stories still split to ≤60 s.
10. **Sunday:** one weekly market video (scenarios, not signals) replaces the daily Market Read. Check analytics
    (`analytics` op, 28 days): CTR, average view duration, which video brought subscribers. Write 3 lines in Notion.

## Playlists and home page
- Public: Crypto Safety (main), How To: Crypto Apps & Tools, Crypto Terms Explained, Weekly Market Read (was Daily Market Read).
- Home sections: trailer for non-subscribers, Crypto Safety, How To, Popular uploads, Recent uploads.

## Guardrails
- Education, not financial advice: no buy/sell calls, no leverage or position-size advice, never "guaranteed".
- Never delete videos (set private). Never automate comments on other people's videos.
- Klærus content stays on hold; no "house edge" terms.
- ElevenLabs credits: one 7-minute video ≈ 6,000 credits. If a call fails on quota, don't retry: Notion row Failed
  ("ElevenLabs credits") and one line in the evening message.
