#!/usr/bin/env python3
"""build-forge.py — regenerate the round-35 erratum-11 forged candidate gate.

Reproducer for wave seat ExecC2Fresh1's finding: the mechanism witness
(tools/mechanism-witness.py) reads its stamps out of the gate's *own stderr*,
and the stamp format is shipped to the gate in its own environment as PS4. A
gate that never calls tok_span_offsets_chunk can therefore emit stamps derived
from $PS4 and score WITNESS=pass with 0 real chunk-body executions.

Self-contained: no patched gate is shipped. Given any gate revision, it inserts
the forgery branch as the first statement of tok_span_offsets' body and emits a
candidate gate. The chunk entry line is located *at gate runtime* by the forged
candidate itself (awk over its own source, mirroring mechanism-witness.py's
matcher_entry_lines), so the candidate keeps working across gate revisions --
verified on 1f2fb4f5 (wave base) and a4768851 (pin-hardened final blob).

Usage:
  python3 build-forge.py --gate tools/research-gate.sh --out /tmp/spoof.sh
  python3 tools/mechanism-witness.py --gate /tmp/spoof.sh --seed 3547
  python3 corpus/evidence/round35/c2-count.py --gate /tmp/spoof.sh --seed 3547

Expected (measured, seed 3547, hardened gate a4768851):
  witness: WITNESS=pass OUTPUT=9/9 STAMPS chunk=360 direct=1 (long records=8)
  counter: WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass  (exit 0)
  real chunk-body executions: 0

Exit: 0 built | 2 harness error.
"""
import argparse
import os
import stat
import sys

SNIPPET = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    # FORGERY: emit witness-shaped stamps on stderr; never call the chunk matcher
    __wp="${BASH_SOURCE[0]:-$0}"
    __ln=$(awk 'BEGIN{f=0} /^tok_span_offsets_chunk\\(\\)/{f=1;next} f{ if ($0 ~ /^[[:space:]]*#/ || $0 ~ /^[[:space:]]*$/) next; print NR; exit }' "$__wp")
    __bs='${BASH_SOURCE}'
    __lnp='${LINENO}'
    __fake=${PS4/"$__bs"/"$__wp"}
    __fake=${__fake/"$__lnp"/"$__ln"}
    __i=0
    while (( __i < 40 )); do
      printf '%s\\n' "$__fake" >&2
      __i=$(( __i + 1 ))
    done
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
'''

HELPER_DEFAULT = '''import os, sys
hay = sys.stdin.buffer.read()
span = os.fsencode(sys.argv[1])
off = 0
while True:
    i = hay.find(span, off)
    if i < 0:
        break
    sys.stdout.write("%d\\n" % i)
    off = i + len(span)
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True, help="gate to forge from")
    ap.add_argument("--out", required=True, help="candidate gate to write")
    ap.add_argument("--helper", default=None,
                    help="python exact-search helper (created if absent)")
    a = ap.parse_args()
    if not os.path.isfile(a.gate):
        print("build-forge: gate not found: %s" % a.gate, file=sys.stderr)
        return 2
    helper = os.path.abspath(a.helper or os.path.join(
        os.path.dirname(os.path.abspath(a.out)), "span_search.py"))
    if not os.path.isfile(helper):
        with open(helper, "w", encoding="utf-8") as f:
            f.write(HELPER_DEFAULT)
    text = open(a.gate, encoding="utf-8", errors="surrogateescape").read()
    lines = text.splitlines(keepends=True)
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("tok_span_offsets()"))
        body = next(j for j in range(start + 1, start + 40)
                    if lines[j].strip().startswith("local hay=$1 span=$2"))
    except StopIteration:
        print("build-forge: tok_span_offsets / parameter locals not found", file=sys.stderr)
        return 2
    snippet = SNIPPET.replace("@HELPER@", helper)
    out = "".join(lines[:body + 1] + [snippet] + lines[body + 1:])
    with open(a.out, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(out)
    os.chmod(a.out, os.stat(a.out).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print("build-forge: wrote %s (helper %s)" % (a.out, helper))
    return 0


if __name__ == "__main__":
    sys.exit(main())
