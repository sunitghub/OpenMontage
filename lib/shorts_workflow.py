from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from lib.package_bootstrap import (
    PackageBootstrapError,
    SHORTS_ROOT,
    _parse_definition_block,
    _parse_scenes,
    _split_level_three_sections,
)


DESIGN_CHANGES_PATH = SHORTS_ROOT.parent / "Design-Changes.md"
STRATEGY_PATH = SHORTS_ROOT.parent.parent / "Blissful-Strategy.md"


@dataclass
class ShortFolderStatus:
    index: int
    folder: Path
    slug: str
    status: str
    md_path: Path | None
    mp4_files: list[Path]
    extra_files: list[Path]


def run_gen_shorts_mode() -> int:
    _clear_screen()
    folders = list_short_folders()
    if not folders:
        print(f"No Shorts folders found under {SHORTS_ROOT}")
        return 1

    while True:
        _print_folder_listing(folders)
        choice = input("Select Idx to inspect, or 'q' to quit: ").strip()
        if choice.lower() in {"q", "quit", "exit"}:
            return 0
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(folders):
            print("Invalid Idx.\n")
            continue

        selected = folders[int(choice) - 1]
        try:
            inspect_short_folder(selected)
        except PackageBootstrapError as exc:
            print(f"Error: {exc}\n")
        folders = list_short_folders()


def run_gen_mp4_mode() -> int:
    _clear_screen()
    folders = list_short_folders()
    if not folders:
        print(f"No Shorts folders found under {SHORTS_ROOT}")
        return 1

    while True:
        _print_folder_listing(folders)
        choice = input("Select Idx to review scene MP4s, or 'q' to quit: ").strip()
        if choice.lower() in {"q", "quit", "exit"}:
            return 0
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(folders):
            print("Invalid Idx.\n")
            continue

        selected = folders[int(choice) - 1]
        if not selected.md_path or not selected.md_path.exists():
            print("This folder has no markdown package yet.\n")
            continue

        try:
            review_scene_mp4s(selected)
        except PackageBootstrapError as exc:
            print(f"Error: {exc}\n")
        folders = list_short_folders()


def list_short_folders() -> list[ShortFolderStatus]:
    if not SHORTS_ROOT.exists():
        return []

    statuses: list[ShortFolderStatus] = []
    for index, folder in enumerate(sorted(path for path in SHORTS_ROOT.iterdir() if path.is_dir()), start=1):
        slug = folder.name
        md_path = folder / f"{slug}.md"
        mp4_files = sorted(folder.glob("scene-*.mp4"))
        extra_files = sorted(
            path
            for path in folder.iterdir()
            if path.is_file()
            and path.suffix.lower() not in {".md", ".mp4"}
            and path.name != "Thumbnail.jpg"
        )

        parts: list[str] = []
        if md_path.exists():
            parts.append("MD")
        if mp4_files:
            parts.append(f"MP4:{len(mp4_files)}")
        if (folder / "Thumbnail.jpg").exists():
            parts.append("Thumbnail")
        if extra_files:
            parts.append(f"Extra:{len(extra_files)}")
        status = ", ".join(parts) if parts else "Empty"

        statuses.append(
            ShortFolderStatus(
                index=index,
                folder=folder,
                slug=slug,
                status=status,
                md_path=md_path if md_path.exists() else None,
                mp4_files=mp4_files,
                extra_files=extra_files,
            )
        )
    return statuses


def inspect_short_folder(entry: ShortFolderStatus) -> None:
    print(f"\nInspecting: {entry.slug}")
    print(f"Folder: {entry.folder}")
    print(f"Status: {entry.status}")
    _print_folder_files(entry.folder)

    if not entry.md_path:
        answer = input("No markdown package found. Open a Codex skill prompt to research and create one? [y/N]: ").strip().lower()
        if answer == "y":
            print_codex_skill_prompt(entry.folder, existing_md_path=None)
            print()
        else:
            print()
        return

    validation = validate_short_markdown(entry.md_path, entry.slug)
    print("Validation:")
    for line in validation["messages"]:
        print(f"- {line}")

    answer = input("Open a Codex skill prompt to research and spruce the markdown package? [y/N]: ").strip().lower()
    if answer == "y":
        print_codex_skill_prompt(entry.folder, existing_md_path=entry.md_path)
        print()
    else:
        print()


def review_scene_mp4s(entry: ShortFolderStatus) -> None:
    md_path = entry.md_path
    if not md_path:
        raise PackageBootstrapError("Markdown package is required before MP4 review.")

    text = md_path.read_text()
    scenes = _parse_scenes(_get_section(text, "Scenes"))
    if not scenes:
        raise PackageBootstrapError("No scenes found in markdown package.")

    results_rows = _parse_results_rows(text)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for index, scene in enumerate(scenes, start=1):
        candidates = [entry.folder / f"scene-{index}.mp4", entry.folder / f"scene-{index:02d}.mp4"]
        existing = next((path for path in candidates if path.exists()), None)
        expected_duration = float(scene["duration_seconds"])
        if not existing:
            results_rows[index] = {"status": "Missing", "datetime": now}
            print(f"\nScene {index}: missing MP4")
            continue

        actual_duration = probe_duration(existing)
        diff = None if actual_duration is None else round(actual_duration - expected_duration, 2)
        print(f"\nScene {index}")
        print(f"- File: {existing.name}")
        print(f"- Expected beat: {scene['script beat']}")
        print(f"- Expected duration: {expected_duration}s")
        if actual_duration is not None:
            print(f"- Actual duration: {actual_duration}s")
            print(f"- Duration delta: {diff}s")

        status = _prompt_scene_status()
        results_rows[index] = {"status": status, "datetime": now}

    updated = upsert_results_section(text, results_rows)
    md_path.write_text(updated)
    print(f"\nUpdated results in {md_path}\n")


def print_codex_skill_prompt(folder: Path, existing_md_path: Path | None) -> None:
    slug = folder.name
    md_path = folder / f"{slug}.md"
    mode = "spruce the existing markdown package" if existing_md_path and existing_md_path.exists() else "create the markdown package"
    print("\nUse this in Codex:\n")
    print(
        build_codex_skill_prompt(
            folder=folder,
            md_path=md_path,
            mode=mode,
            existing_md_path=existing_md_path,
        )
    )


def validate_short_markdown(md_path: Path, slug: str) -> dict[str, Any]:
    text = md_path.read_text()
    title = _extract_h1_or_title(text)
    scenes = _parse_scenes(_get_section(text, "Scenes")) if "## Scenes" in text else []
    folder_tokens = _intent_tokens(slug)
    content_blob = f"{title}\n{text}".lower()
    matched_tokens = [token for token in folder_tokens if token.lower() in content_blob]
    score = 1.0 if not folder_tokens else len(matched_tokens) / len(folder_tokens)

    messages = [
        f"File name matches folder slug: {'yes' if md_path.stem == slug else 'no'}",
        f"Title detected: {'yes' if bool(title) else 'no'}",
        f"Scenes detected: {len(scenes)}",
        f"Intent token match: {len(matched_tokens)}/{len(folder_tokens)} ({score:.0%})",
        f"Results section: {'yes' if '## Results' in text else 'no'}",
    ]
    return {"score": score, "messages": messages}


def render_light_short_markdown(
    slug: str,
    data: dict[str, Any],
    *,
    existing_sections: dict[str, Any] | None = None,
) -> str:
    existing_sections = existing_sections or {}

    title = (existing_sections.get("title") or data["title"]).strip()
    description = (existing_sections.get("description") or data["description"]).strip()
    thumbnail_title = (
        existing_sections.get("thumbnail_title") or data["thumbnail_title"]
    ).strip()
    thumbnail_prompt = (
        existing_sections.get("thumbnail_prompt") or data["thumbnail_prompt"]
    ).strip()
    script = existing_sections.get("script") or data["script"]
    scenes = existing_sections.get("scenes") or data["scenes"]

    lines = [
        f"# {title}",
        "",
        "## Title",
        "",
        title,
        "",
        "## Description",
        "",
        description,
        "",
        "## Thumbnail",
        "",
        f"- Title Text: `{thumbnail_title}`",
        f"- Prompt: {thumbnail_prompt}",
        "",
        "## Script",
        "",
        "### Hook",
        "",
        script["hook"].strip(),
        "",
        "### Body",
        "",
        script["body"].strip(),
        "",
        "### Close",
        "",
        script["close"].strip(),
        "",
        "## Scenes",
        "",
    ]

    normalized_scenes = normalize_scenes_for_render(scenes)
    for scene in normalized_scenes:
        scene_number = int(scene["scene_number"])
        lines.extend(
            [
                f"### Scene-{scene_number}",
                f"- Purpose: {scene['purpose'].strip()}",
                f"- Script beat: `{scene['script_beat'].strip()}`",
                f"- Duration: `{scene['duration'].strip()}`",
                f"- Visual: {scene['visual'].strip()}",
                f"- Camera: {scene['camera'].strip()}",
                f"- Motion: {scene['motion'].strip()}",
                f"- Prompt: {scene['prompt'].strip()}",
                f"- Output: `scene-{scene_number}.mp4`",
                "",
            ]
        )

    existing_results = existing_sections.get("results", {})
    lines.extend(
        [
            "## Results",
            "",
            "| Scene | Status | DateTime |",
            "|---|---|---|",
        ]
    )
    for scene in normalized_scenes:
        scene_number = int(scene["scene_number"])
        result_row = existing_results.get(scene_number, {"status": "Needs Generation", "datetime": ""})
        status_text = result_row["status"].strip()
        datetime_text = result_row["datetime"].strip()
        lines.append(
            f"| {scene_number} | {status_text} | {datetime_text} |"
        )
    lines.append("")
    return "\n".join(lines)


def upsert_results_section(markdown_text: str, results_rows: dict[int, dict[str, str]]) -> str:
    new_section_lines = [
        "## Results",
        "",
        "| Scene | Status | DateTime |",
        "|---|---|---|",
    ]
    for scene_number in sorted(results_rows):
        row = results_rows[scene_number]
        new_section_lines.append(f"| {scene_number} | {row['status']} | {row['datetime']} |")
    new_section = "\n".join(new_section_lines).rstrip() + "\n"

    pattern = re.compile(r"^## Results\s*$.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(markdown_text):
        return pattern.sub(new_section, markdown_text).rstrip() + "\n"
    return markdown_text.rstrip() + "\n\n" + new_section


def probe_duration(path: Path) -> float | None:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    try:
        return round(float(result.stdout.strip()), 2)
    except ValueError:
        return None


def _print_folder_listing(entries: list[ShortFolderStatus]) -> None:
    print("\nAvailable Shorts")
    idx_width = max(3, len(str(len(entries))))
    folder_width = max(len("Folder"), max(len(entry.slug) for entry in entries))
    status_width = max(len("Status"), max(len(entry.status) for entry in entries))

    header = f"{'Idx':<{idx_width}}  {'Folder':<{folder_width}}  {'Status':<{status_width}}"
    divider = f"{'-' * idx_width}  {'-' * folder_width}  {'-' * status_width}"
    print(header)
    print(divider)
    for entry in entries:
        print(f"{entry.index:<{idx_width}}  {entry.slug:<{folder_width}}  {entry.status:<{status_width}}")
    print()


def _print_folder_files(folder: Path) -> None:
    files = sorted(path.name for path in folder.iterdir() if path.is_file())
    if not files:
        print("Files: none")
        return
    print("Files:")
    for file_name in files:
        print(f"- {file_name}")


def _clear_screen() -> None:
    print("\033[2J\033[H", end="")


def build_codex_skill_prompt(
    *,
    folder: Path,
    md_path: Path,
    mode: str,
    existing_md_path: Path | None,
) -> str:
    prompt_lines = [
        "Use the OpenMontage skill `skills/meta/shorts-workflow.md`.",
        "",
        f"Task: {mode}.",
        f"Folder: {folder}",
        f"Markdown path: {md_path}",
        f"Design guidance: {DESIGN_CHANGES_PATH}",
        f"Strategy guidance: {STRATEGY_PATH}",
    ]
    if existing_md_path and existing_md_path.exists():
        prompt_lines.extend(
            [
                f"Existing markdown: {existing_md_path}",
                "Preserve existing Script, Scenes, and Results unless they are missing or clearly weak.",
                "Create a timestamped backup before making changes.",
            ]
        )
    else:
        prompt_lines.extend(
            [
                "Create a new markdown package named after the folder slug.",
                "Use the lighter Shorts format: Title, Description, Thumbnail, Script, Scenes, Results.",
            ]
        )
    prompt_lines.extend(
        [
            "Research and corroborate factual claims on the web.",
            "Keep it suitable for manual Kling Web UI generation.",
            "Avoid horror framing.",
        ]
    )
    return "\n".join(prompt_lines)


def parse_existing_markdown_sections(markdown_text: str) -> dict[str, Any]:
    sections: dict[str, Any] = {}

    title_section = _get_section(markdown_text, "Title")
    if title_section:
        sections["title"] = _first_nonempty_line(title_section)

    description_section = _get_section(markdown_text, "Description")
    if description_section:
        sections["description"] = " ".join(
            line.strip() for line in description_section.splitlines() if line.strip()
        )

    thumbnail_section = _get_section(markdown_text, "Thumbnail")
    if thumbnail_section:
        thumb_data = _parse_definition_block(thumbnail_section)
        if thumb_data.get("Title Text"):
            sections["thumbnail_title"] = thumb_data["Title Text"].strip("` ")
        if thumb_data.get("Prompt"):
            sections["thumbnail_prompt"] = thumb_data["Prompt"]

    script_section = _get_section(markdown_text, "Script")
    if script_section:
        parsed_script = {}
        for heading, body in _split_level_three_sections(script_section):
            cleaned = " ".join(line.strip() for line in body.splitlines() if line.strip())
            if cleaned:
                parsed_script[heading.lower()] = cleaned
        if parsed_script:
            sections["script"] = {
                "hook": parsed_script.get("hook", ""),
                "body": parsed_script.get("body", ""),
                "close": parsed_script.get("close", ""),
            }

    scenes_section = _get_section(markdown_text, "Scenes")
    if scenes_section:
        parsed_scenes = _parse_scenes(scenes_section)
        if parsed_scenes:
            sections["scenes"] = parsed_scenes

    results_rows = _parse_results_rows(markdown_text)
    if results_rows:
        sections["results"] = results_rows

    return sections


def normalize_scenes_for_render(scenes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for index, scene in enumerate(scenes, start=1):
        if "scene_number" in scene:
            normalized.append(scene)
            continue
        heading = scene.get("heading", f"Scene-{index}")
        match = re.search(r"(\d+)$", heading)
        scene_number = int(match.group(1)) if match else index
        normalized.append(
            {
                "scene_number": scene_number,
                "purpose": scene.get("purpose", ""),
                "script_beat": scene.get("script beat", ""),
                "duration": _duration_string_from_seconds(scene.get("duration_seconds")),
                "visual": scene.get("visual", ""),
                "camera": scene.get("camera", ""),
                "motion": scene.get("motion", ""),
                "prompt": scene.get("prompt", ""),
            }
        )
    return normalized


def backup_markdown_file(md_path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    backup_path = md_path.with_name(f"{md_path.stem}.backup-{timestamp}{md_path.suffix}")
    backup_path.write_text(md_path.read_text())
    return backup_path


def _duration_string_from_seconds(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        if float(value).is_integer():
            return f"{int(value)}s"
        return f"{value}s"
    return str(value)


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def _intent_tokens(slug: str) -> list[str]:
    tokens = [token for token in slug.replace("-", " ").split() if len(token) > 2 and not token.isdigit()]
    return tokens


def _extract_h1_or_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    title_section = _get_section(text, "Title")
    return title_section.splitlines()[0].strip() if title_section else ""


def _prompt_scene_status() -> str:
    while True:
        answer = input("Status? [p=Publishable, g=Generate from scene prompt, c=Checked]: ").strip().lower()
        mapping = {
            "p": "Publishable",
            "g": "Generate from scene prompt",
            "c": "Checked",
        }
        if answer in mapping:
            return mapping[answer]
        print("Invalid choice.")


def _parse_results_rows(text: str) -> dict[int, dict[str, str]]:
    pattern = re.compile(r"^## Results\s*$.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    if not match:
        return {}
    rows: dict[int, dict[str, str]] = {}
    for line in match.group(0).splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 3 or cells[0] in {"Scene", "---"}:
            continue
        if cells[0].isdigit():
            rows[int(cells[0])] = {"status": cells[1], "datetime": cells[2]}
    return rows


def scaffold_package(folder: str) -> Path:
    """Create the Shorts folder and minimal markdown stub if they don't exist."""
    folder_path = SHORTS_ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    md_path = folder_path / f"{folder}.md"
    if not md_path.exists():
        md_path.write_text(
            f"# {folder.replace('-', ' ').title()}\n\n"
            "## Script\n\n"
            "Hook: \n\nBody: \n\nClose: \n\nCTA: \n"
        )
        print(f"Created: {md_path}")
    return md_path


def _resolve_md_path(folder: str) -> Path | None:
    """Find the package markdown: prefer <folder>.md, fall back to largest .md (skips Screen-Script files)."""
    folder_path = SHORTS_ROOT / folder
    canonical = folder_path / f"{folder}.md"
    if canonical.exists():
        return canonical
    candidates = [
        p for p in folder_path.glob("*.md")
        if "screen-script" not in p.stem.lower()
    ]
    return max(candidates, key=lambda p: p.stat().st_size) if candidates else None


def read_script_section(folder: str) -> str:
    """Extract the raw ## Script section text for the agent to process."""
    md_path = _resolve_md_path(folder)
    if not md_path:
        return ""
    return _get_section(md_path.read_text(), "Script")


def write_scenes_section(folder: str, scenes_md: str) -> None:
    """Write/replace the ## Scenes block in the package markdown."""
    md_path = SHORTS_ROOT / folder / f"{folder}.md"
    text = md_path.read_text()
    new_block = f"## Scenes\n\n{scenes_md.strip()}\n"
    pattern = re.compile(r"^## Scenes\s*$.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        updated = pattern.sub(new_block, text)
    else:
        updated = text.rstrip() + "\n\n" + new_block
    md_path.write_text(updated)


def read_scenes(folder: str) -> list[dict[str, Any]]:
    """Parse the ## Scenes block into a list of scene dicts."""
    md_path = _resolve_md_path(folder)
    if not md_path:
        return []
    text = md_path.read_text()
    scenes_text = _get_section(text, "Scenes")
    if not scenes_text:
        return []
    try:
        return _parse_scenes(scenes_text)
    except PackageBootstrapError:
        # Markdown uses an extended scene format that the strict parser can't handle.
        # Count ### Scene-N headings as a best-effort scene count.
        return [{"heading": h} for h in re.findall(r"^### Scene-\d+", scenes_text, re.MULTILINE)]


def write_artifact_status_table(folder: str, rows: list[dict[str, str]]) -> None:
    """Write/replace the ## Artifact Status table at the end of the package markdown."""
    md_path = SHORTS_ROOT / folder / f"{folder}.md"
    text = md_path.read_text()
    table_lines = [
        "## Artifact Status",
        "",
        "| Scene | File | Tool | Status |",
        "|---|---|---|---|",
    ]
    for row in rows:
        table_lines.append(
            f"| {row['scene']} | {row['file']} | {row['tool']} | {row['status']} |"
        )
    new_block = "\n".join(table_lines).rstrip() + "\n"
    pattern = re.compile(r"^## Artifact Status\s*$.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        updated = pattern.sub(new_block, text)
    else:
        updated = text.rstrip() + "\n\n" + new_block
    md_path.write_text(updated)


def get_pending_artifacts(folder: str) -> list[dict[str, str]]:
    """Return rows from ## Artifact Status where Status starts with PENDING (run --generate-clips)."""
    md_path = SHORTS_ROOT / folder / f"{folder}.md"
    if not md_path.exists():
        return []
    text = md_path.read_text()
    pattern = re.compile(r"^## Artifact Status\s*$.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    if not match:
        return []
    pending = []
    for line in match.group(0).splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] in {"Scene", "---"}:
            continue
        status = cells[3]
        if "run --generate-clips" in status:
            pending.append({"scene": cells[0], "file": cells[1], "tool": cells[2], "status": status})
    return pending


def run_scenes_mode(folder: str) -> int:
    """Entry point for --scenes: scaffold if needed, then print context for the agent."""
    md_path = scaffold_package(folder)
    script = read_script_section(folder)
    print(f"\nShorts package: {md_path}")
    print(f"Script section:\n{script or '(empty — fill in the Script section first)'}\n")
    print("The agent will now read the shorts-director skill and generate the scene breakdown.")
    print("When done, review the Scenes section in the markdown, then run --artifacts.\n")
    return 0


def run_artifacts_mode(folder: str) -> int:
    """Entry point for --artifacts: print context for the agent."""
    md_path = _resolve_md_path(folder) or SHORTS_ROOT / folder / f"{folder}.md"
    scenes = read_scenes(folder)
    print(f"\nShorts package: {md_path}")
    print(f"Scenes found: {len(scenes)}")
    print("The agent will now read the shorts-director skill and write artifact prompts.")
    print("No API calls will be made. Review prompts in the markdown, then run --generate-clips.\n")
    return 0


def run_generate_clips_mode(folder: str) -> int:
    """Entry point for --generate-clips: print pending artifacts for the agent."""
    md_path = _resolve_md_path(folder) or SHORTS_ROOT / folder / f"{folder}.md"
    pending = get_pending_artifacts(folder)
    print(f"\nShorts package: {md_path}")
    print(f"Pending API-backed artifacts: {len(pending)}")
    for row in pending:
        print(f"  Scene {row['scene']}: {row['file']} via {row['tool']}")
    print("The agent will now call the appropriate tools for each pending artifact.\n")
    return 0


def run_rendershorts_mode(folder: str) -> int:
    """Entry point for --rendershorts when no composition.html exists yet."""
    md_path = _resolve_md_path(folder) or SHORTS_ROOT / folder / f"{folder}.md"
    print(f"\nShorts package: {md_path}")
    print("No composition.html found. The agent will build the HyperFrames composition from the scene markdown.")
    print("Once composition.html is written, re-run --rendershorts to render the final MP4.\n")
    return 0


def _get_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    buffer: list[str] = []
    in_section = False
    for line in lines:
        heading_match = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if heading_match:
            level = len(heading_match.group(1))
            label = heading_match.group(2).strip()
            if in_section and level <= 2:
                break
            if level == 2 and label == heading:
                in_section = True
                continue
        if in_section:
            buffer.append(line)
    return "\n".join(buffer).strip()
