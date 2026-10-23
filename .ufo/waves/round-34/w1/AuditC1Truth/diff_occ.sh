#!/usr/bin/env bash
# Occurrence oracle: enumerates the boundary-delimited occurrences of a span in
# a source file using the GATE's own code path (tok_span_all, research-gate.sh
# :1582-1607), and prints the same information the gate prints ("L1 L2" per
# delimited occurrence).
#
# Usage: diff_occ.sh <source-file> <span-file>
#   the span file holds the raw span bytes
set -u
export LC_ALL=C
cd "$(dirname "$0")"
# shellcheck disable=SC1091
source ./tok.sh
# shellcheck disable=SC1091
source ./tok_all.sh
count_nl() { local n; n=$(printf '%s' "$1" | tr -dc '\n' | wc -c); n=${n//[[:space:]]/}; printf '%d' "$n"; }
src=$1
spanf=$2
hay=$(cat -- "$src"; printf x); hay=${hay%x}
span=$(cat -- "$spanf"; printf x); span=${span%x}
tok_span_all "$hay" "$span"
