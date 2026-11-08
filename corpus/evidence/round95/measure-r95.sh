#!/usr/bin/env bash
# measure-r95.sh — emit the round-95 scored receipts.
# Usage: bash corpus/evidence/round95/measure-r95.sh <freeze-rev> <scratch-dir> [<out-dir>]
#   out-dir defaults to corpus/evidence/round95/after (the F receipts); the F2 receipts go to .../after-f2.
# Run from the lane root on a tree whose tracked files equal <freeze-rev> for the measured paths (the header records
# `git diff --quiet <freeze-rev> -- <paths>`). Scratch is removed by each battery; nothing outside out-dir is written.
set -u
F="$1"; W="$2"; OUT="${3:-corpus/evidence/round95/after}"
cd "$(git rev-parse --show-toplevel)" || exit 2
mkdir -p "$OUT" "$W"
PATHS="tools/search-rerun.py tools/gate-records.py tools/research-gate.sh corpus/fixtures/search-rerun-r95.md corpus/knowledge/search-rerun-record-r95.md corpus/SOURCES.md corpus/captures corpus/evidence/round57/refetch.tsv corpus/evidence/round95/rerun-controls-r95.py corpus/evidence/round95/entry-controls-r95.py corpus/evidence/round95/mutants-r95.py corpus/lessons/round-95.md"
emit() { # name, command...
  local name="$1"; shift
  local out="$OUT/$name.txt"
  # shellcheck disable=SC2086
  git diff --quiet "$F" -- $PATHS; local same=$?
  {
    echo "# computed_against F=$F tree_equals_F_for_measured_paths=$([ $same -eq 0 ] && echo yes || echo NO)"
    echo "# command: $*"
    echo "# measured_at $(date -u +%FT%TZ)"
    "$@" 2>&1
    echo "# exit=$?"
  } > "$out"
  tail -n 3 "$out"
}
emit c1-verify python3 -B tools/search-rerun.py verify corpus/fixtures/search-rerun-r95.md --root .
emit c1-controls python3 -B corpus/evidence/round95/rerun-controls-r95.py --root . --work "$W"
if [ -f corpus/evidence/round95/mutants-r95.py ]; then
  emit c1-mutants python3 -B corpus/evidence/round95/mutants-r95.py --root . --work "$W"
fi
emit c2-gate python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-rerun-record-r95.md
emit c2-metadata bash tools/research-gate.sh verify-metadata corpus/knowledge/search-rerun-record-r95.md --root .
emit c2-controls python3 -B corpus/evidence/round95/entry-controls-r95.py --root . --work "$W"
if [ -f corpus/lessons/round-95.md ]; then
  emit lesson-gate python3 -B tools/gate-records.py verify --root . corpus/lessons/round-95.md
fi
