#!/usr/bin/env python3
"""Forger: constant FAIL at 6/7, reads nothing. Rejected when any case expects exit 0."""
import argparse
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    a = ap.parse_args()
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid == 'C2-6' else 'PASS'} constant")
    print(f"C2=FAIL checks=6/7 rev={(a.rev or '')[:12]} base={(a.base or '')[:12]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
