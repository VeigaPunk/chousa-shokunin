#!/usr/bin/env bash
# Discriminating surface for verify-sweeps under the pin:
#  1. base gate under the same envs (does the refusal exist at all?)
#  2. a sweeps-mode analogue of the C1 counter scored against BOTH gates:
#     if the base gate also scores 9/9 there, the sweeps mode is a blind
#     spot for C1 (tripwire-empty is vacuous, not evidence).
#  3. --help / usage ordering vs the refusal.
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
GATE="$REPO/tools/research-gate.sh"
BASE_GATE="$SCRATCH/clone/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"
TIMEOUT=/usr/bin/timeout
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
SHIMDIR="$SCRATCH/shim"

echo "### 1. base gate under the same override/env (sweeps mode)"
for spec in "RESEARCH_GATE_GREP=bin/grep" "RESEARCH_GATE_GREP=/usr/bin/grep" "CHOUSA_GREP_PIN_ECHO=1"; do
  rc=0
  env -i HOME="$HOME" PATH="$CLEAN_PATH" TMPDIR="$SCRATCH" $spec \
    "$TIMEOUT" 600 bash "$BASE_GATE" verify-sweeps "$FIXTURE" --root "$REPO" \
    >"$SCRATCH/run/base-ovr.out" 2>"$SCRATCH/run/base-ovr.err" || rc=$?
  printf '  base %-34s rc=%s stdout_bytes=%s stderr=%s\n' "$spec" "$rc" \
    "$(stat -c %s "$SCRATCH/run/base-ovr.out")" \
    "$(tr '\n' '|' < "$SCRATCH/run/base-ovr.err" | cut -c1-160)"
done
echo

echo "### 2. sweeps-mode analogue of the C1 counter (tripwire-empty + summary + refusal)"
# Same nine scenarios as corpus/evidence/round35/c1-count.py, but run against
# the verify-sweeps mode on the committed sweep fixture.
sweeps_counter() { # GATE -> prints PASSED/9
  local gate=$1 passed=0 detail=""
  local dir="$SCRATCH/run/sc-$RANDOM"; rm -rf "$dir"; mkdir -p "$dir"
  : > "$SHIMDIR/trip-path.log"; : > "$SHIMDIR/trip-fn.log"
  local rc out err
  # reference
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  local ref_sum ref_out
  ref_sum=$(grep -m1 '^VERIFIED_SWEEPS=' <<<"$out" || true)
  ref_out=$(sed -E 's/ts=[^ ]*//' <<<"$out")
  same() { local o=$1; [[ "$(sed -E 's/ts=[^ ]*//' <<<"$o")" == "$ref_out" ]]; }
  # S1 shim-first PATH
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$SHIMDIR/bin:$CLEAN_PATH" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  local t1=$(stat -c %s "$SHIMDIR/trip-path.log")
  [[ $t1 -eq 0 && $rc -eq 0 && $(grep -m1 '^VERIFIED_SWEEPS=' <<<"$out") == "$ref_sum" ]] && passed=$((passed+1)) || detail+=" S1(trip=$t1 rc=$rc)"
  # S2 BASH_ENV function
  : > "$SHIMDIR/trip-fn.log"
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" BASH_ENV="$SHIMDIR/bash_env.sh" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  local t2=$(stat -c %s "$SHIMDIR/trip-fn.log")
  [[ $t2 -eq 0 && $rc -eq 0 && $(grep -m1 '^VERIFIED_SWEEPS=' <<<"$out") == "$ref_sum" ]] && passed=$((passed+1)) || detail+=" S2(trip=$t2 rc=$rc)"
  # S3 no grep on PATH
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$SCRATCH/nogrepbin" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  [[ $rc -eq 0 && $(grep -m1 '^VERIFIED_SWEEPS=' <<<"$out") == "$ref_sum" ]] && passed=$((passed+1)) || detail+=" S3(rc=$rc)"
  # S4 relative override refused
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=bin/grep bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  err=$(cat "$dir/e")
  [[ $rc -eq 2 && "$err" == *GREP_PROVENANCE* ]] && passed=$((passed+1)) || detail+=" S4(rc=$rc err=${err:0:60})"
  # S5 missing override refused
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=/nonexistent/x bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  err=$(cat "$dir/e")
  [[ $rc -eq 2 && "$err" == *GREP_PROVENANCE* ]] && passed=$((passed+1)) || detail+=" S5(rc=$rc err=${err:0:60})"
  # S6 non-GNU stub refused
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP="$SCRATCH/run/stub-grep" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  err=$(cat "$dir/e")
  [[ $rc -eq 2 && "$err" == *GREP_PROVENANCE* ]] && passed=$((passed+1)) || detail+=" S6(rc=$rc err=${err:0:60})"
  # S7 override + echo
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1 bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  err=$(cat "$dir/e")
  [[ $rc -eq 0 && "$err" == *'path=/usr/bin/grep'* && "$err" == *'source=override'* ]] && passed=$((passed+1)) || detail+=" S7(rc=$rc err=${err:0:60})"
  # S8 default + echo
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" CHOUSA_GREP_PIN_ECHO=1 bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  err=$(cat "$dir/e")
  [[ $rc -eq 0 && "$err" == *'path=/usr/bin/grep'* && "$err" == *'source=default'* ]] && passed=$((passed+1)) || detail+=" S8(rc=$rc err=${err:0:60})"
  # S9 override beats shim
  : > "$SHIMDIR/trip-fn.log"
  rc=0; out=$("$TIMEOUT" 600 env -i HOME="$HOME" PATH="$SHIMDIR/bin:$CLEAN_PATH" BASH_ENV="$SHIMDIR/bash_env.sh" RESEARCH_GATE_GREP=/usr/bin/grep bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  err=$(cat "$dir/e")
  local t3=$(stat -c %s "$SHIMDIR/trip-fn.log") t4=$(stat -c %s "$SHIMDIR/trip-path.log")
  [[ $t3 -eq 0 && $t4 -eq 0 && $rc -eq 0 && "$err" == *'source=override'* ]] && passed=$((passed+1)) || detail+=" S9(trip=$t3/$t4 rc=$rc)"
  printf '  %-24s SWEEPS_PIN_MATCH=%d/9  fails:%s\n' "$(basename "$(dirname "$gate")")/$(sha256sum "$gate" | cut -c1-8)" "$passed" "${detail:- none}"
}
sweeps_counter "$GATE"
sweeps_counter "$BASE_GATE"
echo

echo "### 3. usage/--help ordering vs the refusal (landed gate)"
for args in "--help" "verify-sweeps"; do
  rc=0
  env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=bin/grep \
    "$TIMEOUT" 600 bash "$GATE" $args >"$SCRATCH/run/usage.out" 2>"$SCRATCH/run/usage.err" || rc=$?
  printf '  args=%-16s rc=%s stdout_head=%s stderr=%s\n' "$args" "$rc" \
    "$(head -c 60 "$SCRATCH/run/usage.out" | tr '\n' ' ')" \
    "$(tr '\n' '|' < "$SCRATCH/run/usage.err" | cut -c1-160)"
done
