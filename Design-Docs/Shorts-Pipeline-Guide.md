# Shorts Production Pipeline

Step-by-step guide for producing TikTok/YouTube Shorts using `youtube-shorts.sh`.

The pipeline takes a markdown file with only a `## Script` section and produces a final 9:16 MP4 through four gated phases. Each phase creates a `tk` ticket; nothing moves forward until you approve.

---

## Prerequisites

- OpenMontage repo set up (`make setup` run at least once)
- `.venv/` exists (Python environment)
- `npx` available (for HyperFrames render in Phase 4)
- Optional: API keys in `.env` for AI generation (Kling, Seedance, fal.ai, etc.)

---

## Phase 0 — Create your markdown file

Create a folder and markdown file under `Design-Docs/ToPublish/Shorts/`:

```
Design-Docs/ToPublish/Shorts/
  my-short-name/
    my-short-name.md       ← you create this
```

The markdown only needs a `## Script` section to start:

```markdown
# My Short Title

## Script

Hook: The line that stops the scroll.

Body:
Fact 1 — ...
Fact 2 — ...
Fact 3 — ...

Close: The resonant closing line.

CTA: Follow for more.
```

Alternatively, run `--scenes` without the file and the script scaffolds the folder and a blank markdown for you.

---

## Phase 1 — Generate scene breakdown (`--scenes`)

```bash
./youtube-shorts.sh my-short-name --scenes
# or
make shorts-scenes NAME=my-short-name
```

**What happens:**
- The agent reads your `## Script` section
- Applies competitor cadence rules (motion-light montage, 4–6s holds, max 90s total)
- Writes a full `## Scenes` section to your markdown with one `### Scene-N` block per beat
- Creates a `tk` ticket tagged `shorts,scenes`

**Each scene block contains:**
```markdown
### Scene-3
Script beat: At the very center is Kali's bija mantra — Krim
Duration: 4s
Visual: Yantra close-up, crimson glow, bija text floats in
Camera: Slow push-in to center
Motion Recipe: center-grow yantra reveal, glow pulse, text fade-up
Prompts:
  MidJourney: '/imagine sacred yantra crimson glow dark bg --ar 9:16 --v 6'
  Kling I2V: 'gentle pulse from center outward, divine light'
Artifacts:
  - scene-3-bg.png
  - scene-3-hero.mp4
Status: DRAFT
```

**Your job:** Review the scenes in the markdown. Discuss with the agent to adjust timing, visual descriptions, or motion recipes. When satisfied, close the scenes ticket and move to Phase 2.

**Key rules the agent applies:**
- Hook: 4–5s, strong provocation or mystery
- Body scenes: 4–6s each (reverent/devotional pace)
- Close: 4–5s, resonant
- CTA: 3–4s (optional)
- Total must stay under 90s — agent tightens body holds if needed
- Hero clips (true AI-generated video) only for opener and 1–2 peak moments; rest are animated stills

---

## Phase 2 — Write artifact prompts (`--artifacts`)

```bash
./youtube-shorts.sh my-short-name --artifacts
# or
make shorts-artifacts NAME=my-short-name
```

**What happens:**
- The agent reads each `### Scene-N` block
- Finalizes and sharpens every prompt (MidJourney, DrawThings, Kling, Seedance)
- Appends an `## Artifact Status` table to the markdown
- **No API calls are made** — prompts only, all artifacts stay PENDING
- Creates a `tk` ticket tagged `shorts,artifacts` dependent on the scenes ticket

**Artifact Status table example:**
```markdown
## Artifact Status

| Scene | File | Tool | Status |
|---|---|---|---|
| 1 | scene-1-bg.png | MidJourney | PENDING (manual — run prompt in MidJourney web) |
| 1 | scene-1-hero.mp4 | Kling | PENDING (run --generate-clips) |
| 2 | scene-2-bg.png | MidJourney | PENDING (manual) |
| 3 | scene-3-bg.png | Reuse | READY — Yantra-Energy.png |
```

**Your job:**
- Review all prompts — adjust wording, aspect ratios, style keywords as needed
- Note which tools are manual (MidJourney web, DrawThings GUI) vs automated (`--generate-clips`)
- For `Reuse` rows: confirm the referenced file is the right one
- When satisfied with all prompts, proceed to Phase 3

---

## Phase 3 — Generate artifacts (`--generate-clips` + manual tools)

### 3a — API-backed clips (automated)

```bash
./youtube-shorts.sh my-short-name --generate-clips
# or
make shorts-generate-clips NAME=my-short-name
```

Calls Kling, Seedance (fal.ai), or image gen APIs for all `PENDING (run --generate-clips)` rows. Requires the relevant keys in `.env`. DrawThings and MidJourney rows are skipped (manual only).

Artifact Status updates to `GENERATED ✓` on success or `FAILED — <reason>` on error.

### 3b — Manual tools

**MidJourney:** Copy the `/imagine` prompt from the markdown, run it in MidJourney web or Discord, download the result, and drop it into `Design-Docs/ToPublish/Shorts/my-short-name/` with the exact filename from the Artifacts line.

**DrawThings:** Copy the prompt and settings from the markdown. In the DrawThings app, load `SkyReels v2 I2V 14B 720p`, paste the prompt, apply the settings (strength ~70%, 49 frames), and export to the Shorts folder.

**After dropping files in:** Tell the agent "artifacts for scene N are in the folder" — it will update the status table.

### What to check before Phase 4

- Every `scene-N-bg.png` exists
- Every `scene-N-hero.mp4` exists (for scenes that need true motion)
- All `## Artifact Status` rows are `GENERATED ✓` or `READY`
- Voiceover file placed in `Design-Docs/ToPublish/Shorts/my-short-name/Renders/` (see below)

---

## Voiceover (required before Phase 4)

Phase 4 enforces **voiceover-first** — the render is blocked without a narration audio file.

Place your voiceover in:
```
Design-Docs/ToPublish/Shorts/my-short-name/Renders/<any-name>.mp3
```

Options for generating voiceover:
- **HyperFrames TTS (free, local):** `npx hyperframes tts script.txt --voice af_nova --output Renders/narration.wav`
- **ElevenLabs:** preferred for reusable branded voice
- **Piper TTS:** `make install` includes piper-tts; run via Python

---

## Phase 4 — Render (`--rendershorts`)

```bash
./youtube-shorts.sh my-short-name --rendershorts
# or
make shorts-render NAME=my-short-name
```

**What happens (if `composition.html` already exists):**
1. Shell checks for voiceover — blocks with a clear error if missing
2. Calls `npx hyperframes render composition.html --output Renders/my-short-name-captioned-v1.mp4 --profile tiktok_vertical --quality high --fps 30`

**What happens (first run, no `composition.html` yet):**
1. Shell hands off to the agent
2. Agent builds the HyperFrames HTML composition from the scenes markdown (scenes, timing, text animations, audio sync)
3. Once `composition.html` is written, re-run `--rendershorts` to render

**Output:** `Design-Docs/ToPublish/Shorts/my-short-name/Renders/my-short-name-captioned-v1.mp4`

**QC checklist after render:**
- Duration matches sum of scene durations
- Captions sync with narration
- No silent gaps or audio pops
- Safe zone: text stays within the center 80% of frame (avoid top 15% and bottom 20% — TikTok UI overlay zones)
- Aspect ratio is 9:16 (1080×1920)

---

## Ticket lifecycle

```
tk ls                           # see all open tickets
tk show <id>                    # inspect a ticket
tk close <id>                   # close after approval
tk dep tree <id>                # see dependency chain
```

Dependency chain created automatically:
```
scenes-ticket
  └── artifacts-ticket
        └── render-ticket
```

Close tickets bottom-up after each approval phase.

---

## Quick reference

| Action | Command |
|---|---|
| Start a new short | `./youtube-shorts.sh <folder> --scenes` |
| Write artifact prompts | `./youtube-shorts.sh <folder> --artifacts` |
| Generate API clips | `./youtube-shorts.sh <folder> --generate-clips` |
| Render final MP4 | `./youtube-shorts.sh <folder> --rendershorts` |
| Inspect all Shorts folders | `./youtube-shorts.sh --gen-shorts` |
| Review scene MP4s | `./youtube-shorts.sh --gen-mp4` |
| Full help | `./youtube-shorts.sh --help` |

Makefile equivalents: `make shorts-scenes NAME=<folder>`, `make shorts-artifacts NAME=<folder>`, etc.

---

## File layout for a completed short

```
Design-Docs/ToPublish/Shorts/my-short-name/
  my-short-name.md          ← source of truth (Script + Scenes + Artifact Status)
  composition.html          ← HyperFrames composition (written by agent in Phase 4)
  scene-1-bg.png
  scene-1-hero.mp4
  scene-2-bg.png
  ...
  Renders/
    narration.mp3           ← voiceover (you supply)
    my-short-name-captioned-v1.mp4   ← final output
```
