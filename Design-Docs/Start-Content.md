# Start Content — Devotional Anubhav Video Pipeline

Reference guide for the full content workflow from script to render. Updated: 2026-05-05.

---

## The Daily Loop (Two Steps)

**Step 1 — Write** a new scene (or extend an existing one) in the script MD.

**Step 2 — Say to any agent** (Claude, Codex, Pi):
```
Check [script name] for content generation
```

The agent runs `render-scene --critic`, updates every `### Critique` section, adds missing image prompts, and gives you a summary of what changed and what to do next.

**Then:** generate the flagged images in ChatGPT, repeat from Step 1 for the next scene.

That's it. Everything else in this document is reference detail.

---

## Overview

A devotional anubhav video (devotee experience testimonial) follows this pipeline:

```
Script → Critique → Image Prompts → Generate Images → Render → Publish
```

Each stage has a CLI tool and/or a skill that any agent (Claude, Codex, Pi) can invoke.

---

## Stage 1 — Script

### What goes in a script MD

Each video lives in its own folder under `Design-Docs/ToPublish/Videos/<VideoName>/`.
The script file is `<VideoName>.md` and contains:

- `# Deity:` and `# Title:` headers
- `## Character Bible` — reference image prompts for the deity and protagonist
- `## Scene-N:` sections, each containing:
  - **Hindi script text** (the narration)
  - `### English` — English translation
  - `### Artifacts` — image prompts under `#### Images`, video motion notes
  - `### Critique` — written by an agent after running `render-scene --critic`

### 8-beat anubhav story spine

Every episode must hit these beats in order:

| Beat | Name | What it covers |
|---|---|---|
| 1 | Hook | Tease the outcome upfront — crisis + divine resolution hinted |
| 2 | Devotee + crisis | Who is the sadhak, what impossible situation |
| 3 | Guru / practice | What mantra, sadhana, or stotra was prescribed and why |
| 4 | Ritual setup | Physical preparation, rules, materials |
| 5 | Active sadhana | The nightly/daily practice in detail |
| 6 | The experience | Vision, dream, sign, or inexplicable event |
| 7 | Resolution | How the crisis resolved through divine grace |
| 8 | Teaching close | What viewers can practice, mantra or stotra named |

Beat 1 (Hook) must open the video. If it's missing, viewers scroll past.

### Script file location convention

```
Design-Docs/ToPublish/Videos/
  BaglaMukhi-Sadhana-Anubhav/
    Bagla-Sadhana-Anubhav.md     ← script
    PROMPT-LEARNINGS.md          ← image generation notes for this project
    Scene-1-1.png                ← generated images
    Scene-1-2.png
    ...
    Renders/                     ← rendered MP4s go here
```

---

## Stage 2 — Critique

The critique stage checks: Does each scene hit the right story beat? Is the narration long enough for the planned images? Are images missing?

### One command does all the checking

```bash
render-scene --critic
```

Run from the project folder (where the script MD lives). Output:

**Table 1 — Story beats:**
```
Scene   Level          Story Beat
  ---------------------------------------------------------------
  1      High           Hook (Beat 1) — Devotee + Crisis (Beat 2 missing)
  2      Medium         Ritual Setup (Beat 4)
  ...
```

**Table 2 — Pacing:**
```
  Scene   Words   Narr    Prompted   Generated   Hold     Status
  ------------------------------------------------------------------
  1       40      28s     10         8           2.8s    ❌ Too fast
  2       62      44s     8          8           5.5s    ⚠  Below target
  3       78      55s     6          6           9.2s    ⚠  Slightly slow
  4       69      49s     6          4           8.2s    ⚠  Slightly slow
  5       64      45s     6          2           7.5s    ✓  Good
```

### Pacing targets (from competitor research)

| Status | Hold | Action |
|---|---|---|
| ❌ Too fast | < 5s | Expand narration, or reduce image count |
| ⚠ Below target | 5–6s | Add a sentence to narration |
| ✓ Good | 6–8s | No change needed |
| ⚠ Slightly slow | 8–10s | Add 1–2 images |
| ❌ Too slow | > 10s | Add images and/or tighten narration |

Competitor benchmarks: Charava-Bhootni **4.2s** median · Kumar-Aur-Chudail **5–8s** · Jinn-Masoom **6.0s** median.
Devotional anubhav target: **6–8s** (slower = more reverent).

### Writing / updating critique sections

After running `render-scene --critic`, tell any agent: **"critique the script"** or **"critique scene N"**.

The agent will:
1. Read the `--critic` output
2. Re-read the scene's Hindi text and image list
3. Write or replace the `### Critique` section in the standard format

**Critique section format:**
```markdown
### Critique

**Story Beat:** Hook (Beat 1)
**Level:** High

- **Issue label**: What is wrong and why it matters for viewer retention.
- **Fix**: Concrete suggestion — give the actual Hindi line when possible.

#### English (Suggested)

Rewritten English narration that resolves the issues. Written as the final
narration sounds, not as a description. Used as Hindi adaptation reference.
```

**Works from:** Claude Code, Codex, Pi — all read `devotional-producer` skill via AGENTS.md.

---

## Stage 3 — Image Prompts

Image prompts live inside each scene's `#### Images` section. Format:

```markdown
1.

   **Ref:** Upload `Sadhak_A_Ref.png`

   `painterly AI devotional illustration, Hindustani folk-story art style, ...`
```

### GPT-4o is the primary image tool

MidJourney was used in early sessions but abandoned. GPT-4o solved three blockers MidJourney couldn't:
- Two-arm constraint on Maa Baglamukhi
- Female deity face rendering
- Domestic architecture (vs. temple/palace drift)

### Reference upload rules

| Scene context | Upload | Reason |
|---|---|---|
| Sadhak's face visible, State A (white kurta) | `Sadhak_A_Ref.png` | Pre-ritual attire |
| Sadhak's face visible, State B (yellow dhoti) | `Sadhak_B_Ref.png` | Ritual attire, Scene 3 onward |
| Sadhak back-facing | `Maa-Baglamukhi.png` only | No face lock needed; two crefs causes character bleed |
| Maa floating above sadhak | `Maa-Baglamukhi.png` | Deity reference |
| Maa as subtle translucent presence | No reference | Text alone carries the ghostlike quality; reference overrides it |
| Object / insert shots (no people) | None | No reference needed |

### PROMPT-LEARNINGS.md

Every project folder has a `PROMPT-LEARNINGS.md`. **Read this before writing any prompt.** It contains confirmed patterns and dead ends specific to the project. Update it whenever a new pattern is confirmed or a technique fails.

Key rules currently confirmed for Baglamukhi Sadhana Anubhav:
- `exactly two arms only` is respected by GPT-4o — do not stack arm negatives
- For `courtroom scenes`: use the full colonial court vocabulary in the prompt
- `surgical edit rules` in PROMPT-LEARNINGS.md cover altar corrections (seven mounds, one clove each, gada side)

### File naming

```
Scene-{N}-{M}.png     standard: N = scene number, M = image number within scene
Scene-{N}-{M}-Final.png   use when replacing a draft with an approved version
Scene-{N}-0a.png      hook images prepended to scene N (keep existing numbering intact)
```

---

## Stage 4 — Generate Images

No CLI tool — generation happens manually in ChatGPT (GPT-4o):

1. Open a new ChatGPT conversation (or continue the last one for the same scene)
2. Upload the reference image(s) specified by `**Ref:** Upload ...` in the prompt entry
3. Paste the prompt from the `#### Images` section
4. Save the output as `Scene-N-M.png` in the project folder
5. Run `render-scene --critic` to update the `Generated` count

For surgical edits to existing images, use the rules in `PROMPT-LEARNINGS.md → Surgical edit rules (GPT-4o)`.

---

## Stage 4b — Record Narration (GarageBand)

### Setup

- One GarageBand project per scene. Name each project `Scene-N-Narration`.
- Add an **Audio** track (not Software Instrument). Select your mic as input.
- Set project sample rate to **44100 Hz** (GarageBand default — matches all competitors).
- Turn off the metronome and count-in before recording (they'll bleed in).

### Recording level

Watch the track meter while speaking. Aim for:
- **Peaks at -6 to -3 dBFS** on the GarageBand meter — loud enough to be clean, with headroom
- Never let the meter hit red (0 dB) — that's the clipping Jinn-Masoom has and it's audible

If your voice peaks below -12 dB, increase mic gain. If it's hitting -1 or 0 dB, reduce it.

### Add compression (prevents hot peaks)

In Smart Controls (B key), add the **Compressor** plugin on the vocal track:
- Preset: **"Narration"** if available, otherwise **"Podcast Voice"**
- Or manually: Ratio 3:1, Threshold -18 dB, Attack 10ms, Release 100ms

This evens out the dynamics so loud consonants don't spike while quiet phrases stay audible.

### Trim before export

GarageBand exports the full project length, not just where audio exists. Before exporting:
1. Drag the project end marker (top of the timeline, right edge) to just after the last word
2. Leave 0.5s of silence at the tail — ffmpeg uses it for the fade-out

### Export

**File > Share > Export Song to Disk**
- Format: **AAC** · Quality: **Highest** (gives ~256 kbps)
- Filename: `scene-N-narration.m4a`
- Save to the project folder alongside the scene images

### Check your levels after export

```bash
ffmpeg -i scene-1-narration.m4a -filter_complex volumedetect -f null - 2>&1 \
  | grep -E "mean_volume|max_volume"
```

**Target for raw narration (before music mix):** mean `-14 to -18 dB`, max `-3 to -6 dB`.

The final video (narration + music bed) should land at mean `-20 to -22 dB`. The music bed at `-18 to -20 dB` relative to the narration pulls the overall mix down to that target automatically.

### Competitor audio reference

| Competitor | Mean | Max | Quality |
|---|---|---|---|
| Charava-Bhootni | -21.7 dB | -5.5 dB | Clean — good reference |
| Kumar-Aur-Chudail | -20.9 dB | -4.8 dB | Best mix of the three |
| Jinn-Masoom | -20.1 dB | -0.0 dB | ⚠ Clipping — avoid |

**Our target:** mean `-20 to -22 dB`, max `-4 to -6 dB` in the final video.

### When narration exists, render-scene uses it automatically

```bash
render-scene --scene 1 --narration scene-1-narration.m4a
```

Hold time per image is calculated from the actual audio duration — more accurate than the word-count estimate.

---

## Stage 5 — Render

### Preview a single scene

```bash
cd Design-Docs/ToPublish/Videos/BaglaMukhi-Sadhana-Anubhav
render-scene --scene 1 --preview
```

Output: `Render/Scene-1-test-preview.mp4` (720p, fast encode).

### Full-quality render with narration

```bash
render-scene --scene 1 --narration scene-1-narration.mp3
```

Output: `Render/Scene-1-test.mp4` (1080p, audio-timed hold per image).

### Baked-in effects (from competitor research)

| Effect | Value |
|---|---|
| Ken Burns zoom | 1.00 → 1.04 (slow push-in) |
| Cut style | Hard cuts within scene |
| Fade in / out | 0.8s from/to black at scene boundaries |
| Default hold | 7s per image (when no narration file) |
| Deity glow | Bloom applied to images whose prompt contains the deity name |

### Full video assembly

After all scenes render, concatenate in DaVinci Resolve or ffmpeg:
```bash
# Example ffmpeg concat
ffmpeg -f concat -safe 0 -i scene_list.txt -c copy full-video.mp4
```

Add: music bed at -18 to -20 dB relative to narration. Target mix: -20 to -21 dB mean, -4 to -6 dB max.

---

## Invoking the Skill from Any Agent

The `devotional-producer` skill is registered in `OpenMontage/AGENTS.md`. All three agents load it automatically:

| Agent | How it reads the skill |
|---|---|
| Claude Code | Loads CLAUDE.md → AGENTS.md → `@path/to/devotional-producer.md` |
| Codex | Reads AGENTS.md natively at session start |
| Pi | Reads AGENTS.md via the handoff extension at session start |

### What to say (any agent)

| Goal | What to say |
|---|---|
| Check pacing + beats | "Run render-scene --critic and report" |
| Write/update critiques | "Critique the script" or "Critique scene 3" |
| Check which images are missing | "What images are missing?" |
| Plan next steps | "Production status" |
| Add a new scene | "Write scene 6 — the vision/supernatural experience beat" |
| Write image prompts | "Write image prompts for scene 6" |

The agent will:
1. Run `render-scene --critic` if needed
2. Apply the `devotional-producer` skill logic
3. Write/update the script MD directly

---

## Competitor Benchmarks (captured 2026-05-05)

| Competitor | Style | Runtime | Views | Posted | Velocity | Median Hold |
|---|---|---|---|---|---|---|
| Charava-Bhootni | Painterly folk | 21:59 | 1.1M | Oct 2025 | 157K/month | 4.2s |
| Kumar-Aur-Chudail | Comic illustration | 21:39 | 529K | Mar 2026 | **265K/month** | 5–8s |
| Jinn-Masoom | Photoreal drama | 19:03 | 727K | Jul 2025 | 73K/month | 6.0s |

**Key insight:** Kumar-Aur-Chudail has the highest view velocity with zero I2V clips and lowest production cost (~$4–6/episode). Comic style + fade-to-black + costume continuity = the current fastest-growing format.

For devotional anubhav, Jinn-Masoom's 6.0s median is the closest style match. Target 6–8s per card.

---

## Character Reference Files (Baglamukhi Sadhana Anubhav)

| File | Character | Used in |
|---|---|---|
| `Maa-Baglamukhi.png` | Maa Baglamukhi — blessing pose, golden gada, two arms | All scenes featuring Maa |
| `Sadhak_A_Ref.png` | Sadhak — white kurta, pre-ritual state | Scenes 1–2 (any face-visible shot) |
| `Sadhak_B_Ref.png` | Sadhak — yellow dhoti, ritual state | Scenes 3–5+ (any face-visible shot) |

---

## What Scenes Still Need Work (as of 2026-05-05)

| Scene | Status | Issue |
|---|---|---|
| 1 | ❌ High | Narration too thin (40 words / 10 images = 2.8s). Use Critique English as hook. Generate 2 courtroom images. |
| 2 | ⚠ Medium | 5.5s hold — slightly below target. Expand narration by ~1 sentence. |
| 3 | ⚠ Low | 9.2s hold — add 2 images or trim narration. |
| 4 | ⚠ Low | 8.2s hold + 2 images missing. Generate remaining images. |
| 5 | ✓ Medium | 7.5s hold (good). 4 images still to generate. Prayer beat is the emotional peak. |
| 6 | ○ Not written | The supernatural experience beat — most important scene. |
| 7 | ○ Not written | Resolution — court case turns, adversaries helpless. |
| 8 | ○ Not written | Teaching close — practice for viewers, mantra named. |

Scenes 6–8 are the entire payoff. The script is currently ~3m 41s; competitors run ~20 minutes.
