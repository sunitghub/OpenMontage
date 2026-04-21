"""Sync scene-beat captions from a Shorts markdown package into edit_decisions.

This keeps the markdown package as the editorial source of truth by reading each
scene's `Script beat` and rebuilding `captions` in the matching edit_decisions
artifact using the scene cut timings.
"""

from __future__ import annotations

import argparse
import json
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


def tokenize(text: str) -> list[str]:
    return text.strip().split()


def build_captions(edit_decisions: dict, scene_beats: dict[int, str]) -> list[dict[str, int | str]]:
    captions: list[dict[str, int | str]] = []
    cuts = edit_decisions.get("cuts", [])

    for cut in cuts:
        cut_id = cut.get("id", "")
        match = re.match(r"scene-(\d+)", cut_id)
        if not match:
            continue
        scene_num = int(match.group(1))
        beat = scene_beats.get(scene_num)
        if not beat:
            continue

        words = tokenize(beat)
        if not words:
            continue

        start_ms = round(float(cut["in_seconds"]) * 1000)
        end_ms = round(float(cut["out_seconds"]) * 1000)
        total_ms = max(1, end_ms - start_ms)

        for idx, word in enumerate(words):
            word_start = round(start_ms + (total_ms * idx) / len(words))
            word_end = round(start_ms + (total_ms * (idx + 1)) / len(words))
            captions.append({"word": word, "startMs": word_start, "endMs": word_end})

    return captions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_path", type=Path)
    parser.add_argument("edit_decisions_path", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    markdown_path = args.markdown_path.expanduser().resolve()
    edit_path = args.edit_decisions_path.expanduser().resolve()

    scene_beats = extract_scene_beats(markdown_path)
    if not scene_beats:
        raise SystemExit(f"No scene beats found in {markdown_path}")

    edit_decisions = json.loads(edit_path.read_text(encoding="utf-8"))
    captions = build_captions(edit_decisions, scene_beats)
    if not captions:
        raise SystemExit("No captions were generated from the scene beats")

    edit_decisions["captions"] = captions
    edit_decisions.setdefault("metadata", {})
    edit_decisions["metadata"]["captions_source"] = str(markdown_path)
    edit_decisions["metadata"]["captions_mode"] = "scene-script-beat-sync"

    if args.dry_run:
        print(json.dumps({"scene_beats": scene_beats, "captions_preview": captions[:12]}, indent=2))
        return 0

    edit_path.write_text(json.dumps(edit_decisions, indent=2) + "\n", encoding="utf-8")
    print(f"Updated captions in {edit_path} from scene beats in {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
