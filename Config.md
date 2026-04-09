# OpenMontage Config

Purpose: define the default working rules for the Blissful Chants workflow so script generation, asset selection, and render packaging follow one repeatable system.

## Scope

These defaults are for:
- Blissful Chants YouTube videos
- deity-led spiritual storytelling
- English-language output only
- reference-first image selection from the local deity library
- dynamic supporting-image generation through FAL when local references do not exist

## Video Length

Default target:
- `4m 00s` to `4m 30s`

Default benchmark source:
- competitor reference analyzed from [video_analysis_brief.json](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/_analysis/competition_1_kali_full/video_analysis_brief.json)

Observed benchmark values from the competitor reference:
- duration: about `270.37s`
- total scenes: `48`
- average scene duration: about `5.63s`
- cuts per minute: about `10.65`
- pacing style: `steady_educational`
- transcript segments: `45`
- transcript words: `791`
- approximate narration density: about `176 words per minute`

Recommended Blissful Chants defaults based on that analysis:
- target scenes: `40` to `50`
- average scene hold: `4s` to `7s`
- hook segment: first `15s` to `25s`
- structure: hook, myth setup, sacred turn, human relevance, payoff
- narration density: moderate, not rushed
- recommended script length: about `650` to `800` spoken English words for a full `4m` to `4m30s` story

Narrative guidance:
- use one main narrator unless explicitly changed
- prefer short sentence rhythms over dense explanation blocks
- each scene should communicate one idea
- use impact cards sparingly for emphasis

Tone guidance:
- reverent
- mystical
- emotionally intense but spiritually grounded
- never horror-first
- never sensational at the cost of devotional dignity

Engagement guidance:
- open with a strong curiosity line in the first `1s` to `3s`
- keep visual identity locked across the whole video
- use captions as a narrative driver, not decoration
- alternate between visual scenes and short text-impact beats
- deliver one meaningful reveal every `10s` to `20s`

## Script Creation

User input:
- the user provides a broad topic, deity, verse, story, or spiritual question

AI responsibilities:
- research the topic before writing
- corroborate important claims from at least `2` to `3` sources
- prefer primary or reputable secondary sources when possible
- write a script that matches the `Video Length` defaults above unless the user overrides them
- keep all written output in English

Script output format:
- each script lives in its own subfolder under the current deity's `YouTube` folder
- folder name should match the script slug
- inside that folder, create `<script-slug>.md`

Required script markdown sections:
- `Title`
- `Description`
- `Script`
- `References`

Title and description rules:
- written for YouTube
- attention-grabbing, mystical, and clear
- respectful to the deity and source tradition
- no clickbait that frames the deity as evil, monstrous, or demonic

Default output path pattern:
- `<Asset Root>/<Current Deity>/YouTube/<script-slug>/<script-slug>.md`

## Asset Root

Primary asset root:
- `/Users/sunitjoshi/Documents/Documents/BlissfulChants/Assets/Deities`

Deity reference pattern:
- `<Asset Root>/<Current Deity>/YouTube`

Shared demon reference pattern:
- `/Users/sunitjoshi/Documents/Documents/BlissfulChants/Assets/Deities/Demons`

Competitor/reference source pattern:
- `/Users/sunitjoshi/Documents/Documents/BlissfulChants/Assets/Deities/Competitor`

Rule:
- use the current deity's `YouTube` folder first for all deity-specific references
- use the shared `Demons` folder only when the story requires a demon or rakshasa reference
- use competitor/reference assets only for analysis, not direct reuse in published output

## Current Deity

Default current deity:
- `MahaKali`

Current deity asset folder:
- `/Users/sunitjoshi/Documents/Documents/BlissfulChants/Assets/Deities/MahaKali/YouTube`

Rule:
- only pull deity reference images from the `Current Deity` folder unless the user changes the deity
- when the deity changes, update this section first before generating new scripts or assets

## Scene Asset Strategy

Reference-led assets:
- for deity scenes, start from the `Current Deity` reference folder
- for demon scenes, use the `Demons` folder when relevant

Scene selection rule:
- for each script scene, pick the closest-fitting reference image from the local folder first
- use that reference to guide scene-specific generation when a more tailored visual is needed

Dynamic generation rule:
- if a scene needs non-deity support imagery like a meditating family, walking devotee, temple crowd, battlefield sky, village path, or symbolic object, generate it dynamically via FAL
- generated support imagery should be tuned to the script scene and the Blissful Chants palette
- generated support imagery should remain caption-safe and visually consistent with the rest of the video

Default production priority:
1. local deity reference
2. local demon reference if relevant
3. FAL-generated support image
4. premium FAL motion only for hero beats after stills are approved

## Language

Default language:
- English only

Rules:
- titles, descriptions, scripts, captions, and overlays should all be in English unless the user explicitly changes this
- no mixed-language overlays by default

## Preview Strategy

Default testing path:
- start with still-image generation and simple Remotion motion
- validate tone, structure, and pacing cheaply
- add premium motion clips only after the still-first preview feels right

Why:
- cheaper
- faster
- easier to iterate
- closer to the proven competitor structure

## Notes

This config is meant to drive future script and asset workflows.

If a future automation step needs exact transcript-density targets from benchmark videos, local transcription support should be installed first. The current benchmark values here are based on the analyzed duration, scene structure, pacing, and visual review of the competitor reference, not exact word-count extraction.
