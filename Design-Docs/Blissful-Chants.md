# Blissful Chants Playbook

Purpose: define the core creative and production rules for `Blissful Chants` so devotional videos feel consistent, reverent, and reusable across Shorts and long-form work.

Use this doc for:
- visual consistency
- prompt and anchor discipline
- script-to-scene translation
- render-package expectations
- the default long-form devotional story format

Use these companion docs for adjacent decisions:
- [Blissful-Chants-Strategy.md](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/Blissful-Chants-Strategy.md)
- [Competitor-Analysis.md](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/Competitor-Analysis.md)
- [Design-Changes.md](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/ToPublish/Design-Changes.md)
- [styles/blissful-chants.yaml](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/styles/blissful-chants.yaml)

## Core Principle

Do not ask the model to reinvent the video on every shot.

Consistency comes from reusing a small locked system:
- same deity depiction rules
- same style family
- same color and lighting logic
- same prompt structure
- same anchor assets
- same framing grammar
- same subtitle rules

If those drift, the final video feels like unrelated AI generations stitched together.

## Brand Direction

Channel feeling:
- reverent
- mystical
- luminous
- emotionally intense, but not horror-coded
- devotional first, cinematic second

Avoid:
- horror poster energy
- gore
- chaotic demon aesthetics
- random costume drift
- inconsistent facial features
- typography that changes style scene to scene

## Visual Lock

These choices should be locked before full generation.

### 1. Deity Depiction

Define one anchor description and reuse it throughout the project.

For deity-led work, lock:
- skin tone
- face shape
- hair silhouette
- ornaments
- expression family
- aura logic

Example Maa Kali direction:
- deep blue-black skin
- calm but powerful divine expression
- flowing dark hair
- traditional ornaments rendered reverently
- crimson and lotus-gold aura

### 2. Style Family

Choose one primary style family per project.

Recommended defaults:
- devotional illustration
- temple-mural-inspired digital painting
- sacred storybook-style 2D illustration

Do not mix:
- anime in one scene
- photorealism in another
- comic-book cel shading in another

### 3. Color And Lighting

Recommended Blissful Chants palette:
- midnight indigo: `#0B1026`
- divine crimson: `#C32148`
- ember orange: `#F05A28`
- lotus gold: `#E7B84B`
- moon cream: `#F6E7C8`

Lighting rules:
- low-key environment
- divine rim light
- sacred glow from crimson, gold, and ember
- atmosphere from smoke, incense, particles, or haze only as support

Avoid:
- flat black backgrounds
- neon nightclub lighting
- hard realism in one shot and fantasy glow in another

### 4. Framing Grammar

Use a small repeatable shot library:
- deity close-up
- medium devotional portrait
- full-body sacred silhouette
- symbolic environment wide
- devotee reaction frame
- text impact card

Keep the lower frame readable for subtitles.

### 5. Subtitle And Text Overlay Rules

Use one subtitle system across the entire piece.

Rules:
- bottom-center safe area
- short readable lines
- one emphasis phrase at a time
- one typography family per project

## Consistency Workflow

Use this order by default:

1. Approve the script.
2. Lock the visual bible.
3. Choose anchor images.
4. Approve the anchor images.
5. Generate scene motion from approved anchors where possible.
6. Add captions and overlays after scene direction is stable.
7. Add narration and music after picture direction is stable.
8. Render the publishable package.

## Anchor Asset Rules

Treat every approved still or deity image as a canonical asset, not a disposable draft.

Rules:
- prefer existing approved deity assets before generating new anchors
- record chosen anchors in the package markdown
- keep the same anchors across rerolls when possible
- use image-to-video when continuity matters more than novelty
- do not swap identity anchors casually mid-project

## Prompting Rules

Prompt structure should be stable across scenes.

Recommended shape:
1. subject lock
2. style family
3. color and lighting
4. camera move
5. motion intensity
6. subtitle-safe composition note
7. negative constraints

Short example:

```text
Reverent Maa Kali close-up, temple-mural-inspired devotional illustration, midnight indigo background, crimson and lotus-gold aura, calm but powerful divine expression, slow cinematic push-in, subtitle-safe lower frame, devotional not horror-coded, no gore, no monstrous distortion.
```

Negative constraints to reuse when relevant:
- no gore
- no horror poster energy
- no monstrous distortion
- no costume drift
- no random extra limbs
- no chaotic background clutter

## Script-To-Visual Mapping

Match scene type to narrative function.

### Canonical Identity Beats

Use for:
- opening deity reveals
- key emotional truth moments
- final devotional payoff

Best treatment:
- anchor-led
- minimal drift
- slower camera language

### Symbolic Interpretation Beats

Use for:
- ego, fear, illusion, surrender, cosmic truth
- internal spiritual meaning

Best treatment:
- semi-abstract visuals
- silhouette or symbolic environments
- lower identity pressure than canonical portrait shots

### Information Or List Beats

Use for:
- facts
- numbered lists
- title cards
- utility explainer moments

Best treatment:
- cleaner composition
- text-forward framing
- simpler motion

## Provider Guidance

Keep provider choice secondary to visual discipline.

Working rule:
- use the provider that best supports your approved anchor-driven workflow
- do not change provider, model family, and prompt language all at once

General recommendation:
- use still-first plus composition for fast iteration
- use premium motion selectively on hero beats
- use the companion [Competitor-Analysis.md](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/Competitor-Analysis.md) for provider tradeoffs, Omni testing, and competitor-style recreation strategy

## Subject-Specific Guidance

### Maa Kali

Keep Maa Kali:
- powerful
- sacred
- compassionate even when fierce

Avoid:
- treating fierceness as horror by default
- generic dark-fantasy monster styling
- exaggerated grotesque tongue or facial distortion

### Bhagavad Gita

Keep Gita visuals:
- luminous
- contemplative
- disciplined

Prefer:
- sacred battlefield atmosphere
- calm philosophical pacing
- symbolic inserts over noisy spectacle

## Render Package Workflow

Each publishable Blissful Chants video should have a dedicated render package.

Recommended location:
- `OpenMontage/projects/<project>/renders/<Render-Name>/`

Minimum contents:
- `<Render-Name>.md`
- `Thumbnail.jpg`
- approved anchor images
- generated clips
- final rendered outputs
- supporting artifacts needed for reuse

## Package Rules

### Script Package

The package file should use the render name directly.

Required sections:
- `Title`
- `Description`
- `Script`
- `References` or corroboration notes

### Title And Description

These are publish-facing, not internal notes.

They should be:
- engaging
- devotional
- accurate
- emotionally clear

Avoid:
- sensational horror framing
- vague poetic phrasing with no clear promise
- clickbait that misstates the subject

### Corroboration

Before a script is considered ready:
- corroborate factual or scriptural claims
- distinguish scripture, retelling, and devotional interpretation when needed
- keep source notes in the package

### Thumbnail

Every render package should include a ready-to-use `Thumbnail.jpg`.

Thumbnail rules:
- clear title or close title variant
- devotional tone
- legible at small size
- visually consistent with the package anchors

### Reuse

Each package should remain useful later for:
- YouTube publishing
- Shorts recuts
- localization
- narration swaps
- future rerenders

### Channel Intro

Default channel intro asset:
- `/Users/sunitjoshi/Documents/Documents/BlissfulChants/Blissful-Intro.mp4`

Use it unless the project explicitly opts out.

## 4-Minute Story Template

Use this as the default long-form devotional story shape for `3m 30s` to `4m 30s` videos.

### Core Thesis

The format works because it relies on:
- a strong opening promise
- one locked visual world
- caption-led narrative beats
- simple motion
- gradual emotional escalation

It should move:
- from curiosity to meaning
- from spectacle to interpretation
- from story to spiritual payoff

### Runtime Shape

Recommended targets:
- runtime: `3m 30s` to `4m 30s`
- scene length: `4s` to `7s`
- emphasis cards: `1s` to `2s`
- total cuts: roughly `35` to `55`

Avoid overcutting.

### Five-Part Structure

#### 1. Hook

Target:
- first `0s` to `20s`

Goal:
- create immediate curiosity without disrespect

#### 2. Myth Setup

Target:
- `20s` to `60s`

Goal:
- establish conflict, fear, disorder, or question

#### 3. Sacred Turn

Target:
- `60s` to `150s`

Goal:
- shift from outer spectacle to spiritual meaning

#### 4. Human Relevance

Target:
- `150s` to `220s`

Goal:
- connect myth to inner life, surrender, ego, fear, ignorance, or protection

#### 5. Payoff And Close

Target:
- `220s` to end

Goal:
- land on spiritual takeaway, not only plot closure

### Caption Strategy

Captions are a retention tool, not decoration.

Rules:
- one idea per line
- short lines
- one emphasized phrase at a time
- alternate between statement, reveal, and interpretation

### Motion Strategy

Default to:
- push-ins
- parallax
- glow pulses
- text-card cuts

Reserve premium motion for:
- hero openings
- power-gathering moments
- final payoff beats

### First-Test Pack

For a new long-form topic, generate only:
- one hook close-up
- one mid-story symbolic image
- one closing devotional payoff frame

If those three belong to the same world, the format is viable.
