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
import datetime
import glob
import os
import re
import shutil
import subprocess
import tempfile

ZOOM_TARGET = 1.04
FADE_DUR = 0.8
WPM = 85  # Hindi devotional narration benchmark (80–90 WPM range)
_CRITIQUE_TRUNC = 100
NARRATION_EQ = (
    "highpass=f=90:poles=2,"
    "equalizer=f=120:width_type=q:width=1.5:g=-2.5,"
    "equalizer=f=320:width_type=q:width=1.5:g=-1.5,"
    "equalizer=f=2500:width_type=q:width=1.2:g=2.5,"
    "treble=g=2:f=10000"
)

HONORIFICS = {"maa", "shri", "sri", "mata", "devi", "shree"}

_RE_SCENE_HEADER = re.compile(r"^## Scene-\d+[:\s].*\n")
_RE_SUBSECTION = re.compile(r"^###", re.MULTILINE)
_RE_BLOCKQUOTE = re.compile(r"^>.*$", re.MULTILINE)
_RE_MD_MARKUP = re.compile(r"[*_`#]")


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


def count_script_words(scene_block):
    """Count Hindi/Hinglish words in the script text (before ### English)."""
    text = _RE_SCENE_HEADER.sub("", scene_block, count=1)
    sub_match = _RE_SUBSECTION.search(text)
    if sub_match:
        text = text[:sub_match.start()]
    text = _RE_BLOCKQUOTE.sub("", text)
    text = _RE_MD_MARKUP.sub(" ", text)
    return len(text.split())


def count_prompted_images(scene_block):
    """Count numbered image entries (1., 2., 1a., 1b., etc.) in #### Images section."""
    images_match = re.search(r"#### Images", scene_block)
    if not images_match:
        return 0
    images_block = scene_block[images_match.start():]
    next_section = re.search(r"^### ", images_block, re.MULTILINE)
    if next_section:
        images_block = images_block[:next_section.start()]
    return len(re.findall(r"^\d+[a-z]?\.\s*$", images_block, re.MULTILINE))



def pacing_status(hold_s):
    if hold_s < 5.0:
        return "❌ Too fast"
    if hold_s < 6.0:
        return "⚠  Below target"
    if hold_s <= 8.0:
        return "✓  Good"
    if hold_s <= 10.0:
        return "⚠  Slightly slow"
    return "❌ Too slow"


def extract_critique_rows(content, scenes):
    """Return list of (scene_num, level, issues_str, fix_str, status) tuples."""
    rows = []
    for i, scene_match in enumerate(scenes):
        scene_num = scene_match.group(1)
        start = scene_match.start()
        end = scenes[i + 1].start() if i + 1 < len(scenes) else len(content)
        block = content[start:end]

        level_match = re.search(r"\*\*Level:\*\*\s*(High|Medium|Low|N/A)", block)
        level = level_match.group(1).strip() if level_match else "NOT CRITIQUED"

        issues, fixes = [], []
        critique_match = re.search(r"### Critique", block)
        if critique_match:
            c_block = block[critique_match.start():]
            next_sec = re.search(r"^#### ", c_block, re.MULTILINE)
            if next_sec:
                c_block = c_block[:next_sec.start()]
            for m in re.finditer(r"^- \*\*(.+?)\*\*:\s*(.+)$", c_block, re.MULTILINE):
                label, text = m.group(1).strip(), m.group(2).strip()
                if re.match(r"^Fix(\s*\(.*\))?$", label):
                    fixes.append(text[:_CRITIQUE_TRUNC] + "…" if len(text) > _CRITIQUE_TRUNC else text)
                else:
                    issues.append(label)

        status = "Fixed" if level == "Low" else "ToDo"
        rows.append((
            scene_num, level,
            "; ".join(issues) if issues else "—",
            "; ".join(fixes) if fixes else "—",
            status,
        ))
    return rows


_PACING_LABEL = re.compile(r"^Pacing\b", re.IGNORECASE)


def build_critique_summary(critique_rows, pacing_rows):
    """Build indented bullet format: scene header, one issue per line, fix inline on last."""
    pacing_notes = {}
    for scene_num, _w, narr_s, prompted, _g, hold, _m in pacing_rows:
        if not prompted:
            continue
        if hold > 8.0:
            needed = max(1, round(narr_s / 7) - prompted)
            pacing_notes[scene_num] = f"add ~{needed} image(s) — hold is {hold}s/img"
        elif hold < 6.0:
            pacing_notes[scene_num] = f"trim images or expand narration — hold is {hold}s/img"

    todo_items, fixed_items = [], []
    for scene_num, level, issues, fix, status in critique_rows:
        has_pacing = scene_num in pacing_notes
        if status == "ToDo" or has_pacing:
            issue_list = [
                i.strip() for i in issues.split(";")
                if issues != "—" and not _PACING_LABEL.match(i.strip())
            ]
            todo_items.append((scene_num, level, issue_list, fix, has_pacing))
        else:
            fixed_items.append(scene_num)

    lines = [f"_Last updated: {datetime.date.today()}_\n"]

    if todo_items:
        lines.append("**ToDo**")
        for scene_num, level, issue_list, fix, has_pacing in todo_items:
            lines.append(f"- **Scene-{scene_num} ({level})**:")
            if issue_list:
                for issue in issue_list[:-1]:
                    lines.append(f"  · {issue}")
                last = issue_list[-1]
                if fix and fix != "—":
                    lines.append(f"  · {last} → {fix}")
                else:
                    lines.append(f"  · {last}")
            elif fix and fix != "—":
                lines.append(f"  · → {fix}")
            if has_pacing:
                lines.append(f"  · Pacing: {pacing_notes[scene_num]}")
            lines.append("")

    if fixed_items:
        lines.append("**Fixed:** " + " · ".join(f"Scene-{sn}" for sn in fixed_items))

    return "\n".join(lines)


def write_critique_state(script_path, table_md):
    with open(script_path, encoding="utf-8") as f:
        content = f.read()

    section_header = "## Critique State\n"

    if section_header not in content:
        # Insert before the first ## Scene- heading
        first_scene = re.search(r"\n## Scene-\d+", content)
        if not first_scene:
            return
        insert_at = first_scene.start()
        content = (
            content[:insert_at]
            + f"\n\n{section_header}\n{table_md}\n"
            + content[insert_at:]
        )
    else:
        def _replace(m):
            return m.group(1) + "\n" + table_md + "\n" + m.group(2)

        content = re.sub(
            r"(## Critique State\n).*?(\n## )",
            _replace,
            content,
            flags=re.DOTALL,
        )

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Updated ## Critique State in {os.path.basename(script_path)}")


def print_critic_summary(script_path, base):
    with open(script_path, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    scenes = list(re.finditer(r"^## Scene-(\d+)[:\s]", content, re.MULTILINE))
    if not scenes:
        print("No scenes found in script.")
        return

    beat_rows = []
    pacing_rows = []

    generated_counts = {}
    for png in glob.glob(os.path.join(base, "Scene-*-*.png")):
        m = re.match(r"Scene-(\d+)-", os.path.basename(png))
        if m:
            sn = m.group(1)
            generated_counts[sn] = generated_counts.get(sn, 0) + 1

    for i, scene_match in enumerate(scenes):
        scene_num = scene_match.group(1)
        start = scene_match.start()
        end = scenes[i + 1].start() if i + 1 < len(scenes) else len(content)
        block = content[start:end]

        beat_match = re.search(r"\*\*Story Beat:\*\*\s*(.+)", block)
        level_match = re.search(r"\*\*Level:\*\*\s*(High|Medium|Low|N/A)", block)
        beat = beat_match.group(1).strip() if beat_match else "—"
        level = level_match.group(1).strip() if level_match else "NOT CRITIQUED"
        beat_rows.append((scene_num, beat, level))

        words = count_script_words(block)
        narr_s = round(words / WPM * 60) if words else 0
        prompted = count_prompted_images(block)
        generated = generated_counts.get(scene_num, 0)
        hold = round(narr_s / prompted, 1) if prompted else 0.0
        missing = max(0, prompted - generated)
        pacing_rows.append((scene_num, words, narr_s, prompted, generated, hold, missing))

    # Beat / level table
    print(f"\n{'Scene':<8} {'Level':<14} Story Beat")
    print("  " + "-" * 63)
    for scene_num, beat, level in beat_rows:
        print(f"  {scene_num:<6} {level:<14} {beat}")

    high = [r for r in beat_rows if r[2] == "High"]
    not_critiqued = [r for r in beat_rows if r[2] == "NOT CRITIQUED"]
    if high:
        print(f"\n  ⚠  {len(high)} scene(s) flagged High — critique needed:")
        for r in high:
            print(f"       Scene-{r[0]}: {r[1]}")
    if not_critiqued:
        print(f"\n  ○  {len(not_critiqued)} scene(s) not yet critiqued: "
              + ", ".join(f"Scene-{r[0]}" for r in not_critiqued))

    # Pacing table
    print(f"\n  ─── Pacing Analysis (target 6–8s/image at {WPM} WPM) {'─' * 16}")
    hdr = f"  {'Scene':<7} {'Words':<7} {'Narr':<7} {'Prompted':<10} {'Generated':<11} {'Hold':<8} Status"
    print(hdr)
    print("  " + "-" * 66)
    tw = tn = tp = tg = 0
    for scene_num, words, narr_s, prompted, generated, hold, missing in pacing_rows:
        note = f"  ({missing} to generate)" if missing else ""
        status = pacing_status(hold) if prompted else "—"
        print(f"  {scene_num:<7} {words:<7} {narr_s}s{'':<4} {prompted:<10} {generated:<11} {hold}s{'':<3} {status}{note}")
        tw += words; tn += narr_s; tp += prompted; tg += generated
    print("  " + "-" * 66)
    avg_hold = round(tn / tp, 1) if tp else 0.0
    print(f"  {'Total':<7} {tw:<7} {tn}s{'':<4} {tp:<10} {tg:<11} {avg_hold}s   avg planned hold")
    total_dur_min = tn // 60
    total_dur_sec = tn % 60
    print(f"\n  Script so far: {tw} words → ~{total_dur_min}m {total_dur_sec}s narration across {tp} planned images")
    print(f"  Benchmark: Charava-Bhootni 4.2s · Kumar-Aur-Chudail 5–8s · Jinn-Masoom 6.0s")
    print(f"  Flag: <5s too fast  5–6s below target  6–8s good  8–10s slightly slow  >10s too slow\n")

    critique_rows = extract_critique_rows(content, scenes)
    summary_md = build_critique_summary(critique_rows, pacing_rows)
    write_critique_state(script_path, summary_md)


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
        print_critic_summary(script_md, base)
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
                   "-c:v", "copy", "-af", NARRATION_EQ,
                   "-c:a", "aac", "-b:a", "192k",
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
