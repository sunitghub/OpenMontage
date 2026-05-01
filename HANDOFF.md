# Handoff

_Last updated: 2026-04-23 by Codex (gpt-5)_

## Current Focus
Remotion vertical caption safe-zone adjustment is implemented, committed, and pushed.
Vertical captions now default narrower so they do not compete with Shorts/TikTok-style
right-side action icons.

## In Progress
- Ope-oqbu [in_progress] — Adjust vertical caption width safe zone

## Recent Decisions
- **Vertical caption width** — `CaptionOverlay` now defaults to `68%` max width on vertical
  compositions and keeps `80%` on landscape. Render configs can still override `maxWidth`.
- **Follow-up handoff commit** — `HANDOFF.md` was updated for session continuity and
  `.agents/skills/synthetic-screen-recording/SKILL.md` received skill metadata frontmatter.
- **Replicate over Kling subscription** — Kling $10/mo burned credits too fast on 10s generations. Replicate pay-per-use at ~$1.50/clip (standard Seedance 2.0) is better for low volume.
- **seedance-2.0-fast is unavailable** on standard Replicate billing tier. `seedance_replicate.py` now hardcoded to `bytedance/seedance-2.0` (standard). Fast variant gave 402 Payment Required.
- **Stack confirmed**: MidJourney $10/mo for stills + Replicate pay-per-use for I2V hero clips. Target $5/Short = 3 I2V clips at 5s each.
- **Motion-light montage** is the format — 70-80% animated stills (free in HyperFrames), 2-3 Seedance I2V hero clips per Short.

## Last Completed
- Commit pushed to `origin/main`: `f0d970f Ope-oqbu: adjust vertical caption width`
- Files changed:
  - `remotion-composer/src/components/CaptionOverlay.tsx`
  - `remotion-composer/src/Explainer.tsx`
  - `remotion-composer/src/CinematicRenderer.tsx`
  - `remotion-composer/src/cinematic/types.ts`
  - `.tickets/Ope-oqbu.md`
- Visual check rendered successfully:
  `projects/maa-kali-5-yantra-facts-short/renders/caption-width-v15-check.png`

## Verification
- `git diff --check` passed for the caption source changes.
- Remotion still render succeeded for the affected "It's much deeper..." caption frame.
- `npx tsc --noEmit` still fails on pre-existing unrelated type errors in
  `ProviderChip`, `Root`, `TitledVideo`, and existing `Explainer` overlay props.

## Current Working Tree
- Expected clean after the handoff follow-up commit is pushed.
- The ignored generated project artifact
  `projects/maa-kali-5-yantra-facts-short/artifacts/edit_decisions.voiceover-english-captions-v1.json`
  has local `captionsConfig.maxWidth = "68%"`, but `projects/` is gitignored. The
  committed source now carries the same vertical default.

## Dead Ends
- `seedance-2.0-fast` on Replicate → 402 on standard billing tier, don't use
- Kling $10/mo subscription → credits exhausted too fast for 10s generations

## Next Steps
1. Resume by checking `git status --short`.
2. If the caption task is approved, run the ticket approve workflow for `Ope-oqbu`
   rather than closing it directly.
3. If rendering the final Short again, use the pushed Remotion source; no generated
   project artifact needs to be committed.

## Setup
- `REPLICATE_API_TOKEN` is in `OpenMontage/.env` (rotated 2026-04-23, $10 credits loaded)
- MidJourney: manual workflow — run prompts in web, drop files into Shorts folder
- HyperFrames TTS: free voiceover — `npx hyperframes tts script.txt --voice af_nova --output Renders/narration.wav`

## Key Files
- Blissful strategy guide: `Design-Docs/Blissful-Strategy.md`
- Canon skill (scene rules + prompt templates): `~/Developer/canon/skills/shorts-director.md`
- I2V tool: `tools/video/seedance_replicate.py`
- Test clip output: `Design-Docs/ToPublish/Shorts/Maa-Kali-5-Unknown-Facts/Renders/test-replicate-i2v.mp4`

<!-- HANDOFF-SNAPSHOT:START 2026-05-01 15:32 branch:main -->
**Modified files:**
```
 M Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md
?? Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav-Design.md
?? Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Maa-Baglamukhi-Anushthan.jpg
```

**Recent commits:**
```
a8b8878 chore: auto-update handoff snapshot [2026-05-01 15:31]
a84f818 chore: auto-update handoff snapshot [2026-05-01 15:27]
9bfef9e chore: auto-update handoff snapshot [2026-05-01 15:26]
a4133f5 chore: remove unused agent config files, fix whitespace
a45cc22 feat(scripts): add scenes 2-5 to BaglaMukhi Sadhana video, fix CLAUDE.md imports
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->

<!-- HANDOFF-SNAPSHOT:START 2026-05-01 15:31 branch:main -->
**Modified files:**
```
 M Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav.md
?? Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Bagla-Sadhana-Anubhav-Design.md
?? Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav/Maa-Baglamukhi-Anushthan.jpg
```

**Recent commits:**
```
a84f818 chore: auto-update handoff snapshot [2026-05-01 15:27]
9bfef9e chore: auto-update handoff snapshot [2026-05-01 15:26]
a4133f5 chore: remove unused agent config files, fix whitespace
a45cc22 feat(scripts): add scenes 2-5 to BaglaMukhi Sadhana video, fix CLAUDE.md imports
ad8b5c8 chore: auto-update handoff snapshot [2026-04-29 18:53]
```

**In-progress tickets:**
```
Ope-oqbu [in_progress] - Adjust vertical caption width safe zone
```
<!-- HANDOFF-SNAPSHOT:END -->
