# Shiva Crow Replication Analysis

Purpose: evaluate whether the reference video at `/Users/sunitjoshi/Downloads/Shiva-Crow.mp4` should be recreated inside OpenMontage using the existing fal-backed stack, or via a separate custom script aimed directly at Kling or Veo.

## Bottom Line

Fastest path:
- use OpenMontage, not a separate standalone script
- default to `Kling` via the existing fal integration for the majority of clips
- reserve `Veo` only for a few hero shots if the first sample shows Kling is not good enough

Reason:
- the repo already has working video generation providers, narration, subtitles, music, and final composition wired together
- a separate Kling-only or Veo-only script would duplicate the one part that is already solved here: orchestration
- the real challenge is not API access, it is visual consistency across 4+ minutes

Exactness:
- an exact pixel-for-pixel recreation is not realistic with current stochastic video models
- a very close match in structure, pacing, tone, recurring character design, subtitle treatment, and overall emotional feel is realistic

## What The Reference Is Actually Doing

Studied from:
- direct frame sampling
- OpenMontage `video_analyzer`
- OpenMontage local transcription

Observed structure:
- total duration: `262.1s`
- total detected scenes: `59`
- average shot length: `4.44s`
- pacing: dynamic but calm, closer to narrated social storytelling than to trailer editing

Observed creative pattern:
- one recurring mythic visual world: snowy Himalayan setting, Shiva, crow, soft gold-blue light
- short AI-generated shots stitched together into a longer narrative
- recurring character consistency rather than one long continuous generated take
- slow, reverent pacing with gentle scene changes
- burnt-in subtitles for almost every spoken beat
- simple end-card CTA and channel watermarking

Most likely production method:
- generated stills and/or short generated motion clips
- stitched with narration, music, subtitles, and mild transitions
- not a single long-form model generation

Important implication:
- this is exactly the kind of output OpenMontage is designed to assemble

## What OpenMontage Can Already Do

Verified in the current repo environment:
- video analysis is available
- transcription is available
- Remotion composition is available
- video generation providers available in your setup include `Kling`, `Veo`, `Runway`, `MiniMax`, `Grok`, and others

Relevant repo facts:
- the `animation` pipeline explicitly supports reference-video input and uses `video_analyzer`, `scene_detect`, and `frame_sampler`
- `veo_video` already supports `text_to_video`, `image_to_video`, `reference_to_video`, and `first_last_frame_to_video`
- `kling_video` is already wired through fal for `text_to_video` and `image_to_video`
- `video_compose` already supports subtitle burn-in and Remotion-based final rendering

Practical consequence:
- OpenMontage is already capable of making this class of video end to end
- the missing piece is a locked devotional consistency playbook, not a missing provider integration

## Can This Be Created "Exactly" In OpenMontage?

Short answer:
- exactly, no
- functionally and aesthetically very close, yes

What OpenMontage can match well:
- overall runtime and scene rhythm
- Shiva/crow recurring visual world
- narration-led spiritual story structure
- subtitle style and composition
- selective premium hero shots
- branded final assembly

What will still be hard:
- frame-to-frame identity consistency of Shiva across dozens of scenes
- keeping the snake, jewelry, face shape, and background lighting stable over a full 4-minute piece
- matching the exact flavor of whichever prompt stack was used in the reference

What that means in practice:
- if we lock a proper character bible, generate 3 to 6 anchor frames first, and drive motion from approved anchors, OpenMontage can get close enough for production use
- if we prompt scene-by-scene from scratch with no anchor system, it will drift

## OpenMontage Versus A Separate Kling/Veo Script

### Option A: Use OpenMontage as-is, with a project-specific playbook

Best for:
- fastest time to first sample
- lowest engineering overhead
- keeping narration, subtitles, music, and video generation in one place

Pros:
- already integrated with fal-backed Kling and Veo
- already has analysis, pipeline staging, and final composition
- easier to review, swap providers, and keep artifacts organized
- easier to produce a 10 to 15 second sample before committing to a full run

Cons:
- you still need tighter prompting discipline for recurring character consistency
- some provider-specific tuning will still live in prompts and shot planning, not magically in the pipeline

Verdict:
- recommended

### Option B: Write a separate custom script tuned directly to Kling

Best for:
- batch reroll loops
- bespoke prompt templating
- aggressive experimentation outside the pipeline ceremony

Pros:
- slightly faster if the only goal is to hammer one provider with many prompt variants
- easier to build custom retry logic and ranking around one model

Cons:
- duplicates work OpenMontage already handles
- you still need to solve narration, subtitles, stitching, and project structure
- increases maintenance cost
- makes it harder to compare provider swaps later

Verdict:
- not the fastest overall path for this task

### Option C: Write a separate custom script tuned directly to Veo

Best for:
- premium hero shots where image-guided reference continuity matters more than cost

Pros:
- strongest path for a few anchor moments
- useful if you need custom reference-to-video experiments outside the current scene plan

Cons:
- much slower and much more expensive for a full 4-minute piece
- poor choice for broad iteration across 50+ shots
- still leaves final editorial assembly to another system

Verdict:
- not recommended as the primary workflow

## Speed And Cost Reality

Reference duration:
- `262.1s`

Current public fal pricing observed during research:
- `Kling 2.5 Turbo Pro`: `$0.07/s`
- `Veo 3`: `$0.40/s`

Raw generation math if the whole runtime were generated:
- Kling: about `$18.35` before rerolls
- Veo: about `$104.84` before rerolls

Important note:
- those are raw output-second estimates, not real production totals
- real totals rise because reference-driven work always includes failed generations, rerolls, and anchor-frame prep

OpenMontage-specific implication:
- full-Veo is the wrong default for rapid iteration
- Kling is the sensible base model for most shots
- Veo should be a selective upgrade, not the backbone

## Why I Recommend Kling First, Veo Second

For this specific reference, the winning order is:

1. Build a locked Shiva/crow visual bible
2. Generate anchor stills
3. Animate most scenes with Kling image-to-video
4. Use Veo only for a few emotionally important moments if needed
5. Assemble in OpenMontage with narration, subtitles, music, and end-card

Why this is fastest:
- the reference does not depend on complex dialogue lip sync
- the shots are short and tableau-driven
- the film works because of consistency and pacing, not because every shot is premium-motion cinema
- Kling is much cheaper for broad coverage and good enough for meditative visual storytelling

Why not Veo-first:
- you would pay a large premium to discover prompt issues that could have been solved earlier with cheaper anchor testing
- Veo is better used as a scalpel than as the whole budget

## Recommended OpenMontage Production Plan

### Fastest production path

Pipeline:
- use the `animation` pipeline for this style of mythic visual storytelling

Model stack:
- anchor stills: `FLUX` or `Google Imagen`
- main motion clips: `Kling` through `video_selector`
- premium upgrades: `Veo` for 2 to 5 hero moments only
- narration: `Google TTS` or `ElevenLabs`
- final render: `video_compose` with Remotion and subtitle burn-in

Shot strategy:
- keep most motion clips between `5s` and `8s`
- merge adjacent script beats where one visual can cover multiple lines
- use recurring reference images instead of pure text prompting whenever possible

Consistency strategy:
- lock one canonical Shiva face and one canonical crow design before full production
- reuse the same environment description in every prompt
- keep one lighting family: cold snow + warm divine glow
- define a no-drift list: face shape, moon crescent, snake placement, bead layers, skin tone, hair silhouette

### When a custom script becomes worth it

Write extra custom logic only if:
- you want automatic multi-reroll ranking over dozens of prompts per shot
- you want a provider-specific prompt compiler for devotional scenes
- you want a small "anchor pack to shot pack" helper that expands one approved character bible into scene prompts

If that happens:
- build it inside OpenMontage as helper tooling or a new skill
- do not split the workflow into a separate disconnected production stack

## Decision

Recommended decision:
- proceed inside OpenMontage
- do not start with a standalone Kling or Veo script
- create a devotional consistency playbook for Shiva/crow storytelling
- generate a 10 to 15 second sample first using Kling-backed clips
- only escalate selected shots to Veo if the sample shows a visible quality gap

## Suggested Next Step

The fastest concrete next move is:
- create a new OpenMontage project packet for this reference
- extract 3 anchor stills
- write a locked Shiva/crow character bible
- produce one `10s` sample in-repo with Kling
- compare that sample against one Veo hero-shot sample before committing to the full 4-minute run

## Research Notes

Research used:
- fal pricing page for current public video pricing
- current OpenMontage provider registry in the local repo
- local reference-video analysis and transcription
- V-Zero-3 pricing page was checked, but it appears to be a hosted web product rather than the most direct path for your existing repo-based workflow

## Execution Update: 60s Sample

On April 10, 2026, a first stronger 60-second sample was executed inside OpenMontage:

- output: `projects/shiva-crow-60s/renders/shiva-crow-60s.mp4`

What was used:
- 6 scene beats at about 10 seconds each
- FLUX anchor stills to lock composition and character intent
- Kling `image_to_video` clips through OpenMontage for all six beats
- Remotion composition with word-level captions
- temporary local macOS narration fallback because the configured cloud TTS path was not usable in the current environment

What this confirms:
- OpenMontage is already the fastest execution path for this format
- a Kling-first in-repo workflow can produce a coherent Shiva/crow devotional minute without building a separate custom script
- the newer sample quality is materially above the earlier "basic" test level

Current quality gaps before a polished YouTube-grade version:
- one middle beat still shows visible style drift in Shiva's wardrobe/color treatment
- narration is functional for testing but not final quality
- the next pass should selectively regenerate weak beats and/or upgrade a few hero moments rather than rebuild the whole flow

## ElevenLabs Setup For Automated Voice

If the goal is scalable automation with a reusable personal voice, use `ElevenLabs` as the narration path inside OpenMontage.

Why this is the best fit:
- OpenMontage already supports `voice_id` passthrough for ElevenLabs
- it is better aligned with repeatable script-driven generation than manual recording
- it supports Hindi via multilingual TTS models

Recommended starter path:
- start with the `Starter` plan for initial automation and validation
- upgrade only if monthly volume or cloning quality requirements increase

### Setup Steps

1. Create an ElevenLabs account and subscribe to the `Starter` plan
2. Create an API key in the ElevenLabs dashboard
3. Add the key to OpenMontage `.env`
   - `ELEVENLABS_API_KEY=your_real_key`
4. In ElevenLabs, create your custom voice and capture its `voice_id`
5. Keep one clean reference pack for the clone
   - quiet room
   - minimal background noise
   - natural speaking pace
   - ideally multiple samples with consistent mic quality

### OpenMontage Usage Pattern

Use `tts_selector` or `elevenlabs_tts` with:
- `preferred_provider: "elevenlabs"`
- `voice_id: "<your_voice_id>"`
- `model_id: "eleven_multilingual_v2"` or the current multilingual production model you prefer
- `output_path` pointing into the project audio folder

Practical flow for this project:
1. Generate narration audio from the approved script with your `voice_id`
2. Replace `projects/shiva-crow-60s/assets/audio/narration.mp3`
3. Re-run transcription if timing changes
4. Rebuild composition props
5. Re-render the final video

### Hindi Notes

Hindi is a valid path for this workflow:
- write the script in Hindi
- use a multilingual ElevenLabs model
- test a short 20 to 30 second sample first because cloned-voice accent quality varies by training data

Recommendation:
- if your voice clone is trained mostly on English audio, Hindi may still work but may need prompt/script tuning
- if Hindi is a major target language, train with some clean Hindi reference audio too

### Cost Expectations

For devotional story videos in the `4 to 5 minute` range:
- typical script size is still small enough that raw narration generation cost is not the expensive part
- the main cost driver is the subscription tier, not per-video TTS usage
- `Starter` is enough for initial automation and several such narrations each month

### Precise Estimate For The Competitor-Style Shiva/Crow Video

Calculated on April 10, 2026 from a fresh local transcript of:
- `/Users/sunitjoshi/Downloads/Shiva-Crow.mp4`

Measured values:
- runtime: `262.107s` (`4m 22.1s`)
- transcript word count: `596`
- transcript characters with spaces: `3,345`

#### Voice / Audio

ElevenLabs `Starter` math using current plan details:
- `Starter` includes `30,000` credits per month and `Instant Voice Cloning`
- ElevenLabs pricing FAQ states multilingual v2/v3 text uses `1 character = 1 credit`

Competitor-video narration estimate:
- `3,345 credits` for one full narration pass
- about `11.15%` of the monthly `Starter` allowance
- about `8.96` raw narration passes per month at this exact transcript length
- realistically about `6 to 8` completed narrations per month if you allow samples, rerolls, and timing tweaks

Hindi note:
- for Hindi, the credit model should be directionally similar
- the exact usage changes with the final Hindi script length after translation/adaptation

#### Image / Video

Current public fal pricing observed during research:
- `Kling 2.5 Turbo Pro`: `$0.07/s`
- `Veo 3`: `$0.40/s`

If the full `262.1s` competitor runtime were generated as video:
- Kling-only baseline: about `$18.35` before rerolls
- Veo-only baseline: about `$104.84` before rerolls

More realistic OpenMontage production view:
- main body on Kling, hero shots selectively upgraded to Veo
- actual total rises above the raw baseline because of anchor stills, failed generations, rerolls, and quality control
- this is why OpenMontage should stay Kling-first, not Veo-first

Practical planning takeaway:
- `Voice / Audio` is cheap enough that it should not be the blocker
- `Image / Video` is the real spend category for this type of devotional competitor-style remake

#### Kling App Membership vs Kling Dev API vs fal.ai

These are three different economic paths and should not be treated as equivalent.

##### Kling App Membership

From the shared membership screenshot:
- `Standard`: `$6.99/month` for `660 credits`
- `Pro`: `$25.99/month` for `3000 credits`
- the screenshot states `660 images / 33 720p videos` on Standard
- the screenshot states `3000 images / 150 720p videos` on Pro

Implication:
- the app membership path appears to be the cheapest option if the workflow can tolerate manual or semi-manual generation in the Kling web product
- this is the strongest low-cost path for high monthly volume

##### Kling Dev API

From the shared `kling.ai/dev/pricing` screenshots:
- resource packs are sold by units, not by a flat monthly membership model
- examples shown:
  - `100 units` for `$9.8`
  - `1000 units` for `$98`
  - `1500 units` for `$136.5`
- the page explicitly notes that video deduction units vary by mode and duration

What is clear:
- the developer API is not priced like the consumer membership plan
- image endpoints shown in the screenshot commonly price around:
  - `4 units` → `$0.014`
  - `8 units` → `$0.028`
  - `16 units` → `$0.056`

Implication:
- Kling Dev API may still be useful for automation
- but it should not be assumed to be as cheap as the Kling app membership path

##### fal.ai

From observed fal.ai usage and current live pricing checks:
- the `fal-ai/kling-video/v3/standard/image-to-video` path is materially more expensive than the app membership path
- a 60-second sample already consumed about `$6.30` in dashboard-visible usage

Implication:
- fal.ai is best understood as the convenience/automation premium path
- it is excellent for in-repo orchestration, but weak on pure cost efficiency

##### Working Recommendation

If optimizing for lowest cost:
- generate in the Kling app membership flow
- download assets
- compose, subtitle, and finish in OpenMontage

If optimizing for automation:
- stay inside OpenMontage with API-driven generation
- prefer Kling only when the convenience premium is acceptable

If optimizing for both:
- use a hybrid workflow
- voice and final assembly in OpenMontage
- low-cost shot generation in Kling app when possible

### Operational Advice

For production quality:
- do one approved voice sample before batch generation
- lock one `voice_id` per channel/project
- avoid changing clone, cadence, and model simultaneously
- if the voice is good but slightly synthetic, improve post-processing with `audio_enhance` rather than changing the full voice path first
