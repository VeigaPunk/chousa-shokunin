#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  printf 'usage: %s TREE_ROOT [ANALYSIS_ROOT]\n' "$0" >&2
  exit 2
fi
TREE_ROOT=$(cd -- "$1" && pwd -P)
ANALYSIS_ROOT=${2:-/home/vgpnk/Projects/shokunin}
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
BASELINE_DIR=$SCRIPT_DIR/holds
GATE=tools/research-gate.sh
[[ -f $TREE_ROOT/$GATE ]] || { printf 'gate not found under TREE_ROOT: %s\n' "$TREE_ROOT/$GATE" >&2; exit 2; }
[[ -d $BASELINE_DIR ]] || { printf 'baseline directory not found: %s\n' "$BASELINE_DIR" >&2; exit 2; }
TMP=$(mktemp -d)
trap 'rm -rf -- "$TMP"' EXIT
failed=0

mask_volatile() {
  awk '
    {
      if (index($0, "ts="))
        gsub(/(^|[[:space:]])ts=[^[:space:]]+/, " ts=<MASKED>")
      if (index($0, "\"ts\""))
        gsub(/"ts"[[:space:]]*:[[:space:]]*"[^"]*"/, "\"ts\":\"<MASKED>\"")
      if (index($0, "gate_sha256") || index($0, "gate sha")) {
        gsub(/gate_sha256=[^[:space:]]+/, "gate_sha256=<MASKED>")
        gsub(/"gate_sha256"[[:space:]]*:[[:space:]]*"[^"]*"/, "\"gate_sha256\":\"<MASKED>\"")
        gsub(/gate_sha256:[[:space:]]*[^[:space:]]+/, "gate_sha256:<MASKED>")
        gsub(/gate[[:space:]_-]+sha256[=:][[:space:]]*[^[:space:]]+/, "gate_sha256=<MASKED>")
      }
      print
    }
  ' "$1"
}

run_and_diff() {
  local name=$1 rc got expected
  shift
  got=$TMP/$name.log
  expected=$TMP/$name.expected
  if (cd -- "$TREE_ROOT" && "$@") >"$got" 2>&1; then
    rc=0
  else
    rc=$?
  fi
  printf 'EXIT_CODE=%s\n' "$rc" >>"$got"
  if [[ ! -f $BASELINE_DIR/$name.log ]]; then
    printf 'MISSING BASELINE: %s\n' "$BASELINE_DIR/$name.log" >&2
    failed=1
    return
  fi
  if [[ $name == selftest ]]; then
    # Round 25 adds cases 137+. Compare only the frozen legacy population
    # 1..136 and its exit; the full 154-case PASS is measured separately.
    awk '$1=="ok-case" && $2<=136 || /^EXIT_CODE=/' "$got" >"$got.legacy"
    awk '$1=="ok-case" && $2<=136 || /^EXIT_CODE=/' "$BASELINE_DIR/$name.log" >"$expected.legacy"
    mask_volatile "$got.legacy" >"$got.masked"
    mask_volatile "$expected.legacy" >"$expected"
  else
    mask_volatile "$got" >"$got.masked"
    mask_volatile "$BASELINE_DIR/$name.log" >"$expected"
  fi
  if diff -u -- "$expected" "$got.masked"; then
    printf 'MATCH %s (exit %s)\n' "$name" "$rc"
  else
    printf 'DIFF %s (exit %s)\n' "$name" "$rc" >&2
    failed=1
  fi
}

run_and_diff selftest bash "$GATE" --selftest
run_and_diff drift-r12 bash "$GATE" --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json
for r in A B C; do
  run_and_diff "verify-all-${r}-r9" bash "$GATE" verify-all "corpus/fixtures/archives-r9/$r-r9.md" \
    --claims corpus/fixtures/claims-r9.jsonl --root "$ANALYSIS_ROOT"
done
for record in \
  full-r6 \
  full-r6-broken \
  integrity-r7 \
  integrity-r7-broken \
  sweeps-r5 \
  chain-r3; do
  run_and_diff "verify-all-$record" bash "$GATE" verify-all "corpus/fixtures/$record.md" \
    --root "$ANALYSIS_ROOT"
done
run_and_diff verify-claims-r2 bash "$GATE" verify-claims corpus/fixtures/claims-r2.jsonl \
  --root "$ANALYSIS_ROOT"

exit "$failed"
