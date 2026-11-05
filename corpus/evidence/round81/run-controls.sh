#!/usr/bin/env bash
# round-81 prefreeze controls: do-nothing, forgers and positives for both counters.
# Usage: bash corpus/evidence/round81/run-controls.sh BASE_REV OUTDIR
# Scratch under $HYAKU_SCRATCH/chousa-r81/controls (default /fast/scratch/hyaku), removed on exit.
set -u
LANE=$(cd "$(dirname "$0")/../../.." && pwd)
BASE=${1:?base rev}
OUT=${2:?outdir}
mkdir -p "$OUT"
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/chousa-r81/controls
rm -rf -- "$S"; mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
D1="python3 -B $LANE/corpus/evidence/round81/depth-r81.py"
C2="python3 -B $LANE/corpus/evidence/round81/checklist-run.py"

snap() { # snap NAME -> fresh tree of BASE plus the working-tree fetch evidence
  local d="$S/$1"; mkdir -p "$d"
  git -C "$LANE" archive "$BASE" | tar -x -C "$d"
  cp "$LANE/corpus/evidence/round57/refetch.tsv" "$d/corpus/evidence/round57/refetch.tsv"
  cp "$LANE"/corpus/captures/{f2489455cc311a4de981e926,c52a1f15884a78028febcf43,371c55117727d526805f030d,f221c90f69188f775e32cd34,43a45b49723f7677d6446c92}.* "$d/corpus/captures/"
  echo "$d"
}
rec() { # rec LABEL EXPECT_RC CMD...
  local label=$1 want=$2; shift 2
  { echo "# control: $label"; echo "# expect_rc: $want"; echo "# cmd: $*"; "$@" 2>&1; echo "rc=$?"; } > "$OUT/$label.txt"
  local got; got=$(tail -1 "$OUT/$label.txt")
  echo "$label expect_rc=$want got_$got $(grep -E '^(DEPTH_R81=|CHECKLIST=)' "$OUT/$label.txt" | tr '\n' ' ')"
}
row() { # row ID URL USEDBY
  echo "| $1 | control row — $2 | docs | A | control | control | control | mined | 2026-11-06 | 180d | $3 |"
}
addrows() { # addrows TREE rows...
  local t=$1; shift
  python3 - "$t/corpus/SOURCES.md" "$@" <<'PY'
import sys
p=sys.argv[1]; rows=sys.argv[2:]
L=open(p,encoding='utf-8').read().split('\n')
last=max(i for i,l in enumerate(L) if l.startswith('| S'))
L[last+1:last+1]=rows
open(p,'w',encoding='utf-8').write('\n'.join(L))
PY
}
U205=https://www.nlm.nih.gov/bsd/policy/errata.html
U207=https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/
U206=https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/corrections-and-version-control.html
Q205='retractions (such as for a single graph, statement, table or image) for previously published articles are all uniformly considered by NLM to be errata.'
Q207a='Retraction Watch has also collected a large number of retractions.'
Q206=$(python3 -c "import re;t=' '.join(open('$LANE/corpus/captures/f221c90f69188f775e32cd34.txt',encoding='utf-8').read().split());i=t.find('retraction');print(' '.join(t[i:].split()[:12]))")
entry() { # entry PATH SOURCE_LINE QUOTE_LINES...
  local p=$1 src=$2; shift 2
  { echo "# control entry"; echo; echo "source: $src"; echo "verified-at: 2026-11-06"; echo "recheck: 180d"; echo;
    echo "| when | do | never |"; echo "|---|---|---|"; echo "| a | b | c |"; echo "| d | e | f |"; echo "| g | h | i |"; echo;
    for q in "$@"; do echo "$q"; done; } > "$p"
}

# K0 do-nothing: the base tree, unchanged
T=$(snap k0); rec c1-k0-donothing 1 $D1 --root "$T"
rec c2-k0-donothing 1 $C2 --root "$T"

# C1 positive: two entries on fresh control rows, quotes located in today's captures
T=$(snap c1pos)
addrows "$T" "$(row S901 $U205 corpus/knowledge/ctl-a-r81.md)" "$(row S902 $U207 corpus/knowledge/ctl-a-r81.md)" \
  "$(row S903 $U206 corpus/knowledge/ctl-b-r81.md)" "$(row S904 $U205 corpus/knowledge/ctl-b-r81.md)"
python3 - "$T/corpus/evidence/round57/refetch.tsv" <<'PY'
import sys
p=sys.argv[1]; L=open(p).read().rstrip('\n').split('\n'); add=[]
m={'S205':['S901','S904'],'S207':['S902'],'S206':['S903']}
for l in L:
    f=l.split('\t')
    for new in m.get(f[0],[]):
        add.append('\t'.join([new]+f[1:]))
open(p,'w').write('\n'.join(L+add)+'\n')
PY
entry "$T/corpus/knowledge/ctl-a-r81.md" "S901, S902" "> \"$Q205\" — S901" "> \"$Q207a\" — S902" "> \"previously published articles are all uniformly considered by NLM to be errata.\" — S901"
Q205b='retraction and erratum notices, expressions of concern, corrected and republished articles'
entry "$T/corpus/knowledge/ctl-b-r81.md" "S903, S904" "> \"$Q206\" — S903" "> \"$Q205b\" — S904" "> \"$Q206\" — S903"
rec c1-pos-two-entries 0 $D1 --root "$T"

# C1 forgers (each a copy of the positive tree with one defect)
F=$S/f1; cp -a "$T" "$F"; sed -i 's/— S902$/— S999/' "$F/corpus/knowledge/ctl-a-r81.md"; rec c1-f1-unregistered-id 1 $D1 --root "$F"
F=$S/f2; cp -a "$T" "$F"; sed -i 's/uniformly considered/always considered/' "$F/corpus/knowledge/ctl-a-r81.md"; rec c1-f2-altered-quote 1 $D1 --root "$F"
F=$S/f3; cp -a "$T" "$F"; sed -i 's/| mined | 2026-11-06 | 180d | corpus\/knowledge\/ctl-a-r81.md |/| mined | 2026-10-21 | 180d | corpus\/knowledge\/ctl-a-r81.md |/' "$F/corpus/SOURCES.md"; rec c1-f3-stale-opened-date 1 $D1 --root "$F"
F=$S/f4; cp -a "$T" "$F"; cp "$F/corpus/knowledge/ctl-a-r81.md" "$F/corpus/knowledge/ctl-b-r81.md"; sed -i 's#| corpus/knowledge/ctl-a-r81.md |$#| corpus/knowledge/ctl-a-r81.md corpus/knowledge/ctl-b-r81.md |#' "$F/corpus/SOURCES.md"; rec c1-f4-duplicate-entry 1 $D1 --root "$F"
F=$S/f5; cp -a "$T" "$F"; printf 'tampered\n' >> "$F/corpus/captures/371c55117727d526805f030d.txt"; rec c1-f5-capture-not-recorded 1 $D1 --root "$F"
F=$S/f6; cp -a "$T" "$F"; sed -i '/^| [a-i] |/d' "$F/corpus/knowledge/ctl-a-r81.md"; rec c1-f6-no-table 1 $D1 --root "$F"
F=$S/f7; cp -a "$T" "$F"; sed -i 's/^> "\(.*\)" — S901$/> "\1 \1" — S901/' "$F/corpus/knowledge/ctl-a-r81.md"; rec c1-f7-overlong-quote 1 $D1 --root "$F"

# C2 positive: the candidate Run lines the round intends to land
T=$(snap c2pos)
python3 - "$T/SKILL.md" <<'PY'
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
s=s.replace("- [ ] A negative claim carries its search sweep, naming where it looked.\n",
 "- [ ] A negative claim carries its search sweep, naming where it looked.\n  - Run: `bash tools/research-gate.sh verify-sweeps <record.md> --root .` → exit 0 `RESEARCH_GATE: CLEAN`; a sweep naming nowhere is `SWEEP_LOCATION_ABSENT`, a local sweep with a hit is `SWEEP_CLAIM_FALSE`, exit 1.\n",1)
s=s.replace("- [ ] A rejected source is kept with its rejection reason and flip-condition.\n",
 "- [ ] A rejected source is kept with its rejection reason and flip-condition.\n  - Run: `bash tools/research-gate.sh verify-sweeps <record.md> --root .` → exit 0 `REJECTIONS_OK=K/K`; a kept rejection without reason or flip-condition is `SWEEP_REJECTION_INCOMPLETE`, exit 1.\n",1)
i=s.index("- [ ] Every web quote a round cites")
j=s.index("\n- [ ]",i+1)
s=s[:j]+"\n  - Run: `python3 tools/quote-reopen.py verify --items <items.tsv>` → exit 0 when every quote is `VERBATIM`; exit 1 with `QUOTE_REOPEN_SUMMARY` naming each other verdict (an unregistered id is `NO_SOURCE` before any fetch)."+s[j:]
open(p,'w',encoding='utf-8').write(s)
PY
cp "$T/SKILL.md" "$OUT/c2-candidate-SKILL.md"
rec c2-pos-candidate 0 $C2 --root "$T"
# C2 forgers
F=$S/g1; cp -a "$T" "$F"; sed -i 's#^  - Run: `bash tools/research-gate.sh verify-sweeps <record.md> --root .`#  - Run: `true <record.md>`#; s#^  - Run: `python3 tools/quote-reopen.py verify --items <items.tsv>`#  - Run: `true <items.tsv>`#' "$F/SKILL.md"; rec c2-g1-true-forger 1 $C2 --root "$F"
F=$S/g2; cp -a "$T" "$F"; sed -i 's#verify-sweeps <record.md> --root .`#verify-sweeps <record.md> --root . || true`#' "$F/SKILL.md"; rec c2-g2-or-true-forger 1 $C2 --root "$F"
F=$S/g3; cp -a "$T" "$F"; sed -i 's#verify-sweeps <record.md> --root .`#verify-sweeps --root .`#' "$F/SKILL.md"; rec c2-g3-no-placeholder 1 $C2 --root "$F"
F=$S/g4; cp -a "$T" "$F"; python3 - "$F/SKILL.md" <<'PY'
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
s=s.replace("- [ ] A rejected source is kept with its rejection reason and flip-condition.\n","",1)
open(p,'w',encoding='utf-8').write(s)
PY
rec c2-g4-item-deleted 2 $C2 --root "$F"
F=$S/g5; cp -a "$T" "$F"; sed -i 's#^  - Run: `bash tools/research-gate.sh verify-sweeps <record.md> --root .`#  - Run: `bash tools/research-gate.sh verify-chain <record.md> --root .`#' "$F/SKILL.md"; rec c2-g5-wrong-mode 1 $C2 --root "$F"
