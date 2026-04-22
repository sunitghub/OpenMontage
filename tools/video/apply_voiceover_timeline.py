"""Apply voiceover-derived timing to an edit_decisions artifact.

The input transcript is the JSON produced by tools.analysis.transcriber. The
caller supplies scene end segment numbers after reviewing the transcript; this
keeps timing decisions tied to the real voiceover instead of fixed estimates.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_scene_end_segments(value: str) -> list[int]:
    try:
        segments = [int(part.strip()) for part in value.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("scene end segments must be comma-separated integers") from exc

    if not segments:
        raise argparse.ArgumentTypeError("at least one scene end segment is required")
    if any(segment < 1 for segment in segments):
        raise argparse.ArgumentTypeError("scene end segments are 1-based and must be positive")
    if segments != sorted(segments):
        raise argparse.ArgumentTypeError("scene end segments must be sorted ascending")
    if len(set(segments)) != len(segments):
        raise argparse.ArgumentTypeError("scene end segments must be unique")
    return segments


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_boundaries(
    segments: list[dict[str, Any]],
    scene_end_segments: list[int],
    duration_seconds: float,
) -> list[tuple[float, float]]:
    if scene_end_segments[-1] > len(segments):
        raise ValueError(
            f"scene end segment {scene_end_segments[-1]} exceeds transcript segment count {len(segments)}"
        )

    boundaries: list[tuple[float, float]] = []
    start = 0.0
    for idx, end_segment in enumerate(scene_end_segments):
        if idx == len(scene_end_segments) - 1:
            end = duration_seconds
        else:
            current_end = float(segments[end_segment - 1]["end"])
            next_start = float(segments[end_segment]["start"])
            # Keep inter-beat pauses with the scene that just spoke, so the
            # next visual starts when the next spoken beat begins.
            end = max(current_end, next_start)
        boundaries.append((round(start, 3), round(end, 3)))
        start = end

    return boundaries


def build_word_captions(transcript: dict[str, Any]) -> list[dict[str, int | str]]:
    captions: list[dict[str, int | str]] = []
    for word in transcript.get("word_timestamps", []):
        text = str(word.get("word", "")).strip()
        if not text:
            continue
        start = float(word["start"])
        end = float(word["end"])
        captions.append({
            "word": text,
            "startMs": round(start * 1000),
            "endMs": round(end * 1000),
        })
    return captions


def apply_voiceover_timeline(
    edit_decisions: dict[str, Any],
    transcript: dict[str, Any],
    voiceover_path: Path,
    scene_end_segments: list[int],
    transcript_path: Path,
) -> dict[str, Any]:
    cuts = edit_decisions.get("cuts") or []
    if not cuts:
        raise ValueError("edit_decisions has no cuts")
    if len(cuts) != len(scene_end_segments):
        raise ValueError(
            f"cut count ({len(cuts)}) must match scene end segment count ({len(scene_end_segments)})"
        )

    duration_seconds = float(transcript.get("duration_seconds") or 0)
    if duration_seconds <= 0:
        raise ValueError("transcript duration_seconds is missing or invalid")

    segments = transcript.get("segments") or []
    if not segments:
        raise ValueError("transcript has no segments")

    boundaries = build_boundaries(segments, scene_end_segments, duration_seconds)
    updated = json.loads(json.dumps(edit_decisions))

    for cut, (start, end) in zip(updated["cuts"], boundaries):
        cut["in_seconds"] = start
        cut["out_seconds"] = end

    updated.setdefault("audio", {})
    updated["audio"]["narration"] = {
        "src": str(voiceover_path),
        "volume": 1,
    }
    updated["voiceover"] = {
        "src": str(voiceover_path),
        "duration_seconds": round(duration_seconds, 3),
        "transcript": str(transcript_path),
    }
    updated["captions"] = build_word_captions(transcript)
    updated.setdefault("captionsConfig", {})
    updated["total_duration_seconds"] = round(duration_seconds, 3)
    updated.setdefault("metadata", {})
    updated["metadata"]["target_duration_seconds"] = round(duration_seconds, 3)
    updated["metadata"]["timeline_source"] = "voiceover_analysis"
    updated["metadata"]["voiceover_source"] = str(voiceover_path)
    updated["metadata"]["voiceover_transcript"] = str(transcript_path)
    updated["metadata"]["captions_source"] = str(transcript_path)
    updated["metadata"]["captions_mode"] = "voiceover-word-timestamps"
    updated["metadata"]["render_intent"] = "final"

    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edit_decisions_path", type=Path)
    parser.add_argument("transcript_path", type=Path)
    parser.add_argument("voiceover_path", type=Path)
    parser.add_argument("--scene-end-segments", required=True, type=parse_scene_end_segments)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    edit_path = args.edit_decisions_path.expanduser().resolve()
    transcript_path = args.transcript_path.expanduser().resolve()
    voiceover_path = args.voiceover_path.expanduser().resolve()
    output_path = (
        args.output.expanduser().resolve()
        if args.output
        else edit_path.with_name(f"{edit_path.stem}.voiceover.json")
    )

    if not voiceover_path.exists():
        raise SystemExit(f"Voiceover not found: {voiceover_path}")

    updated = apply_voiceover_timeline(
        load_json(edit_path),
        load_json(transcript_path),
        voiceover_path,
        args.scene_end_segments,
        transcript_path,
    )

    body = json.dumps(updated, indent=2, ensure_ascii=False) + "\n"
    if args.dry_run:
        print(body, end="")
        return 0

    output_path.write_text(body, encoding="utf-8")
    print(f"Wrote voiceover-timed edit decisions: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
