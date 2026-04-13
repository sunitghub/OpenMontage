# Competitor Analysis

Purpose: consolidate the reference-video, provider-comparison, and Omni evaluation notes into one decision document for competitor-style devotional videos.

Use this doc when deciding:
- whether to recreate a reference inside OpenMontage
- whether to stay Kling-first or escalate to Veo
- whether Omni is worth testing for the same project
- what the fastest production path is for Shiva/crow-style spiritual storytelling

## Current Reference Case: Shiva Crow

Reference studied:
- `/Users/sunitjoshi/Downloads/Shiva-Crow.mp4`

Observed pattern:
- recurring mythic world rather than one long continuous generation
- short generated clips stitched into a narrated story
- strong subtitle dependence
- calm but dynamic pacing
- consistency matters more than raw visual novelty

Measured notes:
- runtime: about `262s`
- detected scenes: about `59`
- average shot length: about `4.4s`

Important conclusion:
- OpenMontage is already suited to this class of output
- the hard problem is continuity, not orchestration

## Second Reference Case: Shiva Kailash

Reference studied:
- `/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/ToPublish/Shorts/Competitors/Shiva-Kailash.mp4`

Observed pattern:
- mostly static devotional stills rather than true full-motion generation
- slow zooms, pans, holds, and dissolves carry the pacing
- text and narration do most of the narrative progression
- atmospheric motion is added through smoke, snow, glow, particles, and light shifts
- visual resets happen through scene changes, not constant in-shot action

Important conclusion:
- this class of devotional short is fundamentally a `motion-light montage`
- the perceived richness comes from composition and layered effects, not from generating every beat as native video
- OpenMontage should treat these as `anchor still + motion recipe + overlays`, not as an all-video problem

## Prototype Findings: Maa Kali Yantra Short

Working package:
- `/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/ToPublish/Shorts/Maa-Kali-5-Unknown-Facts`

What the prototype confirmed:
- canonical yantra geometry is better reused directly than regenerated
- MidJourney or curated stills are best used for supporting atmospheres, not sacred-geometry replacement
- dark, unified background treatment is much stronger than plain parchment-on-white presentation
- selective superimposition works well:
  - red triangle within moon-phase ring
  - yantra over cosmic or cremation-ground backplates
- engagement improves when subtle motion is localized:
  - center-grow symbol reveals
  - ember or spark drift in fire scenes
  - light rays or glow pulses around focal sacred symbols

What looked weak:
- white or parchment-heavy scenes without a darker frame felt flat and presentation-like
- persistent border graphics can overpower shots if their center is opaque
- fully regenerated sacred geometry drifted too far from canonical reference material

Operational conclusion:
- use existing sacred assets as the truth layer
- use supporting backgrounds to provide emotional variation
- animate with restrained but visible energy accents
- prefer one focal motion per shot over many competing effects

## Bottom Line

Recommended default path:
- use OpenMontage for planning, assets, narration, subtitles, and final composition
- use `Kling` as the default motion engine for most clips
- use `Veo` only for selective hero moments when the quality gain is clearly worth the cost
- test `Omni` only in a guided, scene-based way

Additional devotional-short conclusion:
- for Shiva/Kailash and Maa Kali/yantra style videos, the fastest strong result is usually:
  - reusable anchor stills
  - selective short hero clips
  - composited symbols or deity overlays
  - editorial motion and particles inside OpenMontage

Not recommended:
- building a separate standalone provider script as the first move
- using pure full-script black-box generation to judge production readiness

## OpenMontage Versus Separate Scripts

### OpenMontage

Best for:
- fastest time to first usable sample
- keeping assets, subtitles, narration, and render output in one workflow
- still-led montage assembly with effect layers

Why it wins:
- orchestration is already solved here
- provider swaps remain possible
- review and reroll discipline is easier
- static-image reuse dramatically reduces generation cost and quality drift

### Separate Kling Or Veo Scripts

Worth it only if:
- you need aggressive provider-specific reroll automation
- you want custom ranking loops over many prompt variants
- the helper logic is clearly reusable enough to belong back in OpenMontage later

Default verdict:
- not worth starting here

## Provider Recommendation

### Kling First

Use Kling for:
- the majority of short devotional motion clips
- image-to-video from approved anchors
- fast coverage across many scenes

Why:
- cheaper than Veo for broad coverage
- good fit for tableau-style spiritual storytelling
- consistency problems are better solved with anchors and prompt discipline than with paying premium rates everywhere

### Veo Second

Use Veo for:
- a few premium hero shots
- moments where reference-driven motion quality materially changes the final video

Why:
- stronger premium-motion path
- wrong as the default backbone for long competitor-style runs

### Omni As An Evaluation Path

Use Omni to answer one question:
- can guided Omni produce materially better continuity or premium motion than the current Kling-first path?

Do not use Omni as a black-box replacement test first.

## Omni Test Strategy

### Best Test Order

1. `Script-only Omni`
   Use only as a curiosity benchmark.

2. `Guided scene-based Omni`
   This is the real comparison path.

### Recommended Guided Pack

For the Shiva/crow project, prepare:
- sectioned script beats
- visual bible
- all approved scene anchors
- optional narration for timing
- baseline OpenMontage render for comparison

### Prompting Rules

For each guided Omni scene, include:
- subject lock
- one clear action
- one camera move
- world rules
- negative constraints

For Shiva/crow specifically, preserve:
- Shiva face shape
- beard consistency
- crow identity
- snowy Himalayan setting
- gold-blue lighting family

### Decision Rule

Adopt Omni for the project only if it:
- is visibly more consistent than the current sample
- or produces materially better hero-shot motion
- without making rerolls and assembly workflow too painful

If Omni only gives prettier isolated clips:
- keep OpenMontage as the main path
- use Omni selectively for hero moments

## Cost And Speed Reality

Directionally:
- `Kling` is the efficient broad-coverage option
- `Veo` is the premium selective-upgrade option
- `fal.ai` is the convenience and automation premium
- Kling web membership can be the cheapest manual-generation path if manual workflow is acceptable

Practical planning rule:
- treat video generation as the real spend category
- treat voice generation as relatively cheap by comparison

## Voice And Final Assembly

For competitor-style devotional videos:
- keep narration, subtitles, music, and final timing inside OpenMontage
- use one locked voice path per project
- do not change voice, cadence, and provider simultaneously

If using a reusable personal voice:
- ElevenLabs is a strong repeatable path for script-driven narration

## Operational Playbook

For the fastest serious test:
1. lock a character and world bible
2. generate or curate anchor stills
3. decide which scenes are:
   - direct asset reuse
   - animated stills
   - true generated hero clips
4. animate only the shots that need real motion
5. add particles, glows, symbol overlays, and slow camera movement inside OpenMontage
6. compare a few hero moments against Veo or guided Omni
7. compose and subtitle inside OpenMontage

## Visual Heuristics For Competitor-Style Devotional Shorts

Use these defaults unless a project clearly needs something else:
- start from a dark devotional base rather than bright flat parchment fills
- keep one dominant sacred focal point per shot
- make motion originate from the focal point when possible
- use fire, spark, mist, snow, or glow as scene-local energy, not everywhere at once
- superimpose symbols when it improves clarity:
  - red triangle inside lunar arc
  - yantra over cosmic plate
  - deity portrait behind or above sacred geometry
- reserve full motion generation for opener shots, hero reveals, or difficult transitions

## Current Recommendation

For Shiva/crow-style devotional competitor remakes:
- stay inside OpenMontage
- stay Kling-first
- use Veo selectively
- use Omni only as a guided evaluation path
- optimize continuity before optimizing provider novelty
