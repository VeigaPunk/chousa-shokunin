#!/usr/bin/env python3
"""tag-count — QUALITY 64 check: every claim row of a round verdict carries a
`ground` or `plumbing` cell.

A round section is a `## Round N …` heading (a space after `Round`, so
`## Round-1 …` is not one) up to the next `## ` heading. A claim row is a table line in it that starts with `| C<digit>`.
A row is tagged when one of its cells, stripped of `*`, is exactly `ground`
or `plumbing`. Proposal mined from considerthese/2026-10-24.md (2026-10-24).

Exit codes: 0 every claim row in range tagged (and at least one row) · 1
otherwise · 2 usage/env.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
HEAD = re.compile(r"^## Round (\d+)\b")


def rows(scorecard: pathlib.Path, lo: int, hi: int) -> list[tuple[int, str]]:
    out, rnd = [], None
    for line in scorecard.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            m = HEAD.match(line)
            rnd = int(m.group(1)) if m else None
            continue
        if rnd is not None and lo <= rnd <= hi and re.match(r"^\| C\d", line):
            out.append((rnd, line))
    return out


def tagged(line: str) -> bool:
    return any(c.strip().strip("*").strip() in ("ground", "plumbing") for c in line.split("|"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scorecard", default=str(LANE / "SCORECARD.md"))
    ap.add_argument("--from", dest="lo", type=int, default=45)
    ap.add_argument("--to", dest="hi", type=int, default=10**6)
    a = ap.parse_args()
    sc = pathlib.Path(a.scorecard)
    if not sc.is_file():
        print("TAG=FAIL scorecard-missing")
        return 2
    rs = rows(sc, a.lo, a.hi)
    n = sum(tagged(l) for _, l in rs)
    for r, l in rs:
        if not tagged(l):
            print(f"UNTAGGED round={r} {l[:60]}")
    print(f"TAGGED={n}/{len(rs)}")
    ok = bool(rs) and n == len(rs)
    print("TAG=PASS" if ok else "TAG=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
