#!/usr/bin/env bash
# measure-all-r94 — re-run every round-94 counter and battery at a named revision and write the six
# scored receipts under corpus/evidence/round94/after/. Every receipt carries its measured revision
# (round-93 spot-check D5: a scored receipt names the revision it was taken against).
#
# Usage: scripts/measure-all-r94.sh <FREEZE_REV> <CARRIER_REV> [SCRATCH_ROOT]
# Exit 0 when every command exits with its expected code (0), 1 otherwise. No network, no writes
# outside corpus/evidence/round94/after/ and the scratch root.
set -u
LANE=$(cd "$(dirname "$0")/.." && pwd)
F=${1:?freeze revision}
C=${2:?carrier revision}
SCR=${3:-${HYAKU_SCRATCH:-/fast/scratch/hyaku}/chousa-r94/measure}
OUT="$LANE/corpus/evidence/round94/after"
mkdir -p "$OUT" "$SCR"
cd "$LANE" || exit 2
rc_total=0

emit() {  # emit <name> <command...>
  local name=$1; shift
  local out="$OUT/$name.txt"
  {
    echo "# computed_against F=$F C=$C"
    echo "# command: $*"
    echo "# measured_at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  } > "$out"
  "$@" >> "$out" 2>&1
  local rc=$?
  echo "# exit=$rc" >> "$out"
  echo "$name rc=$rc -> $out"
  [ "$rc" -eq 0 ] || rc_total=1
}

emit c1-verify python3 -B corpus/evidence/round94/control-driver-r94.py verify \
  --root . --repo . --rev "$F" --receipts-rev "$C" --work "$SCR/c1"
emit c1-forgeries python3 -B corpus/evidence/round94/forgeries-r94.py \
  --root . --repo . --rev "$F" --receipts-rev "$C" --work "$SCR/c1f"
emit c2-counter python3 -B corpus/evidence/round94/curation-r94.py --root .
emit c2-controls python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work "$SCR/c2"
emit c3-counter python3 -B corpus/evidence/round94/skill-tally-r94.py --root . \
  --selftest corpus/evidence/round94/controls/selftest-r94.txt
emit c3-controls python3 -B corpus/evidence/round94/skill-tally-r94-controls.py --root . --work "$SCR/c3"

exit "$rc_total"
