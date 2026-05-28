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

<!-- HANDOFF-SNAPSHOT:START 2026-05-27 19:56 branch:main -->
**Modified files:**
```
 M ../BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md
 D ../BaglaMukhi-Sadhana-Anubhav/Thumbnail-Final.jpg
?? ../BaglaMukhi-Sadhana-Anubhav/TrueStory-1.jpg
?? ./
```

**Recent commits:**
```
d37c0b4 chore: auto-update handoff snapshot [2026-05-27 19:52]
5d0bbd7 chore: auto-update handoff snapshot [2026-05-27 19:39]
79772bc chore: auto-update handoff snapshot [2026-05-27 19:36]
40062f9 chore: auto-update handoff snapshot [2026-05-27 19:31]
d2fead2 chore: auto-update handoff snapshot [2026-05-27 19:25]
```

**In-progress tickets:**
```
BSA-yhol    in_progress   task      p1  Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-27 19:52 branch:main -->
**Modified files:**
```
 M ../BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md
 D ../BaglaMukhi-Sadhana-Anubhav/Thumbnail-Final.jpg
?? ../BaglaMukhi-Sadhana-Anubhav/TrueStory-1.jpg
?? ./
```

**Recent commits:**
```
5d0bbd7 chore: auto-update handoff snapshot [2026-05-27 19:39]
79772bc chore: auto-update handoff snapshot [2026-05-27 19:36]
40062f9 chore: auto-update handoff snapshot [2026-05-27 19:31]
d2fead2 chore: auto-update handoff snapshot [2026-05-27 19:25]
4a329e7 chore: auto-update handoff snapshot [2026-05-27 19:17]
```

**In-progress tickets:**
```
BSA-yhol    in_progress   task      p1  Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->
