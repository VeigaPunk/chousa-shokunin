#!/usr/bin/env bash
# MutPre678 — run the frozen c1-battery on one mutant.
# Usage: run-one.sh MUTANT_NAME <legs|CLEAN,D09,D10> <tag>
# Writes $SCRATCH/logs/<name>.<tag>.log
set -u
NAME="$1"; LEGS="$2"; TAG="$3"
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
BAT="$LANE/corpus/evidence/round63/c1-battery.py"
SCRATCH=/fast/scratch/hyaku/chousa-r63/MutPre678
MUT="$SCRATCH/mutants/$NAME.py"
export TMPDIR="$SCRATCH"
mkdir -p "$SCRATCH/logs"
W="$SCRATCH/w-$TAG-$NAME"
L="$SCRATCH/logs/$NAME.$TAG.log"
rm -rf "$W"
python3 -B "$BAT" --tool "$MUT" --fleet /home/vgpnk/Projects/shokunin --work "$W" --jobs 2 --only "$LEGS" > "$L" 2>&1
rc=$?
echo "== $NAME [$TAG] rc=$rc"
grep -E '^LEG |^CLEAN=|^BATTERY=' "$L"
