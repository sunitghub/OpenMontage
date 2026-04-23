# Handoff

_Last updated: 2026-04-23 by Claude (claude-sonnet-4-6)_

## Current Focus
Replicate I2V integration validated; pipeline is production-ready for devotional Shorts.

## In Progress
- Ope-lnxy [in_progress] — Create TikTok-style video from Maa Kali Shorts artifacts (first real Short pending)

## Recent Decisions
- **Replicate over Kling subscription** — Kling $10/mo burned credits too fast on 10s generations. Replicate pay-per-use at ~$1.50/clip (standard Seedance 2.0) is better for low volume.
- **seedance-2.0-fast is unavailable** on standard Replicate billing tier. `seedance_replicate.py` now hardcoded to `bytedance/seedance-2.0` (standard). Fast variant gave 402 Payment Required.
- **Stack confirmed**: MidJourney $10/mo for stills + Replicate pay-per-use for I2V hero clips. Target $5/Short = 3 I2V clips at 5s each.
- **Motion-light montage** is the format — 70-80% animated stills (free in HyperFrames), 2-3 Seedance I2V hero clips per Short.

## Dead Ends
- `seedance-2.0-fast` on Replicate → 402 on standard billing tier, don't use
- Kling $10/mo subscription → credits exhausted too fast for 10s generations

## Next Steps
1. Open `Maa-Kali-5-Unknown-Facts/Renders/test-replicate-i2v.mp4` and check quality of the test clip
2. If quality is acceptable: proceed to run the full Maa Kali Short through the pipeline (`--rendershorts`)
3. When starting next Short: create folder + markdown with `## Script`, tell Claude "generate scenes for <folder>"
4. For I2V clips in `--generate-clips` phase: Replicate/Seedance is the confirmed provider

## Setup
- `REPLICATE_API_TOKEN` is in `OpenMontage/.env` (rotated 2026-04-23, $10 credits loaded)
- MidJourney: manual workflow — run prompts in web, drop files into Shorts folder
- HyperFrames TTS: free voiceover — `npx hyperframes tts script.txt --voice af_nova --output Renders/narration.wav`

## Key Files
- Pipeline guide: `Design-Docs/Shorts-Pipeline-Guide.md`
- Canon skill (scene rules + prompt templates): `~/Developer/canon/skills/shorts-director.md`
- I2V tool: `tools/video/seedance_replicate.py`
- Test clip output: `Design-Docs/ToPublish/Shorts/Maa-Kali-5-Unknown-Facts/Renders/test-replicate-i2v.mp4`

<!-- HANDOFF-SNAPSHOT:START 2026-04-22 20:29 branch:main -->
**Modified files:**
```
 M Design-Docs/Shorts-Pipeline-Guide.md
```

**Recent commits:**
```
556ed7c Validate Replicate I2V; fix fast-variant 402; update handoff
0ac140d chore: auto-update handoff snapshot [2026-04-22 20:23]
e385cbb chore: auto-update handoff snapshot [2026-04-22 20:22]
33d29af chore: auto-update handoff snapshot [2026-04-22 20:22]
efbf44b chore: auto-update handoff snapshot [2026-04-22 20:21]
```
<!-- HANDOFF-SNAPSHOT:END -->
