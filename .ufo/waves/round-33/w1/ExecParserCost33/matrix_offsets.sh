#!/usr/bin/env bash
# Offset-dependence matrix: fixed0/fixedend/smallloop at 4096 and 65536, C locale, 2 rounds.
set -u
cd "$(dirname "$0")"
out=${1:-matrix_offsets.tsv}
: > "$out"
for mode in fixed0 fixedend smallloop; do
  for size in 4096 65536; do
    LC_ALL=C timeout 900 bash bench.sh "$mode" "line_${size}.jsonl" 2 \
      | grep -v '^probe' >> "$out"
  done
done
wc -l "$out"
