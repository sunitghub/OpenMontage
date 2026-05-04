# Prompt Learnings — Baglamukhi Sadhana Anubhav

Permanent knowledge base for image generation on this project. Read before writing or refining any MidJourney prompt. Update whenever a new pattern is confirmed or a dead end is hit.

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

## MidJourney Web UI Notes

- **Character References** and **Omni Reference** are separate buttons. Use **Character References** for `--cref` — it maps to `--cw` weight. Omni Reference maps to `--oref` / `--ow` (different parameter).
- To upload two crefs: click the Character References button, upload both images in the same panel.
- Remove `--cref NAME` text from the prompt when uploading via UI — keep `--cw 80` in the prompt text.
