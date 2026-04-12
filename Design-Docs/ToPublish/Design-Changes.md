## YouTube Structure

Use `OpenMontage/Design-Docs/ToPublish/` as the root folder for publish-ready YouTube work.

If there are multiple format families later, organize under:
- `OpenMontage/Design-Docs/ToPublish/Shorts/`
- `OpenMontage/Design-Docs/ToPublish/LongForm/`

For example, if we are creating a short titled `Maa Kali 5 Unknown Facts`, the package should live in:
- folder: `OpenMontage/Design-Docs/ToPublish/Shorts/Maa-Kali-5-Unknown-Facts/`
- main file: `Maa-Kali-5-Unknown-Facts.md`

The folder name and main markdown file should always use the same slug.

## Purpose Of This Structure

This structure should not store only a script draft.

It should capture the full lifecycle of a YouTube creation:
- why the idea exists
- why it fits the channel strategy
- what research supports it
- what the final publish-facing metadata is
- how the scenes should be generated
- what assets belong to the render package
- when it should be posted
- what happened after posting

## Required Package Sections

Each main markdown file should contain the following sections.

### 1. Overview

This is the top-level control block for the video.

Include:
- `Slug`
- `Format`: `Short` or `LongForm`
- `Series` or channel lane if applicable
- `Status`: `Idea`, `Researching`, `Script Ready`, `Visuals Ready`, `Scheduled`, `Posted`
- `Target Duration`
- `Aspect Ratio`: usually `9:16` for Shorts
- `Language`
- `Primary Goal`: discovery, views, watch time, devotional utility, subscriber growth

### 2. Premise

This is the starting point or reason for the idea.

Include:
- the core idea
- why this topic matters
- the devotional, educational, or emotional promise
- what audience question it answers

### 3. Strategy Fit

This section explains why the idea belongs on the channel.

Include:
- which content pillar it belongs to
- whether it is a core lane or a measured experiment
- what format logic supports it
- any analytics or observed pattern that justify making it

Examples of content pillars:
- practical devotional utility
- short story or miracle hook
- chant or mantra snippet
- kavach, protection, or recitation
- Shiva secondary lane

### 4. Title

This is the publish-facing YouTube title, not an internal note.

Rules:
- make it engaging
- keep the deity or topic keyword visible
- make the promise concrete
- keep it accurate to the script

### 5. Description

This is the publish-facing YouTube description.

Rules:
- short and catchy by default
- accurate to the script
- devotional in tone where appropriate
- can include a short CTA if needed

### 6. Sources And Corroboration

Before a script is considered ready, track the references used.

Include:
- source links
- scriptural source if applicable
- whether the content is scripture, retelling, commentary, or devotional interpretation
- notes on any uncertain or conflicting claims

If the `Script` section already has content, use it as the base and only ask whether corroboration via web research is needed before changing factual material.

### 7. Script

The script should be written in English unless otherwise specified.

Rules:
- write for spoken delivery, not only for reading
- ensure it works for text-to-audio or narration
- match the target runtime
- keep the tone aligned with the channel
- distinguish between sacred storytelling and unsupported invention

Recommended sub-fields:
- `Hook`
- `Body`
- `Close`
- `CTA` if needed

### 8. Visual And Brand Lock

This section prevents scene drift and should be defined before full generation.

Include:
- deity depiction rules
- style family
- color palette
- lighting logic
- framing grammar
- subtitle-safe composition rule
- text overlay rule
- reverence constraints
- negative constraints such as no horror framing, no gore, no random costume drift

This should stay consistent across all scenes in the same video package.

### 9. Asset Plan

This section defines what files need to exist for production and publication.

Include:
- thumbnail concept
- title card if needed
- narration or TTS plan
- music or ambience plan
- anchor images
- generated clips
- subtitle or caption output
- final render name

Expected render package assets may include:
- `<Slug>.md`
- `Thumbnail.jpg`
- narration audio
- anchor images
- scene clips
- final rendered video

### 10. Scenes

This section should not be only a prompt dump.

Lay out numbered scenes such as `Scene-1`, `Scene-2`, and so on with enough structure that they can be generated consistently in Kling, Veo, Omni, or another supported tool.

Each scene should include:
- scene number
- purpose of the scene
- script line or narration beat covered
- expected duration
- visual description
- camera instruction
- motion intensity
- subtitle or text overlay note
- prompt or generation instruction
- reference or anchor asset if applicable
- output filename if one is assigned

### 11. Production Notes

Use this section for execution details that arise during generation.

Include:
- model choice and why
- seed notes if relevant
- reroll notes
- visual problems found
- continuity issues
- decisions about switching provider or workflow

### 12. Post Timeline

This section tracks publishing and follow-up.

Include:
- tentative publish date and time
- scheduled platform
- checkbox for whether it has been posted
- actual posted date and time
- published URL
- thumbnail used
- early performance notes if tracked
- issues for anything that cropped up later

## Recommended Minimal Template

```md
# <Title>

## Overview
- Slug:
- Format:
- Series:
- Status:
- Target Duration:
- Aspect Ratio:
- Language:
- Primary Goal:

## Premise

## Strategy Fit
- Content Pillar:
- Why now:
- Analytics or reasoning:

## Title

## Description

## Sources And Corroboration
- Source 1:
- Source 2:
- Notes:

## Script
### Hook
### Body
### Close
### CTA

## Visual And Brand Lock
- Deity depiction:
- Style family:
- Palette:
- Lighting:
- Framing:
- Subtitle-safe rule:
- Negative constraints:

## Asset Plan
- Thumbnail:
- Narration:
- Music:
- Anchor images:
- Scene outputs:
- Final render:

## Scenes
### Scene-1
- Purpose:
- Script beat:
- Duration:
- Visual:
- Camera:
- Motion:
- Text overlay:
- Prompt:
- Reference asset:
- Output:

## Production Notes

## Post Timeline
- Tentative publish date/time:
- Posted: [ ]
- Actual post date/time:
- URL:
- Thumbnail used:
- Notes:
- Issues:
```

## Operating Rules

- The title and description are publish-facing fields and should be written as final YouTube candidates.
- The folder slug and markdown filename must match exactly.
- A script should not be marked ready without sources or corroboration notes where factual claims are involved.
- Scenes should be provider-agnostic at the planning layer and provider-specific only where generation instructions are needed.
- Visual consistency rules should be locked before batch generation begins.
- The package should remain useful after publishing, so post results and issues must be preserved instead of discarded.

## Sora Usage

`Sora` can be used for scene-video generation in this workflow.

Preferred use:
- generate scene-by-scene clips, not one full video from the entire script
- use it after the script, scene plan, and visual lock are defined
- use image-guided or reference-led generation where possible for better continuity

Recommended use cases:
- early scene testing before paying for a `Kling` subscription
- short vertical devotional clips
- fast exploration of motion, framing, and tone
- selective scenes where synchronized audio is useful

Rules for use:
- do not depend on Sora to invent the entire visual language from scratch
- keep the same visual and brand lock used for other providers
- reuse approved anchor images and scene descriptions
- evaluate each scene for reverence, identity consistency, subtitle-safe composition, and motion stability

Workflow note:
- use `Sora` for manual or API-based scene generation when access is available
- continue keeping scene planning provider-agnostic so the same package can still be run through `Kling`, `Veo`, `Omni`, or another tool later if needed

Cost and subscription note:
- if `Sora` access is available and quality is sufficient, it can be used first so a `Kling` subscription can be deferred
- revisit the need for `Kling` only if Sora quality, access, or control is not enough for the current batch

Long-term note:
- do not make the package structure Sora-only
- keep prompts, references, and asset planning portable across providers
