# Handoff

_Last updated: 2026-05-05 by Codex (GPT-5)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Expanded visual-card generation pass for Scenes 1-5 plus courtroom crisis/thumbnail exploration. Scene-1 support pass is complete, Scene-2 is generated/reordered, Scene-3 support inserts are generated, and Scene-4 has progressed through the diya-lighting and flower-offering inserts. Current resume point: continue Scene-4 with Image 5, the close top-down shot of exactly seven incense mounds being shaped on the Baglamukhi Yantra.

## In Progress
- `Bagla-Sadhana-Anubhav.md`: Scenes 1–5 fully prompted in GPT-4o format, character refs locked
- `Bagla-Sadhana-Anubhav-Design.md`: updated to prefer competitor-style visual card density for long-form story pacing instead of only 1-2 stills per scene
- `PROMPT-LEARNINGS.md`: updated with new ChatGPT image model surgical-edit rules for framed Maa portraits, seven incense mounds, clove counts, four-arm layout, and gada side
- Courtroom crisis / thumbnail visual lane has started, but final outcome scenes are still not written into the script
- Script incomplete — outcome scenes (court case resolution, adversaries rendered helpless, devotee's gratitude) not yet written

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

## Next Steps
1. **Continue Scene-4 Image 5** — close top-down ritual insert of hands shaping exactly seven incense mounds on the Baglamukhi Yantra, cloves waiting in a copper dish.
2. **Generate/verify Scene-4 Image 6** — close detail of exactly seven incense mounds total, one clove each, smoke trails, diya, framed Maa softly blurred.
3. **Review Scene-5 existing files** — `Scene-5-1.png` and `Scene-5-2.png` exist; decide if they are final enough or need regeneration under the current prompt style.
4. **Write remaining outcome scenes** (Hindi + English) — court case crisis, Maa's grace, court case resolution, adversaries rendered helpless, devotee's gratitude.
5. **Place courtroom/thumbnail assets into final scene numbering** once outcome scenes are written.

<!-- HANDOFF-SNAPSHOT:START 2026-05-05 14:35 branch:main -->
**Modified files:**
```
 M ../../../Competitors/Competitor-Analysis.md
 M Bagla-Sadhana-Anubhav.md
 M PROMPT-LEARNINGS.md
 M ../../../../bin/render_scene.py
?? ../../../Bagla-Sadhana-Anubhav-Design.md
?? ../../../Start-Content.md
?? Scene-1-1a.png
?? Scene-1-1b.png
?? Scene-1.mp3
?? Scene-4-3.png
?? Scene-4-4.png
?? Thumbnail.png
?? courtroom-1.jpeg
?? crowded-courtroom.png
```

**Recent commits:**
```
6277ed9 chore: auto-update handoff snapshot [2026-05-05 14:33]
9a1686d chore: auto-update handoff snapshot [2026-05-05 14:33]
c503991 chore: auto-update handoff snapshot [2026-05-05 14:32]
8b2f33f chore: auto-update handoff snapshot [2026-05-05 14:29]
f966372 chore: auto-update handoff snapshot [2026-05-05 13:53]
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-05 14:33 branch:main -->
**Modified files:**
```
 M ../../../Competitors/Competitor-Analysis.md
 M Bagla-Sadhana-Anubhav.md
 M PROMPT-LEARNINGS.md
 M ../../../../bin/render_scene.py
?? ../../../Bagla-Sadhana-Anubhav-Design.md
?? ../../../Start-Content.md
?? Scene-1-1a.png
?? Scene-1-1b.png
?? Scene-1.mp3
?? Scene-4-3.png
?? Scene-4-4.png
?? Thumbnail.png
?? courtroom-1.jpeg
?? crowded-courtroom.png
```

**Recent commits:**
```
9a1686d chore: auto-update handoff snapshot [2026-05-05 14:33]
c503991 chore: auto-update handoff snapshot [2026-05-05 14:32]
8b2f33f chore: auto-update handoff snapshot [2026-05-05 14:29]
f966372 chore: auto-update handoff snapshot [2026-05-05 13:53]
7e8c5ca chore: auto-update handoff snapshot [2026-05-05 13:47]
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->
