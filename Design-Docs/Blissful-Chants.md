# Blissful Chants Visual Consistency Guide

Purpose: define a repeatable visual system for devotional videos so a full script feels like one film, not a collage of unrelated generations.

This guide is written for:
- Hindu spiritual storytelling
- Maa Kali, Bhagavad Gita, and related devotional/explainer content
- OpenMontage pipelines using fal-backed image and video generation

Concrete playbook:
- [styles/blissful-chants.yaml](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/styles/blissful-chants.yaml)

## Core Principle

Do not ask the model to "be creative" from scratch on every scene.

Consistency comes from locking a small set of decisions and reusing them everywhere:
- same visual style
- same character depiction rules
- same color language
- same prompt structure
- same reference images
- same aspect ratio
- same subtitle system
- same scene grammar

## Brand Direction

Channel name: `Blissful Chants`

Desired feeling:
- reverent
- mystical
- luminous
- emotionally intense, but not horror-coded
- devotional first, cinematic second

Avoid:
- horror poster energy
- chaotic demon aesthetics
- gore
- exaggerated Western fantasy armor styling
- inconsistent facial features from shot to shot
- random typography styles between scenes

## What Must Stay Consistent

Lock these before generating a full script:

### 1. Deity Depiction Rules

For Maa Kali or any deity-driven story, define the depiction once and reuse the same description in every prompt.

Example anchor description:
- deep blue-black skin
- radiant red and gold aura
- calm but powerful divine expression
- luminous red eyes only when spiritually justified, not monstrous
- long flowing black hair
- traditional ornaments and garland rendered reverently
- temple-art-inspired digital illustration

If you change these details scene to scene, the model will treat each shot like a new character.

### 2. Style Family

Pick one primary style family per video:
- `devotional illustration`
- `temple mural inspired digital painting`
- `high-contrast sacred storybook animation`

Do not mix:
- anime in one shot
- comic-book cel shading in another
- photorealism in another

For this channel, the safest repeatable choice is:
- stylized 2D digital illustration
- strong silhouette shapes
- controlled glow effects
- soft texture overlays

### 3. Color System

Use one locked palette per series.

Recommended Blissful Chants palette:
- midnight indigo: `#0B1026`
- divine crimson: `#C32148`
- ember orange: `#F05A28`
- lotus gold: `#E7B84B`
- ash rose: `#E27A8D`
- moon cream: `#F6E7C8`

Rules:
- dark backgrounds should lean indigo, not flat black
- glow accents should come from crimson, gold, and ember
- text highlight color should be one consistent accent only

### 4. Lighting Logic

Use one lighting language across the piece:
- backlit divine aura
- rim-lit silhouettes
- low-key environment with sacred glow
- smoke, incense, or particle atmosphere only as support

Do not alternate between:
- flat daylight
- neon nightclub lighting
- realistic photography lighting

### 5. Framing Grammar

Use a small shot library:
- wide reveal
- medium devotional portrait
- symbolic close-up
- over-the-shoulder listener/devotee shot
- text-card or verse-card interstitial

If every scene uses a different lens feel, consistency breaks even when the character is similar.

### 6. Subtitle and Text Overlay System

Use one system for all videos:
- one font pairing
- one caption placement rule
- one text highlight color
- one animation style
- one safe margin system for mobile crop later

Recommended:
- primary caption color: warm white
- emphasis color: lotus gold or ember orange
- bottom-center captions with high contrast stroke or shadow
- avoid large all-caps for every line unless it is a deliberate stylistic choice

## Best Practice with fal

These suggestions are based on fal's official docs and model guidance:
- fal exposes common arguments like `seed`, which should be locked for reproducibility
- fal Playground is the fastest way to test exact model inputs before integrating
- fal Sandbox is useful for side-by-side comparisons before committing to one model
- some fal-supported models support reference-image and image-to-video workflows
- fal supports LoRA-capable models for stronger style or character consistency when needed

Useful references:
- https://docs.fal.ai/documentation/model-apis/model-arguments
- https://docs.fal.ai/documentation/model-apis/playground
- https://docs.fal.ai/documentation/model-apis/sandbox
- https://docs.fal.ai/documentation/why-fal
- https://fal.ai/models/fal-ai/z-image/turbo/lora/playground
- https://fal.ai/learn/devs/kling-2-6-pro-prompt-guide

## Choosing fal Models

Do not choose the paid model stack by hype alone.

Use this sequence:
1. pick models by job type
2. run a small side-by-side comparison in fal Sandbox
3. lock one image model and one video model per project

### Recommended Starting Stack

For Blissful Chants, the recommended default starting point is:
- `FLUX` for anchor stills and visual bible frames
- `Kling image-to-video` for most animated devotional shots
- `Veo` only for premium hero moments where continuity or realism gain justifies the cost
- `Recraft` only for title cards, verse cards, or cleaner graphic overlays

Why this is the best starting balance:
- FLUX is a strong value model for stylized sacred stills
- Kling is a practical default for cinematic motion from approved stills
- Veo is powerful, but expensive enough that it should be used selectively
- Recraft is more useful for structured design assets than painterly deity imagery

### Decision Rule

Choose models based on the asset type:

#### Still images

Default to:
- `FLUX`

Use `Recraft` if the output needs:
- cleaner title-card design
- stronger text or graphic discipline
- more editorial composition than painterly spirituality

#### Motion clips

Default to:
- `Kling image-to-video`

Escalate to `Veo` when:
- the shot is a hero moment
- continuity between frames matters more than cost
- the scene needs a more premium look and the budget allows it

### Evaluation Criteria

For devotional content, score every model test on:
- reverence of deity depiction
- consistency with Blissful Chants palette and tone
- stability of face, ornaments, and silhouette
- motion quality without morphing
- subtitle-safe composition
- cost per usable shot

If a model looks impressive but fails reverence or consistency, it is the wrong model for this channel.

### Sandbox Testing Plan

Once a fal key is available, run:
- 3 still-image comparisons using the same Maha Kali prompt
- 2 image-to-video comparisons using the same approved anchor frame

Then lock:
- one default image model
- one default motion model
- one optional premium upgrade model

Do not switch models mid-project unless the approved model clearly fails.

## fal Model Test Log

Use this section to record actual comparison outcomes once paid testing begins.

### Planned Initial Test

Reference assets:
- local Maha Kali reference set from `/Users/sunitjoshi/Documents/Documents/BlissfulChants/Assets/Deities/MahaKali`

Initial comparison set:
- images: `FLUX` vs `Recraft` if needed for card-like assets
- motion: `Kling image-to-video` vs `Veo`

Scoring dimensions:
- reverence
- consistency
- motion stability
- caption safety
- cost efficiency

### Results

To be filled in after live fal testing.

Suggested fields to capture:
- date
- prompt used
- reference image used
- model tested
- cost
- strongest quality
- failure mode
- keep or reject decision

## Practical Consistency Workflow

### Stage 1. Create a Visual Bible

Before generating the whole script, generate and approve:
- 1 hero deity portrait
- 1 devotee character portrait
- 1 environment frame
- 1 title-card frame
- 1 verse-card frame

Save these as the canonical references for the project.

This is the single highest-leverage step for consistency.

### Stage 2. Lock a Prompt Prefix

Every prompt should start with a stable prefix that describes the visual world.

Example prefix:

`Reverent Hindu devotional digital illustration, temple-mural-inspired sacred storytelling, midnight indigo and crimson palette, gold divine glow, strong silhouette design, cinematic rim light, soft atmospheric incense haze, elegant spiritual composition, consistent character design`

Then append only the scene-specific action.

Do not rewrite the whole style block each time in a different way.

### Stage 3. Keep a Negative Prompt Stable

For models that support it, keep the negative prompt nearly identical throughout the project.

Suggested negatives:
- horror
- gore
- zombie
- monster face
- extra limbs
- distorted hands
- text artifacts
- low contrast muddy colors
- modern clothing when not intended
- photorealistic skin pores if the style is illustrative

### Stage 4. Reuse Seeds Intentionally

fal's common model arguments document `seed` as the reproducibility control.

Use seeds in a structured way:
- one base seed family for deity shots
- one base seed family for devotee shots
- one base seed family for environments

Do not expect the same seed alone to guarantee the same character if the prompt changes too much, but it helps stabilize composition and style.

Suggested policy:
- keep a seed log per scene
- reuse or slightly vary seeds only within the same subject family

### Stage 5. Generate Anchor Images First

For scene consistency, do not go directly from script to fully independent generations.

Better approach:
1. generate anchor stills for each major scene
2. approve the stills
3. use those stills as inputs for image-to-video
4. preserve the visual identity while adding motion

This is much more stable than asking the video model to invent everything from text every time.

### Stage 6. Prefer Image-to-Video Over Pure Text-to-Video

For a scripted devotional film, consistency is usually better when:
- the image model defines the exact character and scene look
- the video model only animates that approved frame

Pure text-to-video is useful for exploration, but it is more likely to drift in:
- face shape
- jewelry
- number of arms or ornaments
- costume details
- expression
- lighting

### Stage 7. Use Reference Packs

For each recurring subject, maintain a small reference pack:
- front-facing portrait
- 3/4 portrait
- full-body frame
- environment reference
- color reference board

If the chosen fal model supports reference images or elements, use them consistently.

### Stage 8. Use fal Playground and Sandbox Before Batch Runs

Recommended workflow from fal docs:
- use Playground to validate one exact model and its accepted inputs
- use Sandbox to compare a few candidate models side by side

For Blissful Chants, do this before committing to a full production run:
- compare 2 to 3 image models for the deity portrait
- compare 2 video models for image-to-video motion quality
- then lock the model choice for the project

Do not switch models mid-project unless the failure is severe.

### Stage 9. Use LoRA When Consistency Becomes a Real Requirement

fal supports LoRA-capable workflows on some models. This is the strongest longer-term path when you need repeatable brand-specific imagery across many videos.

Use LoRA if:
- the same divine figure appears across many episodes
- the same host/devotee character reappears
- you want a house illustration style for the channel

Do not start with LoRA on day one unless consistency is already breaking your workflow. First prove the style guide, prompt prefix, reference pack, and seed discipline.

### Stage 10. Track Everything

For every approved asset, save:
- prompt
- negative prompt
- model
- seed
- aspect ratio
- output path
- reference inputs used

If you do not log these, consistency becomes impossible to reproduce later.

## Video Consistency Workflow

Video consistency is harder than image consistency because the model must preserve identity, composition, and motion over time.

The safest rule is:
- do not generate each clip from text alone
- do not let every scene invent its own motion language

### What Must Stay Consistent in Video

Lock these for the entire project:
- one primary video provider
- one aspect ratio
- one clip length policy
- one motion intensity level
- one camera grammar
- one character depiction system
- one subtitle-safe composition rule
- one audio philosophy

If any of those drift, the project starts feeling stitched together from unrelated sources.

### Preferred Generation Order

For story-driven devotional videos, use this order:

1. script
2. scene plan
3. visual bible
4. anchor stills
5. image-to-video clips
6. optional continuity bridge clips
7. edit and caption
8. final human narration

Do not start with text-to-video for the full script unless you are still exploring style.

### Best fal Modes for Continuity

For recurring characters or sacred figures, prefer the most constrained mode available.

Recommended order of preference:
- `image_to_video`
- `reference_to_video`
- `first_last_frame_to_video`
- `text_to_video`

Why:
- `image_to_video` keeps a specific approved frame as the visual anchor
- `reference_to_video` helps preserve subject identity and style across motion
- `first_last_frame_to_video` is useful when a scene must move from one approved composition to another without visual drift
- `text_to_video` is the least stable and should be treated as exploration or for non-recurring symbolic shots

OpenMontage already reflects this in the current Veo integration, which supports `image_to_video`, `reference_to_video`, and `first_last_frame_to_video`.

### One Provider Per Project

Do not mix:
- Kling for some scenes
- Veo for some scenes
- MiniMax for some scenes

unless you intentionally separate them by sequence and visual purpose.

Each model has a different:
- motion signature
- texture behavior
- face consistency profile
- lighting interpretation
- camera feel

For Blissful Chants, pick one motion provider per video and stick with it.

Suggested policy:
- choose a default motion provider after a small sample test
- only use a second provider for clearly different inserts such as symbolic cosmic transitions

### One Motion Language Per Series

The motion language should feel devotional, not restless.

Recommended motion vocabulary:
- slow push-in
- gentle parallax
- soft aura pulse
- drifting incense or particles
- subtle hair or cloth movement
- slow hand gesture or blessing motion
- deliberate reveal from darkness into divine glow

Avoid:
- whip pans
- fast snap zooms
- aggressive handheld simulation
- chaotic camera orbiting
- motion that causes face or jewelry morphing

### Clip Duration Rules

Use a narrow duration range for all generated clips.

Recommended:
- hero shots: `5s` to `8s`
- symbolic inserts: `4s` to `6s`
- text-backed background loops: `4s` to `5s`

Longer AI-generated clips create more opportunities for identity drift.

Better approach:
- generate short stable shots
- stitch them with editing
- use transitions and narration to create flow

### Continuity Through Frame Chaining

When you need one shot to flow into the next:
- use the final approved frame of shot A as a reference or starting frame for shot B
- keep the same prompt prefix
- keep the same palette and lighting language

This is especially useful for:
- deity reveal sequences
- battlefield-to-discourse transitions in Gita content
- blessing or transformation moments

### Subject Categories and Their Rules

Not every shot needs the same continuity pressure.

#### Tier 1: Canonical identity shots

These need the strongest continuity controls:
- deity close-ups
- recurring devotee character
- Krishna or Arjuna recurring depictions
- guru or storyteller figure

Use:
- anchor stills
- reference images
- image-to-video
- stable prompt prefix
- stable seeds where supported

#### Tier 2: Semi-symbolic environment shots

These need palette and lighting continuity more than exact identity:
- temple interiors
- battlefield horizons
- night sky with sacred aura
- river, fire, bell, incense scenes

These can tolerate more variation as long as the same art direction remains.

#### Tier 3: Abstract symbolic inserts

These can be most flexible:
- glowing mantra particles
- cosmic backgrounds
- divine energy waves
- abstract aura transitions

These are the best places to experiment without hurting narrative continuity.

### Audio Consistency in Generated Video

If the chosen provider can generate native audio, treat that as optional, not default.

For your channel, final consistency should come from:
- your own voice
- one music philosophy
- one ambience strategy

Recommended:
- disable or ignore provider-generated dialogue for final publish cuts
- use generated clip audio only as temporary texture if needed
- replace with your own narration and final mix in OpenMontage

### Caption-Safe Video Generation

Many generated shots fail later because they place the important subject where captions need to go.

When prompting video backgrounds, include composition constraints such as:
- clean lower-third space
- subtitle-safe bottom margin
- subject framed above caption zone
- negative space for verse text if needed

This is especially important for:
- scripture recitation videos
- bilingual caption videos
- mobile-app repurposing later

### Suggested Video Prompt Structure

Use this structure:

`[locked visual prefix]. [subject identity]. [specific scene action]. [camera move]. [motion intensity]. [lighting and atmosphere]. [composition constraint]. [reverence constraint].`

Example:

`Reverent Hindu devotional digital illustration, temple-mural-inspired sacred storytelling, midnight indigo and crimson palette, lotus-gold highlights, sacred cinematic rim light, soft incense haze, consistent character design. Maa Kali with deep blue-black skin, flowing black hair, traditional sacred ornaments, serene but powerful divine expression. She raises one hand in blessing over a sleeping devotee. Slow cinematic push-in with subtle cloth and hair movement. Gentle divine aura pulse, no violent motion. Keep lower frame clean for subtitles. Sacred and reverent tone, not horror-coded.`

### Failure Signs to Watch For

Reject or regenerate clips when you see:
- face changing mid-shot
- jewelry appearing or disappearing
- extra hands or inconsistent anatomy
- expression turning monstrous when the scene should be reverent
- rapid lighting changes not motivated by the scene
- camera motion stronger than the narration tone
- background objects melting or morphing

Do not try to "fix it in editing" if the core identity is drifting.

### Recommended Provider Usage for Blissful Chants

If using fal-backed motion:
- use Kling when you want smoother cinematic motion from a strong reference image
- use Veo when continuity between guided frames matters more and when reference-driven modes are valuable

In both cases:
- prefer short clips
- avoid switching providers inside one sequence
- keep model variant fixed across the project

### OpenMontage Production Pattern

The most reliable OpenMontage pattern for this channel is:

1. generate canonical stills with `flux_image`
2. save the approved stills as project references
3. animate with one chosen video tool
4. stitch clips in `video_compose`
5. add subtitle overlays
6. replace temp audio with your own voice
7. render the master

This gives the highest continuity while still keeping the workflow automated.

## Model Strategy for Blissful Chants

Recommended default path:

### Images

Use `flux_image` first for:
- painterly spiritual stills
- character portraits
- atmospheric scene anchors

Use `recraft_image` for:
- title cards
- verse cards
- graphic overlays
- assets that need cleaner design structure

### Motion

Use image-to-video rather than text-to-video whenever possible.

Recommended motion style:
- slow aura expansion
- gentle camera push
- cloth or hair drift
- floating incense particles
- subtle divine light pulses

Avoid:
- aggressive action motion unless the story explicitly needs it
- over-dynamic camera moves
- fast morphing effects that break sacred depiction

## Script-to-Visual Mapping

For each script, split the visual plan into three asset types:

### A. Canonical subjects

These must remain most stable:
- deity
- recurring devotee
- guru or narrator character

### B. Symbolic inserts

These can vary more:
- lotus
- trident
- temple bells
- burning diya
- cosmic sky
- battlefield silhouette for Gita passages

### C. Information overlays

These should be the cleanest and most systematized:
- verse number
- chapter title
- key teaching
- short emphasized quote

## Suggested Prompt Template

Use this structure consistently:

`[locked visual prefix]. [subject description]. [scene action]. [camera/framing]. [lighting]. [mood]. [output constraints].`

Example:

`Reverent Hindu devotional digital illustration, temple-mural-inspired sacred storytelling, midnight indigo and crimson palette, lotus-gold highlights, cinematic rim light, soft incense haze, consistent character design. Maa Kali appears with deep blue-black skin, flowing black hair, sacred ornaments, serene but powerful divine expression. She places a protective hand of grace over a frightened devotee resting in bed. Medium-wide composition from bedside angle. Backlit red-gold aura, sacred atmosphere, emotionally intense but reverent, no horror framing, clean subtitle-safe lower area.`

## Prompting Rules

Always include:
- style family
- palette
- lighting
- emotional tone
- reverence constraint
- subtitle-safe area if text overlays will be added later

Avoid vague prompts like:
- "make it spiritual"
- "make it cinematic"
- "make it epic"

Those are too under-specified to produce repeatable results.

## Specific Guidance for Maa Kali Content

Maa Kali imagery can drift into sensationalized horror very easily.

To keep the tone devotional:
- describe divinity, protection, transcendence, maternal ferocity, grace
- avoid prompt words associated with horror posters
- specify `reverent`, `sacred`, `temple-art-inspired`, `devotional`
- keep fear on the human side of the scene, not as a caricature of the deity

## Specific Guidance for Bhagavad Gita Content

For scripture-centered content, consistency depends less on character identity and more on format identity.

Lock:
- one verse-card design
- one narration pace
- one caption style
- one background family
- one Krishna/Arjuna depiction system if characters appear

For Gita videos, use more restrained motion and cleaner overlays than in mythic-story videos.

## OpenMontage Implementation Suggestions

When we automate this in OpenMontage, the project should store:
- a channel-level style preset
- reusable prompt prefix
- reusable negative prompt
- approved reference images
- per-scene seed log
- subtitle style preset

Best production order:
1. approve script
2. create visual bible
3. generate anchor stills
4. approve anchor stills
5. animate selected stills into clips
6. add text overlays
7. add final human narration
8. render YouTube master
9. derive mobile-app versions later

## Recommendation

For Blissful Chants, the best path is:
- use fal for image and motion generation
- keep one locked devotional art direction per series
- use image-to-video for consistency
- use your own voice for final narration
- treat every approved still as a canonical asset, not a disposable draft

This will produce a channel that feels authored and recognizable instead of randomly AI-generated.
