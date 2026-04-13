# Draw Things Image-to-Video Guide

This guide captures a practical local workflow for generating image-to-video clips in Draw Things with `SkyReels v2 I2V 14B 720p` on a `32 GB` Apple Silicon Mac while keeping swap manageable.

## Recommended First Prompt

```text
A sacred geometric mandala with a glowing neon pink-red triangle at the center, black ink line art on textured parchment, perfectly centered and symmetrical. The triangle emits a slow soft pulse of light, a faint radiant shimmer moves outward through the circular pattern, the camera makes a very slow gentle push in, calm meditative mystical atmosphere, clean precise geometry, highly detailed, cinematic.
```

Negative prompt:

```text
warped geometry, asymmetry, extra petals, broken lines, heavy motion, morphing, flicker, jitter, blur, camera shake, text, watermark
```

## Core Settings

Use these as the balanced starting point:

- Model: `SkyReels v2 I2V 14B 720p`
- Style: `Empty`
- LoRA: `Disabled`
- Control: `Disabled`
- Mode: `Image to Video`
- Strength: `68% to 72%`
- Seed: fixed if comparing runs, `-1` if exploring
- Seed Mode: any; use fixed seed mainly for repeatable A/B tests
- Image Size: `832x448`
- Upscaler: `Disabled`
- Steps: `30`
- Number of Frames: `49`
- Text Guidance: `5.0`
- Sampler: `Euler A Trailing`
- Shift: `5.0`
- Refiner Model: `Disabled`
- Casual Inference: `Disabled`
- Sharpness: `0.0`
- Face Restoration: `Disabled`
- High Resolution Fix: `Disabled`

If you are not masking or doing inpaint work, also keep these off or minimal:

- Preserve Original After Inpaint: `Off`
- Mask Blur: low / default
- Mask Blur Outset: `0`

## Why These Changes Help

The biggest drivers of memory usage are:

1. `Number of Frames`
2. `Resolution`
3. `Steps`

If memory pressure or swap is high, reduce work in that order before changing prompt guidance.

## Presets

### Low-Swap Preset

Use this when Draw Things is swapping heavily or other apps are open:

- Image Size: `720x384` if available, otherwise the nearest smaller size
- Number of Frames: `33 to 41`
- Steps: `24 to 28`
- Strength: `68% to 72%`
- Text Guidance: `5.0`
- Shift: `5.0`

### Balanced Preset

Use this for everyday testing:

- Image Size: `832x448`
- Number of Frames: `49`
- Steps: `30`
- Strength: `68% to 72%`
- Text Guidance: `5.0`
- Shift: `5.0`

### Higher-Quality Preset

Use this when you have headroom and want a nicer final pass:

- Image Size: `832x448`
- Number of Frames: `81`
- Steps: `40 to 50`
- Strength: `70% to 75%`
- Text Guidance: `5.0`
- Shift: `5.0`

## Tuning Rules

If the result is too wobbly:

- Lower `Strength` to `65%`
- Reduce frames to `49`
- Keep `Text Guidance` at `5.0`

If the result is too static:

- Raise `Strength` to `75% to 78%`
- Keep the prompt the same

If the geometry starts drifting:

- Shorten the prompt
- Emphasize `centered`, `symmetrical`, and `clean geometry`
- Avoid style presets

If Draw Things is using too much memory:

- Lower `Frames`
- Lower `Image Size`
- Lower `Steps`
- Close other heavy apps before rendering

## System Tips

On a `32 GB` Mac, local video generation with a `14B` model is viable, but swap can rise quickly. Before long runs, close memory-heavy apps such as:

- Teams
- Browser tabs with YouTube or other media
- Kling
- GarageBand
- Extra Code Helper / Chrome helper processes

Freeing even `4 to 6 GB` from other apps can noticeably reduce swap pressure during generation.

## Notes

- `Text Guidance` in Draw Things is the guidance / CFG setting.
- `5.0` is a good starting point for SkyReels image-to-video.
- `Style` should usually stay `Empty` for image-to-video when preserving the source image matters.
