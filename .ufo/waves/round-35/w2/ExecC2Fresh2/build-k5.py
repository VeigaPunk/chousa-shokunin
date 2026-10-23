#!/usr/bin/env python3
"""Build attack variants of the landed chousa gate that answer long-span
searches WITHOUT the chunk matcher, while keeping the printed verdicts
contract-correct (exact, non-overlapping, left-to-right) so an output-only
counter cannot kill them.

Modes:
  skip1   : the FIRST long-span search is answered by an exact python helper;
            every later long span still goes through the chunk matcher.
            (Tests whether the witness's chunk stamp count enforces PER-RECORD
            coverage or only an AGGREGATE count.)
  show    : every long span calls the chunk matcher once (its result discarded)
            and the answer comes from the python helper.
  all     : every long span answered by the python helper (K1-like).
  skipN   : the first N long-span searches answered by the helper.

The counter must persist across the process-substitution subshell, so it is
kept in a file (the shell variable trick does not survive the subshell).

Usage: build-k5.py <gate> <out.sh> <helper.py> <mode> <counterfile> [N]
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

HEAD = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    _K5N=$(cat "%s" 2>/dev/null || echo 0)
    _K5N=$(( _K5N + 1 ))
    printf '%%s' "$_K5N" > "%s"
'''

SKIP_BODY = '''    if (( _K5N <= %d )); then
      printf '%%s' "$hay" | python3 "%s" "$span"
      return 0
    fi
'''

SHOW_BODY = '''    printf '%%s' "$hay" | python3 "%s" "$span"
    return 0
'''


def patch(gate_text, helper, mode, cfile, n):
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
    br = HEAD % (cfile, cfile)
    if mode == "skip1":
        br += SKIP_BODY % (n, helper)
    elif mode == "show":
        br += SHOW_BODY % helper
    elif mode == "all":
        br += SKIP_BODY % (10 ** 9, helper)
    else:
        raise SystemExit("unknown mode " + mode)
    br += "  fi\n"
    return "".join(lines[:body] + [br] + lines[body:])


def main():
    gate, outp, helperp, mode, cfile = sys.argv[1:6]
    n = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    with open(helperp, "w", encoding="utf-8") as f:
        f.write(HELPER_SRC)
    text = open(gate, encoding="utf-8", errors="surrogateescape").read()
    with open(outp, "w", encoding="utf-8") as f:
        f.write(patch(text, helperp, mode, cfile, n))
    print("wrote %s mode=%s n=%s" % (outp, mode, n))


if __name__ == "__main__":
    main()
