#!/usr/bin/env bash
# Differential oracle: uses the gate's OWN tok_left_ok/tok_right_ok/tok_word_char
# (extracted verbatim from tools/research-gate.sh:1506-1551 into tok.sh) and
# prints one verdict per case read from cases.tsv.
# Each field is a literal bash escape string (e.g. \x61\x0a), decoded with
# printf '%b'. A 'Z' sentinel is appended inside the command substitution so a
# field ending in a newline survives (command substitution strips trailing
# newlines of its own output).
set -u
export LC_ALL=C
cd "$(dirname "$0")"
# shellcheck disable=SC1091
source ./tok.sh
dec() { local v; v=$(printf '%b' "$1"; printf 'Z'); printf '%s' "${v%Z}"; }
while IFS='|' read -r eb es ea; do
  before=$(dec "$eb"; printf 'Z'); before=${before%Z}
  span=$(dec "$es"; printf 'Z'); span=${span%Z}
  after=$(dec "$ea"; printf 'Z'); after=${after%Z}
  if tok_left_ok "$before" "$span"; then l=1; else l=0; fi
  if tok_right_ok "$after" "$span"; then r=1; else r=0; fi
  if tok_word_char "${span:0:1}"; then w=1; else w=0; fi
  printf '%s %s %s\n' "$l" "$r" "$w"
done < cases.tsv
