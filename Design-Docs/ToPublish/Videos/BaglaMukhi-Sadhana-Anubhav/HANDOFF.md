# Handoff

_Last updated: 2026-05-08 by Claude (claude-sonnet-4-6)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Scene-4 complete (1a–8 + mp3 committed). Scene-5 images and narration generated but partially uncommitted — 5a/5b split, 5-6/5-7 updated, 5.mp3 added. Next: commit Scene-5 updates, then write outcome scenes 6–8.

## In Progress
- Scene-5: uncommitted changes on disk — `Scene-5-5.png` deleted, `Scene-5-5a.png` + `Scene-5-b.png` added, `Scene-5-6.png` / `Scene-5-7.png` updated, `Scene-5.mp3` added
- Script updated but uncommitted (`Bagla-Sadhana-Anubhav.md`)
- Outcome scenes 6–8 not yet written (vision/experience, court resolution, teaching close)
- Image 7b (sadhak pranam) still to generate — prompt written in script

## Recent Decisions
- **Switched from MidJourney to GPT-4o (ChatGPT)** — GPT-4o solves two-arm constraint, female deity face, domestic architecture. See PROMPT-LEARNINGS.md → GPT-4o section.
- **Surgical GPT-4o edit prompts** — use `Edit only...`, `Do not change anything else`, `viewer's left/right`, exact ritual counts, explicit anti-Shiva symbol negatives.
- **Scene-4 detail finalized** — seven incense mounds, one clove each, corrected framed Maa portrait, warm altar lighting. Images 1a–8 + `Scene-4.mp3` committed.
- **Three character refs locked:**
  - `Maa-Baglamukhi.png` → Maa reference (blessing pose, golden gada, no trident)
  - `Sadhak_A_Ref.png` → Sadhak State A (white kurta — Scenes 1–2)
  - `Sadhak_B_Ref.png` → Sadhak State B (yellow dhoti — Scenes 3–5)
- **EQ chain tuned** — `volume=-4dB` + `alimiter(limit=0.7, attack=5, release=50)`. Target mean -21 dB / max -4.5 dB.

## Dead Ends
- See `PROMPT-LEARNINGS.md` → MidJourney sections for full record of what failed and why.
- `viewer's left/right` must be explicit — "Maa's left hand" confuses GPT-4o.
- When correcting gada: always include `exactly four arms total` or model changes arm count.
- When correcting altar: always repeat `exactly seven incense mounds total, each with one clove`.

## Generated so far (committed)
- Scene-1: 1a, 1b, 2, 3a, 3b, 3c, 4, 5, 6, 7, 8 (11 images) + `Scene-1.mp3`
- Scene-2: 1–8 + `Scene-2.mp3`
- Scene-3: 1–6 + `Scene-3.mp3`
- Scene-4: 1a, 1b, 2, 3, 4, 5, 6, 7, 8 (9 images) + `Scene-4.mp3`
- Scene-5: 1–8 committed; 5a/5b split + 5-6/5-7 updates + `Scene-5.mp3` **uncommitted**
- Court/thumbnail: `courtroom-1.jpeg`, `crowded-courtroom.png`, `Thumbnail.png`
- Videos: `Scene-1-1-Vid.mp4`, `Scene-1-2-Vid.mp4`, `Scene-2-1.mp4`, `Scene-2-3.mp4`

## Next Steps
1. **Commit Scene-5 updates** — 5a/5b, updated 6/7, deleted 5, `Scene-5.mp3`, script changes
2. **Generate image 7b** — sadhak pranam to guru (cave, warm lamp, bowed head). Use `Sadhak_A_Ref.png`. Prompt in script.
3. **Write outcome scenes 6–8** (Hindi + English) — vision/experience, court resolution, teaching close
4. **Render Scenes 1–5** — `render-scene --all` once Scene-5 is final
5. **Place courtroom/thumbnail assets** into scene numbering once 6–8 are written

<!-- HANDOFF-SNAPSHOT:START 2026-05-08 08:32 branch:main -->
**Modified files:**
```
 M Scene-5-5b.png
 D Scene-5-6.png
 M ../../../../bin/render_scene.py
?? Scene-5-5c.png
?? Scene-5-6a.png
?? Scene-5-6b.png
```

**Recent commits:**
```
045d076 chore: auto-update handoff snapshot [2026-05-08 08:21]
8604f60 chore: Scene-5 updates and session handoff
0587866 chore: add Scene-4 full set (1a–8) and Scene-5 images 3–8
4560608 chore: ignore Emacs lock files (#* and .#*)
46ddb91 chore: auto-update handoff snapshot [2026-05-06 20:01]
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-08 08:21 branch:main -->
**Modified files:**
```
 M Scene-5-5b.png
```

**Recent commits:**
```
8604f60 chore: Scene-5 updates and session handoff
0587866 chore: add Scene-4 full set (1a–8) and Scene-5 images 3–8
4560608 chore: ignore Emacs lock files (#* and .#*)
46ddb91 chore: auto-update handoff snapshot [2026-05-06 20:01]
27f1fe7 chore: update Scene 1-3 narration audio for Baglamukhi Anubhav
```
<!-- HANDOFF-SNAPSHOT:END -->
