#!/usr/bin/env python3
"""cited-id-check — every staged id the adopter renumbered must be named on a `source:` line of one of the entries,
not a body cross-reference to another document.

Usage: python3 cited-id-check.py <renumber.tsv> <staged-entry.md> [<staged-entry.md> ...]
Prints `BODY_CROSSREF <staged>-><lane>` for each renumbered staged id that no entry names at the start of a
`source:` line, `CITED_IDS=PASS|FAIL rows=n`. Exit 0 every id is a source id · 1 a body cross-reference ·
2 no rows or an unreadable file. Named limit: it reads the renumber table of the run it is given; an id the
adopter did not renumber (a pass-through such as a lane-registry id) is not seen (QUALITY 77)."""
import pathlib
import re
import sys

if len(sys.argv) < 3:
    print("usage: cited-id-check.py <renumber.tsv> <entry.md> [...]", file=sys.stderr)
    sys.exit(2)
try:
    rows = [l for l in pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    entries = "\n".join(pathlib.Path(p).read_text(encoding="utf-8") for p in sys.argv[2:])
except OSError as exc:
    print(f"ERROR {exc}", file=sys.stderr)
    sys.exit(2)
if not rows:
    print("NO_ROWS")
    sys.exit(2)
bad = 0
for l in rows:
    staged, lane_id = l.split("\t")[:2]
    if not re.search(rf"^source: {staged}\b", entries, re.M):
        print(f"BODY_CROSSREF {staged}->{lane_id}")
        bad += 1
print(f"CITED_IDS={'FAIL' if bad else 'PASS'} rows={len(rows)}")
sys.exit(1 if bad else 0)
