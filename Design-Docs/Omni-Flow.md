# Omni Flow

Purpose: define the fastest reliable way to test `Kling 3.0 Omni` on the Shiva/crow style project without losing consistency, timing, or comparability against the current OpenMontage sample.

This guide assumes you already have the current sample project:
- [script.json](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/artifacts/script.json)
- [scene_plan.json](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/artifacts/scene_plan.json)
- [visual_bible.md](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/artifacts/visual_bible.md)
- [composition_props.json](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/artifacts/composition_props.json)
- [shiva-crow-60s.mp4](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/renders/shiva-crow-60s.mp4)

## Bottom Line

Do not test Omni as a pure black box first.

Best route:
- use OpenMontage for planning and asset prep
- use Omni for guided shot generation
- assemble and compare inside OpenMontage

Not recommended as the first test:
- pasting only the full 60-second script into Omni and letting it invent everything

Reason:
- the main problem is identity consistency, not idea generation
- Shiva face, beard, robe, crow form, and lighting family drift unless guidance is locked

## Best Test Order

### Test A: Script Only

Use this only as a curiosity benchmark.

Input to Omni:
- the 60-second script only
- one high-level style instruction

What it tells you:
- Omni's raw taste
- whether it can produce a cohesive spiritual short with minimal setup

What it does not tell you:
- whether it can replace your current controlled pipeline

Expected risk:
- strong drift in Shiva identity and scene-to-scene tone

### Test B: Guided Omni

This is the real evaluation path.

Input to Omni:
- sectioned script
- scene-level prompts
- anchor images
- locked visual bible
- optional narration for timing

What it tells you:
- whether Omni can outperform current Kling shot generation when properly guided
- whether it can preserve consistency well enough to justify switching

Expected result:
- much fairer comparison against the current OpenMontage sample

## Recommended Asset Pack

Prepare this exact pack before using Omni:

### Script

Use the six-beat structure from:
- [script.json](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/artifacts/script.json)

Keep each beat separate:
- scene 1: sacred reveal
- scene 2: crow arrival
- scene 3: moral question
- scene 4: symbolic snowfall teaching
- scene 5: close spiritual answer
- scene 6: sunrise release

### Visual Bible

Use:
- [visual_bible.md](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/artifacts/visual_bible.md)

Lift the key rules into Omni:
- same Shiva face shape
- no beard drift
- same skin tone
- same hair silhouette
- same moon crescent
- same sacred winter environment
- same crow identity
- cold blue snow plus warm divine gold

### Anchor Images

Use all six anchors:
- [scene-01-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-01-anchor.jpg)
- [scene-02-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-02-anchor.jpg)
- [scene-03-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-03-anchor.jpg)
- [scene-04-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-04-anchor.jpg)
- [scene-05-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-05-anchor.jpg)
- [scene-06-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-06-anchor.jpg)

### Timing Reference

Optional but recommended:
- [narration.mp3](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/audio/narration.mp3)

Use it for:
- beat timing
- emotional pacing
- deciding where scenes should breathe vs cut

### Baseline Comparison Video

Use:
- [shiva-crow-60s.mp4](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/renders/shiva-crow-60s.mp4)

This is your benchmark for:
- consistency
- pacing
- emotional feel
- caption readability after final assembly

## Omni Workflow

### Option 1: Best Serious Test

Generate scene by scene.

Steps:
1. Create one Omni generation per scene, not one giant 60-second request
2. For each scene, provide:
   - the scene text
   - the matching anchor image
   - a consistency note from the visual bible
   - a simple camera instruction
3. Download each generated clip
4. Replace or compare against the current six OpenMontage video clips
5. Assemble in OpenMontage

Why this is best:
- easiest way to control drift
- easiest way to reroll only weak scenes
- easiest way to compare against the current sample

### Option 2: Good Hybrid Test

Generate in two or three larger movements instead of six scenes.

Example split:
- Act 1: scenes 1-2
- Act 2: scenes 3-4
- Act 3: scenes 5-6

Use this when:
- you want to test whether Omni handles continuity over longer spans
- you still want some guardrails

Risk:
- more drift than scene-by-scene
- harder to salvage individual weak beats

### Option 3: Full Script, One Shot

Use only as an experiment.

Do this if you want to answer one question only:
- "What does Omni do with minimal control?"

Do not use this result to decide production readiness by itself.

## Recommended Prompt Structure

For each Omni scene, provide:

1. Subject lock
- Lord Shiva, same exact face and body styling as the reference image
- no beard drift
- same crow identity

2. Scene action
- one clear action only
- avoid multiple transformations in one shot

3. Camera
- one camera move only
- slow devotional motion

4. World rules
- snowy Himalayas
- sacred gold-blue atmosphere
- mythic realism

5. Negative constraints
- no beard changes
- no extra arms
- no costume changes
- no random extra animals
- no text
- no watermark

## Example Omni Inputs

### Scene 1

Use:
- anchor: [scene-01-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-01-anchor.jpg)
- text: "High in the Himalayas, Lord Shiva sits in deep stillness."
- camera: "slow dolly in"
- constraints: "same face, no beard drift, same robe, same crow placement logic"

### Scene 3

Use:
- anchor: [scene-03-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-03-anchor.jpg)
- text: "The crow asks why honest hearts struggle while justice seems delayed."
- camera: "slow push in"
- constraints: "same Shiva identity, same crow, intimate emotional framing, no visual mutation"

### Scene 6

Use:
- anchor: [scene-06-anchor.jpg](/Users/sunitjoshi/Developer/TryOuts/OpenMontage/projects/shiva-crow-60s/assets/images/scene-06-anchor.jpg)
- text: "The crow rises into the open sky as the teaching settles."
- camera: "gentle rising crane"
- constraints: "keep sunrise palette, keep Shiva serene, no chaos, no style break"

## Evaluation Checklist

Judge Omni against the current sample on these points:
- Shiva face consistency
- beard consistency
- crow consistency
- lighting consistency
- scene-to-scene emotional continuity
- whether motion feels more premium than the current Kling sample
- whether rerolls are easier or harder
- whether total cost and effort are justified

## Decision Rule

Omni is worth adopting for this project only if:
- it is visibly more consistent than the current sample
- or it produces materially better premium motion in the hero scenes
- without making rerolls and download/assembly workflow too painful

If Omni only gives prettier isolated shots but worse continuity:
- keep OpenMontage as the main workflow
- use Omni selectively for hero beats only

## Practical Recommendation

For the same 60-second Shiva/crow piece:
- do one `script-only` Omni run for curiosity
- do one `guided six-scene` Omni run for the real comparison
- make the decision from the guided run, not the script-only run

## Best Current Workflow

If optimizing for quality evaluation:
- OpenMontage for planning
- Omni for guided clip generation
- OpenMontage for subtitles, timing, and final render

If optimizing for simplicity only:
- try a full-script Omni run

If optimizing for production reliability:
- stay scene-based and hybrid
