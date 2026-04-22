"""Export per-screen script lines from a Shorts markdown package.

Reads `### Scene-N` sections and extracts each `Script beat`, then writes a
markdown file where every line is:

Screen <no>: <script beat>
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SCENE_HEADER_RE = re.compile(r"^### Scene-(\d+)\s*$")
INLINE_SCRIPT_BEAT_RE = re.compile(r"^- Script beat:\s*`(.+?)`\s*$")
STOP_HEADERS = {"## Production Notes", "## Assembly Map", "## Results", "## Post Timeline"}


def extract_scene_beats(markdown_path: Path) -> dict[int, str]:
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    beats: dict[int, str] = {}
    current_scene: int | None = None
    capture_next_beat = False

    for raw_line in lines:
        line = raw_line.rstrip()
        if line in STOP_HEADERS:
            break

        header_match = SCENE_HEADER_RE.match(line)
        if header_match:
            current_scene = int(header_match.group(1))
            capture_next_beat = False
            continue

        if current_scene is None:
            continue

        inline_match = INLINE_SCRIPT_BEAT_RE.match(line)
        if inline_match:
            beats[current_scene] = inline_match.group(1).strip()
            capture_next_beat = False
            continue

        if line.strip() == "- Script beat:":
            capture_next_beat = True
            continue

        if capture_next_beat:
            stripped = line.strip()
            if stripped.startswith("`") and stripped.endswith("`"):
                beats[current_scene] = stripped.strip("`").strip()
                capture_next_beat = False
            elif stripped:
                beats[current_scene] = stripped
                capture_next_beat = False

    return beats


def default_output_path(markdown_path: Path) -> Path:
    return markdown_path.with_name(f"{markdown_path.stem}-Screen-Script.md")


def build_screen_script_lines(scene_beats: dict[int, str]) -> list[str]:
    lines: list[str] = []
    for scene_num in sorted(scene_beats):
        lines.append(f"Screen {scene_num}: {scene_beats[scene_num]}")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_path", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    markdown_path = args.markdown_path.expanduser().resolve()
    output_path = (args.output.expanduser().resolve() if args.output else default_output_path(markdown_path))

    scene_beats = extract_scene_beats(markdown_path)
    if not scene_beats:
        raise SystemExit(f"No scene beats found in {markdown_path}")

    lines = build_screen_script_lines(scene_beats)
    body = "\n".join(lines) + "\n"

    if args.dry_run:
        print(body, end="")
        return 0

    output_path.write_text(body, encoding="utf-8")
    print(f"Wrote screen script: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
