# Handoff

_Last updated: 2026-05-02 by Claude (claude-sonnet-4-6)_

## Prompt Rules

**Read [`PROMPT-LEARNINGS.md`](PROMPT-LEARNINGS.md) before writing or refining any image generation prompt.**
Update it whenever a new pattern is confirmed or a dead end is discovered — this is the shared knowledge base for all agents on this project.

---

## Current Focus
Baglamukhi Sadhana Anubhav video — script completion before generating more images. Scenes 1–5 prompts are ready; remaining scenes (outcome, court case resolution, divine intervention) need to be written first.

## In Progress
- `Bagla-Sadhana-Anubhav.md`: Scenes 1–5 fully prompted, character refs locked, some scene images generated
- Script incomplete — remaining scenes (the actual story outcome) not yet written

## Recent Decisions
- **`--cref` replaces `--sref`** throughout all scene prompts — character face lock, not style lock
- **Three character refs now locked** and committed:
  - `Mata-Baglamukhi.png` → MAA_REF (blessing pose)
  - `Sadhak_A_Ref.png` → SADHAK_A_REF (white kurta, State A — Scene-1 img 2 and Scene-2 imgs 1,3)
  - `Sadhak_B_Ref.png` → SADHAK_B_REF (yellow dhoti, State B — Scenes 3–5)
- **cref upload via MidJourney web UI** — remove `--cref NAME` text from prompt, upload image via Character References button, keep `--cw 80` in prompt text
- **Back-facing sadhak scenes** (Scene-1 imgs 1 and 3): upload MAA_REF only — no sadhak cref since his face is never seen
- **Scene-1 Image #3** is the thumbnail (cinematic 3D style); Scene-1 Image #1 is the in-video folk style version of the same shot
- **Script-first decision**: stop generating images until remaining scenes are written — the outcome/court case/divine intervention scenes are where viewer engagement lives
- Jinn-Masoom competitor analysis added to Competitor-Analysis.md — key finding: MidJourney v6 `--cref` is how they lock character faces across 230+ scene cards

## Dead Ends
- `--sref` for character identity — wrong tool, causes deity drift and costume override
- Two character `--cref` refs in same prompt for back-facing sadhak scenes — caused sadhak to absorb Maa's divine appearance
- `--sw 60` style weight — too high, overrides composition; use `--sw 20` max or drop entirely

## Generated so far (committed)
- Scene-1: `Scene-1-1-2.png` (one approved variant)
- Scene-2: `Scene-2-1.png`, `Scene-2-2.png`, `Scene-2-3-1.png`, `Scene-2-3-2.png`

## Next Steps
1. **Finish writing remaining script scenes** (Hindi + English) — especially outcome scenes: court case resolution, adversaries rendered helpless, devotee's gratitude
2. **Add prompts for new scenes** to `Bagla-Sadhana-Anubhav.md`
3. **Review full script arc** with Claude — critique hook strength, pacing, tension beats, payoff
4. **Then resume image generation** starting with hook scene (thumbnail candidate) and outcome scenes
5. Untracked scratch file `Sadhak-Backwards.jpg` — decide whether to keep or delete

<!-- HANDOFF-SNAPSHOT:START 2026-05-04 09:56 branch:main -->
**Modified files:**
```
 M Bagla-Sadhana-Anubhav.md
?? PROMPT-LEARNINGS.md
```

**Recent commits:**
```
aeb030b chore: auto-update handoff snapshot [2026-05-04 09:56]
707c3bf chore: auto-update handoff snapshot [2026-05-04 09:52]
0225aef chore: auto-update handoff snapshot [2026-05-04 09:51]
80ffbb6 chore: auto-update handoff snapshot [2026-05-04 09:50]
7a05855 chore: auto-update handoff snapshot [2026-05-04 09:49]
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-04 09:56 branch:main -->
**Modified files:**
```
 M Bagla-Sadhana-Anubhav.md
?? PROMPT-LEARNINGS.md
```

**Recent commits:**
```
707c3bf chore: auto-update handoff snapshot [2026-05-04 09:52]
0225aef chore: auto-update handoff snapshot [2026-05-04 09:51]
80ffbb6 chore: auto-update handoff snapshot [2026-05-04 09:50]
7a05855 chore: auto-update handoff snapshot [2026-05-04 09:49]
99ea265 chore: auto-update handoff snapshot [2026-05-04 09:48]
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->
