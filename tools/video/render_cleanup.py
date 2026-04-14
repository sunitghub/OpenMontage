"""Cleanup helper for versioned render outputs.

Keeps only the newest versioned MP4 files for each render family.

Examples:
  python tools/video/render_cleanup.py projects/foo/renders
  python tools/video/render_cleanup.py projects/foo/renders --keep 2 --dry-run
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


VERSION_RE = re.compile(r"^(?P<family>.+)-v(?P<version>\d+)(?P<suffix>(?:-[^.]+)*)$")


@dataclass(frozen=True)
class VersionedRender:
    path: Path
    family: str
    version: int
    suffix: str


def parse_versioned_render(path: Path) -> VersionedRender | None:
    if path.suffix.lower() != ".mp4":
        return None
    match = VERSION_RE.match(path.stem)
    if not match:
        return None
    return VersionedRender(
        path=path,
        family=match.group("family"),
        version=int(match.group("version")),
        suffix=match.group("suffix") or "",
    )


def collect_versioned_renders(renders_dir: Path) -> dict[str, list[VersionedRender]]:
    groups: dict[str, list[VersionedRender]] = defaultdict(list)
    for path in renders_dir.iterdir():
        if not path.is_file():
            continue
        render = parse_versioned_render(path)
        if render is None:
            continue
        groups[render.family].append(render)
    return groups


def select_deletions(groups: dict[str, list[VersionedRender]], keep: int) -> list[Path]:
    deletions: list[Path] = []
    for renders in groups.values():
        ordered = sorted(
            renders,
            key=lambda item: (item.version, item.path.stat().st_mtime, item.path.name),
            reverse=True,
        )
        deletions.extend(render.path for render in ordered[keep:])
    return deletions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("renders_dir", type=Path, help="Directory containing render outputs")
    parser.add_argument(
        "--keep",
        type=int,
        default=1,
        help="How many newest versions to keep per render family (default: 1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print deletions without removing files",
    )
    args = parser.parse_args()

    renders_dir = args.renders_dir.expanduser().resolve()
    if args.keep < 1:
        raise SystemExit("--keep must be at least 1")
    if not renders_dir.exists():
        raise SystemExit(f"Directory does not exist: {renders_dir}")
    if not renders_dir.is_dir():
        raise SystemExit(f"Not a directory: {renders_dir}")

    groups = collect_versioned_renders(renders_dir)
    deletions = select_deletions(groups, keep=args.keep)

    if not deletions:
        print(f"No old versioned MP4 renders to delete in {renders_dir}")
        return 0

    action = "Would delete" if args.dry_run else "Deleted"
    for path in deletions:
        if not args.dry_run:
            path.unlink()
        print(f"{action}: {path}")

    print(
        f"{'Planned' if args.dry_run else 'Completed'} cleanup for {renders_dir}: "
        f"{len(deletions)} file(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
