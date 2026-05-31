# Handoff

_Last updated: 2026-05-31 by Claude (claude-sonnet-4-6)_

## Current Focus
Tara Sadhana Anubhav — Scene-1 complete. Scene-2 scripts and images next.

## In Progress
- `BaglaMukhi-Sadhana-Anubhav` — Scene-7 voiceover needs recording and rendered video check (ticket BSA-yhol)
- `Tara-Sadhana-Anubhav` — Scene-1 all 11 images approved and saved; Scene-2+ scripts and images pending

## Recent Decisions
- **GPT-4o for all image generation** — MidJourney abandoned after 14+ failed rounds on deity iconography constraints
- **render-scene CLI** — `render-scene --scene N` auto-resolves `Scene-N.mp3`; `--vintage` on by default; `--all` renders and concatenates in numeric order
- **Stack confirmed**: GPT-4o for stills + Replicate Seedance for I2V hero clips (~$0.90/5s via `bytedance/seedance-2.0`)
- **Replicate over Kling** — Kling subscription burns credits too fast
- **Character bible fully locked** — refs approved: `TaraMaa.png`, `Sadhak-A.jpg`, `Sadhak-B.jpg`, `Guru-Ref.jpg`, `Room-Ref.jpg`, `Yantra-Ref.jpg`
- **GPT-4o painterly style won't hold for rice/room scenes** — photorealistic accepted for images 9–11; "NOT photorealistic" directive ignored consistently
- **Maa Tara Signifies section** added to Character Bible and Script English (four arms iconography) — reads over Image #1
- **Sadhak-A** = Ravi in everyday clothes; **Sadhak-B** = Ravi in pink sadhana attire (pink dhoti + shawl + rudraksha)
- **Guru** = handlebar mustache, no beard, saffron cloth, rudraksha mala, red tilak
- **Room** = modern 2020s Indian apartment, rose-pink walls, ceramic tiles, LED ceiling light, glass window
- **Yantra** = GPT-4o refused "Sanskrit bija mantras" in prompt — use geometric description only; `Yantra-Ref.jpg` carries the structure
- **Prompt format** — refs listed as `> Refs: X + Y` under image title, not inline in prompt text

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
- **Tara character bible ref**: `Design-Docs/ToPublish/Videos/Tara-Sadhana-Anubhav/TaraMaa.png`
- Baglamukhi script + prompts: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md`
- Prompt learnings: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/PROMPT-LEARNINGS.md`
- Competitor analysis: `Design-Docs/Competitors/Competitor-Analysis.md`

## Next Steps
1. Tara Scene-1: record voiceover → `render-scene --scene 1` → check output
2. Tara: write Hindi + English scripts for Scene-2 onwards, then generate image prompts
3. Baglamukhi: record Scene-7 voiceover → `render-scene --scene 7` → check output

<!-- HANDOFF-SNAPSHOT:START 2026-05-31 01:09 branch:main -->
**Modified files:**
```
 D Scene-1-1.png
A  Scene-1-10.png
A  Scene-1-11.png
A  Scene-1-8.png
A  Scene-1-9.png
 D Tara-Maa-3.jpg
M  TaraAnubhav.md
A  Yantra-Ref.png
M  ../../../../HANDOFF.md
?? Thumbnail.png
```

**Recent commits:**
```
04f1f83 chore: auto-update handoff snapshot [2026-05-31 01:03]
92147b2 chore: auto-update handoff snapshot [2026-05-31 01:02]
0996259 chore: auto-update handoff snapshot [2026-05-31 01:01]
cec8814 chore: auto-update handoff snapshot [2026-05-31 01:00]
15dd8d8 chore: auto-update handoff snapshot [2026-05-31 00:59]
```

**In-progress tickets:**
```
BSA-yhol    in_progress   task      p1  Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-31 01:03 branch:main -->
**Modified files:**
```
 D Scene-1-1.png
 D Tara-Maa-3.jpg
 M TaraAnubhav.md
?? ../Scene-1-8.png
?? Scene-1-10.png
?? Scene-1-9.png
?? Thumbnail.png
?? Yantra-Ref.png
```

**Recent commits:**
```
92147b2 chore: auto-update handoff snapshot [2026-05-31 01:02]
0996259 chore: auto-update handoff snapshot [2026-05-31 01:01]
cec8814 chore: auto-update handoff snapshot [2026-05-31 01:00]
15dd8d8 chore: auto-update handoff snapshot [2026-05-31 00:59]
19ba00a chore: auto-update handoff snapshot [2026-05-31 00:58]
```

**In-progress tickets:**
```
BSA-yhol    in_progress   task      p1  Record voiceover for Scene-7 and check rendered video
```
<!-- HANDOFF-SNAPSHOT:END -->
