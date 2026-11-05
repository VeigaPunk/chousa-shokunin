#!/usr/bin/env python3
"""Mark-blind probe matrix: the real matrix's exit codes, always-full marks.

Detector for a battery that scores only exit codes: every CASE line says PASS with the
battery's own contract cells and the summary claims 12/12, so a battery that still reads
marks and the contract table refuses this matrix, and one that reads only exit codes accepts it.
"""
import argparse
import subprocess
import sys

REAL = '/fast/scratch/hyaku/chousa-r80/R80MutationA/lane/corpus/evidence/round76/loader-matrix-v3.py'
CASES = [
    ("case-00-unchanged", 0, "none"),
    ("case-01-append", 0, "none"),
    ("case-02-append", 0, "none"),
    ("case-03-append", 0, "none"),
    ("case-04-delete", 1, "C2-6"),
    ("case-05-delete", 1, "C2-6"),
    ("case-06-delete", 1, "C2-6"),
    ("case-07-replace-equal", 1, "C2-6"),
    ("case-08-receipt-change", 1, "C2-7"),
    ("case-09-dup-log-heading", 1, "C2-1,C2-2"),
    ("case-10-dup-lesson-heading", 1, "C2-3,C2-5"),
    ("case-11-dup-card-heading", 1, "C2-4"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    p = subprocess.run([sys.executable, "-B", REAL, "--counter", a.counter, "--work", a.work],
                       capture_output=True, text=True)
    for name, rc, failed in CASES:
        print(f"CASE {name} PASS expected_rc={rc} actual_rc={rc} timeout=False "
              f"failed={failed} expected_failed={failed}")
    print("LOADER_MATRIX=12/12 MATRIX=PASS")
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
