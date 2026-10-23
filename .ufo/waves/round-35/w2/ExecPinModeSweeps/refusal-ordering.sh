#!/usr/bin/env bash
# Refusal ordering + corrected sweeps-mode C1 analogue (S9 with the echo flag).
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
PINNED="$REPO/.ufo/waves/round-35/w2/ExecPinModeSweeps/pinned/tools/research-gate.sh"
BASE_GATE="$SCRATCH/clone/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
SHIMDIR="$SCRATCH/shim"

echo "### refusal ordering: bad override + a record that does not exist"
for g in "$PINNED" "$BASE_GATE"; do
  rc=0
  env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=bin/grep \
    /usr/bin/timeout 600 bash "$g" verify-sweeps "$SCRATCH/no-such-record.md" --root "$REPO" \
    >"$SCRATCH/run/ord.out" 2>"$SCRATCH/run/ord.err" || rc=$?
  printf '  %-10s rc=%s stderr=%s\n' "$(sha256sum "$g" | cut -c1-8)" "$rc" \
    "$(tr '\n' '|' < "$SCRATCH/run/ord.err" | cut -c1-140)"
done
echo

echo "### refusal ordering: bad override + usage error (missing record arg)"
for g in "$PINNED" "$BASE_GATE"; do
  rc=0
  env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=bin/grep \
    /usr/bin/timeout 600 bash "$g" verify-sweeps \
    >"$SCRATCH/run/ord2.out" 2>"$SCRATCH/run/ord2.err" || rc=$?
  printf '  %-10s rc=%s stderr=%s\n' "$(sha256sum "$g" | cut -c1-8)" "$rc" \
    "$(tr '\n' '|' < "$SCRATCH/run/ord2.err" | cut -c1-140)"
done
echo

echo "### corrected sweeps-mode C1 analogue (S9 now sets CHOUSA_GREP_PIN_ECHO=1)"
sc() { # gate
  local gate=$1 passed=0 fails="" dir="$SCRATCH/run/sc2"
  rm -rf "$dir"; mkdir -p "$dir"
  : > "$SHIMDIR/trip-path.log"; : > "$SHIMDIR/trip-fn.log"
  local rc out err ref_sum t
  rc=0; out=$(/usr/bin/timeout 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  ref_sum=$(grep -m1 '^VERIFIED_SWEEPS=' <<<"$out" || true)
  # S1
  rc=0; out=$(/usr/bin/timeout 600 env -i HOME="$HOME" PATH="$SHIMDIR/bin:$CLEAN_PATH" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  t=$(stat -c %s "$SHIMDIR/trip-path.log")
  [[ $t -eq 0 && $rc -eq 0 && $(grep -m1 '^VERIFIED_SWEEPS=' <<<"$out") == "$ref_sum" ]] && passed=$((passed+1)) || fails+=" S1(t=$t rc=$rc)"
  # S2
  : > "$SHIMDIR/trip-fn.log"
  rc=0; out=$(/usr/bin/timeout 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" BASH_ENV="$SHIMDIR/bash_env.sh" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  t=$(stat -c %s "$SHIMDIR/trip-fn.log")
  [[ $t -eq 0 && $rc -eq 0 && $(grep -m1 '^VERIFIED_SWEEPS=' <<<"$out") == "$ref_sum" ]] && passed=$((passed+1)) || fails+=" S2(t=$t rc=$rc)"
  # S3
  rc=0; out=$(/usr/bin/timeout 600 env -i HOME="$HOME" PATH="$SCRATCH/nogrepbin" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" 2>"$dir/e") || rc=$?
  [[ $rc -eq 0 && $(grep -m1 '^VERIFIED_SWEEPS=' <<<"$out") == "$ref_sum" ]] && passed=$((passed+1)) || fails+=" S3(rc=$rc)"
  # S4 relative
  rc=0; /usr/bin/timeout 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=bin/grep bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" >/dev/null 2>"$dir/e" || rc=$?
  [[ $rc -eq 2 && $(cat "$dir/e") == *GREP_PROVENANCE* ]] && passed=$((passed+1)) || fails+=" S4(rc=$rc)"
  # S5 missing
  rc=0; /usr/bin/timeout 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=/nonexistent/x bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" >/dev/null 2>"$dir/e" || rc=$?
  [[ $rc -eq 2 && $(cat "$dir/e") == *GREP_PROVENANCE* ]] && passed=$((passed+1)) || fails+=" S5(rc=$rc)"
  # S6 non-GNU stub
  rc=0; /usr/bin/timeout 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP="$SCRATCH/run/stub-grep" bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" >/dev/null 2>"$dir/e" || rc=$?
  [[ $rc -eq 2 && $(cat "$dir/e") == *GREP_PROVENANCE* ]] && passed=$((passed+1)) || fails+=" S6(rc=$rc)"
  # S7 override + echo
  rc=0; /usr/bin/timeout 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1 bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" >/dev/null 2>"$dir/e" || rc=$?
  err=$(cat "$dir/e")
  [[ $rc -eq 0 && "$err" == *'path=/usr/bin/grep'* && "$err" == *'source=override'* ]] && passed=$((passed+1)) || fails+=" S7(rc=$rc err=${err:0:50})"
  # S8 default + echo
  rc=0; /usr/bin/timeout 600 env -i HOME="$HOME" PATH="$CLEAN_PATH" CHOUSA_GREP_PIN_ECHO=1 bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" >/dev/null 2>"$dir/e" || rc=$?
  err=$(cat "$dir/e")
  [[ $rc -eq 0 && "$err" == *'path=/usr/bin/grep'* && "$err" == *'source=default'* ]] && passed=$((passed+1)) || fails+=" S8(rc=$rc err=${err:0:50})"
  # S9 override beats shim (echo on)
  : > "$SHIMDIR/trip-fn.log"; : > "$SHIMDIR/trip-path.log"
  rc=0; /usr/bin/timeout 600 env -i HOME="$HOME" PATH="$SHIMDIR/bin:$CLEAN_PATH" BASH_ENV="$SHIMDIR/bash_env.sh" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1 bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" >/dev/null 2>"$dir/e" || rc=$?
  err=$(cat "$dir/e"); local tf=$(stat -c %s "$SHIMDIR/trip-fn.log") tp=$(stat -c %s "$SHIMDIR/trip-path.log")
  [[ $tf -eq 0 && $tp -eq 0 && $rc -eq 0 && "$err" == *'source=override'* ]] && passed=$((passed+1)) || fails+=" S9(tf=$tf tp=$tp rc=$rc)"
  printf '  %-16s SWEEPS_PIN_MATCH=%d/9 fails:%s\n' "$(sha256sum "$gate" | cut -c1-8)" "$passed" "${fails:- none}"
}
sc "$PINNED"
sc "$BASE_GATE"
