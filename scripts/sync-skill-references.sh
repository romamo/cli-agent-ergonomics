#!/usr/bin/env bash
# sync-skill-references.sh
#
# Copies spec content from the repo root into the bundled references/ directories
# inside each distributable skill. Run this after editing challenges, requirements,
# schemas, or IMPLEMENTING.md to keep skill bundles in sync.
#
# Usage: scripts/sync-skill-references.sh [--dry-run]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DRY_RUN=false

for arg in "$@"; do
  [[ "$arg" == "--dry-run" ]] && DRY_RUN=true
done

copy() {
  local src="$1" dst="$2"
  if [[ "$DRY_RUN" == true ]]; then
    echo "[dry-run] rsync $src -> $dst"
  else
    rsync -a --delete "$src" "$dst"
    echo "synced: $src -> $dst"
  fi
}

# cli-agent-evaluate: bundles challenges/
copy "$REPO_ROOT/challenges/" \
     "$REPO_ROOT/skills/cli-agent-evaluate/references/challenges/"

# cli-agent-implement: bundles requirements/, schemas/, IMPLEMENTING.md
copy "$REPO_ROOT/requirements/" \
     "$REPO_ROOT/skills/cli-agent-implement/references/requirements/"

copy "$REPO_ROOT/schemas/" \
     "$REPO_ROOT/skills/cli-agent-implement/references/schemas/"

copy "$REPO_ROOT/IMPLEMENTING.md" \
     "$REPO_ROOT/skills/cli-agent-implement/references/IMPLEMENTING.md"

echo "done"
