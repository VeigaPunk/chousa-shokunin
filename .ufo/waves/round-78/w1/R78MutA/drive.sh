#!/bin/bash
# Run the frozen round-78 forge battery against each closure-removal twin.
set -u
S=/fast/scratch/hyaku/chousa-r78/R78MutA
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
FB=$LANE/corpus/evidence/round78/forge-battery.py
mkdir -p "$S/fb"
for t in M1 M1B M2 M3 M4 M5; do
  out="$S/fb/$t.txt"
  python3 -B "$FB" --battery "$S/mirror/$t/corpus/evidence/round78/matrix-battery-v5.py" \
      --work "$S/fb/$t.w" > "$out" 2> "$S/fb/$t.err"
  echo "== $t exit=$?"
  grep -E '^(FORGER|POSITIVE|FORGE_BATTERY)' "$out"
done
# Frozen v5 closure-removal flags, direct (not through forge-battery).
V5=$LANE/corpus/evidence/round78/matrix-battery-v5.py
LEGIT=$LANE/corpus/evidence/round76/loader-matrix-v3.py
for flag in no-permute no-content; do
  python3 -B "$V5" --matrix "$LEGIT" --work "$S/flags/$flag.w" --$flag \
      > "$S/flags-$flag.txt" 2> "$S/flags-$flag.err"
  echo "== frozen-v5 --$flag exit=$?"
  tail -3 "$S/flags-$flag.txt"
done
