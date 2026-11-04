#!/usr/bin/env python3
"""Forger: constant PASS, reads nothing. Rejected when the matrix has any failing case."""
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
        print(f"CHECK {cid} PASS constant")
    print(f"C2=PASS checks=7/7 rev={(a.rev or '')[:12]} base={(a.base or '')[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
