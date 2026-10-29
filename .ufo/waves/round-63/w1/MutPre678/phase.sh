#!/usr/bin/env bash
# MutPre678 — run the frozen c1-battery on each mutant listed in $SCRATCH/<LIST> (name<TAB>legs[,..]).
#   usage: phase.sh LIST_FILE TAG [PAR]
#   TAG `part` uses the legs in the list (BATTERY=PARTIAL); TAG `full` runs every leg (no --only).
# Per mutant: $SCRATCH/logs/<name>.<TAG>.log and $SCRATCH/summary/<name>.<TAG>.txt (KILLED|SURVIVED + failing legs).
set -u
SCRATCH=/fast/scratch/hyaku/chousa-r63/MutPre678
BAT=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round63/c1-battery.py
LIST="$1"; TAG="$2"; PAR="${3:-2}"
export TMPDIR="$SCRATCH"
mkdir -p "$SCRATCH/logs" "$SCRATCH/summary"

one() {
  name="$1"; legs="$2"
  W="$SCRATCH/w-$TAG-$name"; L="$SCRATCH/logs/$name.$TAG.log"; S="$SCRATCH/summary/$name.$TAG.txt"
  rm -rf "$W"
  if [ "$TAG" = "full" ]; then extra=""; else extra="--only $legs"; fi
  # shellcheck disable=SC2086
  python3 -B "$BAT" --tool "$SCRATCH/mutants/$name.py" --fleet /home/vgpnk/Projects/shokunin \
      --work "$W" --jobs 2 $extra > "$L" 2>&1
  rc=$?
  fails=$(grep -E '^LEG .* FAIL ' "$L" | awk '{print $2}' | paste -sd, -)
  bat=$(grep -E '^CLEAN=' "$L" | tail -1)
  if [ -n "$fails" ]; then v=KILLED; else v=SURVIVED; fi
  printf '%s\t%s\trc=%s\tfailing_legs=%s\t%s\n' "$name" "$v" "$rc" "${fails:--}" "$bat" > "$S"
  cat "$S"
}
export -f one
export SCRATCH BAT TAG

while IFS=$'\t' read -r name legs; do
  [ -n "$name" ] || continue
  printf '%s\0%s\0' "$name" "$legs"
done < "$LIST" | xargs -0 -n 2 -P "$PAR" bash -c 'one "$0" "$1"'
echo "PHASE $TAG DONE"
