#!/usr/bin/env python3
"""pdf-crosscheck — every round-53 quote on a PDF capture (S117 JMLA, S118 the issued
guideline) must also occur, whitespace-removed, in an INDEPENDENT extraction of the
PDF (pypdf), so no quote is a two-column glue artefact of the `.txt` sidecar's
`pdftotext -layout` reading (W1 `R53ExecPdfForm`: 50.2 % of the JMLA body sits on
paired-column lines).

Usage (needs pypdf; uv fetches it into its cache, nothing installed system-wide):
    uv run --quiet --with pypdf python corpus/evidence/round53/pdf-crosscheck.py
Prints `PDF_QUOTES=n NOT_IN_INDEPENDENT=k`; exit 0 when k == 0, 1 otherwise.
"""
import csv
import pathlib
import re
import sys

from pypdf import PdfReader

Q = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
EV = pathlib.Path(__file__).resolve().parent
DOCS = {"S117": "0ae65ac01b93119d3c2f3fed.raw", "S118": "16fe8487aa97b98576a0dbac.raw"}


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


ext = {k: norm("".join(p.extract_text() or "" for p in PdfReader(str(Q / f)).pages)) for k, f in DOCS.items()}
n = bad = 0
with open(EV / "quotes.tsv", encoding="utf-8") as fh:
    for sid, _url, quote, _entry in list(csv.reader(fh, delimiter="\t"))[1:]:
        if sid in ext:
            n += 1
            if norm(quote) not in ext[sid]:
                bad += 1
                print(f"NOT_IN_INDEPENDENT {sid} {quote!r}")
print(f"PDF_QUOTES={n} NOT_IN_INDEPENDENT={bad}")
sys.exit(0 if bad == 0 else 1)
