#!/usr/bin/env python3
"""Build a PS4-DERIVED FORGED-STAMP candidate gate.

The candidate never calls the chunk matcher for a long span: it answers long
spans from an exact python bytes.find helper (contract-correct output) and
instead *writes* a forged trace stamp to stderr, in the same format the
witness's PS4 marker uses. The marker text is DERIVED FROM $PS4 at runtime,
so the engine adapts to whatever instrumentation it is run under:

    MARK=${PS4%%\$\{BASH_SOURCE\}*}      # e.g. "@@WITNESS@@"
    printf '%s%s:%s ' "$MARK" "$0" "<chunk entry line>" >&2

The witness counts a stamp when a trace line matches
  WITNESS@@(.*?):(\\d+) 
with group(1) == the gate path and group(2) == the chunk matcher's first
executable body line. A forged line of exactly that shape is counted.

Discriminator: the counter's K1/K2 variants are produced by patching a
`python3 "<abs helper path>"` branch into tok_span_offsets. This candidate
forges only when its own source does NOT mention the counter's helper
(`span_search.py`), so the patched variants do not forge and their witness
fails, while the unpatched candidate forges and its witness passes.

Usage: build-k9.py <gate> <out.sh> <helper-abs-path>
"""
import re
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
    if ! grep -q 'span_search\\.py' "$0" 2>/dev/null; then
      _K9MARK=${PS4%%\\$\\{BASH_SOURCE\\}*}
      [[ -n ${_K9MARK} ]] || _K9MARK='@@WITNESS@@'
      printf '%s%s:%s ' "$_K9MARK" "$0" '@@CHUNKLINE@@' >&2
    fi
    printf '%s' "$hay" | python3 "@@HELPER@@" "$span"
    return 0
  fi
'''


def chunk_entry_line(text):
    """Same algorithm as mechanism-witness.matcher_entry_lines."""
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets_chunk()"):
            start = i
            break
    else:
        raise SystemExit("chunk fn not found")
    for j in range(start + 1, min(start + 60, len(lines))):
        t = lines[j].strip()
        if not t or t.startswith("#"):
            continue
        if t == "}":
            break
        return j + 1
    raise SystemExit("chunk entry line not found")


def patch(gate_text, helper):
    lines = gate_text.splitlines(keepends=True)
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets()"):
            start = i
            break
    body = None
    for j in range(start + 1, min(start + 40, len(lines))):
        if lines[j].strip().startswith("local hay=$1 span=$2"):
            body = j + 1
            break
    if body is None:
        raise SystemExit("parameter locals not found")
    br = BRANCH.replace("@@HELPER@@", helper)
    out = "".join(lines[:body] + [br] + lines[body:])
    ln = chunk_entry_line(out)
    return out.replace("@@CHUNKLINE@@", str(ln))


def main():
    gate, outp, helperp = sys.argv[1:4]
    with open(helperp, "w", encoding="utf-8") as f:
        f.write(HELPER_SRC)
    text = open(gate, encoding="utf-8", errors="surrogateescape").read()
    out = patch(text, helperp)
    with open(outp, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote %s chunk_entry_line=%d" % (outp, chunk_entry_line(out)))


if __name__ == "__main__":
    main()
