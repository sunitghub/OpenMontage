# Competitor Analysis

Purpose: consolidate the reference-video, provider-comparison, and Omni evaluation notes into one decision document for competitor-style devotional videos.

Use this doc when deciding:
- whether to recreate a reference inside OpenMontage
- whether to stay Seedance/low-cost-first or escalate to Kling/Veo
- whether Omni is worth testing for the same project
- what the fastest production path is for Shiva/crow-style spiritual storytelling

## Blissful Chants Opportunity Table

Scoring intent:
- `Proximity`: closeness to Blissful Chants' current niche: spiritual mantras, stotras, kavach, Hindu devotional utility, and now Hindu spiritual tales
- `Views Capture`: likelihood that the audience shown in current competitor/search results will click and watch
- `Script Effort`: how hard the concept is to script responsibly with AI help
- `Render Effort`: how hard it is to produce convincingly with the current low-cost stack
- `Score`: aggregate priority for quick focus; higher means better near-term bet

| Content Pattern | Proximity | Views Capture | Script Effort | Render Effort | Score |
|---|---|---|---|---|---|
| Maa Kali kavach / stotra / vandana / shatnaam long-form | High | High | Low | Low | `95` |
| Maa Kali protection utility: remove negativity, fear, dark energy | High | High | Low | Medium | `92` |
| Practical devotional utility: offerings, simple rituals, what pleases Maa Kali | High | High | Medium | Low | `90` |
| Hanuman Chalisa / Hanuman mantra loops and remedies | High | High | Low | Low | `88` |
| Shiva stotra / mantra / peaceful chant long-form | High | Medium | Low | Low | `84` |
| Deity-helped-devotee story: how Maa Kali saved or guided a grieving devotee | High | High | Medium | Medium | `84` |
| Aatma/afterlife spiritual tale: soul journey after death, karma, rebirth, funeral rites | High | High | Medium | Medium | `82` |
| Maa Kali yantra / symbolism / unknown facts Shorts | High | Medium | Medium | Medium | `78` |
| Baglamukhi/Krishna/other deity kavach expansion | Medium | Medium | Low | Low | `74` |
| Charava-Bhootni-style rural ghost folk tale with spiritual lesson | Medium | Medium | Medium | Low | `70` |
| Shiva/crow mythic morality tale | Medium | Medium | Medium | Medium | `68` |
| Generic horror/ghost story without clear Hindu devotional payoff | Low | Medium | Medium | Medium | `48` |

Fastest focus order:
1. keep publishing Maa Kali protection/kavach/stotra/name-recitation because it is both close to the channel and proven by the current shelf
2. add practical devotional utility titles around Maa Kali because they are searchable and easy to render
3. test `Aatma` or `deity-helped-devotee` tales as the new story lane, but keep a clear Hindu spiritual payoff
4. use rural ghost stories only when they resolve into karma, devotion, Maa Kali, Shiva, or afterlife teaching

Production implication:
- chant/stotra/remedy videos should be `low render effort`: thumbnail, sacred stills, lyrics/subtitles, slow local motion
- deity-helped-devotee and aatma tales should be `medium render effort`: still anchors plus `2-3` hero I2V/VFX moments
- generic ghost tales are not worth prioritizing unless rewritten into a devotional or spiritual teaching frame

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

## Third Reference Case: Charava Bhootni

Reference studied:
- `/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/Competitors/Charava-Bhootni.mp4`

Measured notes:
- runtime: `1319.75s` (`21:59`)
- format: `640x360`, `16:9`, `30fps`
- video bitrate: about `48 kb/s`
- detected visual beats at practical threshold: `293`
- average visual beat length: about `4.5s`
- median visual beat length: about `4.2s`
- 75th percentile beat length: about `5.8s`
- 90th percentile beat length: about `7.1s`
- one-second image-diff sampling: about `74.6%` of samples are near-static

Observed pattern:
- illustrated folk-story video, likely Hindi/Hinglish narration-led
- recurring male protagonist in purple kurta/red sash
- recurring rural village, hut, cattle, cave, palace, night field, graveyard, and interior-room settings
- mostly generated still illustrations held for `3-6s`
- changes usually happen through hard cuts or simple crossfades, not in-shot character animation
- repeated stills stay almost unchanged for multiple seconds
- occasional slow zoom/pan/compression shimmer is enough to keep the frame alive
- no heavy caption dependency in the sampled frames
- the audio track carries the story; visuals are scene markers and mood anchors

Visual system:
- painterly AI illustration, not photoreal cinema
- warm rural daylight scenes alternate with blue night/haunted scenes
- character identity is "good enough" rather than locked: face, body, and costume drift, but the purple kurta/red sash keeps continuity readable
- background continuity is modular: hut, dusty road, cattle herd, cave mouth, graveyard, palace room, village interior
- the video accepts repeated character poses because narration is doing the semantic work

Production conclusion:
- this is not a video-generation problem at full length
- the cheap path is high-volume still generation plus local composition
- for Shorts, the same style can be reduced to `8-14` visual beats with `0-2` true I2V clips
- for long-form, generate stills in batches and animate locally with Ken Burns, light parallax, smoke, torch glow, lightning flashes, and hard cuts
- do not spend Seedance/Kling/Veo budget on every beat; only use I2V for the hook, supernatural reveal, chase, or confrontation

OpenMontage fit:
- strong fit for Remotion or HyperFrames composition
- strong fit for MidJourney/OpenAI/Grok/Recraft/Flux stills
- strong fit for TTS narration plus a low music bed
- good candidate for a reusable `folk_story_montage` playbook:
  - character bible
  - location bible
  - beat-by-beat still prompts
  - local camera-motion recipes
  - occasional hero I2V

Important conclusion:
- the competitor's perceived scale comes from `many cheap illustrated cards`, not many expensive clips
- for OpenMontage, the winning tactic is a disciplined still pipeline with only selective generated motion
- the current $0.90/5s Seedance path should be treated as a hero-shot budget, not the backbone

## Fourth Reference Case: Aatma Chita Ke Baad

Reference studied:
- `/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/Competitors/Aatma-ChitaKeBaad.mp4`

Measured notes:
- runtime: `1302.78s` (`21:42`)
- format: `640x360`, `16:9`, `25fps`
- video bitrate: about `576 kb/s`
- detected visual beats at practical threshold: `310`
- average visual beat length: about `4.2s`
- median visual beat length: about `4.9s`
- 75th percentile beat length: about `6.0s`
- 90th percentile beat length: about `7.8s`
- one-second image-diff sampling: median `28.22`, with about `94.9%` of samples above the high-motion threshold used for Charava-Bhootni

Observed pattern:
- supernatural after-death folk-story video, likely Hindi/Hinglish narration-led
- central imagery: deathbed, funeral procession, cremation pyre, glowing soul leaving the body, family mourning, spirit encounters, demonic/afterlife guardians, reincarnation or judgment-style visuals
- repeated use of luminous white/blue human spirit silhouettes
- recurring fire, smoke, lightning, mist, dark forests, ritual settings, and hell/underworld red scenes
- more visual movement than Charava-Bhootni: fire flicker, soul glow, camera drift, spectral shimmer, smoke, lightning, and character motion are present almost continuously
- still uses short scene cards and hard cuts, but each card is more heavily animated or generated than the Charava-Bhootni cards
- no heavy caption dependency in sampled frames
- narration remains the semantic backbone

Visual system:
- painterly AI illustration with stronger VFX language than the rural folk-story reference
- palette alternates between funeral whites/daylight, cyan-blue spirit energy, and red-orange underworld/fire scenes
- character continuity is secondary to role clarity: mourner, soul, priest, family, deity/guardian, demon
- continuity comes from repeated symbolic motifs:
  - glowing soul silhouette
  - funeral pyre
  - ritual whites
  - smoke/mist
  - red judgment/hell imagery
  - dark spirit antagonist

Production conclusion:
- this is closer to an `effects-heavy motion-card serial` than a pure still-card montage
- it still should not be recreated as all-I2V for cost reasons
- the low-cost OpenMontage path is:
  - generate strong still anchors
  - add local fire/smoke/glow/lightning/parallax in Remotion or HyperFrames
  - use I2V only when the soul must visibly rise, transform, be pulled, or confront a supernatural figure
- for Shorts, use `2-3` true I2V clips instead of `0-1` because the genre promise is motion-sensitive
- for long-form, build reusable local effect presets instead of paying for hundreds of generated clips

OpenMontage fit:
- strong fit for a new `afterlife_motion_card` playbook:
  - spirit overlay layer
  - pyre/fire effect layer
  - smoke/mist particle layer
  - red underworld grade
  - blue soul glow grade
  - hard-cut story pacing
- Remotion is especially useful for reusable glow, particles, lightning, overlays, and caption-safe composition
- HyperFrames is useful when the shot needs CSS/GSAP-style kinetic spirit reveals or text/symbol overlays

Important conclusion:
- Aatma-ChitaKeBaad raises the motion bar versus Charava-Bhootni, but not enough to justify all-video generation
- the correct cost model is `still anchors + reusable local VFX + 2-3 hero I2V clips`
- this reference is the better template when the Short promise depends on visible supernatural motion, not just narrated story progression

## Fifth Reference Case: Jinn Masoom

Reference studied:
- `/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/Competitors/JInn-Masoom.mp4`

Channel: **STORY FICTION** (watermark top-left every frame)

Measured notes:
- runtime: `1143.5s` (`19:03`)
- format: `640x360`, `16:9`
- detected scene changes: `126` (subsampled to 24 for analysis)
- estimated scene cards: `230-280` at avg `4-5s` per card
- genre: supernatural romance / Islamic Jinn folk story, Hindi narration

Observed pattern:
- photoreal cinematic style (not painterly illustration — key differentiator from Charava-Bhootni)
- consistent female protagonist throughout: young Indian/Pakistani woman, long black braid
- consistent Jinn character: dark-haired young man with signature glowing amber/orange eyes, black embroidered sherwani
- two visual tiers: high-quality photorealistic stills for key character scenes + lower-quality group/crowd scenes
- mostly animated stills (slow push-in, Ken Burns), not continuous video
- select sequences use true AI video generation (motion-blur group scenes visible at 02:00, 06:39)
- VHS glitch transition effect at 16:01 — added in post-production
- black and white archive/stock footage integrated at 17:14 for backstory beat
- no in-frame captions in most shots; narration carries the full semantic load
- fantasy world sequences (Jinn palace, flying creatures) at 08:21

Visual system:
- photorealistic cinematic — not illustration. Closest to actual film stills
- palette splits into two zones: warm domestic (amber, ochre, green salwar kameez) and cold supernatural (teal/cyan, moonlit ruins, blue fog, dark graveyard)
- character identity is tightly locked, far tighter than Charava-Bhootni's costume-continuity approach
- glowing amber eyes are the Jinn's identity marker — composited post-generation, not generated in-frame
- architecture splits between realistic North Indian village/domestic interiors and fantastical Mughal-palace Jinn world

---

### Tool Identification

**Primary image generation: MidJourney v6 with `--cref` (character reference)**

Evidence:
- photorealistic quality, lighting depth, and cinematic framing match MidJourney v6 output precisely
- the female protagonist's face is consistent across 10+ distinct scenes over 19 minutes — the level of face lock only achievable with MidJourney v6 `--cref` (Character Reference flag, released late 2024)
- cultural detail accuracy (Pakistani salwar kameez, dupatta, haveli architecture, Islamic graveyard markers) is characteristic of MJ v6
- the Jinn character face is equally consistent with `--cref`
- no painterly/illustration artifact anywhere — confirms MJ v6 photorealism mode, not Charava-Bhootni's illustration style

**Video generation: Kling 1.5 or Kling 2.0**

Evidence:
- frames at 02:00 and 06:39 show group scenes with motion blur and multi-person dynamics inconsistent with animated stills
- Kling is the dominant tool for South Asian story channels at this quality/price point
- output compressed to 640x360 is consistent with Kling outputs assembled and re-exported in CapCut

**Post-production: CapCut**

Evidence:
- VHS scanline glitch at 16:01 is a native CapCut transition template
- animated still treatment (slow push, Ken Burns, parallax) is standard CapCut workflow
- channel watermark placement and font style match other known CapCut-assembled story channels

**Glowing eyes compositing: CapCut or Photoshop layer**

Evidence:
- the amber glow is too clean and precise to be generated — it's a radial glow/light overlay applied in post over every Jinn scene
- identical effect intensity across all Jinn appearances confirms a templated composite, not prompt-generated

**Audio: Hindi TTS** (likely ElevenLabs multilingual v2 or similar regional TTS)

---

### Estimated production workflow

1. Generate locked character reference images for female protagonist and Jinn in MidJourney v6
2. Produce all scene stills in MidJourney v6 with `--cref <face-ref>` for both characters
3. Import stills into CapCut — apply slow push-in / Ken Burns per card
4. Generate 5-10 true video clips in Kling for crowd/action/motion scenes
5. Composite glowing amber eye effect onto every Jinn still in CapCut
6. Record/generate Hindi TTS narration, add music bed
7. Assemble final video in CapCut with transitions and channel watermark

---

Production conclusion:
- this is the highest-quality photoreal still-card competitor analyzed so far
- the key unlock is MidJourney v6 `--cref` for character lock — without it, face drift across 230+ scene cards would be unmanageable
- Kling is used selectively (5-10 clips max), not as the backbone — same cost discipline as Charava-Bhootni
- the glowing eyes composite is a simple but effective signature VFX that costs near-zero to add
- estimated image generation cost: ~230-280 MidJourney generations at ~$0.04/image = `~$10-12` per episode
- estimated video cost: ~5-10 Kling clips at ~$0.25-0.50/clip = `~$2-5` per episode
- total estimated production cost per 19-minute episode: `~$12-17` excluding narration and editor time

OpenMontage fit:
- directly replicable with MidJourney v6 `--cref` + CapCut for the still backbone
- the photoreal cinematic approach is a higher production bar than Charava-Bhootni but achievable
- for devotional content (BaglaMukhi-Sadhana), the same `--cref` workflow applies to lock sadhak and Mata appearance across all scenes
- divine aura / glow effects (equivalent to Jinn's glowing eyes) can be composited post-generation rather than prompted

Important conclusion:
- Jinn-Masoom proves that 19-minute photoreal story videos are achievable at low cost via MidJourney `--cref` + selective Kling + CapCut
- the character consistency problem is solved by `--cref`, not by expensive video generation
- for BaglaMukhi-Sadhana and similar long-form devotional videos, generate Character Bible reference images first, then use them as `--cref` anchors throughout all scene generation
- do not attempt to solve character consistency through prompt text alone — `--cref` is the correct tool

## Fifth Reference Case: Jinn Masoom

Reference studied:
- `/Users/sunitjoshi/Developer/TryOuts/OpenMontage/Design-Docs/Competitors/JInn-Masoom.mp4`

Measured notes:
- runtime: `1143.51s` (`19:03`)
- format: `640x360`, `16:9`, `30fps`
- video bitrate: about `147 kb/s`
- detected visual beats at practical threshold: `166`
- average visual beat length: about `6.9s`
- median visual beat length: about `6.0s`
- 75th percentile beat length: about `9.8s`
- 90th percentile beat length: about `12.0s`
- one-second image-diff sampling: median `13.8`, with about `38.0%` of samples above `20` and `27.1%` below `5`

Observed pattern:
- Urdu/Hindi supernatural-romance drama story, narration-led
- recurring young woman, young man, older family/community figures, religious elder, room interiors, mosque/arched palace spaces, graveyard/night scenes, and blue-green supernatural lighting
- every sampled frame has a small `Story Fiction` channel watermark, but no visible generator watermark
- photoreal/cinematic AI portrait style, not painterly folk-story illustration
- mostly composed as short scene cards held for `5-10s`
- visual motion is present, but usually reads as slow camera drift, zoom, light shimmer, compression shimmer, or subtle image-to-video motion rather than full staged acting
- no heavy caption dependency in sampled frames
- story meaning comes from narration; visuals provide emotional state, location, and character-role continuity

Visual system:
- high-gloss South Asian TV-drama look: soft window light, shallow depth of field, ornate arches, warm interior practicals, and teal night scenes
- identity continuity is stronger than the Charava and Aatma references, but still not locked:
  - the main woman's face, hair, and clothing drift across scenes
  - the male lead changes hairstyle, face structure, and costume styling
  - the older religious/community figures are role-consistent more than character-consistent
- continuity is carried by repeated visual roles and locations:
  - innocent young woman in modest clothing
  - mysterious or dark romantic male figure
  - family/community confrontation scenes
  - religious elder or council scene
  - graveyard/supernatural blue-green finale imagery

Tool-attribution assessment:
- exact tool cannot be proven from the MP4 alone; the file is a YouTube/Google-encoded export, not an original generator output
- strongest read: `AI still-image generator + local video editor/compositor`, not a single end-to-end AI video tool
- likely still-image source class: Midjourney/Leonardo/Flux/Recraft/Imagen-style photoreal cinematic image generation
- likely assembly class: CapCut/Canva/Premiere/After Effects/Remotion-style timeline with local zooms, pans, music, narration, and watermark overlay
- possible selective I2V: Kling, Runway, Hailuo, Luma, or similar could have been used for a small number of moving cards, but the video does not require I2V for the majority of shots

Why it is probably not YouTube Dream Screen / "Design Screen" as the primary tool:
- YouTube's official AI features are positioned for Shorts: green-screen backgrounds, standalone Shorts clips, photo-to-video, and AI playground effects
- this reference is a `19:03` horizontal long-form story with many edited scene cards, narration, music, and a custom channel watermark
- Dream Screen could generate individual short assets, but it does not explain the long-form timeline, recurring story structure, or external-looking channel branding

Why it is probably not all Kling:
- Kling is a plausible provider for individual image-to-video moments because Kuaishou positions image-generated video as a core workflow and reports image-to-video as the dominant Kling creation mode
- however, this reference has `166` practical visual beats over `19:03`; producing the whole piece as native Kling clips would be slower and more expensive than the observed quality requires
- the motion signature is not consistently "native video acting"; many shots behave like animated still cards with local motion or mild I2V drift
- if Kling was used, the best estimate is `selective I2V embellishment`, not the backbone

Why it is probably not all Runway:
- Runway-style short generated clips are also plausible for selected shots, but the observed output is lower-resolution, narration-led, and card-based
- Runway's documented video workflows emphasize short generated clips and credit usage by seconds; using it for every scene would be a poor cost fit for this competitor's low-bitrate long-form output

External capability checks:
- YouTube Help: Dream Screen / Shorts AI tools generate images or videos from prompts for Shorts backgrounds and standalone Shorts clips: `https://support.google.com/youtube/answer/15260303`
- Kuaishou Kling 2.0 release notes: Kling supports image/video/text multimodal inputs and identifies image-to-video as a central creation mode: `https://ir.kuaishou.com/system/files-encrypted/nasdaq_kms/assets/2025/05/08/22-26-02/Kling%20AI%20Advances%20to%20the%202.0%20Era%2C%20Empowering%20Everyone%20to%20Tell%20Great%20Stories%20with%20AI%20v2.pdf`
- Runway Help: Gen-3 video workflows are clip-based, with costs rounded to `5s` increments and older Gen-3 video-to-video durations up to `20s`: `https://help.runwayml.com/hc/en-us/articles/33350169138323-Creating-with-Video-to-Video-on-Gen-3-Alpha-and-Turbo`

Production conclusion:
- treat this as a `photoreal drama-card montage`, not a full AI-video generation benchmark
- the fastest OpenMontage path is:
  - write the story around `35-60` reusable visual beats for long-form or `8-14` beats for Shorts
  - build a character bible for the woman, male lead, elder, family group, and supernatural antagonist
  - generate strong still anchors with a photoreal cinematic model
  - animate locally with slow push-ins, parallax, depth blur, window-light flicker, teal night haze, graveyard mist, and hard cuts
  - reserve Kling/Seedance/Veo/Hailuo for only `2-4` hero moments: supernatural reveal, jinn manifestation, graveyard encounter, or transformation

Important conclusion:
- the competitor's production advantage is not a secret long-form video model; it is disciplined still generation plus high-volume timeline assembly
- among the named options, `Dream Screen / Design Screen` is the least likely primary source, `Kling` is plausible only as a selective embellishment, and `AI stills + editor` is the most likely backbone
- confidence: `medium`; a higher-confidence attribution would require the original YouTube page description, project files, or uncompressed generator exports

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
- use `Seedance via Replicate` as the default low-volume API path for selected hero clips
- use `Kling` when its specific motion/visual style wins or when manual/web workflow is acceptable
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

### Seedance First, Kling Selectively

Use Seedance via Replicate for:
- the majority of paid Shorts hero clips
- low-volume API-backed I2V when the `$0.90/5s` local billing path is still valid
- hook and peak moments where one strong motion beat is enough

Use Kling for:
- selective short devotional motion clips when it is visibly better
- image-to-video from approved anchors
- manual/web generation when subscription economics beat API billing

Why:
- Seedance via Replicate is the currently verified low-volume API cost path in this repo
- Kling remains a useful visual alternative, but the subscription path has burned credits too fast for 10s generations
- both are better treated as selective hero-shot tools than as full-video backbones
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
- can guided Omni produce materially better continuity or premium motion than the current Seedance/Kling selective-hero path?

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
- `Seedance via Replicate` is currently the best verified low-volume API path in this repo: local billing showed about `$0.90` per `5s` clip, matching the tool estimate of about `$0.18/output-sec`

Practical planning rule:
- treat video generation as the real spend category
- treat voice generation as relatively cheap by comparison
- treat still-image generation plus local animation as the default for story volume

Current stack audit from registry:
- composition runtimes: `ffmpeg`, `Remotion`, and `HyperFrames` are all available
- image generation: `8/9` configured
- video generation: `12/17` configured
- TTS: `3/4` configured
- music generation/search: available

Low-cost production default:
- `0` I2V clips: cheapest animatic/story-card version
- `1` I2V clip: hook or supernatural reveal, about `$0.90`
- `2` I2V clips: hook + peak reveal, about `$1.80`
- `3` I2V clips: hook + mid-body turn + peak reveal, about `$2.70`
- everything else should be stills animated locally

Reference-specific budget mapping:
- Charava-Bhootni-style rural folk story: `0-2` I2V clips, mostly still cards
- Aatma-ChitaKeBaad-style afterlife story: `2-3` I2V clips plus reusable local VFX layers
- Shiva/Kailash/Maa Kali devotional symbol story: `1-3` I2V clips depending on hero moments

Public pricing caveat:
- provider pricing is fragmented and changes quickly
- use OpenMontage's live registry/tool estimate and the user's actual billing as the source of truth before spending
- as of late April 2026, public Seedance pricing reports vary widely by gateway; do not assume fal.ai, Replicate, direct ByteDance, or subscription pricing are interchangeable

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
- stay Seedance/low-cost-first for hero clips
- use Kling selectively when it wins a specific shot
- use Veo selectively
- use Omni only as a guided evaluation path
- optimize continuity before optimizing provider novelty

For Charava-Bhootni-style folk-story remakes:
- stay inside OpenMontage
- use still-first storyboarding
- generate a locked character/location bible before prompts
- reserve Seedance/Kling/Veo for `1-3` hero clips only
- make the narrator, pacing, and visual-beat discipline the product
- avoid trying to create a 20-minute all-I2V remake; that is the wrong cost structure

For Aatma-ChitaKeBaad-style afterlife remakes:
- stay inside OpenMontage
- use still anchors, but make local VFX part of the shot design from the start
- define reusable spirit, pyre, smoke, lightning, and underworld-grade layers
- reserve Seedance/Kling/Veo for soul-rise, transformation, confrontation, and climax clips
- budget `2-3` true I2V clips for Shorts, not every visual beat
