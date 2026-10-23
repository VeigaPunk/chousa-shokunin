#!/usr/bin/env bash
# Sweep the LENGTH of the caller-visible `span` and record how many offsets the
# chunk matcher reports. Characterises exactly which visible length makes the
# base gate agree with the landed gate.
#
# usage: slen-sweep.sh GATE
set -u
gate=$1
[[ -f $gate ]] || { echo "slen-sweep: gate not found: $gate" >&2; exit 2; }
tmp=$(mktemp -d "${TMPDIR:-/tmp}/sweep-XXXXXX")
trap 'rm -rf "$tmp"' EXIT
{
  sed -n '/^tok_hex_pattern()/,/^}/p' "$gate"
  sed -n '/^TOK_DIRECT_SPAN_MAX=/,/^token_matcher_require()/p' "$gate" | sed '$d'
} >"$tmp/matcher.sh"
bash -n "$tmp/matcher.sh" || { echo "slen-sweep: extracted block does not parse" >&2; exit 2; }
span_long=$(printf 'w%04d ' {1..5461})   # exactly 32766 bytes
hay="lead ${span_long} tail"

printf 'vislen\toffsets\tfirst\n'
for L in 0 1 2 100 4096 16384 32763 32764 32765 32766 32767 32768 40000; do
  out=$( ( set +u
      source "$tmp/matcher.sh"
      span=$(head -c "$L" /dev/zero | tr '\0' 'x')
      PATH=/usr/bin:/bin tok_span_offsets_chunk "$hay" "$span_long"
    ) 2>/dev/null )
  n=$(printf '%s' "$out" | grep -c . || true)
  printf '%s\t%s\t%s\n' "$L" "$n" "${out%%$'\n'*:-<none>}"
done
