#!/usr/bin/env python3
"""
render_scene.py — Core render logic for render-scene shell command.
Do not call directly. Use the render-scene shell wrapper.

Effects baked in (from competitor research):
  - Ken Burns zoom per image (1.00 → 1.15, random in/out, 3% pan drift)
  - Hard cuts between images within a scene
  - Fade-in from black at scene start (0.8s)
  - Fade-out to black at scene end (0.8s)
  - Bloom glow on deity images (auto-detected from script MD)
"""

import argparse
import datetime
import glob
import os
import random
import re
import shutil
import subprocess
import tempfile

ZOOM_TARGET = 1.15
PAN_DRIFT = 0.03
FADE_DUR = 0.8
WPM = 85  # Hindi devotional narration benchmark (80–90 WPM range)
_CRITIQUE_TRUNC = 100
NARRATION_EQ = (
    "volume=-4dB,"
    "highpass=f=90:poles=2,"
    "equalizer=f=120:width_type=q:width=1.5:g=-2.5,"
    "equalizer=f=320:width_type=q:width=1.5:g=-1.5,"
    "equalizer=f=2500:width_type=q:width=1.2:g=2.5,"
    "treble=g=2:f=10000,"
    "alimiter=level_in=1:level_out=0.7:limit=0.7:attack=5:release=50"
)
# Film dust: per-block shape randomized by a position-only hash (h2).
# h1 (time+position) gates activation; h2 picks shape: 40% V-streak, 30% diagonal, 30% circle.
# Streaks are 4×11px ellipses; circle is r=3.5px. Marks change every 8 frames.
_DUST = (
    "if("
    "lt(mod(abs(sin(floor(X/15)*211.7+floor(Y/15)*173.1+floor(N/8)*97.3)*43758.5),1.0),0.0008),"
    "if(lt(mod(abs(sin(floor(X/15)*431.3+floor(Y/15)*613.7)*43758.5),1.0),0.40),"
    "lt(pow(mod(X,15)-7,2)/4+pow(mod(Y,15)-7,2)/30.25,1),"
    "if(lt(mod(abs(sin(floor(X/15)*431.3+floor(Y/15)*613.7)*43758.5),1.0),0.70),"
    "lt(pow(mod(X+Y,15)-7,2)/4+pow(mod(X-Y,15)-7,2)/30.25,1),"
    "lt(pow(mod(X,15)-7,2)+pow(mod(Y,15)-7,2),12.25))),"
    "0)"
)
_DUST_S = (  # small specks: r=2px circle
    "if("
    "lt(mod(abs(sin(floor(X/8)*331.1+floor(Y/8)*271.7+floor(N/8)*51.9)*43758.5),1.0),0.0002),"
    "lt(pow(mod(X,8)-4,2)+pow(mod(Y,8)-4,2),4),"
    "0)"
)
VINTAGE_VF = (
    "noise=alls=8:allf=t+u,"
    f"geq=lum='if(gt({_DUST}+{_DUST_S},0),0,lum(X,Y))':cb='cb(X,Y)':cr='cr(X,Y)'"
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
    """Count Hindi/Hinglish words in the script text.

    Supports two formats:
      New: ### Script Hindi ... ### Script English
      Old: plain text before first ### subsection
    """
    hindi_match = re.search(r"^### Script Hindi\s*\n", scene_block, re.MULTILINE)
    if hindi_match:
        text = scene_block[hindi_match.end():]
        next_sec = _RE_SUBSECTION.search(text)
        if next_sec:
            text = text[:next_sec.start()]
    else:
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
    """Sort Scene-N-<num>[<suffix>].png correctly: (num, suffix).
    Handles 1a, 1b, 3a, 3b, 3c as well as plain integers.
    """
    stem = os.path.splitext(os.path.basename(path))[0]
    parts = stem.split("-")
    try:
        m = re.match(r"(\d+)([a-z]*)", parts[2])
        if m:
            return (int(m.group(1)), m.group(2))
    except IndexError:
        pass
    return (0, "")


def render_card(img, out, duration, w, h, fps, fade_in, fade_out, preview, glow=False, zoom_in=True):
    frames = max(int(duration * fps), 1)
    zoom_step = (ZOOM_TARGET - 1.0) / frames

    sign = 1 if zoom_in else -1
    z_expr = (
        f"min(1.0+on*{zoom_step:.6f},{ZOOM_TARGET})" if zoom_in
        else f"max({ZOOM_TARGET}-on*{zoom_step:.6f},1.0)"
    )
    zoompan = (
        f"zoompan=z='{z_expr}'"
        f":x='iw/2-(iw/zoom/2)+iw*{sign * PAN_DRIFT}*(1-on/{frames})'"
        f":y='ih/2-(ih/zoom/2)+ih*{sign * PAN_DRIFT}*(1-on/{frames})'"
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


def discover_scenes(base):
    seen = set()
    for path in glob.glob(os.path.join(base, "Scene-*-*.png")):
        m = re.match(r"Scene-(\d+)-", os.path.basename(path))
        if m:
            seen.add(int(m.group(1)))
    return sorted(seen)


def default_narration_path(base, scene_num):
    return os.path.join(base, f"Scene-{scene_num}.mp3")


def resolve_narration_path(base, scene_num, narration_arg):
    if narration_arg:
        return narration_arg if os.path.isabs(narration_arg) else os.path.join(base, narration_arg)
    return default_narration_path(base, scene_num)


def render_one_scene(args, scene_num, narration_path, base, renders_dir, script_md):
    deity_keywords = get_deity_keywords(script_md) if script_md else []
    image_prompts = extract_image_prompts(script_md, str(scene_num)) if script_md else {}

    w, h, fps = (1280, 720, 24) if args.preview else (1920, 1080, 30)

    images = sorted(glob.glob(os.path.join(base, f"Scene-{scene_num}-*.png")), key=image_sort_key)
    if not images:
        print(f"  Scene {scene_num}: no images found — skipping")
        return None

    n = len(images)
    if narration_path:
        total = narration_duration(narration_path)
        dur = total / n
        print(f"\nScene {scene_num}: {n} images, narration {total:.1f}s → {dur:.1f}s/image")
    else:
        dur = args.duration
        print(f"\nScene {scene_num}: {n} images × {dur}s = {n * dur:.0f}s total")

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
            zoom_in = random.random() > 0.4
            label = " [glow]" if use_glow else ""
            label += " [out]" if not zoom_in else ""
            print(f"  [{i+1}/{n}] {os.path.basename(img)}{label}")
            render_card(img, clip, dur, w, h, fps,
                        fade_in=(i == 0), fade_out=(i == n - 1),
                        preview=args.preview, glow=use_glow, zoom_in=zoom_in)
            clips.append(clip)

        concat_txt = os.path.join(tmp, "concat.txt")
        with open(concat_txt, "w") as f:
            for c in clips:
                f.write(f"file '{c}'\n")

        suffix = "-preview" if args.preview else ""
        output = os.path.join(renders_dir, f"Scene-{scene_num}-test{suffix}.mp4")

        base_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt]
        video_opts = (
            ["-vf", VINTAGE_VF, "-c:v", "libx264", "-crf", "18",
             "-preset", "veryfast" if args.preview else "medium", "-pix_fmt", "yuv420p"]
            if args.vintage else ["-c:v", "copy"]
        )
        if narration_path:
            cmd = base_cmd + ["-i", narration_path] + video_opts + [
                "-af", NARRATION_EQ, "-c:a", "aac", "-b:a", "192k", "-shortest", output]
        else:
            cmd = base_cmd + video_opts + (["-c:a", "copy"] if args.vintage else ["-c", "copy"]) + [output]

        subprocess.run(cmd, check=True)
        size_mb = os.path.getsize(output) / 1024 / 1024
        print(f"  → {output} ({size_mb:.1f} MB)")
        return output
    finally:
        shutil.rmtree(tmp)


ZOOM_BURST_DUR = 0.7   # seconds of zoom-burst at scene end
ZOOM_BURST_PROB = 0.4  # probability per scene when using --all


def zoom_burst_end(mp4_path, fps, preview):
    """Apply radial zoom-burst + increasing blur to the last ZOOM_BURST_DUR seconds in-place."""
    dur_out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", mp4_path],
        capture_output=True, text=True, check=True,
    )
    total_dur = float(dur_out.stdout.strip())
    if total_dur < ZOOM_BURST_DUR * 2:
        return  # scene too short — skip

    dim_out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", mp4_path],
        capture_output=True, text=True, check=True,
    )
    w, h = map(int, dim_out.stdout.strip().split("x"))
    split_t = total_dur - ZOOM_BURST_DUR
    burst_frames = max(int(ZOOM_BURST_DUR * fps), 1)

    # zoom ramps 1.0 → 2.5 over burst_frames; blur ramps 0 → 10px
    zoom_expr = f"1+1.5*on/{burst_frames}"
    fc = (
        f"[0:v]split=2[va][vb];"
        f"[va]trim=0:{split_t:.3f},setpts=PTS-STARTPTS[v1];"
        f"[vb]trim={split_t:.3f},setpts=PTS-STARTPTS,"
        f"zoompan=z='{zoom_expr}':d={burst_frames}"
        f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps},"
        f"boxblur=luma_radius='n/{burst_frames}*10':luma_power=1[v2];"
        f"[v1][v2]concat=n=2:v=1:a=0[vout]"
    )
    audio_probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=codec_type",
         "-of", "default=noprint_wrappers=1", mp4_path],
        capture_output=True, text=True,
    )
    has_audio = bool(audio_probe.stdout.strip())

    tmp = mp4_path + ".zburst.mp4"
    cmd = ["ffmpeg", "-y", "-i", mp4_path, "-filter_complex", fc, "-map", "[vout]"]
    if has_audio:
        cmd += ["-map", "0:a", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-crf", "18",
            "-preset", "veryfast" if preview else "medium",
            "-pix_fmt", "yuv420p", tmp]
    subprocess.run(cmd, check=True, capture_output=True)
    os.replace(tmp, mp4_path)
    print(f"  ↳ zoom-burst applied")


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--scene", default=None)
    ap.add_argument("--all", action="store_true",
                    help="Render all scenes that have a matching Scene-N.mp3, then concat")
    ap.add_argument("--duration", type=float, default=7.0)
    ap.add_argument("--narration", default=None)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--glow", action="store_true",
                    help="Force bloom glow on all images (auto-detected per image if omitted)")
    ap.add_argument("--vintage", dest="vintage", action="store_true", default=True,
                    help="Add film grain + dust spots (default)")
    ap.add_argument("--no-vintage", dest="vintage", action="store_false",
                    help="Disable film grain + dust spots")
    ap.add_argument("--zoom-burst", dest="zoom_burst", action="store_true",
                    help="Apply radial zoom-burst at scene end (random 40%% with --all)")
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

    if not args.scene and not args.all:
        print("Error: --scene N or --all is required. Use --critic for script analysis.")
        return 1

    script_md = find_script_md(base)

    if args.all:
        scenes = discover_scenes(base)
        if not scenes:
            print("No Scene-N-*.png files found.")
            return 1

        rows = []
        for s in scenes:
            mp3 = default_narration_path(base, s)
            img_count = len(glob.glob(os.path.join(base, f"Scene-{s}-*.png")))
            has_narr = os.path.exists(mp3)
            rows.append((s, img_count, mp3 if has_narr else None, has_narr))

        print("\nPre-check:")
        print(f"  {'Scene':<6}  {'Images':<7}  {'Narration':<18}  Action")
        print(f"  {'─'*6}  {'─'*7}  {'─'*18}  {'─'*18}")
        for s, img_count, mp3_path, has_narr in rows:
            narr_col = f"Scene-{s}.mp3 ✓" if has_narr else "—"
            action = "RENDER" if has_narr else "SKIP — no narration"
            print(f"  {s:<6}  {img_count:<7}  {narr_col:<18}  {action}")

        to_render = [(s, mp3) for s, _, mp3, has_narr in rows if has_narr]
        skipped = [s for s, _, _, has_narr in rows if not has_narr]
        if not to_render:
            print("\nNothing to render — add Scene-N.mp3 files first.")
            return 1
        if skipped:
            print(f"\nSkipping: Scene {', '.join(str(s) for s in skipped)}")
        print(f"\nRendering {len(to_render)} of {len(scenes)} scenes...")

        fps = 24 if args.preview else 30
        rendered = []
        for s, mp3_path in to_render:
            out = render_one_scene(args, s, mp3_path, base, renders_dir, script_md)
            if out:
                if args.zoom_burst and random.random() < ZOOM_BURST_PROB:
                    zoom_burst_end(out, fps, args.preview)
                rendered.append(out)

        if len(rendered) > 1:
            suffix = "-preview" if args.preview else ""
            scene_nums = [s for s, _ in to_render]
            range_tag = f"Scene-{min(scene_nums)}-{max(scene_nums)}"
            full_out = os.path.join(renders_dir, f"{range_tag}-test{suffix}.mp4")
            tmp = tempfile.mkdtemp()
            try:
                concat_txt = os.path.join(tmp, "concat.txt")
                with open(concat_txt, "w") as f:
                    for r in rendered:
                        f.write(f"file '{r}'\n")
                subprocess.run(
                    ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                     "-i", concat_txt, "-c", "copy", full_out],
                    check=True
                )
                size_mb = os.path.getsize(full_out) / 1024 / 1024
                print(f"\nFull video: {full_out} ({size_mb:.1f} MB)")
            finally:
                shutil.rmtree(tmp)

        return 0

    # Single scene mode
    narration_path = resolve_narration_path(base, args.scene, args.narration)
    if not os.path.exists(narration_path):
        print(f"Error: narration file not found: {narration_path}")
        print("Pass --narration FILE to override the default Scene-N.mp3 path.")
        return 1

    fps = 24 if args.preview else 30
    out = render_one_scene(args, args.scene, narration_path, base, renders_dir, script_md)
    if out and args.zoom_burst:
        zoom_burst_end(out, fps, args.preview)
    return 0 if out else 1


if __name__ == "__main__":
    raise SystemExit(main())
