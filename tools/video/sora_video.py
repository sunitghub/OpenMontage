"""OpenAI Sora video generation via the Videos API."""

from __future__ import annotations

import mimetypes
import os
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class SoraVideo(BaseTool):
    name = "sora_video"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "sora"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set OPENAI_API_KEY to your OpenAI API key.\n"
        "The official Videos API docs currently note that Sora 2 and the Videos API "
        "are deprecated with shutdown scheduled for September 24, 2026."
    )
    agent_skills = ["openai-docs"]

    capabilities = ["text_to_video", "image_to_video", "reference_to_video"]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "reference_image": True,
        "vertical_video": True,
        "native_audio": True,
    }
    best_for = [
        "short scene-by-scene prototyping with OpenAI",
        "reference-guided Sora clips",
        "vertical devotional scenes when OpenAI access is already available",
    ]
    not_good_for = [
        "long-term production dependency without a migration plan",
        "offline generation",
    ]
    fallback_tools = ["kling_video", "veo_video", "minimax_video", "wan_video"]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video", "reference_to_video"],
                "default": "text_to_video",
            },
            "model": {
                "type": "string",
                "enum": ["sora-2", "sora-2-pro"],
                "default": "sora-2",
            },
            "model_variant": {
                "type": "string",
                "enum": ["sora-2", "sora-2-pro"],
                "default": "sora-2",
            },
            "duration": {
                "type": "string",
                "description": "Clip length in seconds, usually 2-20",
                "default": "5",
            },
            "aspect_ratio": {
                "type": "string",
                "enum": ["16:9", "9:16", "1:1"],
                "default": "16:9",
            },
            "size": {
                "type": "string",
                "description": "Explicit resolution, e.g. 1280x720 or 720x1280",
            },
            "reference_image_path": {"type": "string"},
            "reference_image_url": {"type": "string"},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "model", "operation", "duration", "size"]
    side_effects = ["writes video file to output_path", "calls OpenAI Videos API"]
    user_visible_verification = ["Watch generated clip for reverence, composition, and motion stability"]

    def get_status(self) -> ToolStatus:
        if os.environ.get("OPENAI_API_KEY"):
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        model = inputs.get("model") or inputs.get("model_variant") or "sora-2"
        seconds = float(inputs.get("duration", "5"))
        size = inputs.get("size") or self._size_for_aspect(
            str(inputs.get("aspect_ratio", "16:9")),
            str(model),
        )

        base_rate = 0.10 if model == "sora-2" else 0.30
        if model == "sora-2-pro":
            if size in {"1920x1080", "1080x1920"}:
                base_rate = 0.70
            elif size in {"1792x1024", "1024x1792"}:
                base_rate = 0.50
        return round(base_rate * seconds, 4)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        model = inputs.get("model") or inputs.get("model_variant") or "sora-2"
        return 180.0 if model == "sora-2-pro" else 120.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return ToolResult(
                success=False,
                error="OPENAI_API_KEY not set. " + self.install_instructions,
            )

        import requests

        start = time.time()
        prompt = inputs["prompt"]
        operation = str(inputs.get("operation", "text_to_video"))
        model = str(inputs.get("model") or inputs.get("model_variant") or "sora-2")
        size = str(inputs.get("size") or self._size_for_aspect(str(inputs.get("aspect_ratio", "16:9")), model))
        seconds = self._normalize_seconds(inputs.get("duration", "5"))
        output_path = Path(inputs.get("output_path", "sora_output.mp4"))
        output_path.parent.mkdir(parents=True, exist_ok=True)

        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            video = self._create_video(
                requests=requests,
                headers=headers,
                prompt=prompt,
                model=model,
                size=size,
                seconds=seconds,
                operation=operation,
                inputs=inputs,
            )
            video_id = video["id"]
            final_state = self._poll_video(requests, headers, video_id)
            self._download_video(requests, headers, video_id, output_path)
        except Exception as exc:
            return ToolResult(success=False, error=f"Sora video generation failed: {exc}")

        from tools.video._shared import probe_output

        probed = probe_output(output_path)
        return ToolResult(
            success=True,
            data={
                "provider": self.provider,
                "model": model,
                "prompt": prompt,
                "operation": operation,
                "aspect_ratio": inputs.get("aspect_ratio", "16:9"),
                "size": size,
                "video_id": video_id,
                "status": final_state.get("status"),
                "progress": final_state.get("progress"),
                "output": str(output_path),
                "output_path": str(output_path),
                "format": "mp4",
                **probed,
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=model,
        )

    def _create_video(
        self,
        *,
        requests: Any,
        headers: dict[str, str],
        prompt: str,
        model: str,
        size: str,
        seconds: str,
        operation: str,
        inputs: dict[str, Any],
    ) -> dict[str, Any]:
        reference_path = inputs.get("reference_image_path")
        reference_url = inputs.get("reference_image_url")

        if operation in {"image_to_video", "reference_to_video"} and reference_path:
            mime_type = mimetypes.guess_type(str(reference_path))[0] or "image/png"
            with open(reference_path, "rb") as reference_file:
                response = requests.post(
                    "https://api.openai.com/v1/videos",
                    headers=headers,
                    data={
                        "prompt": prompt,
                        "model": model,
                        "size": size,
                        "seconds": seconds,
                    },
                    files={
                        "input_reference": (Path(str(reference_path)).name, reference_file, mime_type),
                    },
                    timeout=120,
                )
        else:
            payload: dict[str, Any] = {
                "prompt": prompt,
                "model": model,
                "size": size,
                "seconds": seconds,
            }
            if operation in {"image_to_video", "reference_to_video"}:
                if reference_url:
                    payload["input_reference"] = {"image_url": reference_url}
                else:
                    return {
                        "status": "failed",
                        "error": {
                            "message": "image_to_video requires reference_image_path or reference_image_url",
                        },
                    }
            response = requests.post(
                "https://api.openai.com/v1/videos",
                headers={**headers, "Content-Type": "application/json"},
                json=payload,
                timeout=120,
            )

        response.raise_for_status()
        data = response.json()
        if "id" not in data:
            raise RuntimeError(f"Unexpected create response: {data}")
        return data

    def _poll_video(self, requests: Any, headers: dict[str, str], video_id: str) -> dict[str, Any]:
        timeout_at = time.time() + 60 * 10
        last_state: dict[str, Any] = {"id": video_id, "status": "queued"}

        while time.time() < timeout_at:
            response = requests.get(
                f"https://api.openai.com/v1/videos/{video_id}",
                headers=headers,
                timeout=60,
            )
            response.raise_for_status()
            last_state = response.json()
            status = last_state.get("status")
            if status == "completed":
                return last_state
            if status == "failed":
                message = (last_state.get("error") or {}).get("message", "video generation failed")
                raise RuntimeError(message)
            time.sleep(5)

        raise RuntimeError("Timed out waiting for Sora video generation to complete")

    def _download_video(
        self,
        requests: Any,
        headers: dict[str, str],
        video_id: str,
        output_path: Path,
    ) -> None:
        response = requests.get(
            f"https://api.openai.com/v1/videos/{video_id}/content",
            headers=headers,
            params={"variant": "video"},
            timeout=240,
            stream=True,
        )
        response.raise_for_status()
        with output_path.open("wb") as file_handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file_handle.write(chunk)

    @staticmethod
    def _normalize_seconds(value: Any) -> str:
        seconds = float(value)
        if seconds < 1:
            raise ValueError("duration must be at least 1 second")
        if seconds.is_integer():
            return str(int(seconds))
        return f"{seconds:.2f}".rstrip("0").rstrip(".")

    @staticmethod
    def _size_for_aspect(aspect_ratio: str, model: str) -> str:
        if aspect_ratio == "9:16":
            return "720x1280"
        if aspect_ratio == "1:1":
            return "1024x1024" if model == "sora-2-pro" else "720x720"
        return "1280x720"
