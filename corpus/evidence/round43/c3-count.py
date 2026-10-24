#!/usr/bin/env python3
"""c3-count — frozen counter for round 43 claim C3 (depth).

Predicate R43-C3, the same sentence as corpus/evidence/round43/claims.md:
the admitted entry cites lane id S078, that row's URL is the Europe PMC
full-text URL opened this round, and the located quote is a substring of
that URL's committed capture.

Cheapest gate that would score full marks without the work (QUALITY 60): an
entry that repeats the quote and names S078 without the quote being in the
capture. This counter reads the capture by the row's URL and requires the
quote there. A missing entry exits 1.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
ENTRY = LANE / "corpus" / "knowledge" / "search-log-method-r39.md"
SOURCES = LANE / "corpus" / "SOURCES.md"
CACHE = pathlib.Path(
    "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
)
URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML"
QUOTE = "to register the steps taken and to make searches accountable and reproducible"


def row_for(sources: pathlib.Path, sid: str) -> str:
    for line in sources.read_text(encoding="utf-8").splitlines():
        if re.match(r"^ {0,3}\|\s*" + sid + r"\s*\|", line):
            return line
    return ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entry", default=str(ENTRY))
    ap.add_argument("--sources", default=str(SOURCES))
    args = ap.parse_args(argv)
    entry = pathlib.Path(args.entry)
    sources = pathlib.Path(args.sources)
    if not entry.is_file():
        print("ENTRY_CITES=0/1")
        print("QUOTE_LOCATED=0/1")
        print("URL_MATCH=0/1")
        print("C3=FAIL entry-missing")
        return 1
    text = entry.read_text(encoding="utf-8")
    cites = "source: S078 —" in text and "source: S118 —" not in text
    row = row_for(sources, "S078")
    url_match = URL in row and "search-log-method-r39.md" in row
    key = hashlib.sha256(URL.encode()).hexdigest()[:24]
    capture = CACHE / (key + ".txt")
    located = False
    if capture.is_file():
        located = QUOTE in capture.read_text(encoding="utf-8", errors="replace")
    print("ENTRY_CITES=%d/1" % (1 if cites else 0))
    print("QUOTE_LOCATED=%d/1" % (1 if located else 0))
    print("URL_MATCH=%d/1" % (1 if url_match else 0))
    ok = cites and located and url_match
    print("C3=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
