# ---- token-boundary matching (header rule; claims spans and chain quotes) ----
# TOK_WS and TOK_PUNCT are the two boundary character classes; `-` and `'` are
# absent from TOK_PUNCT because they are boundaries only when they do not join
# two word characters. Membership is asked with [[ $SET == *"$c"* ]] so an
# ASCII-only set is matched against a whole (possibly multibyte) character:
# every non-ASCII byte misses both sets and is therefore a word character.

TOK_WS=$' \t\n\r\v\f'
TOK_PUNCT='!"#$%&()*+,./:;<=>?@[\]^_`{|}~'

tok_word_char() { # CHAR -> rc0: word character (ASCII alnum or non-ASCII)
  local c=$1
  [[ -n $c ]] || return 1
  [[ $c == [0-9A-Za-z] ]] && return 0
  [[ $c == - || $c == "'" ]] && return 1
  [[ $TOK_WS == *"$c"* || $TOK_PUNCT == *"$c"* ]] && return 1
  return 0
}

tok_left_ok() { # BEFORE SPAN -> rc0: the left edge is a token boundary
  local before=$1 span=$2 c n=''
  [[ -n $before ]] || return 0                    # start of file / line start
  c=${before: -1}                                 # last character before the hit
  if [[ $c == - || $c == "'" ]]; then
    if [[ ${#before} -ge 2 ]]; then n=${before: -2:1}; fi
    if tok_word_char "$n" && tok_word_char "${span:0:1}"; then
      return 1                                    # word-internal joiner
    fi
    return 0
  fi
  [[ $TOK_WS == *"$c"* || $TOK_PUNCT == *"$c"* ]]
}

tok_right_ok() { # AFTER SPAN -> rc0: the right edge is a token boundary
  local after=$1 span=$2 c n=''
  [[ -n $after ]] || return 0                     # end of file / line end
  c=${after:0:1}                                  # first character after the hit
  if [[ $c == - || $c == "'" ]]; then
    if [[ ${#after} -ge 2 ]]; then n=${after:1:1}; fi
    if tok_word_char "$n" && tok_word_char "${span: -1}"; then
      return 1                                    # word-internal joiner
    fi
    return 0
  fi
  [[ $TOK_WS == *"$c"* || $TOK_PUNCT == *"$c"* ]]
}
