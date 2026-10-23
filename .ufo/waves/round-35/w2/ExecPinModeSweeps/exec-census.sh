#!/usr/bin/env bash
# Exec census: which binaries does `verify-sweeps` actually exec?
# Proves (or refutes) that the sweeps mode touches grep at all, which decides
# whether a PATH/BASH_ENV grep shim can influence its verdict at all.
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
GATE="$REPO/tools/research-gate.sh"
BASE_GATE="$SCRATCH/clone/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"
TIMEOUT=/usr/bin/timeout
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin

census() { # NAME GATE MODE
  local name=$1 gate=$2 mode=$3
  local out="$SCRATCH/run/census-$name.txt"
  rm -f "$out"
  env -i HOME="$HOME" PATH="$CLEAN_PATH" TMPDIR="$SCRATCH" \
    strace -f -qq -e trace=execve -o "$out" \
    "$TIMEOUT" 600 bash "$gate" "$mode" "$FIXTURE" --root "$REPO" >/dev/null 2>&1
  printf '=== census %s (%s) ===\n' "$name" "$mode"
  printf 'grep_execs=%s\n' "$(grep -c 'execve(".*grep' "$out")"
  grep 'execve(".*grep' "$out" | sed -E 's/^.*execve\("([^"]*)".*/  \1/' | sort | uniq -c
  printf 'distinct_binaries=%s\n' \
    "$(grep -o 'execve("[^"]*"' "$out" | sed 's/execve("//;s/"//' | sed 's|.*/||' | sort -u | tr '\n' ' ')"
}
census landed-sweeps "$GATE" verify-sweeps
census base-sweeps   "$BASE_GATE" verify-sweeps
census landed-claims "$GATE" verify-claims
census base-claims   "$BASE_GATE" verify-claims
