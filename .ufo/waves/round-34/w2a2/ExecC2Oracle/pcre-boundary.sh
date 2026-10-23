#!/usr/bin/env bash
# Measure the one-pattern (direct) matcher's ceiling on this host:
# for span lengths L, build the \xHH pattern of the whole span and try
# grep -a -z -b -o -P -- "$pattern" on a file that contains the span.
# Prints one line per length: L pattern_bytes rc stderr_first_line
set -u
WORK=$(mktemp -d /fast/scratch/hyaku/chousa-r34-a2/w2/ExecC2Oracle/tmp/pcreb.XXXXXX)
trap 'rm -rf "$WORK"' EXIT
for L in 32760 32762 32763 32764 32765 32766 32767 32768 32769; do
  python3 - "$WORK" "$L" <<'PY'
import sys
work, L = sys.argv[1], int(sys.argv[2])
span = ("ab" * (L // 2 + 1))[:L].encode()
open(work + "/hay.bin", "wb").write(b"x " + span + b" y\n")
open(work + "/span.bin", "wb").write(span)
PY
  pat=$(od -An -v -tx1 < "$WORK/span.bin" | tr -d ' \n' | sed 's/../\\x&/g')
  err=$(grep -a -z -b -o -P -- "$pat" "$WORK/hay.bin" 2>"$WORK/err.txt" >/dev/null; echo $?)
  printf 'L=%d pattern_bytes=%d rc=%s stderr=%s\n' "$L" "$((L*4))" "$err" "$(head -c 120 "$WORK/err.txt" | tr '\n' ' ')"
done
