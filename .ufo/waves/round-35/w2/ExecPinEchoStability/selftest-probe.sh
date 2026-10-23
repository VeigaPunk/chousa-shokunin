#!/usr/bin/env bash
# selftest-probe.sh — the --selftest mode under {base, land} x {echo off, echo on}.
set -uo pipefail
SC=/tmp/hyaku/chousa-r35/w2/ExecPinEchoStability
L=$SC/fleet/chousa-shokunin
G=$L/tools/research-gate.sh
OUT=$SC/out-selftest; rm -rf "$OUT"; mkdir -p "$OUT"

run() { # label gatefile echo
  local label=$1 gatefile=$2 echo_flag=$3
  cp -f "$gatefile" "$G"
  local -a E=()
  [[ $echo_flag == on ]] && E=(CHOUSA_GREP_PIN_ECHO=1)
  ( cd "$L" && env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=/tmp TMPDIR=/tmp \
      LANG=C.UTF-8 LC_ALL=C.UTF-8 CHOUSA_NOW_EPOCH=1761000000 \
      "${E[@]+"${E[@]}"}" bash tools/research-gate.sh --selftest ) \
      >"$OUT/$label.out" 2>"$OUT/$label.err"
  echo $? >"$OUT/$label.rc"
}

run base-echooff "$SC/base-gate.sh" off
run land-echooff "$SC/land-gate.sh" off
run land-echoon  "$SC/land-gate.sh" on

cp -f "$SC/land-gate.sh" "$G"
{
for f in "$OUT"/*.rc; do
  b=${f%.rc}; n=$(basename "$b")
  printf '%-18s rc=%s  stdout_tail=%s  stderr_bytes=%s\n' "$n" "$(cat "$f")" \
    "$(tail -c 200 "$b.out" | tr '\n' '|')" "$(wc -c <"$b.err")"
done
} | tee "$OUT/summary.txt"
