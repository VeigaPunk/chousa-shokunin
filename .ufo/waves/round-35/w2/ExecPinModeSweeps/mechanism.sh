#!/usr/bin/env bash
# Mechanism detail: WHICH grep invocation is the pin's own version probe, and
# does the sweeps mode make any matcher-level grep call at all?
# Contrast: the same four environments on verify-claims, where the matcher
# does call grep.
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
GATE="$REPO/tools/research-gate.sh"
BASE_GATE="$SCRATCH/clone/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"
CLAIMS="$REPO/corpus/fixtures/claims-r2.jsonl"
TIMEOUT=/usr/bin/timeout
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
SHIMDIR="$SCRATCH/shim"

echo "### grep exec argv in each mode (landed gate)"
for mode in verify-sweeps verify-claims; do
  f="$SCRATCH/run/argv-$mode.txt"
  rm -f "$f"
  case "$mode" in
    verify-sweeps) inp="$FIXTURE";;
    verify-claims) inp="$CLAIMS";;
  esac
  env -i HOME="$HOME" PATH="$CLEAN_PATH" TMPDIR="$SCRATCH" \
    strace -f -qq -e trace=execve -o "$f" \
    "$TIMEOUT" 600 bash "$GATE" "$mode" "$inp" --root "$REPO" >/dev/null 2>&1
  printf -- '--- %s: ' "$mode"
  grep 'execve(".*grep' "$f" | sed -E 's/.*execve\("([^"]*)", \[(.*)\].*/\1 :: \2/' | tr '\n' ' '
  printf '\n'
done
echo

echo "### four environments x {sweeps, claims} x {landed, base}: tripwire + summary"
run4() { # MODE RECORD LABEL GATE PATH ENVSPEC
  local mode=$1 record=$2 label=$3 gate=$4 path=$5 envspec=$6
  local dir="$SCRATCH/run/x-$label-$mode"; rm -rf "$dir"; mkdir -p "$dir"
  : > "$SHIMDIR/trip-path.log"; : > "$SHIMDIR/trip-fn.log"
  local rc=0
  # shellcheck disable=SC2086
  env -i HOME="$HOME" PATH="$path" TMPDIR="$SCRATCH" \
    ${envspec:+$(printf '%s' "$envspec" | tr '|' ' ')} \
    "$TIMEOUT" 600 bash "$gate" "$mode" "$record" --root "$REPO" \
    >"$dir/out" 2>"$dir/err" || rc=$?
  local sum
  if [[ "$mode" == verify-sweeps ]]; then sum=$(grep -m1 '^VERIFIED_SWEEPS=' "$dir/out" || true)
  else sum=$(grep -m1 '^VERDICT_BEARING_CLAIMS=' "$dir/out" || true); fi
  printf '%-8s %-14s rc=%s trip_path=%-4s trip_fn=%-4s summary=%s\n' \
    "$label" "$mode" "$rc" "$(stat -c %s "$SHIMDIR/trip-path.log")" \
    "$(stat -c %s "$SHIMDIR/trip-fn.log")" "$sum"
}
for g in landed base; do
  [[ $g == landed ]] && GP="$GATE" || GP="$BASE_GATE"
  run4 verify-sweeps "$FIXTURE" "$g-e1" "$GP" "$CLEAN_PATH" ""
  run4 verify-sweeps "$FIXTURE" "$g-e2" "$GP" "$SHIMDIR/bin:$CLEAN_PATH" ""
  run4 verify-sweeps "$FIXTURE" "$g-e3" "$GP" "$CLEAN_PATH" "BASH_ENV=$SHIMDIR/bash_env.sh"
  run4 verify-sweeps "$FIXTURE" "$g-e4" "$GP" "$SCRATCH/nogrepbin" ""
  run4 verify-claims "$CLAIMS" "$g-e1" "$GP" "$CLEAN_PATH" ""
  run4 verify-claims "$CLAIMS" "$g-e2" "$GP" "$SHIMDIR/bin:$CLEAN_PATH" ""
  run4 verify-claims "$CLAIMS" "$g-e3" "$GP" "$CLEAN_PATH" "BASH_ENV=$SHIMDIR/bash_env.sh"
  run4 verify-claims "$CLAIMS" "$g-e4" "$GP" "$SCRATCH/nogrepbin" ""
  echo
done
