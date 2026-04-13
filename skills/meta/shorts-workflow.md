# Shorts Workflow — Meta Skill

## When to Use

Use this skill when working on YouTube Shorts packages inside OpenMontage.

This is the primary Codex-native workflow for:
- listing Shorts folders under `Design-Docs/ToPublish/Shorts/`
- inspecting the status of a selected folder
- validating an existing markdown package against the folder intent
- researching and improving the markdown package
- preserving strong existing work
- reviewing generated `scene-*.mp4` files
- updating the markdown `## Results` table

Use this skill instead of relying on the shell wrapper when you are already inside Codex and want the full workflow handled here.

## Scope

This skill is for the light Shorts package workflow:
- `Title`
- `Description`
- `Thumbnail`
- `Script`
- `Scenes`
- `Results`

It is not for:
- long-form YouTube packages
- automatic provider execution
- direct platform publishing

## Core Files

| Resource | Path | Purpose |
|---|---|---|
| Shorts root | `Design-Docs/ToPublish/Shorts/` | Source folders |
| Design guidance | `Design-Docs/ToPublish/Design-Changes.md` | Packaging rules |
| Strategy | `Design-Docs/Blissful-Chants-Strategy.md` | Channel fit and content priorities |
| Existing package | `<short-folder>/<slug>.md` | Existing source of truth |

## Codex-Native Workflow

### 1. Enumerate The Shorts Folders

List every folder under:
- `Design-Docs/ToPublish/Shorts/`

When presenting the options, show:
- `Idx`
- `Folder`
- `Status`

Status should reflect what exists, for example:
- `Empty`
- `MD`
- `MD, MP4:2`
- `MD, Thumbnail`

### 2. Establish Intent From The Folder Slug

Treat the folder name as the source of truth.

Examples:
- `Maa-Kali-5-Unknown-Facts` -> `Maa Kali 5 Unknown Facts`
- `Why-Maa-Kali-Stands-On-Shiva` -> `Why Maa Kali Stands On Shiva`

The markdown file should always be:
- `<folder-slug>.md`

### 3. Inspect Existing Work Carefully

If a markdown package exists:
- read it first
- validate it against the folder intent
- preserve good work

Preserve by default:
- `Script`
- `Scenes`
- `Results`

Only replace those sections when:
- they are missing
- they are clearly weak
- they are structurally broken
- the user explicitly asks for regeneration

Before editing an existing markdown package:
- create a timestamped backup beside it
- use the format `<slug>.backup-YYYY-MM-DD-HHMMSS.md`

### 4. Research And Corroborate

When improving a package, use web research.

Goals:
- corroborate factual claims
- distinguish scripture, devotional interpretation, and later retellings where needed
- avoid unsupported symbolic claims

Use research to improve:
- title accuracy
- description quality
- script trustworthiness
- scene prompt specificity

### 5. Apply Channel Strategy

Use `Blissful-Chants-Strategy.md` to align the package with the channel.

For Shorts:
- prefer discovery-led hooks
- keep copy concise and spoken-word friendly
- keep the deity/topic keyword visible
- make the promise concrete

### 6. Write Or Improve The Light Shorts Package

Target structure:

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

### 7. Scene Writing Rules

Scenes are for manual Kling Web UI generation.

Each scene should:
- map clearly to a script beat
- have a practical short duration
- contain a usable prompt
- avoid horror framing unless the subject truly requires fierce energy
- keep subtitle-safe framing in mind

Prefer `5` to `8` scenes for Shorts.

### 8. Review Generated MP4s

If `scene-*.mp4` files exist in the folder:
- compare them to the matching scene beat
- check basic duration sanity
- assess whether they are usable for publication

Recommended statuses:
- `Needs Generation`
- `Generate from scene prompt`
- `Checked`
- `Publishable`
- `Missing`

### 9. Update Results

Always ensure `## Results` exists.

If it already exists:
- preserve existing rows where possible
- add missing rows for missing scenes
- update rows using:
  - `Scene`
  - `Status`
  - `DateTime`

## Suggested Invocation Patterns

Use prompts like:

- `Use the shorts-workflow skill and list the available Shorts folders.`
- `Use the shorts-workflow skill on Maa-Kali-5-Unknown-Facts and inspect what exists.`
- `Use the shorts-workflow skill on Maa-Kali-5-Unknown-Facts, research it, and improve the markdown while preserving strong Script and Scenes.`
- `Use the shorts-workflow skill on Maa-Kali-5-Unknown-Facts and review any scene MP4s, then update Results.`

## Common Pitfalls

- Overwriting strong scene work just because research produced alternate wording.
- Making the title more dramatic but less accurate.
- Writing prompts too abstractly for manual Kling use.
- Letting devotional imagery drift into horror-coded visuals.
- Forgetting to create a backup before editing an existing package.
- Dropping or resetting the `Results` section unintentionally.
