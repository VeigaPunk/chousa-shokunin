#!/usr/bin/env bash
# run-controls-r83.sh REV OUTDIR — round-83 prefreeze controls for C1 (depth-r84.py) and C2 (gate-records-r84.py).
# Every control is a `git archive REV` tree plus one stated overlay; the counters are always the ones committed at
# REV. Scratch lives under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/chousa-r84/controls and is removed on exit.
# Receipts: OUTDIR/<id>.txt, each ending in `rc=<n>`, plus OUTDIR/summary.tsv (id expected observed).
set -u
REV=${1:?REV}; OUT=${2:?OUTDIR}
LANE=$(cd "$(dirname "$0")/../../.." && pwd)
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/chousa-r84/controls
rm -rf -- "$SCR"; mkdir -p "$SCR" "$OUT"
trap 'rm -rf -- "$SCR"' EXIT
CTL=corpus/evidence/round84/c1-controls
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
c1() { python3 -B "$1/corpus/evidence/round84/depth-r84.py" --root "$1"; }
c2() { python3 -B "$1/corpus/evidence/round84/gate-records-r84.py" --root "$1" --repo "$LANE" --work "$SCR" "${@:2}"; }

overlay() { # TREE CONTROLDIR
  local t=$1 d=$2 f
  for f in "$d"/*.md; do cp -- "$f" "$t/corpus/knowledge/"; done
  python3 - "$t/corpus/SOURCES.md" "$d" <<'PY'
import os, re, sys
p, d = sys.argv[1], sys.argv[2]
lines = open(p, encoding='utf-8').read().split('\n')
if os.path.isfile(f'{d}/replace.txt'):
    for new in open(f'{d}/replace.txt', encoding='utf-8').read().strip('\n').split('\n'):
        sid = new.split('|')[1].strip()
        lines = [new if re.match(r'^ {0,3}\| ' + sid + r' \|', l) else l for l in lines]
if os.path.isfile(f'{d}/sources-append.txt'):
    add = open(f'{d}/sources-append.txt', encoding='utf-8').read().strip('\n').split('\n')
    last = max(i for i, l in enumerate(lines) if re.match(r'^ {0,3}\| S\d{3,} \|', l))
    lines[last + 1:last + 1] = add
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
PY
}

# ---- C1 depth ----
T=$(mk c1-d0); rec c1-d0-donothing FAIL c1 "$T"
T=$(mk c1-d1); overlay "$T" "$LANE/$CTL/D1-r81-filler"; rec c1-d1-r81-filler FAIL c1 "$T"
T=$(mk c1-d3); overlay "$T" "$LANE/$CTL/D3-r82-entry-relanded"; rec c1-d3-r82-entry-relanded FAIL c1 "$T"
T=$(mk c1-b1); overlay "$T" "$LANE/$CTL/B1-salad-boundary"; rec c1-b1-salad-boundary PASS c1 "$T"

# ---- C2 gate records ----
S=$LANE/corpus/evidence/round84/controls
T=$(mk c2-k0); git -C "$LANE" show 81b81173:tools/gate-records.py > "$T/tools/gate-records.py"; rec c2-k0-donothing FAIL c2 "$T"
T=$(mk c2-f1); rec c2-f1-stub-accept FAIL c2 "$T" --tool "$S/stub-accept.py"
T=$(mk c2-f2); rec c2-f2-stub-refuse FAIL c2 "$T" --tool "$S/stub-refuse.py"
T=$(mk c2-f3); rec c2-f3-stub-quote-only FAIL c2 "$T" --tool "$S/stub-quote-only.py"
T=$(mk c2-f4); rec c2-f4-stub-whitelist FAIL c2 "$T" --tool "$S/stub-whitelist.py"

cat "$OUT/summary.tsv"
awk -F'\t' '$2!=$3{bad++} END{printf "CONTROLS_AS_EXPECTED=%d/%d\n", NR-bad, NR; exit bad>0}' "$OUT/summary.tsv"
