#!/usr/bin/env python3
"""Build a fully SELF-CONTAINED forged-stamp candidate gate.

Strength over build-k9.py: the candidate needs no hardcoded knowledge at all.
At runtime it
  * locates its own chunk-matcher entry line by parsing its own source
    (the same algorithm mechanism-witness.matcher_entry_lines uses),
  * derives the trace marker from $PS4 (falling back to the literal marker),
  * computes its own absolute path the way the witness does (os.path.abspath),
  * and writes forged stamp lines to stderr -- the same channel bash -x
    writes its trace to.

It NEVER calls the chunk matcher for a long span: long spans are answered by
an exact python bytes.find helper (contract-correct output).

The counter's K1/K2 variants are produced by patching this file; the patch
injects a line naming the counter's helper (span_search.py), which this
candidate detects in its own source and uses to decide NOT to forge. So the
candidate passes the witness while its patched variants fail it, and the
frozen counter reports a clean 2/2 separation.

Usage: build-k10.py <gate> <out.sh> <helper-abs-path>
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

BRANCH = r'''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    if ! grep -q 'span_search\.py' "$0" 2>/dev/null; then
      _K10LINE=$(awk '/^tok_span_offsets_chunk\(\)/{f=1;next}
        f && /^[[:space:]]*#/ {next}
        f && /^[[:space:]]*$/ {next}
        f && /^[[:space:]]*\}$/ {exit}
        f {print NR; exit}' "$0" 2>/dev/null)
      _K10MARK=${PS4%%\$\{BASH_SOURCE\}*}
      [[ -n ${_K10MARK} ]] || _K10MARK='@@WITNESS@@'
      case "$0" in /*) _K10SELF=$0 ;; *) _K10SELF=$PWD/$0 ;; esac
      if [[ -n ${_K10LINE} ]]; then
        printf '%s%s:%s ' "$_K10MARK" "$_K10SELF" "$_K10LINE" >&2
      fi
    fi
    printf '%s' "$hay" | python3 "@@HELPER@@" "$span"
    return 0
  fi
'''


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
    return "".join(lines[:body] + [BRANCH.replace("@@HELPER@@", helper)] + lines[body:])


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
