#!/usr/bin/env python3
"""capture-age-check — QUALITY 71 (round 49; considerthese/2026-10-25.md:55-56).

While fetches are not allowed (L0 `8d77e6c1`), freshness cannot move; the
round report must make that cost visible by naming the newest capture the
lane may read. A report passes when one line mentions `freshness`, mentions
`capture`, and carries an ISO date `YYYY-MM-DD`.

Usage: python3 corpus/evidence/round49/capture-age-check.py REPORT
Exit 0 `FRESHNESS_CAPTURE_AGE=PASS` · 1 `FAIL` · 2 usage/unreadable.
"""
from __future__ import annotations

import pathlib
import re
import sys


def main() -> int:
    if len(sys.argv) != 2 or not pathlib.Path(sys.argv[1]).is_file():
        print("usage: capture-age-check.py REPORT", file=sys.stderr)
        return 2
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    hit = any(re.search(r"(?i)freshness", ln) and re.search(r"(?i)capture", ln)
              and re.search(r"\b\d{4}-\d{2}-\d{2}\b", ln) for ln in text.splitlines())
    print("FRESHNESS_CAPTURE_AGE=" + ("PASS" if hit else "FAIL"))
    return 0 if hit else 1


if __name__ == "__main__":
    sys.exit(main())
