# Handoff

_Last updated: 2026-05-06 by Claude (claude-sonnet-4-6)_

## Current Focus
Baglamukhi Sadhana Anubhav long-form video — `render_scene.py` pipeline enhancements complete. Scenes 1–3 have narration and images. Next: render Scene-3 and work toward a full stitch.

## In Progress
- `BaglaMukhi-Sadhana-Anubhav` — image generation for Scene-3 (Scene-3-7.png, Scene-3-8.png exist untracked)
- Scene-3 narration: `Scene-3.mp3` exists untracked

## Recent Decisions
- **Vintage dust marks** — switched from block-hash rectangles to per-pixel ellipse distance formula with per-block shape selection (40% V-streak, 30% diagonal, 30% circle). Organic look matches competitor reference.
- **Zoom-burst effect** — `zoom_burst_end()` added to `render_scene.py`. Fires in last 0.5s before fade-to-black: 3.5x zoom, 15px blur ramp. Split at `total_dur - FADE_DUR - ZOOM_BURST_DUR` so burst fires on visible content. Enabled by default; disable with `--no-zoom-burst`.
- **Zoom-burst probability in `--all`** — 40% per scene (`ZOOM_BURST_PROB = 0.4`).
- **`--all` cleanup** — intermediate per-scene MP4s deleted after successful concat.
- **Insaan-Aatma competitor analysis** — real video hybrid (not pure AI), radial zoom-burst at 40–60% of cuts, audio clips at 0 dB (avoid). Added to `Competitor-Analysis.md`.
- **Replicate over Kling** — Kling subscription burns credits too fast. Replicate pay-per-use ~$0.90/5s clip via `bytedance/seedance-2.0`.
- **Stack confirmed**: MidJourney/GPT-4o for stills + Replicate Seedance for I2V hero clips.

## Dead Ends
- `seedance-2.0-fast` on Replicate → 402 on standard billing tier, don't use
- Kling $10/mo subscription → credits exhausted too fast
- `boxblur luma_radius` starting at 0 → ffmpeg abort; must start ≥ 1

## Next Steps
1. Commit untracked `Scene-3-7.png`, `Scene-3-8.png`, `Scene-3.mp3` if they're final.
2. Run `render-scene --scene 3` to render Scene-3.
3. Run `render-scene --all 1-3` to stitch Scenes 1–3 into a single preview.
4. Continue image generation for Scenes 4–8 (check `--critic` for pacing targets).

## Setup
- `REPLICATE_API_TOKEN` in `OpenMontage/.env`
- MidJourney / GPT-4o: manual workflow — run prompts, drop files into project folder
- `render-scene` symlinked to `~/bin` — callable from anywhere
- Narration audio EQ applied via `NARRATION_EQ` constant in `render_scene.py`

## Key Files
- Render script: `bin/render_scene.py`
- Script + image prompts: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md`
- Prompt learnings: `Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/PROMPT-LEARNINGS.md`
- Competitor analysis: `Design-Docs/Competitors/Competitor-Analysis.md`

