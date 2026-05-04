#!/usr/bin/env python3
"""
render_scene.py — Core render logic for render-scene shell command.
Do not call directly. Use the render-scene shell wrapper.

Effects baked in (from competitor research):
  - Ken Burns slow push-in per image (zoom 1.00 → 1.04)
  - Hard cuts between images within a scene
  - Fade-in from black at scene start (0.8s)
  - Fade-out to black at scene end (0.8s)
  - Bloom glow on deity images (auto-detected from script MD)
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import tempfile

ZOOM_TARGET = 1.04
FADE_DUR = 0.8

HONORIFICS = {"maa", "shri", "sri", "mata", "devi", "shree"}


def find_script_md(base):
    for path in glob.glob(os.path.join(base, "*.md")):
        with open(path, encoding="utf-8", errors="ignore") as f:
            if "## Scene-" in f.read():
                return path
    return None


def get_deity_keywords(script_path):
    """Extract deity name from '# Diety:' or '# Deity:' header line."""
    with open(script_path, encoding="utf-8", errors="ignore") as f:
        content = f.read()
    match = re.search(r"^# (?:Diety|Deity):\s*(.+)$", content, re.MULTILINE | re.IGNORECASE)
    if not match:
        return []
    name = match.group(1).strip()
    return [w for w in name.lower().split() if w not in HONORIFICS]


def extract_image_prompts(script_path, scene_num):
    """Return {image_index: prompt_text} for a scene's numbered image entries."""
    with open(script_path, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    match = re.search(rf"## Scene-{scene_num}[:\s]", content)
    if not match:
        return {}
    start = match.start()
    next_scene = re.search(r"## Scene-\d+[:\s]", content[start + 1:])
    end = start + 1 + next_scene.start() if next_scene else len(content)
    scene_block = content[start:end]

    images_match = re.search(r"#### Images", scene_block)
    if not images_match:
        return {}
    images_block = scene_block[images_match.start():]

    prompts = {}
    items = list(re.finditer(r"^(\d+)\.\s*$", images_block, re.MULTILINE))
    for i, item in enumerate(items):
        idx = int(item.group(1))
        item_start = item.start()
        item_end = items[i + 1].start() if i + 1 < len(items) else len(images_block)
        item_text = images_block[item_start:item_end]
        # Pick longest backtick block — that's the prompt, not a short filename ref
        candidates = re.findall(r"`([^`]+)`", item_text, re.DOTALL)
        if candidates:
            prompts[idx] = max(candidates, key=len)
    return prompts


def image_has_deity(prompt, deity_keywords):
    low = prompt.lower()
    return any(kw in low for kw in deity_keywords)


def print_critic_summary(script_path):
    with open(script_path, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    scenes = list(re.finditer(r"^## Scene-(\d+)[:\s]", content, re.MULTILINE))
    if not scenes:
        print("No scenes found in script.")
        return

    rows = []

    for i, scene_match in enumerate(scenes):
        scene_num = scene_match.group(1)
        start = scene_match.start()
        end = scenes[i + 1].start() if i + 1 < len(scenes) else len(content)
        block = content[start:end]

        beat_match = re.search(r"\*\*Story Beat:\*\*\s*(.+)", block)
        level_match = re.search(r"\*\*Level:\*\*\s*(High|Medium|Low|N/A)", block)
        beat = beat_match.group(1).strip() if beat_match else "—"
        level = level_match.group(1).strip() if level_match else "NOT CRITIQUED"
        rows.append((scene_num, beat, level))

    print(f"\n{'Scene':<8} {'Level':<10} Story Beat")
    print("-" * 60)
    for scene_num, beat, level in rows:
        print(f"  {scene_num:<6} {level:<10} {beat}")

    high = [r for r in rows if r[2] == "High"]
    if high:
        print(f"\n  {len(high)} scene(s) need attention (Level: High):")
        for r in high:
            print(f"    Scene-{r[0]}: {r[1]}")
    print()


def narration_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def image_sort_key(path):
    parts = os.path.splitext(os.path.basename(path))[0].split("-")
    try:
        return int(parts[2])
    except (IndexError, ValueError):
        return 0


def render_card(img, out, duration, w, h, fps, fade_in, fade_out, preview, glow=False):
    frames = max(int(duration * fps), 1)
    zoom_step = (ZOOM_TARGET - 1.0) / frames

    zoompan = (
        f"zoompan=z='min(zoom+{zoom_step:.6f},{ZOOM_TARGET})'"
        f":x='iw/2-(iw/zoom/2)'"
        f":y='ih/2-(ih/zoom/2)'"
        f":d={frames}:s={w}x{h}:fps={fps}"
    )

    fades = ""
    if fade_in:
        fades += f",fade=t=in:st=0:d={FADE_DUR}"
    if fade_out:
        fades += f",fade=t=out:st={duration - FADE_DUR}:d={FADE_DUR}"

    if glow:
        fc = (
            f"[0:v]scale={w}:{h},{zoompan}{fades}[base];"
            f"[base]split=3[main][s1][s2];"
            f"[s1]eq=brightness=0.55,gblur=sigma=8[tight];"
            f"[s2]eq=brightness=0.3,gblur=sigma=32[wide];"
            f"[tight][wide]blend=all_mode=screen:all_opacity=0.6[bloom];"
            f"[main][bloom]blend=all_mode=screen:all_opacity=0.28,"
            f"eq=saturation=1.12:gamma_r=1.06:gamma_g=1.03[out]"
        )
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", img,
               "-filter_complex", fc, "-map", "[out]",
               "-t", str(duration), "-r", str(fps),
               "-c:v", "libx264", "-pix_fmt", "yuv420p",
               "-preset", "veryfast" if preview else "medium", out]
    else:
        vf = f"scale={w}:{h},{zoompan}{fades}"
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", img,
               "-vf", vf, "-t", str(duration), "-r", str(fps),
               "-c:v", "libx264", "-pix_fmt", "yuv420p",
               "-preset", "veryfast" if preview else "medium", out]

    subprocess.run(cmd, check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--scene", default=None)
    ap.add_argument("--duration", type=float, default=7.0)
    ap.add_argument("--narration", default=None)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--glow", action="store_true",
                    help="Force bloom glow on all images (auto-detected per image if omitted)")
    ap.add_argument("--critic", action="store_true",
                    help="Print critique summary from script MD (no render)")
    ap.add_argument("--project", default=None,
                    help="Project directory (default: current working directory)")
    args = ap.parse_args()

    base = os.path.abspath(args.project) if args.project else os.getcwd()
    renders_dir = base if args.project else os.path.join(base, "Render")

    if args.critic:
        script_md = find_script_md(base)
        if not script_md:
            print("No script MD found in project directory.")
            return 1
        print_critic_summary(script_md)
        return 0

    if not args.scene:
        print("Error: --scene is required for rendering. Use --critic for script analysis.")
        return 1

    script_md = find_script_md(base)
    deity_keywords = get_deity_keywords(script_md) if script_md else []
    image_prompts = extract_image_prompts(script_md, args.scene) if script_md else {}

    if deity_keywords:
        print(f"  Deity keywords: {', '.join(deity_keywords)}")

    w, h, fps = (1280, 720, 24) if args.preview else (1920, 1080, 30)

    pattern = os.path.join(base, f"Scene-{args.scene}-*.png")
    images = sorted(glob.glob(pattern), key=image_sort_key)

    if not images:
        print(f"No images found: {pattern}")
        return 1

    n = len(images)

    if args.narration:
        narration_path = args.narration if os.path.isabs(args.narration) \
            else os.path.join(base, args.narration)
        total = narration_duration(narration_path)
        dur = total / n
        print(f"Scene {args.scene}: {n} images, narration {total:.1f}s → {dur:.1f}s/image")
    else:
        narration_path = None
        dur = args.duration
        print(f"Scene {args.scene}: {n} images × {dur}s = {n * dur:.0f}s total")

    os.makedirs(renders_dir, exist_ok=True)
    tmp = tempfile.mkdtemp()

    try:
        clips = []
        for i, img in enumerate(images):
            clip = os.path.join(tmp, f"card_{i:03d}.mp4")
            img_idx = image_sort_key(img)
            prompt = image_prompts.get(img_idx, "")
            use_glow = args.glow or (bool(prompt) and bool(deity_keywords)
                                     and image_has_deity(prompt, deity_keywords))
            label = " [glow]" if use_glow else ""
            print(f"  [{i+1}/{n}] {os.path.basename(img)}{label}")
            render_card(img, clip, dur, w, h, fps,
                        fade_in=(i == 0), fade_out=(i == n - 1),
                        preview=args.preview, glow=use_glow)
            clips.append(clip)

        concat_txt = os.path.join(tmp, "concat.txt")
        with open(concat_txt, "w") as f:
            for c in clips:
                f.write(f"file '{c}'\n")

        suffix = "-preview" if args.preview else ""
        output = os.path.join(renders_dir, f"Scene-{args.scene}-test{suffix}.mp4")

        if narration_path:
            cmd = ["ffmpeg", "-y",
                   "-f", "concat", "-safe", "0", "-i", concat_txt,
                   "-i", narration_path,
                   "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                   "-shortest", output]
        else:
            cmd = ["ffmpeg", "-y",
                   "-f", "concat", "-safe", "0", "-i", concat_txt,
                   "-c", "copy", output]

        subprocess.run(cmd, check=True)
        size_mb = os.path.getsize(output) / 1024 / 1024
        print(f"\nDone: {output} ({size_mb:.1f} MB)")

    finally:
        shutil.rmtree(tmp)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
