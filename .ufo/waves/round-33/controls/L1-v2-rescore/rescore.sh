#!/usr/bin/env bash
# L1 re-score of every wave-1 C1 control gate under counter v2 (design v2, e3e24ec8), before any
# candidate is scored. Usage: rescore.sh  (lane root = cwd). Two seeds per gate, receipts beside.
set -u
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
OUT=$LANE/.ufo/waves/round-33/controls/L1-v2-rescore
COUNTER=$LANE/corpus/evidence/round33/c1-count-v2.py
export C1_TMP=/fast/scratch/hyaku/chousa-r33/L1/rescore
mkdir -p "$C1_TMP"
cd "$LANE" || exit 2
run_one() { # GATE SEED
  local g=$1 s=$2 seat name
  seat=$(basename "$(dirname "$g")"); name=$(basename "$g" .sh)
  timeout 900 python3 "$COUNTER" --gate "$g" --seed "$s" --receipt "$OUT/$seat--$name-s$s.json" \
    > "$OUT/$seat--$name-s$s.out" 2>&1
  printf '%s %s %s rc=%s %s\n' "$seat" "$name" "$s" "$?" "$(head -1 "$OUT/$seat--$name-s$s.out")"
}
export -f run_one; export OUT COUNTER
for g in .ufo/waves/round-33/w1/CtlC1*/*.sh; do
  [[ $(stat -c %s "$g") -gt 200000 ]] || continue
  for s in 3341 3342; do printf '%s %s\n' "$g" "$s"; done
done | xargs -P 8 -L 1 bash -c 'run_one "$0" "$1"' | sort > "$OUT/summary.txt"
cat "$OUT/summary.txt"
