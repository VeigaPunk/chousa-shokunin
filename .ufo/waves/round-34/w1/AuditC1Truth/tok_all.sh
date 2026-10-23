tok_span_all() { # HAY SPAN -> stdout: "L1 L2" per boundary-delimited occurrence
  # rc0: at least one delimited occurrence; rc1: none. Same matcher and
  # boundary rules as tok_span_at, but every delimited occurrence is emitted
  # (tok_span_at stops at the first) with its 1-based start and end lines.
  local LC_ALL=C
  export LC_ALL
  local hay=$1 span=$2 before after occurrence offset regex='' i c hex l1 l2 found=0
  [[ -n $span ]] || return 1
  for ((i = 0; i < ${#span}; i++)); do
    c=${span:i:1}
    printf -v hex '%02x' "'$c"
    regex+="\\x$hex"
  done
  while IFS= read -r -d '' occurrence; do
    offset=${occurrence%%:*}
    before=${hay:0:offset}
    after=${hay:offset+${#span}}
    if tok_left_ok "$before" "$span" && tok_right_ok "$after" "$span"; then
      found=1
      l1=$(( $(count_nl "$before") + 1 ))
      l2=$(( l1 + $(count_nl "$span") ))
      printf '%d %d\n' "$l1" "$l2"
    fi
  done < <(printf '%s' "$hay" | grep -a -z -b -o -P -- "$regex")
  [[ $found -eq 1 ]]
}
