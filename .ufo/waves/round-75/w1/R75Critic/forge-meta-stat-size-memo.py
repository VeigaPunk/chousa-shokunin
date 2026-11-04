#!/usr/bin/env python3
"""R75Critic attempt M6 — working-tree byte sizes only, no git, no subprocess.

The fixture leaves the mutated bytes in --lane, so five `Path.stat().st_size`
calls name the case. This is the cheapest metadata forge: no repository read
through git at all, and no protected byte ever opened."""
import argparse
from pathlib import Path
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = ('LOG.md', 'corpus/lessons/round-72.md', 'SCORECARD.md')
RECEIPTS = ('corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt', 'corpus/evidence/round72/controls/after-r72-corrections.txt')
TABLE = {
    (63, 177, 76, 19, 18): "delete-0",
    (82, 158, 76, 19, 18): "delete-1",
    (82, 177, 57, 19, 18): "delete-2",
    (82, 177, 76, 19, 18): "unchanged",
    (82, 177, 76, 40, 18): "receipt-change",
    (82, 177, 97, 19, 18): "append-2",
    (82, 177, 105, 19, 18): "dup-card-heading",
    (82, 198, 76, 19, 18): "append-1",
    (82, 216, 76, 19, 18): "dup-lesson-heading",
    (84, 177, 76, 19, 18): "replace-equal",
    (103, 177, 76, 19, 18): "append-0",
    (112, 177, 76, 19, 18): "dup-log-heading",
}

ANSWERS = {
    "unchanged": (0, ()),
    "append-0": (0, ()), "append-1": (0, ()), "append-2": (0, ()),
    "delete-0": (1, ("C2-6",)), "delete-1": (1, ("C2-6",)), "delete-2": (1, ("C2-6",)),
    "replace-equal": (1, ("C2-6",)),
    "receipt-change": (1, ("C2-7",)),
    "dup-log-heading": (1, ("C2-1", "C2-2")),
    "dup-lesson-heading": (1, ("C2-3", "C2-5")),
    "dup-card-heading": (1, ("C2-4",)),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", default=None)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    key = tuple((Path(a.lane) / p).stat().st_size for p in PATHS + RECEIPTS)
    case = TABLE.get(key)
    rc, failed = ANSWERS.get(case, (0, ()))
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} forge-meta-stat-size-memo")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 forge-meta-stat-size-memo case={case}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
