claim_scan() { # LINE -> JSON_* tables + JSON_SCAN_RC; rc0: one well-formed object
  local LC_ALL=C
  local s=$1
  if [[ $s == "$JSON_SCAN_LINE" ]]; then return "$JSON_SCAN_RC"; fi
  JSON_SCAN_LINE=$s
  JSON_SCAN_RC=1
  JSON_PRESENT=(); JSON_STR=(); JSON_DUP=(); JSON_DUPDIFF=()
  local n=${#s} i=0 c key val stk top is_str esc in_str tok
  # JSON whitespace only (space, tab, CR, LF): a form feed or vertical tab is not
  # whitespace in RFC 8259 and makes the line malformed (r33 post-falsify:
  # ProbeWhitespace33). A scalar is one RFC 8259 literal or number (r33
  # post-falsify: ProbeFlatBehaviour33, ProbeMalformed33, CriticClaim33).
  local ws=$' \t\r\n'
  local lit='^(true|false|null|-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?)$'
  # Runs are consumed with one regex match each, not one ${s:i:1} per byte: a
  # substring costs time in the line length, so a byte loop is quadratic in it
  # (r33 post-falsify: ProbeLongLines33, 64 KiB unread member 0.07 s -> 4.7 s).
  local strrun='^[^"\\]+'                      # string body up to " or backslash
  local tokrun=$'^[^][{}",: \t\r\n]+'          # bare token inside a nested value
  local wsrun=$'^[ \t\r\n]+'
  # an escape is one of \" \\ \/ \b \f \n \r \t or \u + four hex digits (RFC 8259
  # §7); anything else is malformed (r33 post-falsify: MutC1GateString, "\q")
  local escok='^\\(["\\/bfnrt]|u[0-9A-Fa-f]{4})'
  # leading whitespace, then the single opening brace
  while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
  (( i < n )) && [[ ${s:i:1} == '{' ]] || return 1
  i=$((i + 1))
  local allow_close=1   # only an empty object may close before a member
  while :; do
    while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
    (( i < n )) || return 1
    c=${s:i:1}
    if [[ $c == '}' ]]; then
      (( allow_close )) || return 1        # a trailing comma is not a member
      i=$((i + 1))
      while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
      (( i == n )) || return 1             # trailing garbage
      JSON_SCAN_RC=0
      return 0
    fi
    [[ $c == '"' ]] || return 1            # a member name is a JSON string
    # member name: raw text, escapes intact, so a key spelled with an escape
    # (the not-claimed "l\u0069ne") is not read as the plain key
    key=''; i=$((i + 1))
    while :; do
      (( i < n )) || return 1
      if [[ ${s:i} =~ $strrun ]]; then
        key+=${BASH_REMATCH[0]}; i=$((i + ${#BASH_REMATCH[0]})); continue
      fi
      c=${s:i:1}
      if [[ $c == '\' ]]; then
        [[ ${s:i:6} =~ $escok ]] || return 1
        key+=${s:i:2}; i=$((i + 2)); continue
      fi
      i=$((i + 1)); break                   # the closing quote
    done
    # colon
    while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
    (( i < n )) && [[ ${s:i:1} == ':' ]] || return 1
    i=$((i + 1))
    while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
    (( i < n )) || return 1
    c=${s:i:1}; val=''; is_str=0
    if [[ $c == '"' ]]; then
      # string value: raw body with escapes intact
      is_str=1; i=$((i + 1))
      while :; do
        (( i < n )) || return 1
        if [[ ${s:i} =~ $strrun ]]; then
          val+=${BASH_REMATCH[0]}; i=$((i + ${#BASH_REMATCH[0]})); continue
        fi
        c=${s:i:1}
        if [[ $c == '\' ]]; then
          [[ ${s:i:6} =~ $escok ]] || return 1
          val+=${s:i:2}; i=$((i + 2)); continue
        fi
        i=$((i + 1)); break                 # the closing quote
      done
    elif [[ $c == '{' || $c == '[' ]]; then
      # nested value: skip to its matching close, strings honoured; every bare
      # token outside strings must be one JSON literal or number
      stk=$c; i=$((i + 1)); in_str=0; tok=''
      while [[ -n $stk ]]; do
        (( i < n )) || return 1
        if (( in_str )); then
          if [[ ${s:i} =~ $strrun ]]; then i=$((i + ${#BASH_REMATCH[0]})); continue; fi
          c=${s:i:1}
          if [[ $c == '\' ]]; then
            [[ ${s:i:6} =~ $escok ]] || return 1
            i=$((i + 2)); continue
          fi
          in_str=0; i=$((i + 1)); continue  # the closing quote
        fi
        if [[ ${s:i} =~ $tokrun ]]; then
          tok+=${BASH_REMATCH[0]}; i=$((i + ${#BASH_REMATCH[0]})); continue
        fi
        if [[ ${s:i} =~ $wsrun ]]; then
          i=$((i + ${#BASH_REMATCH[0]}))     # before the literal test reuses BASH_REMATCH
          [[ -z $tok || $tok =~ $lit ]] || return 1
          tok=''; continue
        fi
        c=${s:i:1}
        case "$c" in
          '"'|'{'|'['|'}'|']'|','|':'|' '|$'\t'|$'\r'|$'\n')
            if [[ -n $tok ]]; then
              [[ $tok =~ $lit ]] || return 1  # not a JSON literal or number
              tok=''
            fi
            ;;
        esac
        case "$c" in
          '"') in_str=1 ;;
          '{'|'[') stk+=$c ;;
          '}'|']')
            top=${stk: -1}
            if [[ $c == '}' && $top == '{' ]] || [[ $c == ']' && $top == '[' ]]; then
              stk=${stk%?}
            else
              return 1                     # mismatched bracket
            fi
            ;;
          ','|':'|' '|$'\t'|$'\r'|$'\n') ;;
          *) tok+=$c ;;
        esac
        i=$((i + 1))
      done
    else
      # number, true, false, null: up to a delimiter, then one RFC 8259 literal
      while (( i < n )); do
        c=${s:i:1}
        case "$c" in
          ','|'}'|']'|' '|$'\t'|$'\r'|$'\n') break ;;
        esac
        val+=$c; i=$((i + 1))
      done
      [[ $val =~ $lit ]] || return 1
    fi
    # an empty member name cannot be an associative-array subscript (bash 5.3
    # rejects ""); no read key is empty, so the table simply skips it.
    if [[ -n $key ]]; then
      if [[ -n ${JSON_PRESENT["$key"]+x} ]]; then
        # flag the key when ANY repeat is not a string whose raw body equals the
        # first occurrence's (r33 post-falsify: three or more repeats,
        # ReviewKnowledge33), so the caller can tell agreeing repeats apart
        if (( ! is_str )) || [[ -z ${JSON_STR["$key"]+x} || $val != "${JSON_STR["$key"]}" ]]; then
          JSON_DUPDIFF["$key"]=1
        fi
        JSON_DUP["$key"]=1
      else
        JSON_PRESENT["$key"]=1
        if (( is_str )); then JSON_STR["$key"]=$val; fi
      fi
    fi
    # after a value only ',' (another member) or the closing brace may follow
    while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
    (( i < n )) || return 1
    c=${s:i:1}
    if [[ $c == '}' ]]; then
      i=$((i + 1))
      while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
      (( i == n )) || return 1
      JSON_SCAN_RC=0
      return 0
    fi
    [[ $c == ',' ]] || return 1
    i=$((i + 1)); allow_close=0
  done
}

json_str() { # LINE KEY -> raw JSON string body of the TOP-LEVEL member; rc=1 absent/non-string
  claim_scan "$1" || return 1
  [[ -n ${JSON_STR["$2"]+x} ]] || return 1
  printf '%s' "${JSON_STR["$2"]}"
}

jfield() { json_str "$1" "$2" 2>/dev/null || true; }

json_has_key() { # LINE KEY -> rc0: KEY is a TOP-LEVEL member of the record (any value type)
  # presence is tracked separately from json_str so a present non-string value
  # (number, bool, null, …) is distinguishable from an absent key, and a member
  # inside a nested object or a key spelling inside a string value is not seen.
  claim_scan "$1" || return 1
  [[ -n ${JSON_PRESENT["$2"]+x} ]]
}

json_dup() { # LINE KEY -> rc0: KEY occurs more than once among the TOP-LEVEL members
  claim_scan "$1" || return 1
  [[ -n ${JSON_DUP["$2"]+x} ]]
}

json_unescape() { # RAW JSON string body -> decoded bytes on stdout
  local s=$1 out='' i c hex cp
  local n=${#s}
  for ((i = 0; i < n; i++)); do
    c=${s:i:1}
    if [[ $c != '\' ]]; then out+=$c; continue; fi
    i=$((i + 1)); c=${s:i:1}
    case "$c" in
      '"') out+='"' ;;
      '\') out+='\' ;;
      /) out+='/' ;;
      b) out+=$'\b' ;;
      f) out+=$'\f' ;;
      n) out+=$'\n' ;;
      r) out+=$'\r' ;;
      t) out+=$'\t' ;;
      u)
        hex=''
        if ((i + 4 < n)); then hex=${s:i+1:4}; fi
        if [[ $hex =~ ^[0-9A-Fa-f]{4}$ ]]; then
          cp=$((16#$hex)); i=$((i + 4))
          if ((cp < 0x80)); then
            printf -v c '%b' "\\$(printf '%03o' "$cp")"; out+=$c
          elif ((cp >= 0xD800 && cp <= 0xDFFF)); then
            out+='?'
          elif printf -v c '%b' "\u$hex" 2>/dev/null; then
            out+=$c
          else
            out+='?'
          fi
        else
          out+='\u'
        fi
        ;;
      *) out+='\'; out+=$c ;;
    esac
  done
  printf '%s' "$out"
}

count_nl() { # STRING -> newline count (linear in bytes). The previous
  local n                        # negated-class expansion was quadratic in the
  n=$(printf '%s' "$1" | tr -dc '\n' | wc -c)  # string length — measured
  n=${n//[[:space:]]/}           # >60 s at the 8 MiB source the r12 cap
  printf '%d' "$n"               # admits; tr|wc -c is ~3 ms there.
}

