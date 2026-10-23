#!/usr/bin/env bash
# multi-occurrence differential: hay holds the long span twice.
# Reports every offset each gate's chunk matcher emits for each visible-span case.
set -u
tmp=$(mktemp -d "${TMPDIR:-/tmp}/mo-XXXXXX")
trap 'rm -rf "$tmp"' EXIT
S=$(printf 'w%04d ' {1..5461})   # 32766 bytes
hay="lead ${S} mid ${S} tail"

for g in "$@"; do
  {
    sed -n '/^tok_hex_pattern()/,/^}/p' "$g"
    sed -n '/^TOK_DIRECT_SPAN_MAX=/,/^token_matcher_require()/p' "$g" | sed '$d'
  } >"$tmp/m.sh"
  echo "=== $g"
  for vis in none 1 30000 32766 arg; do
    out=$( ( set +u
        # shellcheck disable=SC1090
        source "$tmp/m.sh"
        case $vis in
          none) unset span ;;
          arg)  span=$S ;;
          *)    span=$(head -c "$vis" /dev/zero | tr '\0' 'x') ;;
        esac
        PATH=/usr/bin:/bin tok_span_offsets_chunk "$hay" "$S"
      ) 2>&1 )
    n=$(printf '%s' "$out" | grep -c . || true)
    printf '  vis=%-6s offsets=%s list=[%s]\n' "$vis" "$n" \
      "$(printf '%s' "$out" | tr '\n' ',')"
  done
done
