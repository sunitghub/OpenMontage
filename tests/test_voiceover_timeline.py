from pathlib import Path

import pytest

from tools.base_tool import ToolResult
from tools.video.apply_voiceover_timeline import apply_voiceover_timeline
from tools.video.video_compose import VideoCompose


def test_final_render_requires_voiceover() -> None:
    tool = VideoCompose()

    result = tool._validate_voiceover_requirement(
        {"operation": "render"},
        {"cuts": [{"id": "scene-01", "in_seconds": 0, "out_seconds": 1}]},
    )

    assert result is not None
    assert not result.success
    assert "Voiceover is required" in result.error


def test_visual_preview_may_omit_voiceover() -> None:
    tool = VideoCompose()

    result = tool._validate_voiceover_requirement(
        {"operation": "render", "options": {"render_intent": "visual_preview"}},
        {"cuts": [{"id": "scene-01", "in_seconds": 0, "out_seconds": 1}]},
    )

    assert result is None


def test_apply_voiceover_timeline_updates_cuts_audio_and_captions(tmp_path: Path) -> None:
    voiceover = tmp_path / "voiceover.mp3"
    voiceover.write_bytes(b"fake")
    transcript_path = tmp_path / "transcript.json"

    edit_decisions = {
        "cuts": [
            {"id": "scene-01", "source": "a.mp4", "in_seconds": 0, "out_seconds": 5},
            {"id": "scene-02", "source": "b.mp4", "in_seconds": 5, "out_seconds": 10},
        ],
        "metadata": {"target_duration_seconds": 10},
    }
    transcript = {
        "duration_seconds": 8.0,
        "segments": [
            {"start": 0.2, "end": 2.5, "text": "one"},
            {"start": 2.5, "end": 5.5, "text": "two"},
            {"start": 5.5, "end": 8.0, "text": "three"},
        ],
        "word_timestamps": [
            {"word": "hello", "start": 0.2, "end": 0.7},
            {"word": "world", "start": 5.6, "end": 6.1},
        ],
    }

    updated = apply_voiceover_timeline(
        edit_decisions,
        transcript,
        voiceover,
        [1, 3],
        transcript_path,
    )

    assert updated["cuts"][0]["in_seconds"] == 0.0
    assert updated["cuts"][0]["out_seconds"] == 2.5
    assert updated["cuts"][1]["in_seconds"] == 2.5
    assert updated["cuts"][1]["out_seconds"] == 8.0
    assert updated["audio"]["narration"]["src"] == str(voiceover)
    assert updated["metadata"]["timeline_source"] == "voiceover_analysis"
    assert updated["metadata"]["captions_mode"] == "voiceover-word-timestamps"
    assert updated["captions"] == [
        {"word": "hello", "startMs": 200, "endMs": 700},
        {"word": "world", "startMs": 5600, "endMs": 6100},
    ]


def test_render_forwards_visual_preview_intent_to_remotion(monkeypatch: pytest.MonkeyPatch) -> None:
    tool = VideoCompose()

    monkeypatch.setattr(tool, "_pre_compose_validation", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(tool, "_needs_remotion", lambda _cuts: True)

    def fake_remotion_render(inputs: dict) -> ToolResult:
        assert inputs["options"]["render_intent"] == "visual_preview"
        return ToolResult(success=True, data={"checked": True})

    monkeypatch.setattr(tool, "_remotion_render", fake_remotion_render)

    result = tool._render({
        "operation": "render",
        "edit_decisions": {
            "renderer_family": "explainer-data",
            "cuts": [{"id": "scene-01", "source": "scene-01"}],
        },
        "asset_manifest": {"assets": [{"id": "scene-01", "path": "scene-01.png"}]},
        "options": {"render_intent": "visual_preview"},
    })

    assert result.success


def test_render_forwards_audio_path_to_remotion(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    tool = VideoCompose()
    voiceover = tmp_path / "voiceover.mp3"
    voiceover.write_bytes(b"fake")

    monkeypatch.setattr(tool, "_pre_compose_validation", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(tool, "_needs_remotion", lambda _cuts: True)

    def fake_remotion_render(inputs: dict) -> ToolResult:
        assert inputs["audio_path"] == str(voiceover)
        return ToolResult(success=True, data={"checked": True})

    monkeypatch.setattr(tool, "_remotion_render", fake_remotion_render)

    result = tool._render({
        "operation": "render",
        "edit_decisions": {
            "renderer_family": "explainer-data",
            "cuts": [{"id": "scene-01", "source": "scene-01"}],
        },
        "asset_manifest": {"assets": [{"id": "scene-01", "path": "scene-01.png"}]},
        "audio_path": str(voiceover),
    })

    assert result.success
