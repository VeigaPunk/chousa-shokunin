#!/usr/bin/env bash
# round-35 R1 probe: does the chunk matcher read its span length from the
# parameter or from the caller's dynamic scope?
#
# `local hay=$1 span=$2 slen=${#span}` expands every right-hand side BEFORE it
# assigns any of them, so the one-statement form reads the *visible* `span`
# (bash's dynamic scope: the caller's local, or a global), not `$2`. In the
# landed call path the caller's `span` happened to be the same value, so no
# measured behaviour changed — this probe shows the latent failure and that the
# repair closes it, by calling the chunk matcher directly with a visible `span`
# of a different length.
#
# usage: slen-probe.sh GATE   -> SLEN_PROBE offsets=N (N=1 repaired, N=0 before)
# Exit 0 when exactly one offset is reported (the repaired behaviour).
set -u
gate=$1
[[ -f $gate ]] || { echo "slen-probe: gate not found: $gate" >&2; exit 2; }
tmp=$(mktemp -d "${TMPDIR:-/tmp}/slen-XXXXXX")
trap 'rm -rf "$tmp"' EXIT
{
  sed -n '/^tok_hex_pattern()/,/^}/p' "$gate"
  sed -n '/^TOK_DIRECT_SPAN_MAX=/,/^token_matcher_require()/p' "$gate" | sed '$d'
} >"$tmp/matcher.sh"
bash -n "$tmp/matcher.sh" || { echo "slen-probe: extracted block does not parse" >&2; exit 2; }
# shellcheck disable=SC1090
source "$tmp/matcher.sh"
span_long=$(printf 'w%04d ' {1..5461})          # exactly 32766 bytes, dead zone
hay="lead ${span_long} tail"
span=decoy_span_of_other_length                  # visible dynamic-scope span
out=$(PATH=/usr/bin:/bin tok_span_offsets_chunk "$hay" "$span_long")
n=$(printf '%s' "$out" | grep -c . || true)
printf 'SLEN_PROBE offsets=%s first=%s\n' "$n" "${out%%$'\n'*}"
[[ $n -eq 1 ]]
