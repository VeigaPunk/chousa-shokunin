#!/usr/bin/env bash
# drift-probe.sh — how CHOUSA_GREP_PIN_ECHO interacts with --pin/--drift.
SC=/tmp/hyaku/chousa-r35/w2/ExecPinEchoStability
L=$SC/fleet/chousa-shokunin
G=$L/tools/research-gate.sh
cp -f "$SC/land-gate.sh" "$G"
OUT=$SC/out-drift; rm -rf "$OUT"; mkdir -p "$OUT"

run() { # ECHO BASELINE LABEL
  local echo_flag=$1 baseline=$2 label=$3
  local -a E=()
  [[ $echo_flag == on ]] && E=(CHOUSA_GREP_PIN_ECHO=1)
  ( cd "$L" && env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=/tmp TMPDIR=/tmp \
      LANG=C.UTF-8 LC_ALL=C.UTF-8 CHOUSA_NOW_EPOCH=1761000000 \
      "${E[@]+"${E[@]}"}" bash tools/research-gate.sh --drift "$baseline" ) \
      >"$OUT/$label.out" 2>"$OUT/$label.err"
  echo $? >"$OUT/$label.rc"
}

# pin twice, once per flag state
for e in off on; do
  ( cd "$L" && env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=/tmp TMPDIR=/tmp \
      LANG=C.UTF-8 LC_ALL=C.UTF-8 CHOUSA_NOW_EPOCH=1761000000 \
      $( [ $e = on ] && echo CHOUSA_GREP_PIN_ECHO=1 ) \
      bash tools/research-gate.sh --pin "$OUT/$e.baseline" ) >"$OUT/$e.pin.out" 2>"$OUT/$e.pin.err"
  echo $? >"$OUT/$e.pin.rc"
done

run off "$OUT/on.baseline"  "drift_onbase_echooff"
run on  "$OUT/on.baseline"  "drift_onbase_echoon"
run on  "$OUT/off.baseline" "drift_offbase_echoon"
run off "$OUT/off.baseline" "drift_offbase_echooff"

{
for f in "$OUT"/*.rc; do
  b=${f%.rc}; n=$(basename "$b")
  printf '%-24s rc=%s\n' "$n" "$(cat "$f")"
  printf '   stdout: %s\n' "$(cat "$b.out" 2>/dev/null | tr '\n' '|')"
  printf '   stderr: %s\n' "$(cat "$b.err" 2>/dev/null | tr '\n' '|')"
done
} >"$OUT/summary.txt"
cat "$OUT/summary.txt"
