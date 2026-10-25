#!/usr/bin/env python3
"""decode-form-check — a lesson that gives `char N` offsets must name the capture form they index (QUALITY 76).

A `char N` offset is meaningless without the text form it indexes: round 49 gave NCPSSD help-page offsets
24872/25269 while a plain `utf-8-sig` read puts the same quotes at 24556/24953 (verifier spot-check defect 5).
Usage: python3 decode-form-check.py LESSON.md [LESSON.md ...]
For each file with at least one `char <digits>` token, prints `FORM_NAMED` when its text names a form
(`.txt` read as UTF-8, `utf-8-sig`, or `.raw` decoded as UTF-16LE) and `FORM_MISSING` otherwise, then
`DECODE_FORM=PASS|FAIL`. Exit 1 when any file is FORM_MISSING, 0 otherwise, 2 on usage. A file with no offset
is `NO_OFFSETS` and passes. Named limit: one naming per file, not one per offset."""
import pathlib
import re
import sys

if len(sys.argv) < 2:
    print("usage: decode-form-check.py LESSON.md ...", file=sys.stderr)
    sys.exit(2)
FORM = re.compile(r"utf-?8-sig|UTF-16LE|`\.txt` (?:read as )?UTF-8|\.txt.{0,40}UTF-8|decode form", re.I)
bad = 0
for p in sys.argv[1:]:
    t = pathlib.Path(p).read_text(encoding="utf-8", errors="replace")
    if not re.search(r"\bchar\s+\d+", t):
        print(f"NO_OFFSETS {p}")
    elif FORM.search(t):
        print(f"FORM_NAMED {p}")
    else:
        print(f"FORM_MISSING {p}")
        bad += 1
print("DECODE_FORM=" + ("FAIL" if bad else "PASS"))
sys.exit(1 if bad else 0)
