#!/bin/bash
S=/fast/scratch/hyaku/chousa-r97/R97SentinelC1; R=$S/repo
cd "$R" || exit 9
mkdir -p "$S/work-full"
stat -c 'idx_before %y %s' .git/index > "$S/full-idx.txt"; sha256sum .git/index >> "$S/full-idx.txt"
git -C "$R" status --porcelain > "$S/full-status-before.txt"
timeout 1500 strace -f -qq -e trace=file,network,process -o "$S/full-battery-strace.txt" python3 -B corpus/evidence/round97/selftest-controls-r97.py --root . --work "$S/work-full" > "$S/full-battery-stdout.txt" 2> "$S/full-battery-stderr.txt"
echo "full_battery_exit=$?" > "$S/full-exit.txt"
stat -c 'idx_after %y %s' .git/index >> "$S/full-idx.txt"; sha256sum .git/index >> "$S/full-idx.txt"
git -C "$R" status --porcelain > "$S/full-status-after.txt"
echo done >> "$S/full-exit.txt"
