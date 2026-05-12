# Handoff

_Last updated: 2026-05-09 by Claude (claude-sonnet-4-6)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Scene-5 fully committed (5a–5c, 6a–6d, mp3). Next: write outcome scenes 6–8 and generate missing image 7b.

## In Progress
- Outcome scenes 6–8 not yet written (vision/experience, court resolution, teaching close)
- Image 7b (sadhak pranam to guru — cave, warm lamp, bowed head) not generated; prompt in script. Use `Sadhak_A_Ref.png`.

## Recent Decisions
- **Switched from MidJourney to GPT-4o (ChatGPT)** — GPT-4o solves two-arm constraint, female deity face, domestic architecture. See PROMPT-LEARNINGS.md → GPT-4o section.
- **Surgical GPT-4o edit prompts** — use `Edit only...`, `Do not change anything else`, `viewer's left/right`, exact ritual counts, explicit anti-Shiva symbol negatives.
- **Three character refs locked:**
  - `Maa-Baglamukhi.png` → Maa reference (blessing pose, golden gada, no trident)
  - `Sadhak_A_Ref.png` → Sadhak State A (white kurta — Scenes 1–2)
  - `Sadhak_B_Ref.png` → Sadhak State B (yellow dhoti — Scenes 3–5)
- **EQ chain tuned** — `volume=-4dB` + `alimiter(limit=0.7, attack=5, release=50)`. Target mean -21 dB / max -4.5 dB.
- **zoom-burst fixed (v2)** — zoompan on a multi-frame video segment produces corrupt PTS (video duration inflated to hours). Fix: extract one still frame at `split_t`, run zoompan on that still (its intended mode), concat back with original audio via `-shortest`. Direction still randomized (zoom-in 1.0→3.5 or zoom-out 3.5→1.0).

## Dead Ends
- See `PROMPT-LEARNINGS.md` → MidJourney sections for full record.
- `viewer's left/right` must be explicit — "Maa's left hand" confuses GPT-4o.
- When correcting gada: always include `exactly four arms total`.
- When correcting altar: always repeat `exactly seven incense mounds total, each with one clove`.

## Generated so far (all committed)
- Scene-1: 1a, 1b, 2, 3a, 3b, 3c, 4, 5, 6, 7, 8 + `Scene-1.mp3`
- Scene-2: 1–8 + `Scene-2.mp3`
- Scene-3: 1–6 + `Scene-3.mp3`
- Scene-4: 1a, 1b, 2–8 + `Scene-4.mp3`
- Scene-5: 1–4, 5a, 5b, 5c, 6a, 6b, 6c, 6d, 7, 8 + `Scene-5.mp3`
- Court/thumbnail: `courtroom-1.jpeg`, `crowded-courtroom.png`, `Thumbnail.png`
- Videos: `Scene-1-1-Vid.mp4`, `Scene-1-2-Vid.mp4`, `Scene-2-1.mp4`, `Scene-2-3.mp4`

## Next Steps
1. **Generate image 7b** — sadhak pranam (use `Sadhak_A_Ref.png`, prompt in script)
2. **Write scenes 6–8** (Hindi + English) — vision/experience, court resolution, teaching close
3. **Place courtroom/thumbnail assets** into scene numbering once 6–8 are written
4. **Render Scenes 1–5** — `render-scene --all` once Scene-5 image count is final

<!-- HANDOFF-SNAPSHOT:START 2026-05-12 17:45 branch:main -->
**Modified files:**
```
?? ../../../../.tickets/BSA-yhol.md
```

**Recent commits:**
```
129bd44 fix: remove two-arms-only constraint from Maa Baglamukhi portrait prompts
a8fee54 chore: auto-update handoff snapshot [2026-05-12 17:44]
990a84a feat: add Scene-7 images and refine prompts for apparition sequence
2646146 chore: auto-update handoff snapshot [2026-05-12 17:34]
18330f5 chore: auto-update handoff snapshot [2026-05-12 17:34]
```

**In-progress tickets:**
```
BSA-yhol [in_progress] - Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-12 17:44 branch:main -->
**Modified files:**
```
 M Bagla-Sadhana-Anubhav.md
?? ../../../../.tickets/BSA-yhol.md
```

**Recent commits:**
```
990a84a feat: add Scene-7 images and refine prompts for apparition sequence
2646146 chore: auto-update handoff snapshot [2026-05-12 17:34]
18330f5 chore: auto-update handoff snapshot [2026-05-12 17:34]
c25a7ea chore: auto-update handoff snapshot [2026-05-12 17:33]
40807c9 chore: auto-update handoff snapshot [2026-05-12 17:32]
```

**In-progress tickets:**
```
BSA-yhol [in_progress] - Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->
