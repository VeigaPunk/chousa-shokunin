#!/usr/bin/env bash
# Foreground load-run: 4 recorded `timeout 120 yes` PIDs, counter, kill by recorded PID.
set -u
cd /home/vgpnk/Projects/shokunin/chousa-shokunin || exit 9
OUT=.ufo/waves/round-33/w2/RerunC1b
SEED=$1
TAG=$2
PIDS=()
for i in 1 2 3 4; do timeout 120 yes >/dev/null & PIDS+=("$!"); done
{
  printf 'load_pids=%s\n' "${PIDS[*]}"
  ps -o pid,ppid,pcpu,comm -p "$(IFS=,; echo "${PIDS[*]}")"
  uptime
} > "$OUT/$TAG.load" 2>&1
C1_TMP=/fast/scratch/hyaku/chousa-r33/w2/RerunC1b TMPDIR=/fast/scratch/hyaku/chousa-r33/w2/RerunC1b \
  timeout 900 python3 corpus/evidence/round33/c1-count-v2.py --gate tools/research-gate.sh \
  --seed "$SEED" --receipt "$OUT/$TAG.json" > "$OUT/$TAG.out" 2> "$OUT/$TAG.err"
rc=$?
for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null; done
for p in "${PIDS[@]}"; do wait "$p" 2>/dev/null; done
{
  printf 'counter_rc=%s\n' "$rc"
  ps -o pid,comm -p "$(IFS=,; echo "${PIDS[*]}")" 2>&1 || true
} >> "$OUT/$TAG.load"
exit "$rc"
