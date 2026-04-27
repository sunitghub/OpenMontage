"""Ingest screenshots into a Screen-Script.md or append scenes to an existing markdown.

Supports:
  - Folder of images → Screen-Script.md (batch mode)
  - Single image → append/update a named scene in an existing markdown (scene mode)
  - HEIC/HEIF via macOS sips conversion (no extra deps)
  - OCR engine choice: easyocr (default, better for photos/scans) or tesseract
  - Optional LLM cleanup pass via Claude Haiku (ANTHROPIC_API_KEY required)
  - Hindi translation via deep-translator (optional)

Usage:
    # Batch: folder → new Screen-Script.md
    python -m tools.ingest.screen_to_script \\
        --screenshots /path/to/imgs --project "My-Project" --type shorts

    # Single file → append Scene-1 to existing markdown, with LLM cleanup
    python -m tools.ingest.screen_to_script \\
        --image /path/to/Sceen-1.HEIC \\
        --append-to /path/to/Baglamukchi-Anubhav.md \\
        --scene 1 --cleanup
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ResumeSupport,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".heic", ".heif"}
SHORTS_DIR = Path(__file__).resolve().parent.parent.parent / "Design-Docs" / "ToPublish" / "Shorts"

_CLEANUP_PROMPT = """\
The text below was extracted by OCR from a photographed or scanned page. \
The reading order is scrambled and there are OCR artifacts (split words, stray characters, \
broken sentences). Reconstruct the original text as clean, readable prose paragraphs. \
Preserve the author's exact words wherever recognisable — do not paraphrase or summarise. \
Remove only OCR noise (repeated characters, isolated punctuation, garbled fragments). \
Return only the cleaned text, no commentary.

OCR TEXT:
{raw}"""


class ScreenToScript(BaseTool):
    name = "screen_to_script"
    version = "0.3.0"
    tier = ToolTier.SOURCE
    capability = "ingest"
    provider = "easyocr"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.LOCAL

    dependencies = ["python:easyocr"]
    install_instructions = (
        "pip install easyocr            # OCR engine (default)\n"
        "pip install pytesseract pillow # alternative OCR engine\n"
        "pip install anthropic          # optional: --cleanup LLM pass\n"
        "pip install deep-translator    # optional: --hindi translation\n"
        "HEIC: built-in via macOS sips (no install needed)\n"
        "Cleanup: set ANTHROPIC_API_KEY in .env"
    )
    agent_skills = []

    best_for = [
        "Converting screenshot sequences into Screen-Script.md",
        "Appending a single OCR'd scene into an existing video markdown",
        "Scanned/photographed book pages with LLM cleanup",
        "HEIC/HEIF screenshots from iPhone/iPad",
        "English OCR + optional Hindi translation for gen-voice pipeline",
    ]

    input_schema = {
        "type": "object",
        "properties": {
            "screenshots_dir": {"type": "string", "description": "Folder of images (batch mode)"},
            "image": {"type": "string", "description": "Single image file (scene mode)"},
            "project_name": {"type": "string", "description": "Project name for output folder (batch mode)"},
            "video_type": {"type": "string", "enum": ["shorts", "video"], "default": "shorts"},
            "translate_hindi": {"type": "boolean", "default": False},
            "output_dir": {"type": "string", "description": "Override output folder (batch mode)"},
            "append_to": {"type": "string", "description": "Existing markdown to append/update (scene mode)"},
            "scene_number": {"type": "integer", "description": "Scene label number (scene mode, default: auto)"},
            "engine": {"type": "string", "enum": ["easyocr", "tesseract"], "default": "easyocr"},
            "cleanup": {"type": "boolean", "default": False, "description": "Run Claude Haiku cleanup on raw OCR text"},
        },
    }

    output_schema = {
        "type": "object",
        "properties": {
            "script_path": {"type": "string"},
            "hindi_script_path": {"type": "string"},
            "screen_count": {"type": "integer"},
            "extracted_text": {"type": "string"},
            "cleaned_text": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=2, ram_mb=2000, disk_mb=200, network_required=False)
    retry_policy = RetryPolicy(max_retries=1, retryable_errors=["RuntimeError"])
    resume_support = ResumeSupport.FROM_START
    idempotency_key_fields = ["screenshots_dir", "image", "append_to", "scene_number"]
    side_effects = ["may create project folder", "writes or appends to markdown file"]

    def get_status(self) -> ToolStatus:
        try:
            import easyocr  # noqa: F401
            return ToolStatus.AVAILABLE
        except ImportError:
            try:
                import pytesseract  # noqa: F401
                return ToolStatus.DEGRADED
            except ImportError:
                return ToolStatus.UNAVAILABLE

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        t0 = time.time()
        if "image" in inputs:
            return self._scene_mode(inputs, t0)
        elif "screenshots_dir" in inputs:
            return self._batch_mode(inputs, t0)
        else:
            return ToolResult(success=False, error="Provide 'image' (scene mode) or 'screenshots_dir' (batch mode)")

    # ── scene mode ────────────────────────────────────────────────────────

    def _scene_mode(self, inputs: dict[str, Any], t0: float) -> ToolResult:
        image = Path(inputs["image"])
        if not image.exists():
            return ToolResult(success=False, error=f"Image not found: {image}")

        engine = inputs.get("engine", "easyocr")
        do_cleanup = inputs.get("cleanup", False)

        reader = self._get_reader(engine)
        ocr_path = _ensure_readable(image)
        try:
            raw = reader(ocr_path)
        finally:
            if ocr_path != image:
                ocr_path.unlink(missing_ok=True)

        raw_cleaned = _clean(raw)
        if not raw_cleaned:
            return ToolResult(success=False, error=f"No text extracted from {image.name}")

        result_data: dict[str, Any] = {"extracted_text": raw_cleaned}
        final_text = raw_cleaned

        if do_cleanup:
            try:
                final_text = _llm_cleanup(raw_cleaned)
                result_data["cleaned_text"] = final_text
                print(f"[screen_to_script] LLM cleanup done ({len(raw_cleaned)} → {len(final_text)} chars)")
            except Exception as e:
                print(f"[screen_to_script] cleanup failed: {e} — using raw OCR")

        artifacts: list[str] = []
        if "append_to" in inputs:
            md_path = Path(inputs["append_to"])
            scene_num = inputs.get("scene_number") or _next_scene_number(md_path)
            _append_scene(md_path, scene_num, final_text)
            result_data["script_path"] = str(md_path)
            result_data["scene_number"] = scene_num
            artifacts.append(str(md_path))
            print(f"[screen_to_script] Scene-{scene_num} → {md_path}")
        else:
            print(f"[screen_to_script] extracted:\n{final_text}")

        return ToolResult(
            success=True,
            data=result_data,
            artifacts=artifacts,
            duration_seconds=round(time.time() - t0, 1),
        )

    # ── batch mode ────────────────────────────────────────────────────────

    def _batch_mode(self, inputs: dict[str, Any], t0: float) -> ToolResult:
        screenshots_dir = Path(inputs["screenshots_dir"])
        project_name = inputs.get("project_name", screenshots_dir.name)
        video_type = inputs.get("video_type", "shorts")
        translate_hindi = inputs.get("translate_hindi", False)
        engine = inputs.get("engine", "easyocr")
        do_cleanup = inputs.get("cleanup", False)

        if not screenshots_dir.is_dir():
            return ToolResult(success=False, error=f"screenshots_dir not found: {screenshots_dir}")

        images = sorted(p for p in screenshots_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
        if not images:
            return ToolResult(success=False, error=f"No images found in {screenshots_dir}")

        project_dir = Path(inputs["output_dir"]) if "output_dir" in inputs else SHORTS_DIR / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        lines = self._ocr_images(images, engine, do_cleanup)
        if not lines:
            return ToolResult(success=False, error="OCR returned no text from any image")

        script_path = project_dir / "Screen-Script.md"
        _write_screen_script(script_path, lines, video_type)
        artifacts = [str(script_path)]
        result_data: dict[str, Any] = {
            "script_path": str(script_path),
            "screen_count": len(lines),
            "project_dir": str(project_dir),
            "video_type": video_type,
        }

        if translate_hindi:
            hindi_lines = _translate_to_hindi(lines)
            hindi_path = project_dir / "Screen-Script-Hindi.md"
            _write_screen_script(hindi_path, hindi_lines, video_type)
            artifacts.append(str(hindi_path))
            result_data["hindi_script_path"] = str(hindi_path)

        return ToolResult(
            success=True,
            data=result_data,
            artifacts=artifacts,
            duration_seconds=round(time.time() - t0, 1),
        )

    def _ocr_images(self, images: list[Path], engine: str, do_cleanup: bool) -> list[str]:
        reader = self._get_reader(engine)
        lines: list[str] = []
        for img in images:
            ocr_path = _ensure_readable(img)
            try:
                raw = reader(ocr_path)
            finally:
                if ocr_path != img:
                    ocr_path.unlink(missing_ok=True)
            text = _clean(raw)
            if not text:
                print(f"[screen_to_script] warning: no text from {img.name}")
                continue
            if do_cleanup:
                try:
                    text = _llm_cleanup(text)
                except Exception as e:
                    print(f"[screen_to_script] cleanup failed for {img.name}: {e}")
            lines.append(text)
        return lines

    def _get_reader(self, engine: str = "easyocr"):
        if engine == "tesseract":
            try:
                import pytesseract
                from PIL import Image as PILImage

                def read_tesseract(img: Path) -> str:
                    return pytesseract.image_to_string(PILImage.open(img))

                return read_tesseract
            except ImportError:
                raise RuntimeError("pytesseract not installed. Run: pip install pytesseract pillow")

        # easyocr (default)
        try:
            import easyocr
            _reader = easyocr.Reader(["en"], gpu=False, verbose=False)

            def read_easyocr(img: Path) -> str:
                results = _reader.readtext(str(img), detail=0, paragraph=True)
                return " ".join(results)

            return read_easyocr
        except ImportError:
            raise RuntimeError("easyocr not installed. Run: pip install easyocr")


# ── LLM cleanup ───────────────────────────────────────────────────────────

def _llm_cleanup(raw: str) -> str:
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set — add it to .env")

    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": _CLEANUP_PROMPT.format(raw=raw)}],
    )
    return msg.content[0].text.strip()


# ── HEIC handling ─────────────────────────────────────────────────────────

def _ensure_readable(img: Path) -> Path:
    if img.suffix.lower() not in {".heic", ".heif"}:
        return img
    try:
        import pillow_heif
        from PIL import Image as PILImage
        pillow_heif.register_heif_opener()
        tmp = Path(tempfile.mktemp(suffix=".png"))
        PILImage.open(img).save(tmp)
        return tmp
    except ImportError:
        pass
    if shutil.which("sips"):
        tmp = Path(tempfile.mktemp(suffix=".png"))
        subprocess.run(
            ["sips", "-s", "format", "png", str(img), "--out", str(tmp)],
            check=True, capture_output=True,
        )
        return tmp
    raise RuntimeError("Cannot decode HEIC: install pillow-heif or run on macOS (sips).")


# ── markdown helpers ───────────────────────────────────────────────────────

def _next_scene_number(md_path: Path) -> int:
    if not md_path.exists() or not md_path.stat().st_size:
        return 1
    matches = re.findall(r"^Scene-(\d+):", md_path.read_text(encoding="utf-8"), re.MULTILINE)
    return max((int(m) for m in matches), default=0) + 1


def _append_scene(md_path: Path, scene_num: int, text: str) -> None:
    existing = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
    scene_line = f"Scene-{scene_num}: {text}\n"
    pattern = re.compile(rf"^Scene-{scene_num}:.*$", re.MULTILINE)
    if pattern.search(existing):
        md_path.write_text(pattern.sub(scene_line.rstrip(), existing), encoding="utf-8")
    else:
        sep = "\n" if existing and not existing.endswith("\n\n") else ""
        md_path.write_text(existing + sep + scene_line, encoding="utf-8")


def _clean(text: str) -> str:
    text = text.strip()
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"(?m)^[\s\-•·|…]+$", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()
    text = re.sub(r"\n+", " ", text).strip()
    return text


def _write_screen_script(path: Path, lines: list[str], video_type: str) -> None:
    header = f"<!-- type: {video_type} -->\n"
    body = "\n".join(f"Screen {i}: {line}" for i, line in enumerate(lines, 1))
    path.write_text(header + body + "\n", encoding="utf-8")


def _translate_to_hindi(lines: list[str]) -> list[str]:
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        raise RuntimeError("pip install deep-translator")
    translator = GoogleTranslator(source="en", target="hi")
    result = []
    for line in lines:
        try:
            result.append(translator.translate(line) or line)
        except Exception as e:
            print(f"[screen_to_script] translation error: {e} — keeping English")
            result.append(line)
    return result


# ── CLI ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import sys

    ap = argparse.ArgumentParser(description="OCR screenshots → Screen-Script.md or scene append")
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--screenshots", metavar="DIR", help="Folder of images (batch mode)")
    grp.add_argument("--image", metavar="FILE", help="Single image (scene mode)")
    ap.add_argument("--project", help="Project name (batch mode)")
    ap.add_argument("--type", dest="video_type", choices=["shorts", "video"], default="shorts")
    ap.add_argument("--hindi", action="store_true")
    ap.add_argument("--out", help="Override output directory (batch mode)")
    ap.add_argument("--append-to", dest="append_to", metavar="MD", help="Markdown to append scene into (scene mode)")
    ap.add_argument("--scene", dest="scene_number", type=int, help="Scene number (default: auto)")
    ap.add_argument("--engine", choices=["easyocr", "tesseract"], default="easyocr")
    ap.add_argument("--cleanup", action="store_true", help="LLM cleanup via Claude Haiku (needs ANTHROPIC_API_KEY)")
    args = ap.parse_args()

    inputs: dict[str, Any] = {
        "video_type": args.video_type,
        "translate_hindi": args.hindi,
        "engine": args.engine,
        "cleanup": args.cleanup,
    }
    if args.image:
        inputs["image"] = args.image
        if args.append_to:
            inputs["append_to"] = args.append_to
        if args.scene_number:
            inputs["scene_number"] = args.scene_number
    else:
        inputs["screenshots_dir"] = args.screenshots
        if args.project:
            inputs["project_name"] = args.project
        if args.out:
            inputs["output_dir"] = args.out

    tool = ScreenToScript()
    result = tool.execute(inputs)
    if result.success:
        if "script_path" in result.data:
            print(f"[screen_to_script] → {result.data['script_path']}")
        elif "extracted_text" in result.data:
            print(result.data.get("cleaned_text") or result.data["extracted_text"])
    else:
        print(f"[screen_to_script] error: {result.error}", file=sys.stderr)
        sys.exit(1)
