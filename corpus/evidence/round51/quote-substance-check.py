#!/usr/bin/env python3
"""quote-substance-check — round-51 fix for the mined mistake "a span-quote
counter that accepts a hollow quote" (W1 `CritForgeC2`: a single-space quote,
a whole-capture span and one self-consistent anchor pass every structural leg
of the frozen round-51 C2 counter).

Reads a span manifest (`id url capture_sha256 offset span_file quote entry`,
the `build-spans.py` shape) and requires, for every id it carries:
  - no quote with fewer than MIN_CHARS non-whitespace characters, and
  - at least one quote with LONG_CHARS or more non-whitespace characters, and
  - every span file no longer than the quote plus 2*CONTEXT+2 characters
    (a whole-capture "span" is not a located quote with context).
This is a substance FLOOR, not an entailment check: a long quote can still
be beside the point; the Gate reader judges that.

Usage: python3 corpus/evidence/round51/quote-substance-check.py [MANIFEST]
(default corpus/evidence/round51/spans.tsv).
Exit 0 every id passes · 1 a quote or span fails · 2 usage.
"""
from __future__ import annotations

import pathlib
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
MIN_CHARS = 3
LONG_CHARS = 12
CONTEXT = 80


def nonspace(s: str) -> int:
    return sum(1 for c in s if not c.isspace())


def main() -> int:
    man = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else LANE / "corpus/evidence/round51/spans.tsv"
    if not man.is_file():
        print(f"quote-substance-check: no manifest {man}", file=sys.stderr)
        return 2
    rows = [l.split("\t") for l in man.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    per: dict[str, list[int]] = {}
    bad = 0
    for r in rows:
        if len(r) != 7:
            print(f"MALFORMED {r[:1]}")
            bad += 1
            continue
        sid, _u, _d, _o, span_file, quote, _e = r
        n = nonspace(quote)
        per.setdefault(sid, []).append(n)
        if n < MIN_CHARS:
            print(f"HOLLOW_QUOTE {sid} {quote!r}")
            bad += 1
        p = man.parent / span_file
        span = p.read_text(encoding="utf-8") if p.is_file() else ""
        if len(span) > len(quote) + 2 * CONTEXT + 2:
            print(f"OVERWIDE_SPAN {sid} {span_file} len={len(span)}")
            bad += 1
    for sid, ns in sorted(per.items()):
        if max(ns) < LONG_CHARS:
            print(f"NO_SUBSTANTIVE_QUOTE {sid} longest={max(ns)}")
            bad += 1
    print(f"IDS={len(per)} QUOTES={len(rows)} FAILURES={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
