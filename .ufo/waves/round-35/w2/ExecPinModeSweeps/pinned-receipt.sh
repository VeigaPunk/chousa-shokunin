#!/usr/bin/env bash
# FINAL consolidated receipt run — every measurement is against the PINNED
# landed gate blob (sha 1f2fb4f5…, extracted from e87c5d7 into this seat's own
# directory), never against the concurrently-drifting worktree copy.
#
# Target: mode `verify-sweeps` under the pin — four environments on the
# committed sweep fixture, plus a refused override.
# Report per environment: exit, summary line, tripwire, refusal.
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
PINNED="$REPO/.ufo/waves/round-35/w2/ExecPinModeSweeps/pinned/tools/research-gate.sh"
BASE_GATE="$SCRATCH/clone/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
SHIMDIR="$SCRATCH/shim"
TIMEOUT=/usr/bin/timeout

echo "===== PINS ====="
sha256sum "$PINNED" "$BASE_GATE" "$FIXTURE"
printf 'pinned_gate_is_landed_blob_1f2fb4f5: '
[[ "$(sha256sum "$PINNED" | cut -d' ' -f1)" == "1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617" ]] && echo YES || echo NO
echo

run4() { # LABEL GATE PATH ENVSPEC
  local label=$1 gate=$2 path=$3 envspec=$4
  local dir="$SCRATCH/run/final-$label"; rm -rf "$dir"; mkdir -p "$dir"
  : > "$SHIMDIR/trip-path.log"; : > "$SHIMDIR/trip-fn.log"
  local rc=0
  # shellcheck disable=SC2086
  env -i HOME="$HOME" PATH="$path" TMPDIR="$SCRATCH" \
    ${envspec:+$(printf '%s' "$envspec" | tr '|' ' ')} \
    "$TIMEOUT" 600 bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" \
    >"$dir/out" 2>"$dir/err" || rc=$?
  printf -- '--- %s\n' "$label"
  printf '  exit=%s\n' "$rc"
  printf '  summary=%s\n' "$(grep -m1 '^VERIFIED_SWEEPS=' "$dir/out" || true)"
  printf '  verdict=%s\n' "$(grep -m1 '^RESEARCH_GATE: ' "$dir/out" || true)"
  printf '  tripwire_path_bytes=%s tripwire_fn_bytes=%s\n' \
    "$(stat -c %s "$SHIMDIR/trip-path.log")" "$(stat -c %s "$SHIMDIR/trip-fn.log")"
  printf '  stderr=%s\n' "$(tr '\n' '|' < "$dir/err" | cut -c1-300)"
  printf '  stdout_sha_norm=%s\n' \
    "$(sed -E 's/ts=[0-9T:Z-]+//' "$dir/out" | sha256sum | cut -d' ' -f1)"
}
echo "===== FOUR ENVIRONMENTS (PINNED LANDED GATE) ====="
run4 E1-clean              "$PINNED" "$CLEAN_PATH" ""
run4 E2-shim-first-PATH    "$PINNED" "$SHIMDIR/bin:$CLEAN_PATH" ""
run4 E3-BASH_ENV-function  "$PINNED" "$CLEAN_PATH" "BASH_ENV=$SHIMDIR/bash_env.sh"
run4 E4-no-grep-on-PATH    "$PINNED" "$SCRATCH/nogrepbin" ""
echo
echo "===== SAME FOUR, BASE GATE (round-34 blob a6307edf…, NO pin) ====="
run4 B1-clean              "$BASE_GATE" "$CLEAN_PATH" ""
run4 B2-shim-first-PATH    "$BASE_GATE" "$SHIMDIR/bin:$CLEAN_PATH" ""
run4 B3-BASH_ENV-function  "$BASE_GATE" "$CLEAN_PATH" "BASH_ENV=$SHIMDIR/bash_env.sh"
run4 B4-no-grep-on-PATH    "$BASE_GATE" "$SCRATCH/nogrepbin" ""
echo
echo "===== REFUSED OVERRIDE (PINNED LANDED GATE) ====="
for spec in "RESEARCH_GATE_GREP=bin/grep" "RESEARCH_GATE_GREP=/nonexistent/x" "RESEARCH_GATE_GREP=$SCRATCH/run/stub-grep"; do
  rc=0
  env -i HOME="$HOME" PATH="$CLEAN_PATH" $spec \
    "$TIMEOUT" 600 bash "$PINNED" verify-sweeps "$FIXTURE" --root "$REPO" \
    >"$SCRATCH/run/final-ovr.out" 2>"$SCRATCH/run/final-ovr.err" || rc=$?
  printf '  %-46s exit=%s stdout_bytes=%s\n' "$spec" "$rc" "$(stat -c %s "$SCRATCH/run/final-ovr.out")"
  printf '    refusal=%s\n' "$(tr '\n' '|' < "$SCRATCH/run/final-ovr.err")"
done
echo
echo "===== ACCEPTED OVERRIDE + ECHO (PINNED LANDED GATE) ====="
for spec in "RESEARCH_GATE_GREP=/usr/bin/grep" "CHOUSA_GREP_PIN_ECHO=1"; do
  rc=0
  env -i HOME="$HOME" PATH="$CLEAN_PATH" $spec \
    "$TIMEOUT" 600 bash "$PINNED" verify-sweeps "$FIXTURE" --root "$REPO" \
    >"$SCRATCH/run/final-echo.out" 2>"$SCRATCH/run/final-echo.err" || rc=$?
  printf '  %-46s exit=%s summary=%s\n' "$spec" "$rc" "$(grep -m1 '^VERIFIED_SWEEPS=' "$SCRATCH/run/final-echo.out" || true)"
  printf '    stderr=%s\n' "$(tr '\n' '|' < "$SCRATCH/run/final-echo.err")"
done
