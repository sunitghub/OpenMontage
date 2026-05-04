# Handoff

_Last updated: 2026-05-02 by Claude (claude-sonnet-4-6)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Scene-3 image generation — Scenes 1–2 fully imaged and committed. Thumbnail locked. Remaining scenes (3–5 images, plus outcome scenes not yet written) are next.

## In Progress
- `Bagla-Sadhana-Anubhav.md`: Scenes 1–5 fully prompted, character refs locked
- Script incomplete — outcome scenes (court case resolution, adversaries rendered helpless, devotee's gratitude) not yet written

## Recent Decisions
- **Scene-1-3.png approved as thumbnail** — cinematic 3D style, no cref used, glowing arch framing Maa. See PROMPT-LEARNINGS.md → Thumbnail Composition section for full lessons from 14-round iteration.
- **`--cref` replaces `--sref`** throughout all scene prompts — character face lock, not style lock
- **Three character refs locked** and committed:
  - `Mata-Baglamukhi.png` → MAA_REF (blessing pose)
  - `Sadhak_A_Ref.png` → SADHAK_A_REF (white kurta, State A — Scene-1 img 2 and Scene-2 imgs 1,3)
  - `Sadhak_B_Ref.png` → SADHAK_B_REF (yellow dhoti, State B — Scenes 3–5)
- **cref upload via MidJourney web UI** — remove `--cref NAME` text from prompt, upload image via Character References button, keep `--cw 80` in prompt text

## Dead Ends
- See `PROMPT-LEARNINGS.md` for full record — cref bleeding, multi-arm negatives, floating Maa failures, primary/secondary subject labels, all documented there.

## Generated so far (committed)
- Scene-1: `Scene-1-1-2.png` (folk style, in-video), `Scene-1-2.png` (guru scene), `Scene-1-3.png` (thumbnail ✓)
- Scene-2: `Scene-2-1.png`, `Scene-2-2.png`, `Scene-2-3-1.png`, `Scene-2-3-2.png`
- Videos: `Scene-1-1-Vid.mp4`, `Scene-1-2-Vid.mp4`, `Scene-2-1.mp4`, `Scene-2-3.mp4`

## Next Steps
1. **Generate Scene-3 images** — 2 prompts ready in script, SADHAK_B_REF only
2. **Generate Scene-4 and Scene-5 images** — prompts ready
3. **Write remaining outcome scenes** (Hindi + English) — court case resolution, adversaries helpless, devotee's gratitude
4. **Review full script arc** — hook strength, pacing, tension beats, payoff

<!-- HANDOFF-SNAPSHOT:START 2026-05-04 10:17 branch:main -->
**Modified files:**
```
 M Scene-1-3.png
?? Scene-3-1.png
```

**Recent commits:**
```
e981a8b chore: auto-update handoff snapshot [2026-05-04 10:16]
fbbe652 chore: auto-update handoff snapshot [2026-05-04 10:15]
0208da2 chore: auto-update handoff snapshot [2026-05-04 10:12]
6a7cde1 chore: auto-update handoff snapshot [2026-05-04 10:12]
f191f88 feat: approve Scene-1-3 thumbnail, add PROMPT-LEARNINGS
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-04 10:16 branch:main -->
**Modified files:**
```
 M Scene-1-3.png
?? Scene-3-1.png
```

**Recent commits:**
```
fbbe652 chore: auto-update handoff snapshot [2026-05-04 10:15]
0208da2 chore: auto-update handoff snapshot [2026-05-04 10:12]
6a7cde1 chore: auto-update handoff snapshot [2026-05-04 10:12]
f191f88 feat: approve Scene-1-3 thumbnail, add PROMPT-LEARNINGS
e22ea36 chore: auto-update handoff snapshot [2026-05-04 10:03]
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->
