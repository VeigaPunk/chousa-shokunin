#!/usr/bin/env bash
# Differential of the LANDED gate's boundary predicates (tok_left_ok,
# tok_right_ok) against the python oracle's transcription, on random byte
# contexts.  The predicate block is extracted VERBATIM from a copy of the
# landed gate blob (sha256 a6307edf687ac0fb...); the lane is never written.
set -u
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
GATE=$HERE/landed-gate-a6307edf.sh
WORK=$(mktemp -d "$HERE/tmp/bnd.XXXXXX")
trap 'rm -rf "$WORK"' EXIT

sed -n '/^TOK_WS=/,/^}/p' "$GATE" > "$WORK/pred.sh"
sed -n '/^tok_word_char() {/,/^}/p' "$GATE" >> "$WORK/pred.sh"
sed -n '/^tok_left_ok() {/,/^}/p' "$GATE" >> "$WORK/pred.sh"
sed -n '/^tok_right_ok() {/,/^}/p' "$GATE" >> "$WORK/pred.sh"
echo "extracted_predicate_lines=$(grep -c . "$WORK/pred.sh")"

python3 - "$WORK/cases.tsv" <<'PY'
import random, sys
rng = random.Random(20261023)
ALPHA = "abcdefghijklmnopqrstuvwxyz"
SPECIAL = list(" -'.,;:!?()[]{}\"@#$%^&*+=|/\\~`\t\n\r\x0b\x0c")
NONASCII = ["é", "日", "ß", "→"]
rows = []
for i in range(4000):
    def ctx(n):
        out = []
        for _ in range(n):
            r = rng.random()
            if r < 0.45:
                out.append(rng.choice(ALPHA))
            elif r < 0.85:
                out.append(rng.choice(SPECIAL))
            else:
                out.append(rng.choice(NONASCII))
        return "".join(out)
    before = ctx(rng.randint(0, 4))
    span = ctx(rng.randint(1, 4))
    after = ctx(rng.randint(0, 4))
    # the tab separator must not appear inside a field: SPECIAL has \t, drop it
    def hx(t):
        return t.encode("utf-8").hex()
    rows.append((hx(before), hx(span), hx(after)))
with open(sys.argv[1], "w", encoding="ascii") as fh:
    for b, s, a in rows:
        fh.write("%s\t%s\t%s\n" % (b, s, a))
print("cases=%d" % len(rows))
PY

export LC_ALL=C
while IFS=$'\t' read -r hbefore hspan hafter; do
  # command substitution strips trailing newlines: append a sentinel and drop it
  before=$(printf '%s' "$hbefore" | xxd -r -p; printf X); before=${before%X}
  span=$(printf '%s' "$hspan" | xxd -r -p; printf X); span=${span%X}
  after=$(printf '%s' "$hafter" | xxd -r -p; printf X); after=${after%X}
  # shellcheck disable=SC1090
  source "$WORK/pred.sh"
  if tok_left_ok "$before" "$span"; then lb=1; else lb=0; fi
  if tok_right_ok "$after" "$span"; then rb=1; else rb=0; fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$lb" "$rb" "$hbefore" "$hspan" "$hafter"
done < "$WORK/cases.tsv" > "$WORK/bash_out.tsv"

python3 - "$WORK/bash_out.tsv" <<'PY'
import sys
sys.path.insert(0, "/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC2Oracle")
from oracle import left_ok, right_ok
n = bad = 0
for line in open(sys.argv[1], "rb").read().split(b"\n"):
    if not line.strip():
        continue
    lb, rb, hb, hs, ha = line.split(b"\t", 4)
    before = bytes.fromhex(hb.decode()); span = bytes.fromhex(hs.decode()); after = bytes.fromhex(ha.decode())
    hay = before + span + after
    off = len(before)
    ol = 1 if left_ok(hay, off, span) else 0
    orr = 1 if right_ok(hay, off, span) else 0
    n += 1
    if ol != int(lb) or orr != int(rb):
        bad += 1
        if bad <= 10:
            print("DIVERGE bash(l=%s,r=%s) oracle(l=%d,r=%d) before=%r span=%r after=%r"
                  % (lb.decode(), rb.decode(), ol, orr, before, span, after))
print("BOUNDARY_CASES=%d DIVERGENCES=%d" % (n, bad))
PY
