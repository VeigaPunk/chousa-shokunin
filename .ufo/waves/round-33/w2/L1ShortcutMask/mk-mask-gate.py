#!/usr/bin/env python3
"""L1 test of CriticControls33's inferred shortcut (post-data falsify finding, not a candidate):
base gate + (1) the six counter CONFUSER literals masked, (2) CtlC1StripNested control-a's regex
deletion of nested {...}/[...], (3) the base flat regex read on the stripped text, (4) a read key
whose `"key":` occurs more than once in the stripped text makes the record invalid.
Usage: mk-mask-gate.py BASE_GATE OUT_GATE"""
import sys

src = open(sys.argv[1]).read()
helper = r'''json_mask_strip() { # ORACLE-SHORTCUT: fixture-keyed mask + regex strip (no string lexer)
  python3 - "$1" <<'PY'
import json, re, sys
CONFUSERS = [
    "open { brace and [ bracket",
    "close } brace ] bracket",
    'a quote " then } more',
    "ends with a backslash \\",
    'fake "line": "3", "sha256": "x"',
    '{"line": "2"} ] } , :',
]
s = sys.argv[1]
for c in CONFUSERS:
    s = s.replace(json.dumps(c, ensure_ascii=False), '"x"')
body = s.strip()[1:-1]
while True:
    t = re.sub(r'\{[^{}]*\}', '', body)
    t = re.sub(r'\[[^\[\]]*\]', '', t)
    if t == body:
        break
    body = t
sys.stdout.write('{' + body + '}')
PY
}

json_dup_read_key() { # rc0 when a read key occurs more than once in the stripped text
  local s k re n
  s=$(json_mask_strip "$1")
  for k in id source span expect marker line sha256; do
    n=$(grep -o "\"$k\"[[:space:]]*:" <<<"$s" | wc -l)
    (( n > 1 )) && return 0
  done
  return 1
}

'''
i = src.index("json_str() {")
src = src[:i] + helper + src[i:]
old_str = '''json_str() { # LINE KEY -> raw JSON string body on stdout (escapes intact); rc=1 absent
  local line=$1 key=$2'''
assert src.count(old_str) == 1
src = src.replace(old_str, '''json_str() { # LINE KEY -> raw JSON string body on stdout (escapes intact); rc=1 absent
  local line key=$2
  line=$(json_mask_strip "$1")''')
old_hk = '''  local re="\\"${2}\\"[[:space:]]*:"
  [[ $1 =~ $re ]]'''
assert src.count(old_hk) == 1, src.count(old_hk)
src = src.replace(old_hk, '''  local re="\\"${2}\\"[[:space:]]*:" s
  s=$(json_mask_strip "$1")
  [[ $s =~ $re ]]''')
anchor = '    if [[ -z $id ]]; then bad="missing id"\n'
assert src.count(anchor) == 1
src = src.replace(anchor, '    if json_dup_read_key "$line"; then bad="duplicate top-level key"\n    elif [[ -z $id ]]; then bad="missing id"\n', 1)
open(sys.argv[2], "w").write(src)
