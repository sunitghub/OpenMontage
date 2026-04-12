from __future__ import annotations

from pathlib import Path

from lib.shorts_workflow import (
    list_short_folders,
    render_light_short_markdown,
    upsert_results_section,
    validate_short_markdown,
)


def test_render_light_short_markdown_includes_results_section() -> None:
    markdown = render_light_short_markdown(
        "Maa-Kali-5-Unknown-Facts",
        {
            "title": "5 Unknown Facts About Maa Kali",
            "description": "A short devotional discovery piece.",
            "thumbnail_title": "5 Unknown Facts",
            "thumbnail_prompt": "Close-up portrait with title text.",
            "script": {
                "hook": "Hook line.",
                "body": "Body line.",
                "close": "Close line.",
            },
            "scenes": [
                {
                    "scene_number": 1,
                    "purpose": "Open strong",
                    "script_beat": "Hook line.",
                    "duration": "5s",
                    "visual": "Portrait",
                    "camera": "slow push-in",
                    "motion": "low",
                    "prompt": "Prompt text",
                }
            ],
        },
    )

    assert "## Results" in markdown
    assert "| 1 | Needs Generation |  |" in markdown
    assert "- Output: `scene-1.mp4`" in markdown


def test_upsert_results_section_replaces_existing_rows() -> None:
    source = """# Demo

## Results

| Scene | Status | DateTime |
|---|---|---|
| 1 | Needs Generation | |
"""
    updated = upsert_results_section(
        source,
        {
            1: {"status": "Checked", "datetime": "2026-04-12 10:00:00"},
            2: {"status": "Publishable", "datetime": "2026-04-12 10:05:00"},
        },
    )

    assert "| 1 | Checked | 2026-04-12 10:00:00 |" in updated
    assert "| 2 | Publishable | 2026-04-12 10:05:00 |" in updated
    assert updated.count("## Results") == 1


def test_validate_short_markdown_detects_expected_content(tmp_path: Path) -> None:
    folder = tmp_path / "Maa-Kali-5-Unknown-Facts"
    folder.mkdir()
    md_path = folder / "Maa-Kali-5-Unknown-Facts.md"
    md_path.write_text(
        """# 5 Unknown Facts About Maa Kali

## Title

5 Unknown Facts About Maa Kali

## Scenes

### Scene-1
- Purpose: Open
- Script beat: `Maa Kali reveals mystery`
- Duration: `5s`
- Visual: Close-up
- Camera: slow push-in
- Motion: low
- Prompt: Prompt

## Results

| Scene | Status | DateTime |
|---|---|---|
| 1 | Needs Generation | |
"""
    )

    result = validate_short_markdown(md_path, "Maa-Kali-5-Unknown-Facts")
    assert result["score"] > 0.5
    assert any("Scenes detected: 1" in message for message in result["messages"])


def test_list_short_folders_reports_composite_status(tmp_path: Path, monkeypatch) -> None:
    shorts_root = tmp_path / "Shorts"
    folder = shorts_root / "Maa-Kali-5-Unknown-Facts"
    folder.mkdir(parents=True)
    (folder / "Maa-Kali-5-Unknown-Facts.md").write_text("# Demo\n")
    (folder / "scene-1.mp4").write_bytes(b"fake")
    (folder / "Thumbnail.jpg").write_bytes(b"fake")

    monkeypatch.setattr("lib.shorts_workflow.SHORTS_ROOT", shorts_root)

    entries = list_short_folders()
    assert len(entries) == 1
    assert entries[0].status == "MD, MP4:1, Thumbnail"
