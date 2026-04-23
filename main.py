from __future__ import annotations

import argparse
import json
import sys

from lib.package_bootstrap import (
    PackageBootstrapError,
    bootstrap_package,
    generate_scene_videos,
)
from lib.shorts_workflow import (
    run_gen_mp4_mode,
    run_gen_shorts_mode,
    run_scenes_mode,
    run_artifacts_mode,
    run_generate_clips_mode,
    run_rendershorts_mode,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenMontage CLI")
    parser.add_argument(
        "--gen-shorts",
        action="store_true",
        help="Enter interactive Shorts mode",
    )
    parser.add_argument(
        "--gen-mp4",
        action="store_true",
        help="Enter interactive scene MP4 review mode",
    )
    # Pipeline phase flags — used by youtube-shorts.sh <folder> --<phase>
    parser.add_argument("--scenes", action="store_true", help="Phase 1: generate scene breakdown")
    parser.add_argument("--artifacts", action="store_true", help="Phase 2: write artifact prompts")
    parser.add_argument("--generate-clips", action="store_true", dest="generate_clips", help="Phase 3: execute API-backed generation")
    parser.add_argument("--rendershorts", action="store_true", help="Phase 4: build HyperFrames composition for render")
    parser.add_argument("--folder", default=None, help="Shorts folder name (required for pipeline phases)")
    subparsers = parser.add_subparsers(dest="command")

    package_parser = subparsers.add_parser("package", help="Bootstrap and manage markdown packages")
    package_subparsers = package_parser.add_subparsers(dest="package_command")

    bootstrap_parser = package_subparsers.add_parser(
        "bootstrap",
        help="Create a project workspace and initial artifacts from a Shorts markdown package",
    )
    bootstrap_parser.add_argument(
        "--md",
        required=True,
        help="Path to the markdown package under Design-Docs/ToPublish/Shorts",
    )
    bootstrap_parser.add_argument(
        "--force",
        action="store_true",
        help="Allow bootstrap to proceed even if project/package artifacts already exist",
    )

    generate_parser = package_subparsers.add_parser(
        "generate-scenes",
        help="Generate scene video clips for a Shorts markdown package",
    )
    generate_parser.add_argument(
        "--md",
        required=True,
        help="Path to the markdown package under Design-Docs/ToPublish/Shorts",
    )
    generate_parser.add_argument(
        "--provider",
        default="auto",
        help="Preferred provider name to route through video_selector, e.g. sora",
    )
    generate_parser.add_argument(
        "--model",
        default=None,
        help="Optional provider-specific model or variant name",
    )
    generate_parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate scene clips even if output files already exist",
    )
    generate_parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip scenes whose output files already exist and generate only the missing ones",
    )
    generate_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan scene generation without calling providers",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.gen_shorts:
        return run_gen_shorts_mode()
    if args.gen_mp4:
        return run_gen_mp4_mode()

    if args.scenes:
        if not args.folder:
            print("--scenes requires a folder name", file=sys.stderr)
            return 2
        return run_scenes_mode(args.folder)
    if args.artifacts:
        if not args.folder:
            print("--artifacts requires a folder name", file=sys.stderr)
            return 2
        return run_artifacts_mode(args.folder)
    if args.generate_clips:
        if not args.folder:
            print("--generate-clips requires a folder name", file=sys.stderr)
            return 2
        return run_generate_clips_mode(args.folder)
    if args.rendershorts:
        if not args.folder:
            print("--rendershorts requires a folder name", file=sys.stderr)
            return 2
        return run_rendershorts_mode(args.folder)

    if args.command == "package" and args.package_command == "bootstrap":
        try:
            result = bootstrap_package(args.md, force=args.force)
        except PackageBootstrapError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "package" and args.package_command == "generate-scenes":
        try:
            result = generate_scene_videos(
                args.md,
                preferred_provider=args.provider,
                model=args.model,
                force=args.force,
                resume=args.resume,
                dry_run=args.dry_run,
            )
        except PackageBootstrapError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
