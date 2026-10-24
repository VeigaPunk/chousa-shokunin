#!/usr/bin/env bash
# Round-24 counting commands, one script (chousa-shokunin). Usage, from anywhere:
#   bash corpus/evidence/round24-measure.sh <tree-root> [<pre-round QUALITY.md>]
# <tree-root> is a lane checkout (the landing commit, or `git archive ab19cff`
# unpacked for the before-state). The calibration count compares the r24 lesson
# table against the given QUALITY.md (default: the tree's own). Read-only except
# a mktemp manifest it removes. Research root for the round-1 command:
# SHOKUNIN_ROOT (default /home/vgpnk/Projects/shokunin).
set -u
R=${1:?tree root}; QB=${2:-}
cd "$R" || exit 1
FLEET=${SHOKUNIN_ROOT:-/home/vgpnk/Projects/shokunin}
echo "== tree $(pwd -P) gate $(sha256sum tools/research-gate.sh 2>/dev/null | cut -c1-8)"

echo "== claim 1 (operability): append onto a manifest whose last byte is not '\n'"
T=$(mktemp -d); printf '{"prior":true}' >"$T/m.jsonl"
bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --json "$T/m.jsonl" --root . >/dev/null 2>&1
python3 -c 'import json,sys
L=[l for l in open(sys.argv[1]).read().splitlines() if l.strip()]
bad=0
for l in L:
    try: json.loads(l)
    except Exception: bad+=1
print("MANIFEST_LINES=%d INVALID_JSON_LINES=%d" % (len(L), bad))' "$T/m.jsonl"; rm -rf "$T"

echo "== operability score re-derived (SCORECARD round-1 counting command)"
python3 -c 'import subprocess,sys; f=sys.argv[1]; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify",f+"/research/deep-research-2026-09-28/"+n,"--root",f],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))' "$FLEET"

echo "== claim 2 (coverage + source registry): 3 method entries admitted through the registry"
n=0
for f in corpus/knowledge/claim-support-states-r24.md corpus/knowledge/citation-chain-fidelity-r24.md corpus/knowledge/contextual-source-admission-r24.md; do
  ok=1; [ -f "$f" ] || ok=0
  grep -q '^source: ' "$f" 2>/dev/null || ok=0
  grep -q '^verified-at: [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' "$f" 2>/dev/null || ok=0
  grep -qE '^recheck: ([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]+d|on-release)' "$f" 2>/dev/null || ok=0
  ids=$(grep -m1 '^source: ' "$f" 2>/dev/null | grep -oE '\bS[0-9]{3}\b' | sort -u)
  [ -n "$ids" ] || ok=0
  for i in $ids; do   # every cited row must be mined and name this entry in used-by
    awk -F'|' -v i="$i" -v p="$f" '{x=$2; gsub(/[[:space:]]/,"",x); s=$9; gsub(/[[:space:]]/,"",s)} x==i && s=="mined" && index($12,p) {hit=1} END{exit !hit}' corpus/SOURCES.md 2>/dev/null || ok=0
  done
  grep -qF "\`${f#corpus/}\`" corpus/README.md 2>/dev/null || ok=0   # coverage-map row
  echo "  $f admitted=$ok ids=$(echo $ids | tr '\n' ' ')"; n=$((n+ok))
done
echo "EXPANSION_ADMITTED=$n/3"

echo "== claim 2: SOURCES contract v1 census (clean = no diagnostics inside [ ])"
if [ -f corpus/SOURCES.md ]; then
  S=corpus/SOURCES.md
  echo "rows: $(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' $S)"
  echo "malformed: $(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' $S)"
  echo "tiers: $(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' $S | tr ' ' '\n' | sort | tr '\n' ' ')"
  echo "status: $(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' $S | tr ' ' '\n' | sort | tr '\n' ' ')"
  echo "dup-ids: [$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' $S | sort | uniq -d)]"
  echo "enum/inflation: [$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' $S)]"
  echo "missing-used-by: [$(awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' $S | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done)]"
  echo "sections: $(grep -cE '^## (Registry|Paths|Search log|Leads \(unopened\))$' $S)/4"
else
  echo "corpus/SOURCES.md absent"
fi

echo "== claim 3 (calibration): mined mistake classes captured by a numbered QUALITY criterion"
L=corpus/lessons/round-24.md; Q=${QB:-corpus/QUALITY.md}
if [ -f "$L" ]; then
  awk -F'|' -v Q="$Q" 'BEGIN{while((getline l < Q)>0) if (match(l,/^[0-9]+\. /)) have[substr(l,1,RLENGTH-2)]=1}
  /^\| M-[0-9]+ /{total++; c=$5; gsub(/[^0-9]/," ",c); n=split(c,a," "); cap=0; for(j=1;j<=n;j++) if(a[j] in have) cap=1; if(cap) k++}
  END{printf "MISTAKE_CLASSES=%d CAPTURED_BY_CRITERION=%d UNCAPTURED=%d (bar: %s)\n", total, k, total-k, Q}' "$L"
else
  echo "$L absent"
fi
