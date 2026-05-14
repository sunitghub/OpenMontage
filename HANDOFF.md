# Handoff

_Last updated: 2026-05-08 by Claude (claude-sonnet-4-6)_

## Current Focus
Baglamukhi Sadhana Anubhav long-form video. Scenes 1–4 complete with narration. Scene-5 images and narration generated, uncommitted. Next: commit Scene-5, then write outcome scenes 6–8.

## In Progress
- `BaglaMukhi-Sadhana-Anubhav` — Scene-5 has uncommitted updates (see subfolder HANDOFF.md for detail)
- Outcome scenes 6–8 not yet written

## Recent Decisions
- **GPT-4o for all image generation** — MidJourney abandoned after 14+ failed rounds on deity iconography constraints
- **render-scene CLI** — `render-scene --scene N` auto-resolves `Scene-N.mp3`; `--vintage` on by default; `--all` renders and concatenates in numeric order
- **Stack confirmed**: GPT-4o for stills + Replicate Seedance for I2V hero clips (~$0.90/5s via `bytedance/seedance-2.0`)
- **Replicate over Kling** — Kling subscription burns credits too fast

## Dead Ends
- `seedance-2.0-fast` on Replicate → 402 on standard billing tier, don't use
- Kling $10/mo subscription → credits exhausted too fast
- `boxblur luma_radius` starting at 0 → ffmpeg abort; must start ≥ 1

## Setup
- `REPLICATE_API_TOKEN` in `OpenMontage/.env`
- GPT-4o / ChatGPT: manual workflow — run prompts in browser, drop files into project folder
- `render-scene` symlinked to `~/bin` — callable from anywhere

## Key Files
- Render script: `bin/render_scene.py`
- Script + image prompts: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md`
- Prompt learnings: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/PROMPT-LEARNINGS.md`
- Scene-level handoff: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/HANDOFF.md`
- Competitor analysis: `Design-Docs/Competitors/Competitor-Analysis.md`

<!-- HANDOFF-SNAPSHOT:START 2026-05-14 17:15 branch:main -->
**Modified files:**
```
 M AGENTS.md
 M CLAUDE.md
 M Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md
?? .tickets/BSA-yhol.md
?? Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Scene-7.mp3
```

**Recent commits:**
```
597d23e chore: auto-update handoff snapshot [2026-05-14 17:15]
1d1dd10 chore: auto-update handoff snapshot [2026-05-14 17:11]
c686e8d chore: auto-update handoff snapshot [2026-05-14 17:09]
c859a8c chore: auto-update handoff snapshot [2026-05-12 17:45]
a55b98f chore: auto-update handoff snapshot [2026-05-12 17:45]
```

**In-progress tickets:**
```
BSA-yhol [in_progress] - Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-14 17:15 branch:main -->
**Modified files:**
```
 M AGENTS.md
 M CLAUDE.md
 M Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md
?? .tickets/BSA-yhol.md
?? Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Scene-7.mp3
```

**Recent commits:**
```
1d1dd10 chore: auto-update handoff snapshot [2026-05-14 17:11]
c686e8d chore: auto-update handoff snapshot [2026-05-14 17:09]
c859a8c chore: auto-update handoff snapshot [2026-05-12 17:45]
a55b98f chore: auto-update handoff snapshot [2026-05-12 17:45]
129bd44 fix: remove two-arms-only constraint from Maa Baglamukhi portrait prompts
```

**In-progress tickets:**
```
BSA-yhol [in_progress] - Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->
