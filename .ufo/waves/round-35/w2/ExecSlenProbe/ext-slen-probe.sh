#!/usr/bin/env bash
# round-35 R1 extension (v2): does the chunk matcher's span length come from its
# own parameter ($2) or from the caller's dynamically visible `span`?
#
# Extends .ufo/waves/round-35/repairs/slen-probe.sh over visible-span variants
# the round-35 repair claim does not cover:
#   a_none        no visible `span` at all
#   b_one         visible `span` of 1 byte
#   c_30000       visible `span` of 30000 bytes
#   d_samelen     visible `span` of exactly len($2)=32766 bytes, other content
#   e_arg         visible `span` == the argument (the real call path)
#   f_decoy       visible `span` = the committed probe's decoy (29 bytes)
#   g_callpath    call tok_span_offsets (the real call path), not the chunk
#                 matcher directly -- control for "no measured change today"
#
# Extraction is byte-identical to the committed probe so the two are comparable.
# Each case runs in a fresh subshell so `span` visibility is exactly the case.
#
# usage: ext-slen-probe.sh GATE
set -u
gate=$1
[[ -f $gate ]] || { echo "ext-slen-probe: gate not found: $gate" >&2; exit 2; }
tmp=$(mktemp -d "${TMPDIR:-/tmp}/ext-slen-XXXXXX")
trap 'rm -rf "$tmp"' EXIT
{
  sed -n '/^tok_hex_pattern()/,/^}/p' "$gate"
  sed -n '/^TOK_DIRECT_SPAN_MAX=/,/^token_matcher_require()/p' "$gate" | sed '$d'
} >"$tmp/matcher.sh"
bash -n "$tmp/matcher.sh" || { echo "ext-slen-probe: extracted block does not parse" >&2; exit 2; }

span_long=$(printf 'w%04d ' {1..5461})          # exactly 32766 bytes, dead zone
hay="lead ${span_long} tail"

run_case() { # LABEL VISLEN NOUNSET ENTRY
  local label=$1 vislen=$2 nounset=$3 entry=$4
  local out rc n first err
  errfile="$tmp/err.$label.$nounset"
  out=$( ( if [[ $nounset == 1 ]]; then set -u; else set +u; fi
      # shellcheck disable=SC1090
      source "$tmp/matcher.sh"
      case $vislen in
        none) unset span ;;
        arg)  span=$span_long ;;
        same) span=$(head -c 32766 /dev/zero | tr '\0' 'x') ;;
        decoy) span=decoy_span_of_other_length ;;
        *)    span=$(head -c "$vislen" /dev/zero | tr '\0' 'x') ;;
      esac
      PATH=/usr/bin:/bin "$entry" "$hay" "$span_long"
    ) 2>"$errfile" )
  rc=$?
  n=$(printf '%s' "$out" | grep -c . || true)
  first=${out%%$'\n'*}
  local e
  e=$(tr '\n' ' ' <"$errfile" 2>/dev/null | cut -c1-110)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$label" "$vislen" "$nounset" "$n" "${first:-<none>}" "$rc" "${e:-<none>}"
}

printf 'case\tvislen\tnounset\toffsets\tfirst\trc\tstderr\n'
run_case a_none       none  1 tok_span_offsets_chunk
run_case a_none       none  0 tok_span_offsets_chunk
run_case b_one        1     1 tok_span_offsets_chunk
run_case b_one        1     0 tok_span_offsets_chunk
run_case c_30000      30000 1 tok_span_offsets_chunk
run_case c_30000      30000 0 tok_span_offsets_chunk
run_case d_samelen    same  1 tok_span_offsets_chunk
run_case e_arg        arg   1 tok_span_offsets_chunk
run_case f_decoy      decoy 1 tok_span_offsets_chunk
run_case g_callpath   none  1 tok_span_offsets
run_case g_callpath   none  0 tok_span_offsets
run_case g_callpath   arg   1 tok_span_offsets
