import os
src = open('gate-landed.sh', encoding='utf-8').read()
HELPER = os.path.abspath('span_search.py')

def replace_once(text, old, new):
    assert text.count(old) == 1, (old[:60], text.count(old))
    return text.replace(old, new)

# ---- (a1) honest gate: silence stderr across the whole matcher dispatch ----
old = '''  local hay=$1 span=$2
  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    tok_span_offsets_chunk "$hay" "$span"
  else
    tok_span_offsets_direct "$hay" "$span"
  fi
'''
new = '''  local hay=$1 span=$2
  exec 3>&2 2>/dev/null
  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    tok_span_offsets_chunk "$hay" "$span"
  else
    tok_span_offsets_direct "$hay" "$span"
  fi
  exec 2>&3 3>&-
'''
open('gate-a1-honest-stderr.sh', 'w').write(replace_once(src, old, new))

# ---- (a2) K1 python-exact shortcut, stderr silenced inside the branch ----
anchor = '  local hay=$1 span=$2\n  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then\n    tok_span_offsets_chunk "$hay" "$span"\n  else\n    tok_span_offsets_direct "$hay" "$span"\n  fi\n'
branch_a2 = '''  exec 3>&2 2>/dev/null
  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "HELPER" "$span"
    exec 2>&3 3>&-
    return 0
  fi
  exec 2>&3 3>&-
'''.replace('HELPER', HELPER)
open('gate-a2-shortcut-stderr.sh', 'w').write(replace_once(src, anchor, anchor.split('\n')[0] + '\n' + branch_a2))

# ---- (b) python-exact INSIDE tok_span_offsets_chunk (entry line fires) ----
old = '''tok_span_offsets_chunk() { # HAY SPAN -> stdout: byte offset of each occurrence
'''
assert src.count(old) == 1
# insert after the comment block, just before `local LC_ALL=C` of chunk
marker = '''tok_span_offsets_chunk() { # HAY SPAN -> stdout: byte offset of each occurrence
'''
chunk_head = src.index(marker)
local_line = src.index('  local LC_ALL=C\n', chunk_head)
branch_b = '''  if (( ${#2} > 0 )); then
    printf '%s' "$1" | python3 "HELPER" "$2"
    return 0
  fi
'''.replace('HELPER', HELPER)
b = src[:local_line] + branch_b + src[local_line:]
open('gate-b-inside-chunk.sh', 'w').write(b)

# ---- (c) K1 shortcut, but call the chunk matcher on a synthetic hay first ----
branch_c = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    tok_span_offsets_chunk "$span" "$span" >/dev/null
    printf '%s' "$hay" | python3 "HELPER" "$span"
    return 0
  fi
'''.replace('HELPER', HELPER)
c = replace_once(src, anchor, anchor.split('\n')[0] + '\n' + branch_c)
open('gate-c-synthetic-call.sh', 'w').write(c)
print("wrote mutants")
