#!/usr/bin/env python3
"""pdf-crosscheck (round 55; successor of corpus/evidence/round54/pdf-crosscheck.py, fixing round-54
W2 `R54W2SentFinal` F6): every S123 quote of the round-54 manifest occurs, whitespace removed and
NFKC-normalised, in an independent pypdf extraction of the pinned PDF. The denominator is the full
frozen set (21 S123 rows; a missing, renamed or extra row fails), an empty quote fails, a malformed
row (wrong cell count, a tab inside a quote) fails without a traceback, and the PDF is pinned by
sha256 (a changed capture is ENV_CHANGED, exit 2).
Usage: uv run --with pypdf python corpus/evidence/round55/pdf-crosscheck.py [QUOTES_TSV]
Exit 0 all quotes found · 1 a quote or row fails · 2 environment changed."""
import csv
import hashlib
import pathlib
import re
import sys
import unicodedata

from pypdf import PdfReader

Q = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
EV = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54")
DOCS = {"S123": ("0f33243fd7ac2fe88b85c1ba.raw", "cb3ffbf5013e7a3a60e2c9408aef4fb65e2a23b58d785b57d8830a4c3d3c2a41")}

def raw(s):
    return re.sub(r"\s+", "", s)

def norm(s):
    return raw(unicodedata.normalize("NFKC", s))

def fail(message, code=1):
    print(message, file=sys.stderr)
    raise SystemExit(code)

pages = {}
for sid, (filename, expected) in DOCS.items():
    path = Q / filename
    try:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        fail(f"ENV_CHANGED {sid}: cannot read pinned PDF: {exc}", 2)
    if digest != expected:
        fail(f"ENV_CHANGED {sid}: sha256 {digest} != {expected}", 2)
    try:
        pages[sid] = "".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    except Exception as exc:
        fail(f"PDF extraction failed for {sid}: {exc}")
ext = {sid: norm(text) for sid, text in pages.items()}
rawext = {sid: raw(text) for sid, text in pages.items()}
counts = {sid: 0 for sid in DOCS}
bad = rawbad = 0
try:
    with (pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else EV / "quotes.tsv").open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh, delimiter="\t", strict=True)
        header = next(reader, None)
        if header != ["id", "url", "quote", "entry"]:
            fail("malformed quotes.tsv header")
        for line, row in enumerate(reader, 2):
            if len(row) != 4:
                fail(f"malformed quotes.tsv row {line}: expected 4 cells, got {len(row)}")
            sid, _url, quote, _entry = row
            if sid in DOCS:
                if not quote:
                    fail(f"empty quote in S123 row {line}")
                counts[sid] += 1
                rawbad += raw(quote) not in rawext[sid]
                if norm(quote) not in ext[sid]:
                    bad += 1
                    print(f"NOT_IN_INDEPENDENT {sid} {quote!r}")
except (OSError, csv.Error, UnicodeError) as exc:
    fail(f"malformed quotes.tsv: {exc}")
expected_counts = {"S123": 21}
for sid, expected in expected_counts.items():
    if counts[sid] != expected or counts[sid] < 1:
        fail(f"row denominator mismatch {sid}: got {counts[sid]}, expected {expected}")
print(f"PDF_QUOTES={sum(counts.values())} NOT_IN_INDEPENDENT={bad} RAW_NOT_IN={rawbad}")
sys.exit(0 if bad == 0 else 1)
