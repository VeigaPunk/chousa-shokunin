#!/usr/bin/env bash
# Attack battery for C1 grep provenance (round-35 critic). Read-only on lane; scratch only.
set -u
GATE=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
W=/tmp/hyaku/chousa-r35/w2/CritGrepProvenance
mkdir -p "$W"
cd "$W"

# --- fixture (same shape as c1-count.make_fixture) ---
rm -rf fx && mkdir -p fx/src
python3 - <<'PY'
import json, os
root = "/tmp/hyaku/chousa-r35/w2/CritGrepProvenance/fx"
words = ["alpha","bravo","charlie","delta","echo","foxtrot","golf","hotel","india","juliett"]
span = " ".join(words)
open(root+"/src/ok.md","w").write("lead "+span+" tail\n")
mut = span[:-1]+("z" if span[-1]!="z" else "y")
open(root+"/src/glued.md","w").write("leadQ"+span+" tail\n")
rows=[{"id":"K1","source":"src/ok.md","span":span,"expect":"supported"},
      {"id":"K2","source":"src/ok.md","span":mut,"expect":"supported"},
      {"id":"K3","source":"src/glued.md","span":span,"expect":"supported"}]
open(root+"/claims.jsonl","w").write("\n".join(json.dumps(r) for r in rows)+"\n")
PY

run() { # name env... -- cmd...
  local name=$1; shift
  local envspec=()
  while [[ $1 != -- ]]; do envspec+=("$1"); shift; done
  shift
  env -i PATH=/usr/local/bin:/usr/bin:/bin HOME="$W" "${envspec[@]}" \
    timeout 120 bash "$GATE" verify-claims "$W/fx/claims.jsonl" --root "$W/fx" \
    >"$W/$name.out" 2>"$W/$name.err"
  local rc=$?
  echo "== $name rc=$rc"
  head -c 400 "$W/$name.out" | tr '\n' '|'; echo
  grep -a "GREP_PROVENANCE\|GATE_GREP" "$W/$name.err" | head -3
}

# reference
run ref --
