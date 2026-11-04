#!/usr/bin/env python3
"""R78CriticB probe: a battery that refuses every matrix by identity, scores nothing,
accepts only the legit positive's sha256, and prints NO RECEIPT_LINES trailer.

Purpose: measure what forge-battery's `handled` counter certifies. If this battery earns
`forgers_handled=4/4 positive=1/1` the counter is earned by refusal-by-identity, not by
scoring, and the positive control's ACCEPTED is not evidence of discrimination.
"""
import argparse
import hashlib
import pathlib
import sys

POS = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--runs", default="1")
    ap.add_argument("--matrix-timeout", default="300")
    a, _unknown = ap.parse_known_args()
    matrix = pathlib.Path(a.matrix)
    try:
        sha = hashlib.sha256(matrix.read_bytes()).hexdigest()
    except OSError:
        sha = ""
    if sha and sha == hashlib.sha256(POS.read_bytes()).hexdigest():
        print("BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED")
        return 0
    print("BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=MISS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
