from __future__ import annotations

import json
from pathlib import Path

import pytest

from lib.package_bootstrap import (
    PackageBootstrapError,
    bootstrap_package,
    generate_scene_videos,
    parse_package_markdown,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_PATH = (
    REPO_ROOT
    / "Design-Docs"
    / "ToPublish"
    / "Shorts"
    / "Maa-Kali-5-Unknown-Facts"
    / "Maa-Kali-5-Unknown-Facts.md"
)


def test_parse_package_markdown_extracts_expected_fields() -> None:
    package = parse_package_markdown(PACKAGE_PATH)

    assert package.slug == "Maa-Kali-5-Unknown-Facts"
    assert package.title == "5 Unknown Facts About Maa Kali"
    assert package.overview["Format"] == "`Short`"
    assert len(package.script_sections) == 4
    assert len(package.scenes) == 8
    assert package.production_notes["First provider to test"] == "`Sora`"


def test_bootstrap_package_writes_pipeline_friendly_artifacts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("lib.package_bootstrap.REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        "lib.package_bootstrap.SHORTS_ROOT",
        PACKAGE_PATH.parents[1],
    )

    result = bootstrap_package(PACKAGE_PATH)

    project_dir = Path(result["project_dir"])
    script_path = project_dir / "artifacts" / "script.json"
    scene_plan_path = project_dir / "artifacts" / "scene_plan.json"

    assert script_path.exists()
    assert scene_plan_path.exists()

    script = json.loads(script_path.read_text())
    scene_plan = json.loads(scene_plan_path.read_text())

    assert script["title"] == "5 Unknown Facts About Maa Kali"
    assert script["total_duration_seconds"] == 52.0
    assert len(script["sections"]) == 4
    assert scene_plan["style_playbook"] == "blissful-chants"
    assert len(scene_plan["scenes"]) == 8
    assert scene_plan["metadata"]["provider_preference"] == "Sora"


def test_bootstrap_package_refuses_to_overwrite_existing_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_dir = tmp_path / "projects" / "Maa-Kali-5-Unknown-Facts"
    artifact_dir = project_dir / "artifacts"
    artifact_dir.mkdir(parents=True)
    (artifact_dir / "script.json").write_text("{}\n")

    monkeypatch.setattr("lib.package_bootstrap.REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        "lib.package_bootstrap.SHORTS_ROOT",
        PACKAGE_PATH.parents[1],
    )

    with pytest.raises(PackageBootstrapError, match="Refusing to overwrite"):
        bootstrap_package(PACKAGE_PATH)


def test_generate_scene_videos_dry_run_lists_planned_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("lib.package_bootstrap.REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        "lib.package_bootstrap.SHORTS_ROOT",
        PACKAGE_PATH.parents[1],
    )

    result = generate_scene_videos(
        PACKAGE_PATH,
        preferred_provider="sora",
        dry_run=True,
    )

    assert result["dry_run"] is True
    assert len(result["results"]) == 8
    assert result["results"][0]["provider"] == "sora"
    assert result["asset_manifest_path"] is None


def test_generate_scene_videos_uses_selector_and_writes_asset_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("lib.package_bootstrap.REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        "lib.package_bootstrap.SHORTS_ROOT",
        PACKAGE_PATH.parents[1],
    )

    class FakeSelector:
        def execute(self, inputs):
            output_path = Path(inputs["output_path"])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(b"fake-mp4")
            return type(
                "FakeResult",
                (),
                {
                    "success": True,
                    "data": {
                        "selected_tool": "sora_video",
                        "selected_provider": "sora",
                        "provider": "sora",
                        "model": "sora-2",
                    },
                    "cost_usd": 0.5,
                    "model": "sora-2",
                },
            )()

    monkeypatch.setattr("lib.package_bootstrap._get_video_selector", lambda: FakeSelector())

    result = generate_scene_videos(PACKAGE_PATH, preferred_provider="sora")

    asset_manifest_path = Path(result["asset_manifest_path"])
    assert asset_manifest_path.exists()
    asset_manifest = json.loads(asset_manifest_path.read_text())
    assert len(asset_manifest["assets"]) == 8
    assert asset_manifest["assets"][0]["provider"] == "sora"
    assert result["results"][0]["status"] == "generated"


def test_generate_scene_videos_refuses_existing_outputs_without_resume_or_force(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("lib.package_bootstrap.REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        "lib.package_bootstrap.SHORTS_ROOT",
        PACKAGE_PATH.parents[1],
    )

    bootstrap_package(PACKAGE_PATH)
    existing_output = (
        tmp_path
        / "projects"
        / "Maa-Kali-5-Unknown-Facts"
        / "assets"
        / "video"
        / "scene-01.mp4"
    )
    existing_output.parent.mkdir(parents=True, exist_ok=True)
    existing_output.write_bytes(b"existing")

    with pytest.raises(PackageBootstrapError, match="Scene outputs already exist"):
        generate_scene_videos(PACKAGE_PATH, preferred_provider="sora")
