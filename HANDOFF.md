# Handoff

_Last updated: 2026-05-29 by Claude (claude-sonnet-4-6)_

## Current Focus
Two videos in flight: Baglamukhi (nearly done — Scene-7 voiceover pending) and Tara Sadhana Anubhav (just scaffolded — character bible established, no scenes written yet).

## In Progress
- `BaglaMukhi-Sadhana-Anubhav` — Scene-7 voiceover needs recording and rendered video check (ticket BSA-yhol)
- `Tara-Sadhana-Anubhav` — scaffolded; character bible image selected and verified; Script Hindi written for Scene-1 only; all scene images and narration pending

## Recent Decisions
- **GPT-4o for all image generation** — MidJourney abandoned after 14+ failed rounds on deity iconography constraints
- **render-scene CLI** — `render-scene --scene N` auto-resolves `Scene-N.mp3`; `--vintage` on by default; `--all` renders and concatenates in numeric order
- **Stack confirmed**: GPT-4o for stills + Replicate Seedance for I2V hero clips (~$0.90/5s via `bytedance/seedance-2.0`)
- **Replicate over Kling** — Kling subscription burns credits too fast
- **Tara character bible anchor** — `Tara-Maa-3.jpg` is the approved reference image; upload it when generating all scene images to maintain consistency

## Dead Ends
- `seedance-2.0-fast` on Replicate → 402 on standard billing tier, don't use
- Kling $10/mo subscription → credits exhausted too fast
- `boxblur luma_radius` starting at 0 → ffmpeg abort; must start ≥ 1

## Setup
- `REPLICATE_API_TOKEN` in `OpenMontage/.env`
- GPT-4o / ChatGPT: manual workflow — run prompts in browser, drop files into project folder
- `render-scene` symlinked to `~/bin` — callable from anywhere
- Emacs `om-utils.el` (`~/.emacs.d/om-utils.el`) — custom keybindings for this workflow:
  - `C-c o t` → `om/translate` — translates selection/line via qwen2.5:14b (ollama); output in `*Translation*` side buffer; re-open with `M-x switch-to-buffer RET *Translation*`
  - `C-c o p` → `om/image-prompts` — generates image prompts from selection → side buffer (for experimenting)
  - `C-c o P` → `om/scene-image-prompts` — scene-aware prompt gen → inserts numbered prompts directly under `#### Images` in the md file
  - `C-c o i` → `om/insert-at-marker` — manual insert at marker
  - `C-c o s` → `om/goto-scene` — jump to scene
  - `C-c o n` → `om/new-scene` — scaffold new scene block
  - `C-u 7 C-c o P` — generates 7 prompts instead of default 3
- Ollama must be running (`ollama serve`) for `om/translate` to work

## Key Files
- Render script: `bin/render_scene.py`
- **Tara script + prompts**: `Design-Docs/ToPublish/Videos/Tara-Sadhana-Anubhav/TaraAnubhav.md`
- **Tara character bible ref**: `Design-Docs/ToPublish/Videos/Tara-Sadhana-Anubhav/Tara-Maa-3.jpg`
- Baglamukhi script + prompts: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md`
- Prompt learnings: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/PROMPT-LEARNINGS.md`
- Competitor analysis: `Design-Docs/Competitors/Competitor-Analysis.md`

## Next Steps
1. Baglamukhi: record Scene-7 voiceover → `render-scene --scene 7` → check output
2. Tara: write Hindi scripts for Scene-2 onwards, then generate image prompts per scene
3. Tara: generate scene images in GPT-4o with `Tara-Maa-3.jpg` as reference

<!-- HANDOFF-SNAPSHOT:START 2026-05-30 07:54 branch:main -->
**Modified files:**
```
?? Scene-1-4.png
?? Scene-1-5.png
```

**Recent commits:**
```
f2fe951 chore: auto-update handoff snapshot [2026-05-30 07:39]
d71e711 chore(tara): add character bible images and approved scene-1 images
d352d98 chore: auto-update handoff snapshot [2026-05-30 07:33]
24e8495 refactor(tara): move refs to title line, clean inline refs from all scene-1 prompts
f40379f chore: auto-update handoff snapshot [2026-05-30 07:31]
```

**In-progress tickets:**
```
BSA-yhol    in_progress   task      p1  Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-30 07:39 branch:main -->
**Modified files:**
```
?? Scene-1-4.png
```

**Recent commits:**
```
d71e711 chore(tara): add character bible images and approved scene-1 images
d352d98 chore: auto-update handoff snapshot [2026-05-30 07:33]
24e8495 refactor(tara): move refs to title line, clean inline refs from all scene-1 prompts
f40379f chore: auto-update handoff snapshot [2026-05-30 07:31]
b1256cc chore: auto-update handoff snapshot [2026-05-30 07:28]
```

**In-progress tickets:**
```
BSA-yhol    in_progress   task      p1  Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->
