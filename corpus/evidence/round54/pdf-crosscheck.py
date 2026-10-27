#!/usr/bin/env python3
"""pdf-crosscheck — every round-54 quote on a PDF capture (S123, the JMU reproduction of
GB/T 7714-2025) must also occur in an INDEPENDENT extraction of the PDF (pypdf), so no
quote is a column-glue artefact of the `.txt` sidecar (QUALITY 96; the round-53 tool,
round-54 paths). Round 54 adds one fold: the sidecar renders fullwidth Latin letters
and digits (`附录Ａ`, `ＹＹＹＹ`) where pypdf renders some halfwidth (W1
`R54DraftGateTable`), so both sides are compared whitespace-removed AND NFKC-folded;
the raw (unfolded) miss count is printed too.

Usage (needs pypdf; uv fetches it into its cache, nothing installed system-wide):
    uv run --quiet --with pypdf python corpus/evidence/round54/pdf-crosscheck.py
Prints `PDF_QUOTES=n NOT_IN_INDEPENDENT=k RAW_NOT_IN=r`; exit 0 when k == 0, 1 otherwise.
"""
import csv
import pathlib
import re
import sys
import unicodedata

from pypdf import PdfReader

Q = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
EV = pathlib.Path(__file__).resolve().parent
DOCS = {"S123": "0f33243fd7ac2fe88b85c1ba.raw"}


def raw(s: str) -> str:
    return re.sub(r"\s+", "", s)


def norm(s: str) -> str:
    return raw(unicodedata.normalize("NFKC", s))


pages = {k: "".join(p.extract_text() or "" for p in PdfReader(str(Q / f)).pages) for k, f in DOCS.items()}
ext = {k: norm(v) for k, v in pages.items()}
rawext = {k: raw(v) for k, v in pages.items()}
n = bad = rawbad = 0
with open(EV / "quotes.tsv", encoding="utf-8") as fh:
    for sid, _url, quote, _entry in list(csv.reader(fh, delimiter="\t"))[1:]:
        if sid in ext:
            n += 1
            rawbad += raw(quote) not in rawext[sid]
            if norm(quote) not in ext[sid]:
                bad += 1
                print(f"NOT_IN_INDEPENDENT {sid} {quote!r}")
print(f"PDF_QUOTES={n} NOT_IN_INDEPENDENT={bad} RAW_NOT_IN={rawbad}")
sys.exit(0 if bad == 0 else 1)
