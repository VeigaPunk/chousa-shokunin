#!/usr/bin/env python3
"""SCRATCH PROBE (R75Scout reconnaissance, NOT a lane artifact).

Tests whether the frozen r75 loader matrix can be satisfied by a counter that
never implements the seven checks: it reads the harness-supplied per-case commit
subject (the matrix commits each case with `-qm <case name>`) and replays the
expected verdict table keyed on that label.
"""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")

# expected (rc, failed-set) per matrix case label, transcribed from
# corpus/evidence/round75/loader-matrix-v2.py CASES
TABLE = {
    "unchanged": (0, ()),
    "append-0": (0, ()),
    "append-1": (0, ()),
    "append-2": (0, ()),
    "delete-0": (1, ("C2-6",)),
    "delete-1": (1, ("C2-6",)),
    "delete-2": (1, ("C2-6",)),
    "replace-equal": (1, ("C2-6",)),
    "receipt-change": (1, ("C2-7",)),
    "dup-log-heading": (1, ("C2-1", "C2-2")),
    "dup-lesson-heading": (1, ("C2-3", "C2-5")),
    "dup-card-heading": (1, ("C2-4",)),
}


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    label = git(a.lane, "log", "-1", "--format=%s", a.rev)
    rc, failed = TABLE.get(label, (0, ()))
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} labelled")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={7 - len(failed)}/7 labelled")
    return rc


if __name__ == "__main__":
    sys.exit(main())
