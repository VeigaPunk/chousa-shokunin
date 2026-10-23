#!/usr/bin/env bash
# Main matrix: slice/walk/growappend/grow x 4 sizes x 2 locales, 3 rounds each.
set -u
cd "$(dirname "$0")"
out=${1:-matrix_main.tsv}
: > "$out"
for loc in C en_US.UTF-8; do
  for mode in slice walk growappend grow; do
    for size in 500 4096 16384 65536; do
      LC_ALL=$loc timeout 900 bash bench.sh "$mode" "line_${size}.jsonl" 3 \
        | grep -v '^probe' >> "$out"
    done
  done
done
wc -l "$out"
