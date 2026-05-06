# Prompt Learnings — Baglamukhi Sadhana Anubhav

Permanent knowledge base for image generation on this project. Read before writing or refining any image generation prompt. Update whenever a new pattern is confirmed or a dead end is hit.

**Primary tool: GPT-4o (ChatGPT).** MidJourney sections below are historical — kept as reference for why we switched.

---

## Character Reference Rules

- **Back-facing sadhak reads ambiguously gendered** when MAA_REF is the only cref — the female deity's energy bleeds into the figure's silhouette. Always include explicit male descriptors: `young Indian man male devotee, broad muscular back, masculine build, broad male shoulders, bare muscular male back`. Add negatives: `no female sadhak, no woman devotee`.
- **"primary/secondary subject" labels push the secondary figure too small.** Maa renders as a tiny idol or distant portrait. Use explicit spatial anchors instead: `foreground large figure [sadhak]` and `upper center of the frame large prominent floating divine figure [Maa]`. Add `filling the upper half of the frame` to force her scale.
- **Add `no idol, no statue, no portrait painting` to negatives** when Maa needs to be a living floating figure — without these, she collapses into a small ornamental object in the background.
- **`--cref MAA_REF --cw 80` in two-figure scenes eats the sadhak.** The cref is so dominant it turns the whole image into a deity portrait — 3 of 4 outputs had no sadhak at all. For two-figure compositions where the sadhak is the primary subject, drop the cref entirely and let text description carry Maa.
- **Back-facing sadhak scenes: MAA_REF only.** Never include SADHAK cref when his face isn't visible. Two crefs in the same prompt causes the sadhak to absorb the deity's divine appearance (jewelry, ornaments, skin glow bleed onto his bare back). Face lock is pointless when the face is hidden.
- **Multiple arms persist despite `no multiple arms` negative.** Stack the negatives: `no multiple arms, no third arm, no fourth arm, no extra limbs, no extra hands`. The model associates floating deities strongly with multi-armed iconography.
- **Two crefs in one prompt = character bleeding.** Deity attributes transfer to the human figure and vice versa. Use one cref per scene; let text description carry the other character.
- **`--sref` is wrong for character identity.** It locks style, not face/costume — causes deity drift and costume override across variants. Always use `--cref` for character face lock.

## Style & Weight Rules

- **`--sw 60` is too high.** Overrides composition entirely. Use `--sw 20` max or drop `--sw` entirely.
- **`--s 30` for cinematic 3D scenes** (not 70). Higher style weight fights the 3D render style.
- **`--cw 80`** is the confirmed working value for character reference weight on this project.

## Maa Baglamukhi Rendering

- Without strong femininity descriptors, MidJourney defaults to a male deity (Vishnu/Krishna appearance). Always include: `explicitly female goddess, woman deity, feminine face feminine body feminine form, long black hair, clearly female`.
- Add to negatives: `no Vishnu, no Krishna, no masculine figure, no male deity`.
- She must be described as `floating freely in the open air, NOT on any throne or altar` — otherwise she renders as a statue, idol, or wall painting rather than a living floating goddess.

## Environment / Architecture Problems

- **"cinematic 3D art style" pulls toward palace/temple interiors** regardless of negatives. Negatives alone don't win — add strong positive: `plain domestic home room, simple home interior`.
- Adding `no palace` to negatives helps; `no temple arch, no alcove, no niche` are also needed.

## Per-Scene Cref Map

| Scene | Image | Cref(s) to upload | Reason |
|---|---|---|---|
| Scene-1 | Img 1 (folk back-facing) | MAA_REF only | Sadhak's face never seen |
| Scene-1 | Img 2 (guru in cave) | SADHAK_A_REF only | Sadhak faces viewer; no Maa in scene |
| Scene-1 | Img 3 (cinematic 3D thumbnail) | None | No cref — text alone gave best female face; arch framing replaced floating |
| Scene-2 | Imgs 1 & 3 (white kurta) | SADHAK_A_REF only | Sadhak faces viewer; no Maa in scene |
| Scene-2 | Img 2 (empty room) | None | No characters |
| Scenes 3–5 | All | SADHAK_B_REF only | Ritual attire; no floating Maa in these scenes |

## Thumbnail Composition (Confirmed Working — Scene-1 Img 3)

After 14 rounds of iteration, what finally produced an approved thumbnail:

- **No cref at all** — drop MAA_REF entirely for two-figure cinematic scenes. Text description alone produced the best female face rendering.
- **Glowing arch framing Maa** gave her the scale and prominence that "floating in open air" never could. The arch acts as a natural frame that forces Maa to be large and centered.
- **Accept the arch** — `no temple arch` in negatives was counterproductive for the thumbnail. The arch framing is what made Maa prominent. For thumbnails, composition and readability > exact spec compliance.
- **Accept multi-armed Maa** — after extensive negative stacking, the model will not reliably produce a two-armed floating Baglamukhi. For a devotional thumbnail at scroll speed, multi-armed reads as powerful divine iconography, not an error.
- **Sadhak locked by text alone** — `young Indian man male devotee, broad muscular back, masculine build, bare upper back in traditional sadhak attire, back fully turned toward camera` is sufficient without any cref.

**Approved thumbnail:** `Scene-1-3.png`

## MidJourney Web UI Notes (historical)

- **Character References** and **Omni Reference** are separate buttons. Use **Character References** for `--cref` — it maps to `--cw` weight. Omni Reference maps to `--oref` / `--ow` (different parameter).
- To upload two crefs: click the Character References button, upload both images in the same panel.
- Remove `--cref NAME` text from the prompt when uploading via UI — keep `--cw 80` in the prompt text.

---

## GPT-4o (ChatGPT) — Active Tool

### Why we switched from MidJourney

- MidJourney could not reliably produce two-armed Maa Baglamukhi despite extensive negative stacking — multi-armed iconography kept bleeding in.
- Female face rendering for Maa required heavy descriptors and was still inconsistent.
- "Cinematic 3D" style kept pulling toward palace/temple interiors regardless of negatives.
- GPT-4o solved all three in one or two shots.

### What works well

- **Two-arm constraint respected** — GPT-4o follows `exactly two arms only` reliably without negative stacking.
- **Female deity face** — no need for heavy femininity descriptors; GPT-4o defaults correctly with `female goddess`.
- **Architecture control** — `simple domestic home room` honored without needing a list of negatives.
- **Reference image upload** — upload image in chat before sending prompt; GPT-4o uses it for character/costume consistency without weight tuning.
- **Edits and variations** — can describe what to change; GPT-4o applies surgical edits across generations.
- **Scene-1 guru/sadhak continuity works across varied poses** when the stable identifiers are repeated: dark teal turban, long white beard, white-clad sadhak, warm amber cave light, moonlit cave opening. Seated teaching, close listening, standing instruction, and symbolic moon insert can cut together without exact face matching because costume, palette, and setting carry continuity.
- **Character-driven support cards add motion without new plot events.** Good long-form filler beats include guru's raised hand, sadhak listening in namaste, sadhak sitting alone with pensive expression, lamp flame, and moon seen from cave opening. These create local camera moves and emotional pacing between anchor scenes.

### Surgical edit rules (GPT-4o)

- **Framed Maa image edits can be isolated** if the prompt says `Edit only the framed Maa Baglamukhi image` and explicitly lists altar elements to preserve. Without this, GPT-4o may alter the bajot, yantra, mounds, lighting, or sadhak while fixing the portrait.
- **Gada replacement needs anti-trident language.** Use `replace the trident with a golden gada mace / club` plus `Remove all trident/Shiva symbolism completely`. Otherwise trident-like shapes can persist or return in later edits.
- **Four-arm Maa needs a final arm layout.** When correcting arm count, specify `exactly four arms total` and list the intended hands: `one hand holding the golden gada mace`, `one blessing hand`, `one hand holding the small golden sacred object`, `one relaxed hand`. If there is an obvious bad limb, identify it as `the awkward central overlapping arm/hand near her chest`.
- **Gada side must be stated from viewer perspective.** For continuity in framed portraits, say `golden gada mace held in Maa Baglamukhi's left-side hand from the viewer's perspective`; otherwise the model may place it in the opposite hand while still satisfying "holding gada".
- **Seven incense mounds require repeated count constraints.** Use `exactly seven incense mounds total, not eight` and `each incense mound must have exactly one clove on top`. Count both mound number and clove-per-mound in every edit prompt that touches the altar.
- **Scene-4/Scene-5 altar edits work best as preservation-first prompts.** Start with what must remain unchanged: `preserving the overall composition, sadhak, room, lighting, bajot, yantra, diya, flowers, smoke, and devotional atmosphere`; then request the single correction.

### Reference upload workflow (GPT-4o)

- Upload the reference image(s) in the chat message along with the prompt text.
- No special syntax needed — just describe what the reference is for in the prompt or a brief note.
- Notes in script file use `**Ref:** Upload \`filename.png\`` to flag which reference to attach.

## Thumbnail Composition — Courtroom Hook (Confirmed Working)

**Approved image:** `Courtroom-1.png`

What worked:
- Semi-realistic painterly style (not folk illustration) — more cinematic, stronger thumbnail impact
- Wide courtroom establishing shot with sadhak in foreground at the railing, head bowed
- Maa rendered fully visible and prominent in upper-left, golden glow and gada clearly readable
- Police officer, judge, lawyer, stacked files — authentic Indian district court vocabulary in one frame
- Golden particle scatter as connective tissue between Maa and the courtroom floor

**For the thumbnail variation (`Courtroom-2.png`):**
The key change from the approved image is the sadhak's gaze — head bowed reads "defeat" for in-video use, but a thumbnail needs the desperate-upward-look that creates a curiosity gap ("will she help him?"). Use the edit prompt in Scene-1 Image 1b to generate this via ChatGPT's "Describe edits" button.

**Competitor thumbnail pattern to match:**
- Deity fills upper 35-40% of frame — large, immediately recognizable
- Protagonist looking UP toward deity with desperation or hope
- Background darker than foreground — high contrast between divine glow and courtroom shadow
- Leave lower quarter clear for title text overlay added in post

---

## Courtroom & Secular Settings

- **Courtroom architectural vocabulary** for Indian district/sessions court: `colonial-era wooden judge's bench elevated at the far end, worn wooden benches and railing dividers, lawyers in black coats, stacks of thick document files tied with red ribbon, ceiling fans, faded framed portraits on yellowed walls, high windows with grey daytime light`. This gives GPT-4o a complete, specific room without ambiguity.
- **Subtle / translucent Maa for non-ritual scenes**: When Maa appears as a hint of divine protection (not a full apparition), describe her as `extremely faint barely-visible translucent golden haze, ghostlike outline of a female divine form in a sari barely discernible as golden mist, soft luminous golden shimmer, no crown visible, no solid figure`. Do NOT upload `Maa-Baglamukhi.png` as reference — the solid reference will override the translucency instruction and render her too defined. Text alone carries the ghost quality.
- **Sadhak in secular attire** (court, home, casual): always State A (`plain white kurta`). State B (yellow dhoti) only in ritual scenes (Scene 3 onward). Upload `Sadhak_A_Ref.png` whenever sadhak's face is visible.

### Per-scene reference map (GPT-4o)

| Scene | Image | Reference to upload | Reason |
|---|---|---|---|
| Scene-1 | Img 0a (courtroom wide) | `Sadhak_A_Ref.png` | Sadhak's worried face visible |
| Scene-1 | Img 0b (courtroom close + translucent Maa) | `Sadhak_A_Ref.png` | Sadhak's face close; NO Maa ref — text carries translucency |
| Scene-1 | Img 1 (folk back-facing) | `Mata-Baglamukhi.png` | Floating Maa above sadhak |
| Scene-1 | Img 2 (guru in cave) | `Sadhak_A_Ref.png` | Sadhak faces viewer |
| Scene-1 | Img 3 (thumbnail) | None | Text alone worked best |
| Scene-1 | Img 4 (guru with portrait and mala) | `Sadhak_A_Ref.png` | Sadhak faces viewer |
| Scene-1 | Imgs 5, 7, 8 (guru/sadhak support beats) | `Sadhak_A_Ref.png` | Keep young sadhak face/costume consistent |
| Scene-1 | Img 6 (Chaudas moon insert) | None | Symbolic object/setting insert, no characters |
| Scene-2 | Imgs 1 & 3 (white kurta) | `Sadhak_A_Ref.png` | Sadhak faces viewer |
| Scene-2 | Img 2 (empty room) | None | No characters |
| Scenes 3–5 | Sadhak scenes | `Sadhak_B_Ref.png` | Yellow dhoti ritual attire |
| Scenes 3–5 | Detail/object-only shots | None | No characters |

---

## Image File Naming Convention

### Rule: `Scene-N-<num>[<suffix>].png`

Image files must follow this pattern exactly for `render-scene` to sort them correctly:

| Example | Meaning |
|---|---|
| `Scene-1-1a.png` | Scene 1, image 1a |
| `Scene-1-1b.png` | Scene 1, image 1b |
| `Scene-1-2.png` | Scene 1, image 2 |
| `Scene-1-3a.png` | Scene 1, image 3a |
| `Scene-1-3c.png` | Scene 1, image 3c |

**Sort key** is `(integer, suffix)` — e.g. `1a` → `(1, 'a')`, `3c` → `(3, 'c')`, `4` → `(4, '')`. This is handled by `image_sort_key()` in `render_scene.py`.

### Why this matters
The original `image_sort_key` did `int(parts[2])` which threw `ValueError` on any suffix letter (`1a`, `3a`, `3b`, `3c`) and collapsed all of them to sort key `0`. They then rendered in arbitrary filesystem order — causing the video to start mid-sequence (e.g. `3a` before `1a`). Fixed 2026-05-06.

### Do not use
- `Scene-1-2-1.png` style (extra hyphen-number) — the third segment `"2"` parses fine but the convention is inconsistent. Rename to `Scene-1-2.png`.
- Non-numeric prefixes or scene-level folders — the glob is flat: `Scene-N-*.png` in the project root.
