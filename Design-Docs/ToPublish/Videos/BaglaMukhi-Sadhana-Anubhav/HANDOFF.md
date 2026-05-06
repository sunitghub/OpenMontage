# Handoff

_Last updated: 2026-05-06 by Claude (claude-sonnet-4-6)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Render CLI defaults updated for current workflow. `render-scene --scene N` now uses `Scene-N.mp3` automatically, vintage is on by default, and `render-scene --all` renders discovered scenes in numeric order with matching narration. Next production task: generate image 7b (pranam), then write outcome scenes (6–8).

## In Progress
- `Bagla-Sadhana-Anubhav.md`: Scene-1 images 1a–8 on disk (11 images, 7.5s hold ✓); image 7b (sadhak pranam) still to generate
- Script incomplete — outcome scenes (Beats 6–8: vision/experience, court resolution, teaching close) not yet written
- Courtroom/thumbnail assets exist but not yet placed into final scene numbering
- Scene-4 images 5–6 not yet generated

## Recent Decisions
- **Switched from MidJourney to GPT-4o (ChatGPT)** — GPT-4o solves two-arm constraint, female deity face, and domestic architecture in one shot. MidJourney required 14+ rounds and still failed on key constraints. See PROMPT-LEARNINGS.md → GPT-4o section.
- **User is now using the new ChatGPT image model** — preservation is better than previous runs, but iconography corrections still need surgical prompts: `Edit only...`, `Do not change anything else`, `viewer's left/right`, exact ritual counts, and explicit anti-Shiva symbol negatives.
- **All prompts converted to GPT-4o format** — stripped MidJourney params (`--ar`, `--cref`, `--cw`, `--sref`, `--s`, `--v 6`), added `wide 16:9 composition` in plain text, added `**Ref:** Upload \`filename.png\`` notes in script.
- **Scene-1-3.png approved as thumbnail** — GPT-4o, no reference, glowing arch framing Maa.
- **Scene-1-4.png added** — new scene: guru with Maa portrait and mala, sadhak listening. GPT-4o + `Sadhak_A_Ref.png`.
- **Scene-1 support cards approved** — `Scene-1-5.png` close sadhak listening with guru raised hand, `Scene-1-6.png` Chaudas moon and lamp insert, `Scene-1-7.png` standing guru instruction, `Scene-1-8.png` pensive sadhak alone after guru instruction. These match `Scene-1-4.png` well enough through teal turban, white-bearded guru, white-clad sadhak, warm cave light, and moonlit cave setting.
- **Scene-2 sequence generated and reordered** — `Scene-2-1.png` choosing cluttered room, `Scene-2-2.png` clearing/removing objects, `Scene-2-3.png` pensive half-cleared planning moment, `Scene-2-4.png` painting room, `Scene-2-5.png` brush closeup, `Scene-2-6.png` hanging yellow curtain, `Scene-2-7.png` empty completed yellow room, `Scene-2-8.png` completed room transition with folded asan/lamp. `Scene-2-2` prompt was tightened to avoid yellow curtain/ritual setup too early.
- **Scene-3 support inserts generated** — `Scene-3-3.png` yellow cloth on bajot, `Scene-3-4.png` rice yantra top-down, `Scene-3-5.png` Maa frame placement, `Scene-3-6.png` 10 o'clock room discipline shot.
- **Scene-4 current progress** — `Scene-4-3.png` regenerated with better front-facing posture for lighting diya; `Scene-4-4.png` saved as close hand/flower offering insert to avoid duplicating `Scene-4-3`.
- **Courtroom crisis/thumbnail assets started** — `courtroom-1.jpeg` and `crowded-courtroom.png` are reference/source images. `Thumbnail.png` is the engaging court-grace thumbnail where Maa Baglamukhi appears above the white-kurta sadhak in court. The latest courtroom edit prompt should move the black-coated standing lawyer to the right, turned toward the sadhak, with the police constable less dominant in the background.
- **Scene-4 detail finalized** — seven incense mounds, one clove each, corrected framed Maa portrait, warm altar lighting. Current local file: `Scene-4-2-Final.png`.
- **Standalone Maa reference corrected** — trident replaced with golden gada, four arms restored. Current local file appears as `Maa-Baglamukhi.png`; old `Mata-Baglamukhi.png` is deleted in the working tree.
- **Visual-card density increased** — Scenes 1-5 now use 34 total image prompts: Scene-1 = 8, Scene-2 = 8, Scene-3 = 6, Scene-4 = 6, Scene-5 = 6. New support beats include guru standing instruction, sadhak pensive after guru talk, choosing the room, clearing/painting the room, ritual hand inserts, exact seven incense mounds, achaman, and prayer closeups.
- **Three character refs locked:**
  - `Maa-Baglamukhi.png` → Maa reference (blessing pose, golden gada, no trident)
  - `Sadhak_A_Ref.png` → Sadhak State A (white kurta — Scenes 1–2)
  - `Sadhak_B_Ref.png` → Sadhak State B (yellow dhoti — Scenes 3–5)

## Dead Ends
- See `PROMPT-LEARNINGS.md` → MidJourney sections for full record of what failed and why.
- For framed Maa portrait edits, phrasing such as "Maa's left hand" or "right hand" confused the model. Use `viewer's LEFT side` / `viewer's RIGHT side` and describe the visible frame placement instead.
- When correcting the gada, the model may fix the weapon but change arm count. Always include `exactly four arms total` and a final hand layout.
- When correcting altar details, the model may drift from seven incense mounds. Always repeat `exactly seven incense mounds total` and `each mound has exactly one clove`.

## Generated so far (committed)
- Scene-1: `Scene-1-1-2.png` (folk, in-video), `Scene-1-2.png` (guru cave), `Scene-1-3.png` (thumbnail candidate), `Scene-1-4.png` (guru with mala), `Scene-1-5.png`, `Scene-1-6.png`, `Scene-1-7.png`, `Scene-1-8.png`
- Scene-2: `Scene-2-1.png` through `Scene-2-8.png` generated and ordered
- Scene-3: `Scene-3-1.png` through `Scene-3-6.png` generated
- Scene-4: `Screen-4-1.png` draft, `Scene-4-2-Final.png` final incense/clove altar detail, `Scene-4-3.png` diya lighting, `Scene-4-4.png` flower offering hand insert
- Scene-5: `Scene-5-1.png` and `Scene-5-2.png` exist from earlier generation
- Court/thumbnail: `courtroom-1.jpeg`, `crowded-courtroom.png`, `Thumbnail.png`
- Videos: `Scene-1-1-Vid.mp4`, `Scene-1-2-Vid.mp4`, `Scene-2-1.mp4`, `Scene-2-3.mp4`

## Recent Changes (2026-05-06)
- **Render CLI workflow simplified** — `render-scene --scene 2 --preview` now auto-resolves `Scene-2.mp3`; `--narration` remains an override; `--vintage` is default with `--no-vintage` as the opt-out; `--all` renders/concats scenes in numeric order when matching narration exists.
- **Image sort bug fixed** — `image_sort_key()` now parses `(int, suffix)` tuple via regex; previously `int("1a")` crashed → all keys collapsed to 0 → render started with wrong image. Documented in `PROMPT-LEARNINGS.md`.
- **Script format updated** — scenes now use `### Script Hindi` / `### Script English` sections; `count_script_words()` in `render_scene.py` updated to parse new format with backward-compat fallback.
- **Scene-1 image sequence reordered** — 1a, 1b, 2, 3a, 3b, 3c, 4, 5, 6, 7, 8 (11 on disk); 5b dropped (not needed); 7b pending.
- **EQ chain tuned** — `volume=-5dB` → `volume=-4dB` + `alimiter(limit=0.7, attack=5, release=50)` to match competitor benchmark: target mean -20.9 dB / max -4.8 dB. Current render: mean -22.7 dB / max -2.2 dB (pre-limiter render; re-render pending).
- **Audio benchmarked vs Kumar-Aur-Chudail** — competitor: 638×360, mean -20.9 dB, max -4.8 dB, median frame diff 26.1. Ours: 1280×720, mean -22.7 dB, max -2.2 dB, median diff 7.8. Resolution and motion style differences are intentional; audio gap is closed by new EQ settings.
- **Critique State / ToDo updated** — Scene-1 pacing marked resolved (7.5s/img ✓, 5b not needed); 7b pranam still pending.

## Next Steps
1. **Generate image 7b** — sadhak pranam to guru (cave interior, warm lamp, bowed head). Needs `Sadhak_A_Ref.png`. Prompt already written in `Bagla-Sadhana-Anubhav.md`.
2. **Re-render Scene-1** — `render-scene --scene 1 --narration Scene-1.mp3 --vintage --preview` to verify new EQ (alimiter added) hits ~-21 dB mean / ~-4.5 dB max.
3. **Write outcome scenes 6–8** (Hindi + English) — vision/divine experience, court resolution, teaching close. These are the payoff beats; script is incomplete without them.
4. **Continue Scene-4 images 5–6** — close top-down ritual insert (seven incense mounds, cloves in copper dish), then smoke/diya detail.
5. **Review Scene-5 files** — `Scene-5-1.png` and `Scene-5-2.png` exist; confirm sufficient or regenerate.
6. **Place courtroom/thumbnail assets** into final scene numbering once outcome scenes are written.

<!-- HANDOFF-SNAPSHOT:START 2026-05-06 18:02 branch:main -->
**Modified files:**
```
?? .#Bagla-Sadhana-Anubhav.md
?? Render/
```

**Recent commits:**
```
a391455 chore: auto-update handoff snapshot [2026-05-06 17:08]
69743a4 fix: zoom-burst boxblur radius floor and trim/zoompan frame mismatch
6f327bc chore: auto-update handoff snapshot [2026-05-06 16:48]
9679373 chore: auto-update handoff snapshot [2026-05-06 16:48]
5fd0f24 feat: make --zoom-burst default, add --no-zoom-burst to disable
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-06 17:08 branch:main -->
**Modified files:**
```
?? .#Bagla-Sadhana-Anubhav.md
```

**Recent commits:**
```
69743a4 fix: zoom-burst boxblur radius floor and trim/zoompan frame mismatch
6f327bc chore: auto-update handoff snapshot [2026-05-06 16:48]
9679373 chore: auto-update handoff snapshot [2026-05-06 16:48]
5fd0f24 feat: make --zoom-burst default, add --no-zoom-burst to disable
8eecc8d chore: auto-update handoff snapshot [2026-05-06 16:48]
```
<!-- HANDOFF-SNAPSHOT:END -->
