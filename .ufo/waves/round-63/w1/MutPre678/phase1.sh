#!/usr/bin/env bash
# MutPre678 — phase 1: run the frozen battery (partial legs) on every mutant, in parallel.
set -u
SCRATCH=/fast/scratch/hyaku/chousa-r63/MutPre678
HERE=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-63/w1/MutPre678
export TMPDIR="$SCRATCH"
mkdir -p "$SCRATCH/logs" "$SCRATCH/summary"
PAR="${PAR:-4}"

run_mutant() {
  name="$1"; legs="$2"; tag="${3:-part}"
  W="$SCRATCH/w-$tag-$name"
  L="$SCRATCH/logs/$name.$tag.log"
  rm -rf "$W"
  python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round63/c1-battery.py \
     --tool "$SCRATCH/mutants/$name.py" --fleet /home/vgpnk/Projects/shokunin \
     --work "$W" --jobs 2 --only "$legs" > "$L" 2>&1
  rc=$?
  # a mutant is KILLED if some run leg reports FAIL
  if grep -qE '^LEG .* FAIL ' "$L"; then
    verdict=KILLED
  elif grep -qE '^LEG ' "$L"; then
    verdict=SURVIVED
  else
    verdict=ERROR
  fi
  printf '%s\t%s\t%s\t%s\n' "$name" "$verdict" "$legs" "$(grep -E '^LEG .* FAIL ' "$L" | sed 's/^LEG \([A-Z0-9]*\) .* FAIL \(.*\)$/\1:\2/' | tr '\n' ';')" \
     > "$SCRATCH/summary/$name.$tag.tsv"
}
export -f run_mutant
export SCRATCH

while IFS=$'\t' read -r name legs; do
  echo "$name	$legs"
done < "$SCRATCH/legs.tsv" | xargs -P "$PAR" -I{} bash -c '
  IFS=$'"'"'\t'"'"' read -r n l <<< "{}"
  run_mutant "$n" "$l" part
'
echo "PHASE1 DONE"
