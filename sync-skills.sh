#!/usr/bin/env bash
#
# sync-skills.sh — collect every installed Claude Code and Codex skill into one
# flat folder, one directory per skill (the same layout ~/.claude/skills uses).
#
# A "skill" is any directory that contains a SKILL.md. This script finds them
# across all known Claude + Codex locations, deduplicates by skill name
# (keeping the newest copy when a name appears in several places / plugin
# versions), and copies each skill's whole directory into the target folder.
#
# Usage:
#   ./sync-skills.sh [options] [TARGET_DIR]
#
# Options:
#   -n, --dry-run     Show what would be copied, change nothing.
#   -f, --force       Overwrite skills that already exist in TARGET.
#       --no-plugins  Only sync the flat skill dirs (~/.claude/skills,
#                     ~/.codex/skills); skip plugin-bundled skills.
#       --no-claude   Skip Claude sources.
#       --no-codex    Skip Codex sources.
#   -q, --quiet       Only print the final summary.
#   -h, --help        Show this help.
#
# TARGET_DIR defaults to the directory this script lives in.
#
set -euo pipefail

# ---------------------------------------------------------------------------
# Defaults & argument parsing
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR"
DRY_RUN=0
FORCE=0
INCLUDE_PLUGINS=1
INCLUDE_CLAUDE=1
INCLUDE_CODEX=1
QUIET=0

usage() { sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

while [ $# -gt 0 ]; do
  case "$1" in
    -n|--dry-run)   DRY_RUN=1 ;;
    -f|--force)     FORCE=1 ;;
    --no-plugins)   INCLUDE_PLUGINS=0 ;;
    --no-claude)    INCLUDE_CLAUDE=0 ;;
    --no-codex)     INCLUDE_CODEX=0 ;;
    -q|--quiet)     QUIET=1 ;;
    -h|--help)      usage 0 ;;
    -*)             echo "Unknown option: $1" >&2; usage 1 ;;
    *)              TARGET="$1" ;;
  esac
  shift
done

log() { [ "$QUIET" -eq 1 ] || printf '%s\n' "$*"; }

# ---------------------------------------------------------------------------
# Build the list of source roots to scan, in priority order.
# Earlier roots win when the same skill name appears in several places.
# ---------------------------------------------------------------------------
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

# Flat "installed" skill dirs first (canonical), then plugin bundles.
FLAT_ROOTS=()
PLUGIN_ROOTS=()
[ "$INCLUDE_CLAUDE" -eq 1 ] && FLAT_ROOTS+=("$CLAUDE_HOME/skills")
[ "$INCLUDE_CODEX"  -eq 1 ] && FLAT_ROOTS+=("$CODEX_HOME/skills")
[ "$INCLUDE_CLAUDE" -eq 1 ] && PLUGIN_ROOTS+=("$CLAUDE_HOME/plugins")
[ "$INCLUDE_CODEX"  -eq 1 ] && PLUGIN_ROOTS+=("$CODEX_HOME/plugins")

TARGET_ABS="$(cd "$TARGET" 2>/dev/null && pwd || echo "$TARGET")"

# ---------------------------------------------------------------------------
# Collect candidate SKILL.md files (null-delimited to survive odd paths).
# For each, the skill directory is its parent; the skill name is that dir's
# basename. We keep, per name, the candidate whose SKILL.md is newest — so the
# latest plugin version wins over stale cached ones.
# ---------------------------------------------------------------------------
declare -A CHOSEN_DIR=()   # name -> chosen source directory
declare -A CHOSEN_MTIME=() # name -> mtime of chosen SKILL.md

mtime_of() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null || echo 0; }

consider() {
  # $1 = path to a SKILL.md
  local md="$1" dir name mt
  dir="$(dirname "$md")"
  name="$(basename "$dir")"
  # Never re-ingest skills that already live in the target tree.
  case "$dir/" in "$TARGET_ABS"/*) return ;; esac
  mt="$(mtime_of "$md")"
  if [ -z "${CHOSEN_DIR[$name]:-}" ] || [ "$mt" -gt "${CHOSEN_MTIME[$name]:-0}" ]; then
    CHOSEN_DIR[$name]="$dir"
    CHOSEN_MTIME[$name]="$mt"
  fi
}

scan_root() {
  # $1 = root, $2 = maxdepth-for-flat (flat roots are shallow; plugins deep)
  local root="$1" depth="$2"
  [ -d "$root" ] || return 0
  while IFS= read -r -d '' md; do
    consider "$md"
  done < <(find "$root" -maxdepth "$depth" -type f -name SKILL.md -print0 2>/dev/null)
}

# Flat roots: SKILL.md sits at <root>/<skill>/SKILL.md  (depth 2).
for r in "${FLAT_ROOTS[@]:-}"; do
  [ -n "$r" ] && scan_root "$r" 2
done

# Plugin roots: SKILL.md can be nested arbitrarily deep inside versioned caches.
if [ "$INCLUDE_PLUGINS" -eq 1 ]; then
  for r in "${PLUGIN_ROOTS[@]:-}"; do
    [ -n "$r" ] && scan_root "$r" 12
  done
fi

TOTAL=${#CHOSEN_DIR[@]}
if [ "$TOTAL" -eq 0 ]; then
  echo "No skills found. Checked: ${FLAT_ROOTS[*]:-} ${PLUGIN_ROOTS[*]:-}" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Copy each chosen skill directory into TARGET/<name>.
# ---------------------------------------------------------------------------
mkdir -p "$TARGET"
copied=0; skipped=0; overwritten=0

for name in $(printf '%s\n' "${!CHOSEN_DIR[@]}" | sort); do
  src="${CHOSEN_DIR[$name]}"
  dest="$TARGET/$name"
  if [ -e "$dest" ] && [ "$FORCE" -eq 0 ]; then
    log "skip   $name (exists)"
    skipped=$((skipped+1))
    continue
  fi
  if [ -e "$dest" ]; then
    action="over"; overwritten=$((overwritten+1))
  else
    action="copy"; copied=$((copied+1))
  fi
  log "$action   $name  <-  ${src/#$HOME/~}"
  if [ "$DRY_RUN" -eq 0 ]; then
    rm -rf "$dest"
    cp -R "$src" "$dest"
  fi
done

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo
if [ "$DRY_RUN" -eq 1 ]; then
  echo "DRY RUN — nothing written."
fi
printf 'Skills found: %d | copied: %d | overwritten: %d | skipped (existing): %d\n' \
  "$TOTAL" "$copied" "$overwritten" "$skipped"
echo "Target: $TARGET_ABS"
[ "$FORCE" -eq 0 ] && [ "$skipped" -gt 0 ] && echo "Tip: re-run with --force to refresh skills that already exist."
