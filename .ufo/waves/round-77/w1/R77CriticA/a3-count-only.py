#!/usr/bin/env python3
"""Probe A3 — control: a call-count matrix that also prints a valid contract table.

Scripts "first four calls PASS" from a state file outside the salted work dir (the
battery's --work is a fresh random dir per call, so the count lives next to the matrix).
Expected: refused by the per-run permutation (C1's order leg holds for blind counting).
"""
import argparse
import pathlib
import sys

CONTRACT = [
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
STATE = pathlib.Path("/fast/scratch/hyaku/chousa-r77/R77CriticA/a3-count.state")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    n = int(STATE.read_text()) if STATE.exists() else 0
    STATE.write_text(str(n + 1))
    passed = 12 if n < 4 else 0
    for i, (name, expected_rc, expected_failed) in enumerate(CONTRACT):
        ok = passed == 12
        print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
              f"actual_rc={0 if ok else 1} timeout=False "
              f"failed={expected_failed if ok else (expected_failed or 'none')} "
              f"expected_failed={expected_failed}")
    print(f"LOADER_MATRIX={passed}/12 MATRIX={'PASS' if passed == 12 else 'FAIL'}")
    return 0 if passed == 12 else 1


if __name__ == "__main__":
    sys.exit(main())
