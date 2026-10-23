import os
src = open('gate-landed.sh', encoding='utf-8').read()
HELPER = os.path.abspath('span_search.py')
anchor = '''  local hay=$1 span=$2
  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    tok_span_offsets_chunk "$hay" "$span"
  else
    tok_span_offsets_direct "$hay" "$span"
  fi
'''
assert src.count(anchor) == 1

def insert_before_if(text, branch):
    head = '  local hay=$1 span=$2\n'
    i = text.index(anchor)
    return text[:i] + head + branch + text[i + len(head):]

# (a2 fixed) K1 shortcut with stderr silenced only inside the shortcut branch
branch_a2 = '''  exec 3>&2 2>/dev/null
  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "HELPER" "$span"
    exec 2>&3 3>&-
    return 0
  fi
  exec 2>&3 3>&-
'''.replace('HELPER', HELPER)
open('gate-a2-shortcut-stderr.sh', 'w').write(insert_before_if(src, branch_a2))

# (c fixed) K1 shortcut that first calls the chunk matcher on a synthetic hay
branch_c = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    tok_span_offsets_chunk "$span" "$span" >/dev/null
    printf '%s' "$hay" | python3 "HELPER" "$span"
    return 0
  fi
'''.replace('HELPER', HELPER)
open('gate-c-synthetic-call.sh', 'w').write(insert_before_if(src, branch_c))

# (b2) keep chunk entry line AND locals; replace only the grep/confirm body
old_body = '''  local hay=$1 span=$2 chunk pattern occurrence offset resume=0
  # round-35 R1: slen must be read from the parameter, not from the caller's
  # dynamic scope. `local a=$1 b=${#a}` expands every right-hand side before it
  # assigns any of them, so the one-statement form read the caller's `span`
  # (correct only while every caller happened to pass its own `span` unchanged).
  local slen
  slen=${#span}
  chunk=${span:0:TOK_CHUNK_BYTES}
  pattern="$(tok_hex_pattern "${chunk:0:1}")(?=$(tok_hex_pattern "${chunk:1}"))"
  while IFS= read -r -d '' occurrence; do
    offset=${occurrence%%:*}
    (( offset >= resume )) || continue
    [[ ${hay:offset:slen} == "$span" ]] || continue
    printf '%s\\n' "$offset"
    resume=$(( offset + slen ))
  done < <(printf '%s' "$hay" | grep -a -z -b -o -P -- "$pattern")
'''
new_body = '''  local hay=$1 span=$2
  printf '%s' "$hay" | python3 "HELPER" "$span"
  return 0
'''.replace('HELPER', HELPER)
assert src.count(old_body) == 1
open('gate-b2-body-swap.sh', 'w').write(src.replace(old_body, new_body))
print('ok')
