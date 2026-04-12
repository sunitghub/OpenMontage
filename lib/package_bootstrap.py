from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from schemas.artifacts import validate_artifact


REPO_ROOT = Path(__file__).resolve().parent.parent
SHORTS_ROOT = REPO_ROOT / "Design-Docs" / "ToPublish" / "Shorts"


class PackageBootstrapError(ValueError):
    """Raised when a markdown package cannot be bootstrapped safely."""


@dataclass
class PackageData:
    markdown_path: Path
    package_dir: Path
    slug: str
    title: str
    overview: dict[str, str]
    script_sections: list[dict[str, Any]]
    scenes: list[dict[str, Any]]
    visual_lock: dict[str, str]
    production_notes: dict[str, str]


def bootstrap_package(markdown_path: str | Path, *, force: bool = False) -> dict[str, Any]:
    md_path = Path(markdown_path).expanduser().resolve()
    package = parse_package_markdown(md_path)

    project_dir = REPO_ROOT / "projects" / package.slug
    package_collisions = _find_existing_outputs(package.package_dir)
    project_collisions = _find_existing_outputs(project_dir)
    collisions = package_collisions + project_collisions
    if collisions and not force:
        collision_text = "\n".join(f"- {path}" for path in collisions)
        raise PackageBootstrapError(
            "Existing package/project artifacts found. Refusing to overwrite without --force:\n"
            f"{collision_text}"
        )

    artifacts_dir = project_dir / "artifacts"
    images_dir = project_dir / "assets" / "images"
    video_dir = project_dir / "assets" / "video"
    audio_dir = project_dir / "assets" / "audio"
    music_dir = project_dir / "assets" / "music"
    renders_dir = project_dir / "renders"
    for directory in (artifacts_dir, images_dir, video_dir, audio_dir, music_dir, renders_dir):
        directory.mkdir(parents=True, exist_ok=True)

    script_artifact = _build_script_artifact(package)
    scene_plan_artifact = _build_scene_plan_artifact(package)
    validate_artifact("script", script_artifact)
    validate_artifact("scene_plan", scene_plan_artifact)

    script_path = artifacts_dir / "script.json"
    scene_plan_path = artifacts_dir / "scene_plan.json"
    package_link_path = artifacts_dir / "package_bootstrap.json"

    script_path.write_text(json.dumps(script_artifact, indent=2) + "\n")
    scene_plan_path.write_text(json.dumps(scene_plan_artifact, indent=2) + "\n")
    package_link_path.write_text(
        json.dumps(
            {
                "version": "1.0",
                "slug": package.slug,
                "markdown_path": str(package.markdown_path),
                "package_dir": str(package.package_dir),
                "project_dir": str(project_dir),
            },
            indent=2,
        )
        + "\n"
    )

    return {
        "slug": package.slug,
        "project_dir": str(project_dir),
        "markdown_path": str(package.markdown_path),
        "artifacts_written": [
            str(script_path),
            str(scene_plan_path),
            str(package_link_path),
        ],
        "existing_outputs_detected": [str(path) for path in collisions],
    }


def generate_scene_videos(
    markdown_path: str | Path,
    *,
    preferred_provider: str = "auto",
    model: str | None = None,
    force: bool = False,
    resume: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    package = parse_package_markdown(markdown_path)
    project_dir = _ensure_bootstrapped_project(package)
    video_dir = project_dir / "assets" / "video"
    video_dir.mkdir(parents=True, exist_ok=True)

    planned_outputs: list[tuple[dict[str, Any], Path]] = []
    existing_outputs: list[Path] = []
    for index, scene in enumerate(package.scenes):
        filename = scene["output"] or f"scene-{index + 1:02d}.mp4"
        output_path = video_dir / filename
        planned_outputs.append((scene, output_path))
        if output_path.exists():
            existing_outputs.append(output_path)

    if existing_outputs and not (force or resume or dry_run):
        collision_text = "\n".join(f"- {path}" for path in existing_outputs)
        raise PackageBootstrapError(
            "Scene outputs already exist. Use --resume to skip them or --force to regenerate:\n"
            f"{collision_text}"
        )

    selector = _get_video_selector()
    results: list[dict[str, Any]] = []
    asset_entries: list[dict[str, Any]] = []

    for index, (scene, output_path) in enumerate(planned_outputs):
        scene_id = f"scene-{index + 1:02d}"
        if output_path.exists() and resume and not force:
            asset_entries.append(_asset_entry_from_existing(scene_id, scene, output_path))
            results.append(
                {
                    "scene_id": scene_id,
                    "status": "skipped_existing",
                    "output_path": str(output_path),
                }
            )
            continue

        selector_inputs: dict[str, Any] = {
            "prompt": scene["prompt"],
            "preferred_provider": preferred_provider,
            "operation": "text_to_video",
            "aspect_ratio": package.overview.get("Aspect Ratio", "").strip("` ") or "9:16",
            "duration": _duration_string(scene["duration_seconds"]),
            "output_path": str(output_path),
            "task_context": {
                "format": package.overview.get("Format", "").strip("` "),
                "series": package.overview.get("Series", "").strip("` "),
                "goal": package.overview.get("Primary Goal", "").strip("` "),
            },
        }
        if model:
            selector_inputs["model"] = model
            selector_inputs["model_variant"] = model

        if dry_run:
            results.append(
                {
                    "scene_id": scene_id,
                    "status": "planned",
                    "provider": preferred_provider,
                    "output_path": str(output_path),
                    "prompt": scene["prompt"],
                }
            )
            continue

        result = selector.execute(selector_inputs)
        if not result.success:
            raise PackageBootstrapError(
                f"Scene generation failed for {scene_id}: {result.error or 'unknown error'}"
            )

        asset_entries.append(_asset_entry_from_result(scene_id, scene, output_path, result))
        results.append(
            {
                "scene_id": scene_id,
                "status": "generated",
                "provider": result.data.get("selected_provider", result.data.get("provider")),
                "tool": result.data.get("selected_tool"),
                "model": result.model or result.data.get("model"),
                "output_path": str(output_path),
                "cost_usd": result.cost_usd,
            }
        )

    if not dry_run:
        asset_manifest = {
            "version": "1.0",
            "assets": asset_entries,
            "total_cost_usd": round(sum(entry.get("cost_usd", 0.0) for entry in asset_entries), 4),
            "metadata": {
                "source_markdown": str(package.markdown_path),
                "preferred_provider": preferred_provider,
            },
        }
        validate_artifact("asset_manifest", asset_manifest)
        asset_manifest_path = project_dir / "artifacts" / "asset_manifest.json"
        asset_manifest_path.write_text(json.dumps(asset_manifest, indent=2) + "\n")
    else:
        asset_manifest_path = None

    return {
        "slug": package.slug,
        "project_dir": str(project_dir),
        "preferred_provider": preferred_provider,
        "model": model,
        "dry_run": dry_run,
        "asset_manifest_path": str(asset_manifest_path) if asset_manifest_path else None,
        "results": results,
    }


def parse_package_markdown(markdown_path: str | Path) -> PackageData:
    md_path = Path(markdown_path).expanduser().resolve()
    if not md_path.exists():
        raise PackageBootstrapError(f"Markdown package not found: {md_path}")
    if md_path.suffix.lower() != ".md":
        raise PackageBootstrapError(f"Expected a markdown file, got: {md_path}")
    if SHORTS_ROOT not in md_path.parents:
        raise PackageBootstrapError(
            f"Markdown package must live under {SHORTS_ROOT}, got: {md_path}"
        )

    text = md_path.read_text()
    title = _extract_h1(text)
    overview = _parse_definition_block(_get_section(text, "Overview"))
    script_sections = _parse_script_sections(_get_section(text, "Script"))
    scenes = _parse_scenes(_get_section(text, "Scenes"))
    visual_lock = _parse_definition_block(_get_section(text, "Visual And Brand Lock"))
    production_notes = _parse_definition_block(_get_section(text, "Production Notes"))

    slug = overview.get("Slug", "").strip("` ")
    if not slug:
        raise PackageBootstrapError("Overview must include a Slug field.")
    if slug != md_path.stem:
        raise PackageBootstrapError(
            f"Slug/file mismatch: overview slug {slug!r} does not match file name {md_path.stem!r}"
        )
    if md_path.parent.name != slug:
        raise PackageBootstrapError(
            f"Slug/folder mismatch: overview slug {slug!r} does not match folder name {md_path.parent.name!r}"
        )
    if not script_sections:
        raise PackageBootstrapError("Script section is required and must include content.")
    if not scenes:
        raise PackageBootstrapError("Scenes section is required and must include at least one scene.")

    return PackageData(
        markdown_path=md_path,
        package_dir=md_path.parent,
        slug=slug,
        title=title,
        overview=overview,
        script_sections=script_sections,
        scenes=scenes,
        visual_lock=visual_lock,
        production_notes=production_notes,
    )


def _build_script_artifact(package: PackageData) -> dict[str, Any]:
    total_duration = _script_total_duration(package)
    sections = []
    current_start = 0.0
    word_counts = [_word_count(section["text"]) for section in package.script_sections]
    total_words = sum(word_counts) or len(package.script_sections)

    for index, section in enumerate(package.script_sections):
        fraction = (word_counts[index] or 1) / total_words
        duration = round(total_duration * fraction, 2)
        if index == len(package.script_sections) - 1:
            end = float(total_duration)
        else:
            end = round(current_start + duration, 2)
        sections.append(
            {
                "id": f"s{index + 1}",
                "label": section["label"],
                "text": section["text"],
                "start_seconds": round(current_start, 2),
                "end_seconds": round(end, 2),
                "speaker_directions": _default_speaker_direction(section["label"]),
                "enhancement_cues": [
                    {
                        "type": "animation",
                        "description": _matching_scene_description(package.scenes, section["label"]),
                        "timestamp_seconds": round(current_start, 2),
                    }
                ],
            }
        )
        current_start = end

    artifact = {
        "version": "1.0",
        "title": package.title,
        "total_duration_seconds": float(total_duration),
        "sections": sections,
        "metadata": {
            "source_markdown": str(package.markdown_path),
            "style_playbook": "blissful-chants",
            "format": package.overview.get("Format", "").strip("` "),
            "series": package.overview.get("Series", "").strip("` "),
            "primary_goal": package.overview.get("Primary Goal", "").strip("` "),
            "status": package.overview.get("Status", "").strip("` "),
        },
    }
    return artifact


def _build_scene_plan_artifact(package: PackageData) -> dict[str, Any]:
    script_id_map = {
        section["label"].lower(): f"s{idx + 1}"
        for idx, section in enumerate(package.script_sections)
    }

    current_start = 0.0
    scenes = []
    for index, scene in enumerate(package.scenes):
        duration = scene["duration_seconds"]
        end = round(current_start + duration, 2)
        scene_id = f"scene-{index + 1:02d}"
        scene_type = "text_card" if "title card" in scene["visual"].lower() else "generated"
        scenes.append(
            {
                "id": scene_id,
                "type": scene_type,
                "description": scene["visual"],
                "start_seconds": round(current_start, 2),
                "end_seconds": end,
                "script_section_id": _script_section_for_scene(scene, script_id_map),
                "framing": scene["camera"],
                "movement": scene["motion"],
                "transition_in": "fade" if index == 0 else "dissolve",
                "transition_out": "fade" if index == len(package.scenes) - 1 else "dissolve",
                "overlay_notes": scene.get("text overlay", ""),
                "shot_language": _shot_language_from_scene(scene),
                "shot_intent": scene["purpose"],
                "narrative_role": _narrative_role_from_scene(scene["purpose"]),
                "information_role": scene["script beat"],
                "hero_moment": index in {0, len(package.scenes) - 1},
                "texture_keywords": _texture_keywords(package, scene),
                "required_assets": [
                    {
                        "type": "video",
                        "description": scene["visual"],
                        "source": "generate",
                    }
                ],
            }
        )
        current_start = end

    return {
        "version": "1.0",
        "style_playbook": "blissful-chants",
        "scenes": scenes,
        "metadata": {
            "animation_mode": "clip_video",
            "renderer_family": "animation-first",
            "source_markdown": str(package.markdown_path),
            "provider_preference": package.production_notes.get("First provider to test", "").strip("` "),
            "negative_constraints": package.visual_lock.get("Negative constraints", ""),
        },
    }


def _find_existing_outputs(base_dir: Path) -> list[Path]:
    if not base_dir.exists():
        return []
    collisions: list[Path] = []
    for relative in ("artifacts", "assets", "renders"):
        target = base_dir / relative
        if target.exists():
            for path in sorted(target.rglob("*")):
                if path.is_file():
                    collisions.append(path)
    return collisions


def _ensure_bootstrapped_project(package: PackageData) -> Path:
    project_dir = REPO_ROOT / "projects" / package.slug
    script_path = project_dir / "artifacts" / "script.json"
    scene_plan_path = project_dir / "artifacts" / "scene_plan.json"
    if script_path.exists() and scene_plan_path.exists():
        return project_dir
    bootstrap_package(package.markdown_path)
    return project_dir


def _get_video_selector():
    from tools.video.video_selector import VideoSelector

    return VideoSelector()


def _extract_h1(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if not match:
        raise PackageBootstrapError("Markdown package must start with an H1 title.")
    return match.group(1).strip()


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
    if not buffer and heading not in text:
        raise PackageBootstrapError(f"Missing required section: {heading}")
    return "\n".join(buffer).strip()


def _parse_definition_block(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        bullet_match = re.match(r"^\s*-\s+([^:]+):\s*(.*)$", line)
        if bullet_match:
            if current_key is not None:
                result[current_key] = "\n".join(v for v in current_value if v).strip()
            current_key = bullet_match.group(1).strip()
            current_value = [bullet_match.group(2).strip()]
            continue
        if current_key is not None and (line.startswith("  ") or line.startswith("\t")):
            current_value.append(line.strip())
    if current_key is not None:
        result[current_key] = "\n".join(v for v in current_value if v).strip()
    return result


def _parse_script_sections(text: str) -> list[dict[str, str]]:
    sections = []
    for heading, body in _split_level_three_sections(text):
        cleaned = " ".join(line.strip() for line in body.splitlines() if line.strip())
        if cleaned:
            sections.append({"label": heading, "text": cleaned})
    return sections


def _parse_scenes(text: str) -> list[dict[str, Any]]:
    scenes = []
    for heading, body in _split_level_three_sections(text):
        data = _parse_definition_block(body)
        duration_text = data.get("Duration", "")
        duration_seconds = _parse_duration_seconds(duration_text)
        scenes.append(
            {
                "heading": heading,
                "purpose": data.get("Purpose", ""),
                "script beat": data.get("Script beat", "").strip("` "),
                "duration_seconds": duration_seconds,
                "visual": data.get("Visual", ""),
                "camera": data.get("Camera", ""),
                "motion": data.get("Motion", ""),
                "text overlay": data.get("Text overlay", "").strip("` "),
                "prompt": data.get("Prompt", ""),
                "reference asset": data.get("Reference asset", "").strip("` "),
                "output": data.get("Output", "").strip("` "),
            }
        )
    return scenes


def _split_level_three_sections(text: str) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    current_heading: str | None = None
    current_lines: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if match:
            if current_heading is not None:
                results.append((current_heading, "\n".join(current_lines).strip()))
            current_heading = match.group(1).strip()
            current_lines = []
            continue
        if current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        results.append((current_heading, "\n".join(current_lines).strip()))
    return results


def _parse_duration_seconds(value: str) -> float:
    numbers = re.findall(r"\d+(?:\.\d+)?", value)
    if not numbers:
        raise PackageBootstrapError(f"Could not parse scene duration from: {value!r}")
    return float(numbers[-1])


def _duration_string(seconds: float) -> str:
    if float(seconds).is_integer():
        return str(int(seconds))
    return f"{seconds:.2f}".rstrip("0").rstrip(".")


def _script_total_duration(package: PackageData) -> int:
    if package.scenes:
        return int(round(sum(scene["duration_seconds"] for scene in package.scenes)))
    target = package.overview.get("Target Duration", "")
    numbers = [float(num) for num in re.findall(r"\d+(?:\.\d+)?", target)]
    if numbers:
        return int(round(max(numbers)))
    return 60


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def _default_speaker_direction(label: str) -> str:
    mapping = {
        "Hook": "Immediate curiosity, devotional tone, clear emphasis on the opening line.",
        "Body": "Steady, informative, reverent delivery with short pauses between facts.",
        "Close": "Warm, reflective closing cadence.",
        "CTA": "Gentle and concise invitation, not pushy.",
    }
    return mapping.get(label, "Natural, clear delivery.")


def _matching_scene_description(scenes: list[dict[str, Any]], label: str) -> str:
    normalized = label.lower()
    if normalized == "hook" and scenes:
        return scenes[0]["visual"]
    if normalized == "close" and scenes:
        return scenes[-1]["visual"]
    if normalized == "cta" and scenes:
        return scenes[-1]["visual"]
    if normalized == "body" and len(scenes) > 2:
        return scenes[1]["visual"]
    return scenes[0]["visual"] if scenes else "Scene support visual."


def _script_section_for_scene(scene: dict[str, Any], script_id_map: dict[str, str]) -> str:
    purpose = scene["purpose"].lower()
    if "open" in purpose or "frame" in purpose:
        return script_id_map.get("hook", "s1")
    if "close" in purpose:
        return script_id_map.get("close", "s1")
    return script_id_map.get("body", "s1")


def _shot_language_from_scene(scene: dict[str, Any]) -> dict[str, Any]:
    camera = scene["camera"].lower()
    visual = scene["visual"].lower()
    shot_size = "medium"
    if "close-up" in visual or "close-up" in camera or "portrait" in visual:
        shot_size = "close_up"
    elif "full-body" in visual or "full body" in visual:
        shot_size = "medium_wide"
    elif "wide" in visual:
        shot_size = "wide"
    elif "title card" in visual:
        shot_size = "insert"

    movement = "static"
    if "push-in" in camera:
        movement = "dolly_in"
    elif "drift outward" in camera:
        movement = "dolly_out"
    elif "rise" in camera:
        movement = "crane_up"
    elif "lateral" in camera:
        movement = "tracking_right"
    elif "top-to-bottom" in camera:
        movement = "tilt_down"

    lighting = "rim_lit"
    if "cosmic" in visual:
        lighting = "volumetric"
    elif "indigo darkness" in visual or "darkness" in visual:
        lighting = "low_key"
    elif "title card" in visual:
        lighting = "silhouette"

    return {
        "shot_size": shot_size,
        "camera_movement": movement,
        "lens_mm": 50 if shot_size in {"close_up", "medium"} else 35,
        "lighting_key": lighting,
        "depth_of_field": "medium",
        "color_temperature": "mixed",
    }


def _narrative_role_from_scene(purpose: str) -> str:
    value = purpose.lower()
    if "open" in value or "frame" in value:
        return "establish_context"
    if "close" in value:
        return "call_to_action"
    if "deliver" in value:
        return "deliver_payload"
    return "emotional_beat"


def _texture_keywords(package: PackageData, scene: dict[str, Any]) -> list[str]:
    palette = package.visual_lock.get("Palette", "")
    keywords = [part.strip() for part in re.split(r",|\n", palette) if part.strip()]
    keywords.extend(
        [
            package.visual_lock.get("Style family", ""),
            package.visual_lock.get("Lighting", ""),
            scene["motion"],
        ]
    )
    return [keyword for keyword in keywords if keyword][:6]


def _asset_entry_from_result(
    scene_id: str,
    scene: dict[str, Any],
    output_path: Path,
    result: Any,
) -> dict[str, Any]:
    project_dir = output_path.parents[2]
    relative_path = output_path.relative_to(project_dir)
    return {
        "id": scene_id,
        "type": "video",
        "path": str(relative_path),
        "source_tool": result.data.get("selected_tool", result.data.get("provider", "video_selector")),
        "scene_id": scene_id,
        "prompt": scene["prompt"],
        "model": result.model or result.data.get("model"),
        "cost_usd": result.cost_usd,
        "duration_seconds": float(scene["duration_seconds"]),
        "format": "mp4",
        "subtype": "generated",
        "generation_summary": scene["visual"],
        "provider": result.data.get("selected_provider", result.data.get("provider")),
    }


def _asset_entry_from_existing(scene_id: str, scene: dict[str, Any], output_path: Path) -> dict[str, Any]:
    project_dir = output_path.parents[2]
    relative_path = output_path.relative_to(project_dir)
    return {
        "id": scene_id,
        "type": "video",
        "path": str(relative_path),
        "source_tool": "existing",
        "scene_id": scene_id,
        "prompt": scene["prompt"],
        "duration_seconds": float(scene["duration_seconds"]),
        "format": "mp4",
        "subtype": "generated",
        "generation_summary": scene["visual"],
        "provider": "existing",
    }
