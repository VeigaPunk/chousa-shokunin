#!/usr/bin/env python3
"""Round-35 w2 threshold attack: build candidate engines from a pristine gate.

Engine A: tok_span_offsets_chunk is called exactly ONCE per gate run (on the
          first long-span record); every other long span is answered by an exact
          python bytes.find search.
Engine B: tok_span_offsets_chunk is called once per long-span record and the
          result is discarded; every long span is answered by exact search.
Engine C: as B, but the chunk matcher is called 8 times on the FIRST long record
          only (total count == long_records); the other 7 long records never
          touch it. Probes whether the frozen threshold attributes calls to
          records or only counts them.
Engine D: as C, but 7 calls total (< long_records); boundary control that the
          pass/fail line is the total count.

Only the gate is patched; mechanism-witness.py is used unmodified.
"""
import hashlib
import os
import sys

HELPER = sys.argv[1]          # abs path to span_search.py
OUT = sys.argv[2]             # output dir
PRISTINE = sys.argv[3]        # pristine gate path

PY = 'printf \'%%s\' "$hay" | python3 "%s" "$span"' % HELPER

BRANCHES = {
    # exactly one chunk call for the whole run
    "engine-A": '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    if [[ ! -e $_WONCE_FILE ]]; then
      : > "$_WONCE_FILE"
      tok_span_offsets_chunk "$hay" "$span"
    else
      %s
    fi
    return 0
  fi
''' % PY,
    # one chunk call per long record, result discarded
    "engine-B": '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    tok_span_offsets_chunk "$hay" "$span" >/dev/null
    %s
    return 0
  fi
''' % PY,
    # 8 chunk calls on the first long record only (== long_records)
    "engine-C": '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    if [[ ! -e $_WONCE_FILE ]]; then
      : > "$_WONCE_FILE"
      local _wi=0
      for (( _wi=0; _wi<8; _wi++ )); do
        tok_span_offsets_chunk "$hay" "$span" >/dev/null
      done
    fi
    %s
    return 0
  fi
''' % PY,
    # 7 chunk calls on the first long record only (< long_records)
    "engine-D": '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    if [[ ! -e $_WONCE_FILE ]]; then
      : > "$_WONCE_FILE"
      local _wi=0
      for (( _wi=0; _wi<7; _wi++ )); do
        tok_span_offsets_chunk "$hay" "$span" >/dev/null
      done
    fi
    %s
    return 0
  fi
''' % PY,
}


def patch(text, branch):
    lines = text.splitlines(keepends=True)
    # top-level sentinel path, evaluated once per gate process
    for i, l in enumerate(lines):
        if l.startswith("TOK_DIRECT_SPAN_MAX="):
            lines.insert(i + 1, '_WONCE_FILE="${TMPDIR:-/tmp}/.mw-once-$$-$RANDOM"\n')
            break
    else:
        raise SystemExit("constants anchor not found")
    start = next(j for j, l in enumerate(lines) if l.startswith("tok_span_offsets()"))
    body = None
    for j in range(start + 1, start + 40):
        if lines[j].strip() == "local hay=$1 span=$2":
            body = j + 1
            break
    if body is None:
        raise SystemExit("locals anchor not found")
    return "".join(lines[:body] + [branch] + lines[body:])


def main():
    text = open(PRISTINE, encoding="utf-8", errors="surrogateescape").read()
    for name, branch in BRANCHES.items():
        p = os.path.join(OUT, name + ".sh")
        with open(p, "w", encoding="utf-8") as f:
            f.write(patch(text, branch))
        os.chmod(p, 0o755)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        print("%s sha256=%s" % (name, h))


if __name__ == "__main__":
    main()
