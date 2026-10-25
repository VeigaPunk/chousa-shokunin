#!/usr/bin/env python3
"""decode-form-check — a lesson that gives `char N` offsets must name the capture form they index (QUALITY 76).

A `char N` offset is meaningless without the text form it indexes: round 49 gave NCPSSD help-page offsets
24872/25269 while a plain `utf-8-sig` read puts the same quotes at 24556/24953 (verifier spot-check defect 5).
Usage: python3 decode-form-check.py LESSON.md [LESSON.md ...]
For each file with at least one `char <digits>` token, prints `FORM_NAMED` when its text names a form
(`.txt` read as UTF-8, `utf-8-sig`, or `.raw` decoded as UTF-16LE) on a line that also says `char`, offset or decode form, not negated and `FORM_MISSING` otherwise, then
`DECODE_FORM=PASS|FAIL`. Exit 1 when any file is FORM_MISSING, 0 otherwise, 2 on usage or an unreadable file. A file with no offset
is `NO_OFFSETS` and passes. Named limits (W2 `R50ExecFormProbe`): one naming per file, not one per offset; a WRONG form named in the right place passes (the check cannot open the capture)."""
import pathlib
import re
import sys

if len(sys.argv) < 2:
    print("usage: decode-form-check.py LESSON.md ...", file=sys.stderr)
    sys.exit(2)
# a form is NAMED on a line that also says offset/char/decode form, names one of the three forms, and does not negate it
FORM_LINE = re.compile(r"(?=.*(?:\bchar\b|offset|decode form))(?=.*(?:utf-?8-sig|UTF-16LE|\.txt[^\n]{0,40}UTF-8|UTF-8[^\n]{0,40}\.txt))", re.I)
NEGATED = re.compile(r"\b(?:not|never|no)\b[^\n]{0,15}(?:utf-?8-sig|UTF-16LE|UTF-8)", re.I)
def named(t: str) -> bool:
    return any(FORM_LINE.search(l) and not NEGATED.search(l) for l in t.splitlines())
bad = 0
for p in sys.argv[1:]:
    try:
        t = pathlib.Path(p).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(2)
    if not re.search(r"\bchar\s+\d+", t):
        print(f"NO_OFFSETS {p}")
    elif named(t):
        print(f"FORM_NAMED {p}")
    else:
        print(f"FORM_MISSING {p}")
        bad += 1
print("DECODE_FORM=" + ("FAIL" if bad else "PASS"))
sys.exit(1 if bad else 0)
