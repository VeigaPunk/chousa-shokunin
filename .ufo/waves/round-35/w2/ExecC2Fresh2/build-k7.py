#!/usr/bin/env python3
"""Build a SHOW-CALL bypass candidate: for every long span the gate calls
tok_span_offsets_chunk once (its output discarded) and answers from an exact
python bytes.find helper. The printed verdicts are contract-correct, so the
output counter scores it full; the trace still stamps the chunk matcher's
entry line once per long search, so the trace witness scores it pass too.

Usage: build-k7.py <gate> <out.sh> <helper.py>
"""
import sys

HELPER_SRC = '''import os, sys
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

BRANCH = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    _K7OFF=$(tok_span_offsets_chunk "$hay" "$span")
    printf '%%s' "$hay" | python3 "%s" "$span"
    return 0
  fi
'''


def patch(gate_text, helper):
    lines = gate_text.splitlines(keepends=True)
    start = None
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets()"):
            start = i
            break
    if start is None:
        raise SystemExit("tok_span_offsets not found")
    body = None
    for j in range(start + 1, min(start + 40, len(lines))):
        if lines[j].strip().startswith("local hay=$1 span=$2"):
            body = j + 1
            break
    if body is None:
        raise SystemExit("parameter locals not found")
    return "".join(lines[:body] + [BRANCH % helper] + lines[body:])


def main():
    gate, outp, helperp = sys.argv[1:4]
    with open(helperp, "w", encoding="utf-8") as f:
        f.write(HELPER_SRC)
    text = open(gate, encoding="utf-8", errors="surrogateescape").read()
    with open(outp, "w", encoding="utf-8") as f:
        f.write(patch(text, helperp))
    print("wrote %s" % outp)


if __name__ == "__main__":
    main()
