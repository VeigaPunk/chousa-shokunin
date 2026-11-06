#!/usr/bin/env bash
# run-controls-r82.sh REV OUTDIR — round-82 prefreeze controls for C1 (k2-gate-r82.py) and
# C2 (depth-r82.py). Every control is a `git archive REV` tree plus one stated overlay; the
# counters are always the ones committed at REV. Scratch lives under $HYAKU_SCRATCH (default
# /fast/scratch/hyaku)/chousa-r82/controls and is removed on exit. Receipts: OUTDIR/<id>.txt,
# each ending in `rc=<n>`, plus OUTDIR/summary.tsv (id expected observed).
set -u
REV=${1:?REV}; OUT=${2:?OUTDIR}
LANE=$(cd "$(dirname "$0")/../../.." && pwd)
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/chousa-r82/controls
rm -rf -- "$SCR"; mkdir -p "$SCR" "$OUT"
trap 'rm -rf -- "$SCR"' EXIT
CTL=corpus/evidence/round82/c2-controls
: >"$OUT/summary.tsv"

mk() { # NAME -> tree path on stdout
  local t=$SCR/$1
  mkdir -p "$t" && git -C "$LANE" archive "$REV" | tar -x -C "$t" && printf '%s' "$t"
}
rec() { # ID EXPECTED(PASS|FAIL) CMD...
  local id=$1 exp=$2; shift 2
  local f=$OUT/$id.txt rc obs
  { printf '# control %s (expected %s) at REV %s\n# cmd: %s\n' "$id" "$exp" "$(git -C "$LANE" rev-parse "$REV")" "$*"
    "$@"; rc=$?; printf 'rc=%d\n' "$rc"; } >"$f" 2>&1
  rc=$(sed -n 's/^rc=//p' "$f" | tail -1)
  if [[ $rc == 0 ]]; then obs=PASS; elif [[ $rc == 1 ]]; then obs=FAIL; else obs=ERROR; fi
  printf '%s\t%s\t%s\n' "$id" "$exp" "$obs" >>"$OUT/summary.tsv"
}
c1() { python3 -B "$1/corpus/evidence/round82/k2-gate-r82.py" --root "$1"; }
c2() { python3 -B "$1/corpus/evidence/round82/depth-r82.py" --root "$1"; }

# ---- C1 ----
T=$(mk c1-k0); rec c1-k0-donothing FAIL c1 "$T"
# blanket refusal: verify-sweeps refuses everything (positives must catch it)
T=$(mk c1-f1); python3 - "$T/tools/research-gate.sh" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
a='verify_sweeps() {\n  local record=$1\n'
assert a in s; s=s.replace(a,a+'  printf "FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=forger\\nFINDING SWEEP_LOCATION_ABSENT severity=warn surface=sweeps obs=forger\\nFINDING SWEEP_NEGATIVE_UNRESOLVED severity=warn surface=sweeps obs=forger\\nRESEARCH_GATE: DRIFT\\n"; return 1\n',1)
open(p,'w').write(s)
PY
rec c1-f1-blanket-refuse FAIL c1 "$T"
# wrong finding id: verify-sweeps refuses everything non-positive with a generic finding
T=$(mk c1-f2); python3 - "$T/tools/research-gate.sh" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
a='verify_sweeps() {\n  local record=$1\n'
assert a in s; s=s.replace(a,a+'  case "$record" in *pass*|*sweeps-r5*|*alt-section.md|*prose*) ;; *) printf "FINDING SWEEP_GENERIC severity=warn surface=sweeps obs=forger\\nRESEARCH_GATE: DRIFT\\n"; return 1 ;; esac\n',1)
open(p,'w').write(s)
PY
rec c1-f2-wrong-finding-keyed FAIL c1 "$T"
# fixture-keyed Run line (the round-81 C2 forger shape): SKILL item-4 Run line rewritten
T=$(mk c1-f3); python3 - "$T/SKILL.md" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
a='  - Run: `bash tools/research-gate.sh verify-sweeps <record.md> --root .`'
assert a in s; s=s.replace(a,'  - Run: `grep -q pass <record.md> || { echo "FINDING SWEEP_REJECTION_INCOMPLETE"; false; }`',1)
open(p,'w').write(s)
PY
rec c1-f3-keyed-runline FAIL c1 "$T"

# ---- C2 ----
overlay() { # TREE CONTROLDIR
  local t=$1 d=$2 f
  for f in "$d"/*.md; do cp -- "$f" "$t/corpus/knowledge/"; done
  python3 - "$t/corpus/SOURCES.md" "$d" <<'PY'
import os, re, sys
p, d = sys.argv[1], sys.argv[2]
lines = open(p, encoding='utf-8').read().split('\n')
if os.path.isfile(f'{d}/s008-replace.txt'):
    new = open(f'{d}/s008-replace.txt', encoding='utf-8').read().strip('\n')
    lines = [new if l.startswith('| S008 |') else l for l in lines]
if os.path.isfile(f'{d}/sources-append.txt'):
    add = open(f'{d}/sources-append.txt', encoding='utf-8').read().strip('\n').split('\n')
    last = max(i for i, l in enumerate(lines) if re.match(r'^ {0,3}\| S\d{3,} \|', l))
    lines[last + 1:last + 1] = add
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
PY
}
T=$(mk c2-d0); rec c2-d0-donothing FAIL c2 "$T"
T=$(mk c2-d1); cp "$LANE/$CTL/D1-r81-filler/"*.md "$T/corpus/knowledge/"; rec c2-d1-r81-filler FAIL c2 "$T"
for x in D2-fabricated-quotes D3-stale-r81-sources D4-duplicate-cells D5-four-rows D6-placeholder-cells D7-unregistered; do
  T=$(mk "c2-$x"); overlay "$T" "$LANE/$CTL/$x"; rec "c2-${x,,}" FAIL c2 "$T"
done
T=$(mk c2-p1); overlay "$T" "$LANE/$CTL/P1-positive"; rec c2-p1-positive PASS c2 "$T"
T=$(mk c2-b1); overlay "$T" "$LANE/$CTL/B1-salad-boundary"; rec c2-b1-salad-boundary PASS c2 "$T"
cat "$OUT/summary.tsv"
awk -F'\t' '$2!=$3{bad++} END{printf "CONTROLS_AS_EXPECTED=%d/%d\n", NR-bad, NR; exit bad>0}' "$OUT/summary.tsv"
