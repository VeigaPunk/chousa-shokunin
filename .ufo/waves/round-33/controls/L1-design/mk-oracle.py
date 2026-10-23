#!/usr/bin/env python3
"""Feasibility oracle (L1, never a candidate): base gate with json_str/json_has_key
replaced by a python3 top-level member reader, plus a duplicate-read-key check."""
import sys
src = open(sys.argv[1]).read()
old_str = src[src.index("json_str() {"):src.index("jfield() {")]
new_str = r'''json_str() { # ORACLE: top-level string member, re-escaped by python
  local out
  out=$(python3 -c '
import json,sys
o=json.loads(sys.argv[1]); k=sys.argv[2]
if not isinstance(o,dict) or k not in o or not isinstance(o[k],str): sys.exit(1)
sys.stdout.write(json.dumps(o[k],ensure_ascii=False)[1:-1]+"x")' "$1" "$2" 2>/dev/null) || return 1
  printf '%s' "${out%x}"
}

json_dup_read_key() { # ORACLE: rc0 when a read key repeats among top-level members
  python3 -c '
import json,sys
ks=[]
json.loads(sys.argv[1], object_pairs_hook=lambda p: ks.append([k for k,_ in p]) or dict(p))
top=ks[-1]
R={"id","source","span","expect","marker","line","sha256"}
sys.exit(0 if any(top.count(k)>1 for k in R) else 1)' "$1" 2>/dev/null
}

'''
src = src.replace(old_str, new_str)
old_hk = src[src.index("json_has_key() {"):src.index("json_unescape() {")]
new_hk = r'''json_has_key() { # ORACLE
  python3 -c '
import json,sys
o=json.loads(sys.argv[1]); sys.exit(0 if isinstance(o,dict) and sys.argv[2] in o else 1)' "$1" "$2" 2>/dev/null
}

'''
src = src.replace(old_hk, new_hk)
anchor = '    if [[ -z $id ]]; then bad="missing id"\n'
assert anchor in src
src = src.replace(anchor, '    if json_dup_read_key "$line"; then bad="duplicate top-level key"\n    elif [[ -z $id ]]; then bad="missing id"\n', 1)
open(sys.argv[2], "w").write(src)
