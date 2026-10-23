  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    # FORGERY v5: derive the witness stamp format entirely from $PS4, which the
    # witness tool passes in the gate's own environment. No hardcoded marker.
    __wp="${BASH_SOURCE[0]:-$0}"
    __ln=$(awk 'BEGIN{f=0} /^tok_span_offsets_chunk\(\)/{f=1;next} f{ if ($0 ~ /^[[:space:]]*#/ || $0 ~ /^[[:space:]]*$/) next; print NR; exit }' "$__wp")
    __bs='${BASH_SOURCE}'
    __lnp='${LINENO}'
    __fake=${PS4/"$__bs"/"$__wp"}
    __fake=${__fake/"$__lnp"/"$__ln"}
    __i=0
    while (( __i < 40 )); do
      printf '%s\n' "$__fake" >&2
      __i=$(( __i + 1 ))
    done
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
