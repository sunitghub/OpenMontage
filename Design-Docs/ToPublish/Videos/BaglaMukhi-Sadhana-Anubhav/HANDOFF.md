# Handoff

_Last updated: 2026-05-20 by Claude (claude-sonnet-4-6)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Scene-11 images complete. Next: record voiceovers for Scene-10 and Scene-11, then write Scene-12 (court resolution + closing teaching).

## In Progress
- Voiceover for Scene-10 — pending
- Voiceover for Scene-11 — pending
- Ticket BSA-yhol still open (Scene-7 voiceover check)

## Recent Decisions
- **Switched from MidJourney to GPT-4o (ChatGPT)** — solves two-arm constraint, female deity face, domestic architecture. See PROMPT-LEARNINGS.md.
- **Four character refs locked:**
  - `Maa-Baglamukhi.png` → Maa reference (blessing pose, golden gada, no trident)
  - `Sadhak_A_Ref.png` → Sadhak State A (white kurta — Scenes 1–2)
  - `Sadhak_B_Ref.png` → Sadhak State B (yellow dhoti — Scenes 3–11)
  - `Mahakali-1.png` → Kali apparition (Scenes 7–10)
- **GPT-4o guardrail** — "skull garland/mundmala/blood-filled bowl" triggers violence block. Use "dark ancient garland" + "dark vessel"; let `Mahakali-1.png` carry the visual.
- **Sadhak gaze problem** — strip all mention of presence/darkness; describe only the sadhak facing Maa's portrait. Accept drift — narration carries subtext.
- **Scene-10 garland** — flower haar (marigold + jasmine), not prayer beads.
- **Scene-11 Maa form** — beautiful luminous woman in yellow-gold sari with golden anklets (payal). Standing with halo + abhaya mudra for closing blessing. Use `Maa-Baglamukhi.png` ref.
- **Doubt/crisis shots** — remove ritual objects and ref entirely; model defaults to sadhana scene otherwise.
- **EQ chain** — `volume=-4dB` + `alimiter(limit=0.7, attack=5, release=50)`. Target mean -21 dB / max -4.5 dB.

## Dead Ends
- `viewer's left/right` must be explicit — "Maa's left hand" confuses GPT-4o.
- Empty-room shots: never upload Mahakali ref — model adds her even with negatives.
- Wide shot with 3 elements (Kali blowing + breath + Sridhar watching) = too crowded; split instead.

## Generated & Committed
- Scene-1: 1a, 1b, 2, 3a, 3b, 3c, 4, 5, 6, 7, 8 + `Scene-1.mp3`
- Scene-2: 1–8 + `Scene-2.mp3`
- Scene-3: 1–6 + `Scene-3.mp3`
- Scene-4: 1a, 1b, 2–8 + `Scene-4.mp3`
- Scene-5: 1–8 + `Scene-5.mp3`
- Scene-7: images + `Scene-7.mp3`
- Scene-8: 1–11 images + `Scene-8.mp3`
- Scene-9: 1–8 images + `Scene-9.mp3`
- Scene-10: 1–13 images + `Scene-10.mp3`
- Scene-11: 1–10 images (voiceover pending)
- Court/thumbnail: `courtroom-1.jpeg`, `crowded-courtroom.png`, `Thumbnail.png`

## Next Steps
1. **Record Scene-10 and Scene-11 voiceovers**
2. **Write Scene-12** — court case resolution + closing teaching with mantra for viewers
3. **Close ticket BSA-yhol** — after Scene-7 render verified

<!-- HANDOFF-SNAPSHOT:START 2026-05-21 14:22 branch:main -->
**Modified files:**
```
 M Bagla-Sadhana-Anubhav.md
 D Scene-11-3.png
 D Scene-11-7.png
 M Scene-11.mp3
 D Scene-12-1.png
?? Scene-11-10b.png
?? Scene-11-10c.png
?? Scene-12-1png.png
?? Scene-12-5b.png
?? Scene-12-8.png
?? Scene-12.mp3
?? ../Scene-11-3.png
```

**Recent commits:**
```
961d80e feat: add Scene-12 images and Scene-11 voiceover
98f82fd chore: auto-update handoff snapshot [2026-05-21 11:10]
c35a668 chore: auto-update handoff snapshot [2026-05-21 11:07]
396e733 chore: auto-update handoff snapshot [2026-05-21 11:02]
d9f7881 chore: auto-update handoff snapshot [2026-05-21 11:00]
```

**In-progress tickets:**
```
BSA-yhol [in_progress] - Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-21 11:10 branch:main -->
**Modified files:**
```
 M Bagla-Sadhana-Anubhav.md
?? Scene-11-11.png
?? Scene-11.mp3
?? Scene-12-1.png
?? Scene-12-2.png
?? Scene-12-3.png
?? Scene-12-4.png
?? Scene-12-5.png
?? Scene-12-6.png
?? Scene-12-7.png
```

**Recent commits:**
```
c35a668 chore: auto-update handoff snapshot [2026-05-21 11:07]
396e733 chore: auto-update handoff snapshot [2026-05-21 11:02]
d9f7881 chore: auto-update handoff snapshot [2026-05-21 11:00]
edb798c chore: auto-update handoff snapshot [2026-05-21 10:57]
2f889f0 chore: auto-update handoff snapshot [2026-05-21 10:54]
```

**In-progress tickets:**
```
BSA-yhol [in_progress] - Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->
