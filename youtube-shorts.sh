#!/usr/bin/env bash

set -euo pipefail

SOURCE_PATH="${BASH_SOURCE[0]}"
while [ -L "$SOURCE_PATH" ]; do
  SOURCE_DIR="$(cd "$(dirname "$SOURCE_PATH")" && pwd)"
  SOURCE_PATH="$(readlink "$SOURCE_PATH")"
  [[ "$SOURCE_PATH" != /* ]] && SOURCE_PATH="$SOURCE_DIR/$SOURCE_PATH"
done
SCRIPT_DIR="$(cd "$(dirname "$SOURCE_PATH")" && pwd)"
PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
MAIN_PY="$SCRIPT_DIR/main.py"

show_help() {
  cat <<'EOF'
youtube-shorts

Helper wrapper for the OpenMontage Shorts workflow.

Usage:
  youtube-shorts --help
  youtube-shorts --gen-shorts
  youtube-shorts --gen-mp4

Options:
  --gen-shorts   Enter interactive Shorts mode. Lists folders under
                 OpenMontage/Design-Docs/ToPublish/Shorts, lets you inspect
                 one, and optionally research/create or spruce the markdown package.

  --gen-mp4      Enter interactive scene MP4 review mode. Reviews scene-*.mp4
                 files in a selected Shorts folder and updates the markdown
                 Results table with status + timestamp.

  --help         Show this help text.
EOF
}

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "OpenMontage virtualenv python not found at: $PYTHON_BIN" >&2
  exit 1
fi

if [[ ! -f "$MAIN_PY" ]]; then
  echo "OpenMontage main.py not found at: $MAIN_PY" >&2
  exit 1
fi

if [[ $# -eq 0 ]]; then
  show_help
  exit 0
fi

case "${1:-}" in
  --help|-h)
    show_help
    exit 0
    ;;
  --gen-shorts|--gen-mp4)
    exec "$PYTHON_BIN" "$MAIN_PY" "$@"
    ;;
  *)
    echo "Unknown option: $1" >&2
    echo >&2
    show_help >&2
    exit 2
    ;;
esac
