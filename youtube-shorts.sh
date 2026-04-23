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
SHORTS_ROOT="$SCRIPT_DIR/Design-Docs/ToPublish/Shorts"

show_help() {
  local cmd_name
  cmd_name="$(basename "$0")"
  cat <<EOF
$cmd_name — OpenMontage Shorts pipeline

Turns a markdown file with a Script section into a final 9:16 TikTok/Shorts MP4
through four gated phases. Each phase creates a ticket; nothing advances until approved.

PIPELINE USAGE  (one folder, four phases in order):

  $cmd_name <folder> --scenes
      Phase 1 — Agent reads your ## Script and writes a full scene breakdown
      to the markdown: timing, visuals, camera moves, motion recipes, prompts.
      A ticket is created for your review before proceeding.

  $cmd_name <folder> --artifacts
      Phase 2 — Agent finalizes all image/video prompts per scene (MidJourney,
      DrawThings, Kling, Seedance). Writes an Artifact Status table. No API
      calls are made — all artifacts stay PENDING until you approve the prompts.

  $cmd_name <folder> --generate-clips
      Phase 3 — Calls Kling/Seedance/image-gen APIs for PENDING artifacts where
      keys are configured. MidJourney and DrawThings remain manual (prompts are
      already written — run them in their apps and drop files into the folder).

  $cmd_name <folder> --rendershorts
      Phase 4 — Requires a voiceover file in <folder>/Renders/. Builds a
      HyperFrames composition from the scene markdown (if not yet built), then
      renders a 9:16 MP4 at tiktok_vertical profile, 1080×1920, 30fps.

LEGACY USAGE  (interactive modes):

  $cmd_name --gen-shorts
      Interactive Shorts mode — browse all Shorts folders, inspect a package,
      and optionally research or spruce the markdown via the agent.

  $cmd_name --gen-mp4
      Interactive scene MP4 review mode — review scene-*.mp4 files in a
      selected Shorts folder and update the Results table with status + timestamp.

OTHER:

  $cmd_name --help    Show this help text.

MAKEFILE SHORTCUTS:

  make shorts-scenes NAME=<folder>
  make shorts-artifacts NAME=<folder>
  make shorts-generate-clips NAME=<folder>
  make shorts-render NAME=<folder>

FULL GUIDE:
  Design-Docs/Shorts-Pipeline-Guide.md
EOF
  if [[ "$cmd_name" == "shorts-workflow" ]]; then
    echo ""
    echo "Shortcut: running \`shorts-workflow\` with no arguments defaults to --gen-shorts."
  fi
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
  if [[ "$(basename "$0")" == "shorts-workflow" ]]; then
    exec "$PYTHON_BIN" "$MAIN_PY" --gen-shorts
  fi
  show_help
  exit 0
fi

# Legacy flags (no positional arg)
case "${1:-}" in
  --help|-h)
    show_help
    exit 0
    ;;
  --gen-shorts|--gen-mp4)
    exec "$PYTHON_BIN" "$MAIN_PY" "$@"
    ;;
esac

# Pipeline flags: youtube-shorts.sh <folder> --<phase>
if [[ $# -ge 2 ]]; then
  FOLDER="${1}"
  PHASE="${2}"
  FOLDER_PATH="$SHORTS_ROOT/$FOLDER"

  case "$PHASE" in
    --scenes|--artifacts|--generate-clips)
      exec "$PYTHON_BIN" "$MAIN_PY" "$PHASE" --folder "$FOLDER"
      ;;
    --rendershorts)
      # Voiceover-first enforcement — shell validates before invoking HyperFrames
      RENDERS_DIR="$FOLDER_PATH/Renders"
      VOICEOVER=""
      if [[ -d "$RENDERS_DIR" ]]; then
        VOICEOVER="$(find "$RENDERS_DIR" -maxdepth 1 \( -name "*.mp3" -o -name "*.wav" -o -name "*.m4a" \) | head -1)"
      fi
      if [[ -z "$VOICEOVER" ]]; then
        echo "ERROR: No voiceover found in $RENDERS_DIR" >&2
        echo "Place a .mp3/.wav/.m4a file there before rendering." >&2
        echo "This pipeline enforces voiceover-first — final renders require narration audio." >&2
        exit 1
      fi

      # Locate HyperFrames composition
      COMPOSITION=""
      if [[ -f "$FOLDER_PATH/composition.html" ]]; then
        COMPOSITION="$FOLDER_PATH/composition.html"
      elif [[ -f "$FOLDER_PATH/index.html" ]]; then
        COMPOSITION="$FOLDER_PATH/index.html"
      fi

      if [[ -z "$COMPOSITION" ]]; then
        # No composition yet — hand off to agent to build it from the markdown
        exec "$PYTHON_BIN" "$MAIN_PY" --rendershorts "$FOLDER"
      fi

      mkdir -p "$RENDERS_DIR"
      OUTPUT="$RENDERS_DIR/${FOLDER}-captioned-v1.mp4"
      echo "==> Rendering $FOLDER via HyperFrames..."
      echo "    Composition: $COMPOSITION"
      echo "    Voiceover:   $VOICEOVER"
      echo "    Output:      $OUTPUT"
      npx hyperframes render "$COMPOSITION" \
        --output "$OUTPUT" \
        --profile tiktok_vertical \
        --quality high \
        --fps 30
      echo "==> Render complete: $OUTPUT"
      ;;
    *)
      echo "Unknown flag: $PHASE" >&2
      echo >&2
      show_help >&2
      exit 2
      ;;
  esac
fi

# Single unrecognized arg
echo "Unknown option: ${1:-}" >&2
echo >&2
show_help >&2
exit 2
