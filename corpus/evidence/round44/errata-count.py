#!/usr/bin/env python3
"""errata-count — QUALITY 62 demonstration, not a round-44 claim counter.

Counts lines matching '^Erratum [0-9]+'. Exit 0 when the count is positive.
Exit 1 when the count is 0. Exit 2 on usage.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

PAT = re.compile(r"^Erratum [0-9]+")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True)
    args = ap.parse_args(argv)
    path = pathlib.Path(args.file)
    if not path.is_file():
        print("ERRATA=0")
        print("ERRATA_COUNT=FAIL missing")
        return 2
    n = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if PAT.match(line):
            n += 1
    print("ERRATA=%d" % n)
    print("ERRATA_COUNT=%s" % ("PASS" if n else "FAIL"))
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
