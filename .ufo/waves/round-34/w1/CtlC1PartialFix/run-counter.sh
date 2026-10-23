#!/usr/bin/env bash
set -eu
printf 'RUN_PID=%s GATE=%s SEED=%s\n' "$$" "$1" "$2"
export C1_TMP=/fast/scratch/hyaku/chousa-r34/w1/CtlC1PartialFix
export TMPDIR=$C1_TMP
exec prlimit --as=2147483648 --nproc=65536 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py --gate "$1" --seed "$2" --receipt "$3"
