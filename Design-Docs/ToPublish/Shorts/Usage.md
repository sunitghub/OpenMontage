# Shorts Usage

This folder is for publish-ready Shorts packages. Each Short should live in its
own folder under `OpenMontage/Design-Docs/ToPublish/Shorts/`.

## Core Rule

Final Shorts renders are voiceover-first.

Do not create a final, captioned, or publishable render until the voiceover file
is available and configured in the edit decisions. The voiceover is the timing
source of truth.

For Blissful Chants Shorts, the default language split is:

```text
Hindi voiceover. English on-screen text and captions.
```

Use the Hindi transcript to find scene timing, but do not render Hindi/Urdu
transcript words as captions unless explicitly requested. Captions should come
from the approved English screen script and be aligned to the Hindi voiceover
scene windows.

Visual-only renders are allowed only as previews. Mark those renders with:

```json
{
  "options": {
    "render_intent": "visual_preview"
  }
}
```

Use preview renders only to check framing, visual direction, and asset quality.
Do not treat preview renders as final exports.

## Standard Flow

### 1. Create Or Inspect The Shorts Package

Each package should have a markdown file with the same slug as its folder.

Expected shape:

```text
OpenMontage/Design-Docs/ToPublish/Shorts/<Short-Slug>/
  <Short-Slug>.md
  Renders/
```

The package markdown should define:

- `Title`
- `Description`
- `Script`
- `Scenes`
- `Results`
- asset references and assembly notes as needed

### 2. Prepare The Final Voiceover

Place the final voiceover in the package `Renders/` folder, for example:

```text
OpenMontage/Design-Docs/ToPublish/Shorts/<Short-Slug>/Renders/Hindi-VoiceOver.mp3
```

This should be the final spoken track. Do not build final scene timing from a
draft script if the actual voiceover may differ.

### 3. Probe The Voiceover

Check the voiceover duration before editing the timeline:

```bash
rtk ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 OpenMontage/Design-Docs/ToPublish/Shorts/<Short-Slug>/Renders/Hindi-VoiceOver.mp3
```

The final render duration should match this audio duration closely.

### 4. Transcribe The Voiceover

Use the local transcriber to create word and segment timestamps:

```bash
cd OpenMontage
.venv/bin/python - <<'PY'
from pathlib import Path
from tools.analysis.transcriber import Transcriber

voiceover = Path("Design-Docs/ToPublish/Shorts/<Short-Slug>/Renders/Hindi-VoiceOver.mp3")
out_dir = Path("projects/<project-slug>/artifacts")

result = Transcriber().execute({
    "input_path": str(voiceover),
    "model_size": "base",
    "language": "hi",
    "output_dir": str(out_dir),
})

print(result.success)
print(result.artifacts)
PY
```

Use the correct language code for the voiceover. For Hindi, use `hi`.

### 5. Review Transcript Segments

Print the transcript segments and decide where each visual scene should end:

```bash
cd OpenMontage
rtk jq -r '.segments[] | [.start, .end, .text] | @tsv' projects/<project-slug>/artifacts/Hindi-VoiceOver_transcript.json
```

Choose one segment end per scene. For a 9-scene Short, provide 9 segment numbers.
The segment numbers are 1-based.

Example from `Maa-Kali-5-Unknown-Facts`:

```text
SCENE_END_SEGMENTS=4,6,9,12,15,19,20,24,26
```

### 6. Apply Voiceover Timing

Generate a voiceover-timed edit artifact:

```bash
cd OpenMontage
make apply-voiceover-timeline \
  EDIT=projects/<project-slug>/artifacts/edit_decisions.resolved-v8.json \
  TRANSCRIPT=projects/<project-slug>/artifacts/Hindi-VoiceOver_transcript.json \
  VOICEOVER=Design-Docs/ToPublish/Shorts/<Short-Slug>/Renders/Hindi-VoiceOver.mp3 \
  SCENE_END_SEGMENTS=4,6,9,12,15,19,20,24,26 \
  OUT=projects/<project-slug>/artifacts/edit_decisions.voiceover-v1.json
```

This updates:

- `cuts[].in_seconds`
- `cuts[].out_seconds`
- `audio.narration.src`
- `voiceover.src`
- `total_duration_seconds`
- `metadata.target_duration_seconds`
- `metadata.timeline_source`
- `captions` from transcript word timestamps

For the standard Blissful Chants format, replace those transcript-language
captions with English screen-script captions after the voiceover timeline is
created. Keep the scene cut timing from the Hindi transcript, but distribute the
English words inside each scene's voiceover window.

### 7. Verify The Voiceover-Timed Edit Artifact

Check that the timeline and voiceover are present:

```bash
cd OpenMontage
rtk jq -r '.metadata.timeline_source, .metadata.target_duration_seconds, .audio.narration.src, (.captions|length), (.cuts[] | [.id, .in_seconds, .out_seconds, (.out_seconds-.in_seconds)] | @tsv)' projects/<project-slug>/artifacts/edit_decisions.voiceover-v1.json
```

Expected:

- `metadata.timeline_source` is `voiceover_analysis`
- `audio.narration.src` points to the voiceover file
- caption count is greater than zero
- final cut ends at the voiceover duration

### 8. Render

Use the voiceover-timed edit artifact for final rendering.

Do not render from the old fixed-duration edit artifact unless the render intent
is explicitly `visual_preview`.

The render layer now blocks final/captioned/publishable renders without a
voiceover source.

### 9. Post-Render Checks

After rendering, verify:

```bash
rtk ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,duration -of default=noprint_wrappers=1 <final-output.mp4>
```

Also check for accidental silence:

```bash
rtk ffmpeg -hide_banner -i <final-output.mp4> -map 0:a:0 -af silencedetect=noise=-35dB:d=0.25 -f null -
```

The final output should:

- have audible narration
- have duration close to the voiceover duration
- show scene changes at spoken beat boundaries
- show English captions aligned to the Hindi voiceover scene timing

## Maa Kali Example

For the current Maa Kali project:

```text
Voiceover:
OpenMontage/Design-Docs/ToPublish/Shorts/Maa-Kali-5-Unknown-Facts/Renders/Hindi-VoiceOver.mp3

Transcript:
OpenMontage/projects/maa-kali-5-yantra-facts-short/artifacts/Hindi-VoiceOver_transcript.json

Voiceover-timed edit:
OpenMontage/projects/maa-kali-5-yantra-facts-short/artifacts/edit_decisions.voiceover-v1.json

Voiceover-timed edit with English captions:
OpenMontage/projects/maa-kali-5-yantra-facts-short/artifacts/edit_decisions.voiceover-english-captions-v1.json

Scene end segments:
4,6,9,12,15,19,20,24,26
```

The resulting timeline is about `96.052s`, matching the voiceover.

## Common Mistakes

- Rendering final video from fixed scene durations before voiceover exists.
- Rendering Hindi/Urdu transcript captions when the required on-screen language is English.
- Treating a silent MP4 audio stream as valid narration.
- Letting the visual timeline end before the voiceover.
- Reusing old `edit_decisions` artifacts after the voiceover changes.
- Calling a preview render publishable.

## Policy Summary

Use this rule for all Shorts going forward:

```text
Voiceover first. Transcript second. Scene cuts third. English captions fourth. Render last.
```
