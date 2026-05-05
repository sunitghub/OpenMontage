# Handoff

_Last updated: 2026-05-04 by Codex (GPT-5)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Expanded visual-card generation pass for Scenes 1-5. Scene-1 support cards 5, 6, and 7 are generated and approved. Next immediate prompt is Scene-1 Image 8: sadhak sitting alone after the guru's instruction, pensive decision moment.

## In Progress
- `Bagla-Sadhana-Anubhav.md`: Scenes 1–5 fully prompted in GPT-4o format, character refs locked
- `Bagla-Sadhana-Anubhav-Design.md`: updated to prefer competitor-style visual card density for long-form story pacing instead of only 1-2 stills per scene
- `PROMPT-LEARNINGS.md`: updated with new ChatGPT image model surgical-edit rules for framed Maa portraits, seven incense mounds, clove counts, four-arm layout, and gada side
- Script incomplete — outcome scenes (court case resolution, adversaries rendered helpless, devotee's gratitude) not yet written

## Recent Decisions
- **Switched from MidJourney to GPT-4o (ChatGPT)** — GPT-4o solves two-arm constraint, female deity face, and domestic architecture in one shot. MidJourney required 14+ rounds and still failed on key constraints. See PROMPT-LEARNINGS.md → GPT-4o section.
- **User is now using the new ChatGPT image model** — preservation is better than previous runs, but iconography corrections still need surgical prompts: `Edit only...`, `Do not change anything else`, `viewer's left/right`, exact ritual counts, and explicit anti-Shiva symbol negatives.
- **All prompts converted to GPT-4o format** — stripped MidJourney params (`--ar`, `--cref`, `--cw`, `--sref`, `--s`, `--v 6`), added `wide 16:9 composition` in plain text, added `**Ref:** Upload \`filename.png\`` notes in script.
- **Scene-1-3.png approved as thumbnail** — GPT-4o, no reference, glowing arch framing Maa.
- **Scene-1-4.png added** — new scene: guru with Maa portrait and mala, sadhak listening. GPT-4o + `Sadhak_A_Ref.png`.
- **Scene-1 support cards approved** — `Scene-1-5.png` close sadhak listening with guru raised hand, `Scene-1-6.png` Chaudas moon and lamp insert, `Scene-1-7.png` standing guru instruction. These match `Scene-1-4.png` well enough through teal turban, white-bearded guru, white-clad sadhak, warm cave light, and moonlit cave setting.
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
- Scene-1: `Scene-1-1-2.png` (folk, in-video), `Scene-1-2.png` (guru cave), `Scene-1-3.png` (thumbnail ✓), `Scene-1-4.png` (guru with mala)
- Scene-2: `Scene-2-1.png`, `Scene-2-2.png`, `Scene-2-3-1.png`, `Scene-2-3-2.png`
- Scene-3: `Scene-3-1.png` (ritual setup, sadhak back-facing), `Scene-3-2.png` (bajot/yantra close detail)
- Scene-4: `Screen-4-1.png` (sadhak lighting diya, likely draft), `Scene-4-2-Final.png` (final incense/clove altar detail)
- Scene-5: Image 1 is in active edit loop; latest version has good sadhak/lota/altar but framed Maa needs gada moved to viewer-left
- Videos: `Scene-1-1-Vid.mp4`, `Scene-1-2-Vid.mp4`, `Scene-2-1.mp4`, `Scene-2-3.mp4`

## Next Steps
1. **Generate Scene-1 Image 8** — upload `Sadhak_A_Ref.png`; pensive sadhak alone after guru instruction.
2. **Generate Scene-2 room-choice/preparation beats** — choosing the room, clearing objects, half-cleared planning moment, painting insert, completed yellow room.
3. **Generate remaining Scene-3 to Scene-5 inserts** — hands spreading cloth, yantra formation, framed Maa placement, diya lighting, flower offering, seven incense mounds, achaman, and oleander/water closeups.
4. **Write remaining outcome scenes** (Hindi + English) — court case resolution, adversaries helpless, devotee's gratitude.
5. **Review full script arc** — hook strength, pacing, tension beats, payoff.

<!-- HANDOFF-SNAPSHOT:START 2026-05-05 08:16 branch:main -->
**Modified files:**
```
 M ../../../Competitors/Competitor-Analysis.md
 M Bagla-Sadhana-Anubhav.md
 M PROMPT-LEARNINGS.md
 M ../../../../bin/render_scene.py
?? ../../../Bagla-Sadhana-Anubhav-Design.md
?? ../../../Start-Content.md
?? .#Bagla-Sadhana-Anubhav.md
?? Scene-4-3.png
?? Scene-4-4.png
?? courtroom-1.jpeg
?? crowded-courtroom.png
```

**Recent commits:**
```
f9d17cb chore: auto-update handoff snapshot [2026-05-05 08:14]
ef3b474 chore: auto-update handoff snapshot [2026-05-05 08:07]
7982c03 chore: auto-update handoff snapshot [2026-05-05 08:03]
ee1a244 chore: auto-update handoff snapshot [2026-05-05 07:59]
cd436aa chore: auto-update handoff snapshot [2026-05-05 07:58]
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-05 08:14 branch:main -->
**Modified files:**
```
 M ../../../Competitors/Competitor-Analysis.md
 M Bagla-Sadhana-Anubhav.md
 M PROMPT-LEARNINGS.md
 M ../../../../bin/render_scene.py
?? ../../../Bagla-Sadhana-Anubhav-Design.md
?? ../../../Start-Content.md
?? .#Bagla-Sadhana-Anubhav.md
?? Scene-4-3.png
?? Scene-4-4.png
?? courtroom-1.jpeg
?? crowded-courtroom.png
```

**Recent commits:**
```
ef3b474 chore: auto-update handoff snapshot [2026-05-05 08:07]
7982c03 chore: auto-update handoff snapshot [2026-05-05 08:03]
ee1a244 chore: auto-update handoff snapshot [2026-05-05 07:59]
cd436aa chore: auto-update handoff snapshot [2026-05-05 07:58]
acd6b32 chore: auto-update handoff snapshot [2026-05-05 07:47]
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->
