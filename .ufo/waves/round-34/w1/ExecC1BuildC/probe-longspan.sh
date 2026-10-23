#!/usr/bin/env bash
# probe-longspan.sh -- independent behaviour+timing probe for the long-span
# matcher. It builds its own fixtures (its own vocabulary and its own span
# shapes; it is NOT the round-34 counter) and runs the gate under test once
# per record, reporting the gate verdict and the wall time per record.
#
# Usage: probe-longspan.sh <gate.sh> <workdir>
# Prints one "REC <id> rc=<rc> <verdict> elapsed=<s>" line per record and a
# final summary line. The fixture and the per-record logs stay in <workdir>.
set -uo pipefail

GATE=$1
WORK=$2
mkdir -p "$WORK/lib" "$WORK/logs"
LC_ALL=C
export LC_ALL

python3 - "$WORK" <<'PY'
import json, os, random, sys
work = sys.argv[1]
rng = random.Random(20241023)
vocab = [''.join(rng.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(rng.randint(3, 11)))
         for _ in range(6000)]

def text(nbytes):
    out = []
    total = 0
    while total < nbytes:
        w = rng.choice(vocab)
        if out:
            sep = '\n' if rng.randrange(12) == 0 else ' '
            out.append(sep); total += 1
        out.append(w); total += len(w)
    return ''.join(out)

def mutate(s, at):
    i = at
    while i < len(s) and not s[i].isalpha():
        i += 1
    return s[:i] + ('Z' if s[i] != 'Z' else 'Y') + s[i+1:]

cases = []
# --- short band (the direct one-pattern matcher must be unchanged) ---
sh = text(3000)
open(f'{work}/lib/short.md', 'w').write("lead " + sh + " tail\n")
cases.append(("SHORT-VERBATIM", f'{work}/lib/short.md', sh, None))
cases.append(("SHORT-MUTATED", f'{work}/lib/short.md', mutate(sh, 1500), None))
# --- long band (the chunked matcher) ---
lv = text(33000)
open(f'{work}/lib/long.md', 'w').write("lead " + lv + " tail\n")
cases.append(("LONG-VERBATIM", f'{work}/lib/long.md', lv, None))
cases.append(("LONG-MUT-HEAD", f'{work}/lib/long.md', mutate(lv, 30), None))
cases.append(("LONG-MUT-MID", f'{work}/lib/long.md', mutate(lv, 20000), None))
cases.append(("LONG-MUT-TAIL", f'{work}/lib/long.md', mutate(lv, len(lv) - 30), None))
# split: both halves present, never adjacent
k = len(lv) // 2
open(f'{work}/lib/split.md', 'w').write("lead " + lv[:k] + " mid " + lv[k+1:] + " tail\n")
cases.append(("LONG-SPLIT", f'{work}/lib/split.md', lv, None))
# glued on the left / on the right
open(f'{work}/lib/glued-l.md', 'w').write("leadx" + lv + " tail\n")
cases.append(("LONG-GLUED-LEFT", f'{work}/lib/glued-l.md', lv, None))
open(f'{work}/lib/glued-r.md', 'w').write("lead " + lv + "xtail\n")
cases.append(("LONG-GLUED-RIGHT", f'{work}/lib/glued-r.md', lv, None))
# two occurrences; "line" names the second (bound) and a line that names
# neither occurrence (mislocated)
open(f'{work}/lib/two.md', 'w').write("head\n" + lv + "\nmid\n" + lv + "\n")
cases.append(("LONG-LINE-BOUND", f'{work}/lib/two.md', lv, "4"))
cases.append(("LONG-LINE-WRONG", f'{work}/lib/two.md', lv, "3"))
# edges of the direct/chunk boundary
for n in (16384, 16385, 32767, 32768):
    e = text(n)
    open(f'{work}/lib/edge{n}.md', 'w').write("lead " + e + " tail\n")
    cases.append((f"EDGE-{n}", f'{work}/lib/edge{n}.md', e, None))

for cid, src, span, line in cases:
    rec = {"id": cid, "source": src, "span": span, "expect": "supported"}
    if line:
        rec["line"] = line
    with open(f'{work}/claims-{cid}.jsonl', 'w') as f:
        f.write(json.dumps(rec) + "\n")
print(len(cases))
PY

n=$(ls "$WORK"/claims-*.jsonl 2>/dev/null | wc -l)
printf 'records=%s\n' "$n"
for c in "$WORK"/claims-*.jsonl; do
  id=$(basename "$c" .jsonl); id=${id#claims-}
  start=$(date +%s.%N)
  out=$(timeout 900 bash "$GATE" verify-claims "$c" --root "$WORK" 2>"$WORK/logs/$id.err")
  rc=$?
  end=$(date +%s.%N)
  el=$(awk -v a="$start" -v b="$end" 'BEGIN{printf "%.2f", b-a}')
  obs=$(printf '%s\n' "$out" | sed -n "s/^CLAIM id=$id expected=[^ ]* observed=\([^ ]*\).*/\1/p" | head -1)
  [ -n "$obs" ] || obs=$(printf '%s\n' "$out" | grep -c '^CLAIM ' | sed 's/^0$/no-claim-line/')
  printf 'REC %s rc=%s observed=%s elapsed=%ss\n' "$id" "$rc" "$obs" "$el"
  printf '%s\n' "$out" > "$WORK/logs/$id.out"
done
