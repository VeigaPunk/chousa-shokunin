# R55ExecPdfCrossV2 — PDF cross-check successor

Scope: draft only for `corpus/evidence/round55/pdf-crosscheck.py`; production lane untouched. F6 fix implemented in scratch; execution receipts below remain pending.

```python
# corpus/evidence/round55/pdf-crosscheck.py
#!/usr/bin/env python3
"""Independently cross-check all S123 quotes against the pinned PDF extraction."""
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
    with (EV / "quotes.tsv").open(encoding="utf-8", newline="") as fh:
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
```

## Evidence

- Frozen assignment input `corpus/evidence/round55/claims.md:11-13`: no network; capture cache is local. F6 request in `.ufo/waves/round-54/w2/R54W2SentFinal.md:137-153` explicitly requires S123 denominator, nonempty quote, pinned digest with `ENV_CHANGED`/2, malformed rows rejected, and four attacks.
- Existing file `corpus/evidence/round54/pdf-crosscheck.py:22-24` names raw capture `0f33243fd7ac2fe88b85c1ba.raw`. Digest retained from documented capture receipt in `.ufo/waves/round-48/w2/QuarantineS088.md:18-21`: `cb3ffbf5013e7a3a60e2c9408aef4fb65e2a23b58d785b57d8830a4c3d3c2a41`.
- `corpus/evidence/round54/quotes.tsv:1-34` has 21 S123 records (IDs S123, rows 14–34), with a tab-delimited header and four cells.
- Script is prepared at `/fast/scratch/hyaku/chousa-r55/R55ExecPdfCrossV2/pdf-crosscheck.py`; **not run**. The required pypdf-version receipt, positive baseline and all four negative fixture receipts are unavailable. No behavior is claimed as observed.
- Defect in this draft: it retains the round-54 quotes path (intentional existing corpus location); malformed CSV parsing and row-level cell counts are guarded, blank S123 quotes rejected, all S123 rows tallied against 21, and raw digest pin is checked before PDF extraction. It does not yet have attack-run evidence.

VERDICT: built a round-55 F6 successor draft with the specified denominator, empty-quote, digest, and malformed-row guards; execution and falsifier results are not established.
