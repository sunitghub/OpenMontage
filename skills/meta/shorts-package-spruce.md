# Shorts Package Spruce — Meta Skill

> Superseded by `meta/shorts-workflow.md` for the full Codex-native workflow.
> Keep this file as a narrow package-improvement reference only.

## When to Use

Use this when you need to create or improve a YouTube Shorts markdown package under `Design-Docs/ToPublish/Shorts/`.

This skill is specifically for the light Shorts package workflow:
- `Title`
- `Description`
- `Thumbnail`
- `Script`
- `Scenes`
- `Results`

Use it when:
- a Shorts folder exists but has no markdown package yet
- a markdown package exists and needs research-backed improvement
- the package should be made more usable for manual Kling Web UI scene generation

Do not use this skill for:
- long-form YouTube packages
- direct MP4 validation
- automatic provider execution

## Prerequisites

| Resource | Path | Purpose |
|---|---|---|
| Shorts root | `Design-Docs/ToPublish/Shorts/` | Source folders to inspect |
| Design guidance | `Design-Docs/ToPublish/Design-Changes.md` | Packaging rules |
| Channel strategy | `Design-Docs/Blissful-Chants-Strategy.md` | Topic and format strategy |
| Existing package | `<short-folder>/<slug>.md` | Existing source of truth, if present |

## Process

### 1. Establish The Folder Intent

Treat the folder slug as the source of truth.

Examples:
- `Maa-Kali-5-Unknown-Facts` -> `Maa Kali 5 Unknown Facts`
- `Why-Maa-Kali-Stands-On-Shiva` -> `Why Maa Kali Stands On Shiva`

The markdown file should be named exactly:
- `<folder-slug>.md`

### 2. Inspect Existing Work Carefully

If the markdown file already exists:
- read it first
- preserve good work
- do not overwrite strong `Script`, `Scenes`, or `Results` sections casually

Before changing an existing markdown package:
- create a timestamped backup beside it
- use the format `<slug>.backup-YYYY-MM-DD-HHMMSS.md`

Preserve by default:
- `Script`
- `Scenes`
- `Results`

Only replace those sections when:
- they are missing
- they are structurally broken
- they clearly do not match the folder intent
- the user explicitly asks for regeneration

### 3. Research And Corroborate

Use web research when improving factual or interpretive claims.

Goals:
- corroborate factual claims
- distinguish between scripture, devotional interpretation, and later retellings where needed
- avoid making up unsupported symbolic claims

Research should improve:
- title accuracy
- description quality
- script clarity and trustworthiness
- scene prompt specificity

### 4. Apply Channel Strategy

Use `Blissful-Chants-Strategy.md` to make the package fit the channel.

For Shorts:
- prefer discovery-oriented hooks
- keep language concise and spoken-word friendly
- keep the deity/topic keyword visible
- make the payoff concrete

### 5. Write The Light Shorts Package

The target structure is:

```md
# <Title>

## Title

## Description

## Thumbnail
- Title Text:
- Prompt:

## Script
### Hook
### Body
### Close

## Scenes
### Scene-1
- Purpose:
- Script beat:
- Duration:
- Visual:
- Camera:
- Motion:
- Prompt:
- Output:

## Results
| Scene | Status | DateTime |
|---|---|---|
| 1 | Needs Generation | |
```

### 6. Scene Writing Rules

Scenes are for manual Kling Web UI generation.

Each scene should:
- be concise
- map clearly to a script beat
- have a practical duration
- include a usable prompt
- avoid horror framing unless the topic truly requires fierce energy
- preserve subtitle-safe lower framing where appropriate

Prefer `5` to `8` scenes for Shorts.

### 7. Results Section Rules

Always ensure a `## Results` section exists.

If it already exists:
- preserve existing rows and statuses
- add missing rows for missing scenes

Recommended statuses:
- `Needs Generation`
- `Generate from scene prompt`
- `Checked`
- `Publishable`
- `Missing`

### 8. Final Check

Before finishing, verify:
- markdown filename matches folder slug
- title matches folder intent
- description is publish-facing
- script is spoken-word friendly
- scenes are generation-ready
- results table exists
- existing strong work was preserved unless there was a reason to replace it

## Common Pitfalls

- Rewriting a good `Scenes` section just because research produced alternate wording.
- Making the title more dramatic but less accurate.
- Writing scene prompts that are too abstract for manual generation.
- Letting devotional content drift into horror-coded visuals.
- Dropping the `Results` section during a rewrite.
