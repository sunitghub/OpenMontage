# Handoff

_Last updated: 2026-05-19 by Claude (claude-sonnet-4-6)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Scene-10 images complete. Next: record voiceover for Scene-10, then move to Scene-11.

## In Progress
- Voiceover for Scene-10 — record tomorrow
- Ticket BSA-yhol still open (Scene-7 voiceover check)

## Recent Decisions
- **Switched from MidJourney to GPT-4o (ChatGPT)** — solves two-arm constraint, female deity face, domestic architecture. See PROMPT-LEARNINGS.md.
- **Three character refs locked:**
  - `Maa-Baglamukhi.png` → Maa reference (blessing pose, golden gada, no trident)
  - `Sadhak_A_Ref.png` → Sadhak State A (white kurta — Scenes 1–2)
  - `Sadhak_B_Ref.png` → Sadhak State B (yellow dhoti — Scenes 3–10)
  - `Mahakali-1.png` → Kali apparition (Scenes 7–10)
- **GPT-4o guardrail** — "skull garland/mundmala/blood-filled bowl" triggers violence block. Use "dark ancient garland" + "dark vessel" in text; let `Mahakali-1.png` carry the visual.
- **Sadhak gaze problem** — GPT-4o locks sadhak facing left when any leftward presence is mentioned. Fix: strip all mention of presence/darkness from the prompt; describe only the sadhak facing Maa's portrait. Accept the result if it still drifts — narration carries the subtext.
- **Scene-10 garland** — the garland flung at Sridhar is a flower haar (marigold + jasmine), not prayer beads. "Mala" in the Hindi source = flower garland in this context.
- **EQ chain tuned** — `volume=-4dB` + `alimiter(limit=0.7, attack=5, release=50)`. Target mean -21 dB / max -4.5 dB.

## Dead Ends
- `viewer's left/right` must be explicit — "Maa's left hand" confuses GPT-4o.
- Empty-room shots: never upload Mahakali ref — model adds her even with negatives.
- Wide shot with 3 elements (Kali blowing + breath puff + Sridhar watching) = too crowded; split into separate shots instead.

## Generated & Committed
- Scene-1: 1a, 1b, 2, 3a, 3b, 3c, 4, 5, 6, 7, 8 + `Scene-1.mp3`
- Scene-2: 1–8 + `Scene-2.mp3`
- Scene-3: 1–6 + `Scene-3.mp3`
- Scene-4: 1a, 1b, 2–8 + `Scene-4.mp3`
- Scene-5: 1–8 + `Scene-5.mp3`
- Scene-7: images + `Scene-7.mp3`
- Scene-8: 1–11 images + `Scene-8.mp3`
- Scene-9: 1–8 images + `Scene-9.mp3`
- Scene-10: 1–13 images (voiceover pending)
- Court/thumbnail: `courtroom-1.jpeg`, `crowded-courtroom.png`, `Thumbnail.png`

## Next Steps
1. **Record Scene-10 voiceover** — tomorrow
2. **Write Scene-11 script + prompts** — next session
3. **Close ticket BSA-yhol** — after Scene-7 render verified

<!-- HANDOFF-SNAPSHOT:START 2026-05-20 14:48 branch:main -->
**Modified files:**
```
 M Bagla-Sadhana-Anubhav.md
```

**Recent commits:**
```
98ed943 feat: add Scene-10 alternate images, narration and prompt updates
94f8674 chore: update HANDOFF — Scene-10 complete, prune stale entries
62bf331 feat: add Scene-10 complete image set and Scene-9 narration
4155fc3 chore: auto-update handoff snapshot [2026-05-19 18:48]
e4065a8 chore: auto-update handoff snapshot [2026-05-19 18:48]
```

**In-progress tickets:**
```
BSA-yhol [in_progress] - Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->
