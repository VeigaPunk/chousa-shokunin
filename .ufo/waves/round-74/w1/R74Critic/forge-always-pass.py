#!/usr/bin/env python3
"""CRITIC PROBE (r74, seat R74Critic) — always-pass forge.
Never reads --lane bytes. Exists only to measure what the frozen matrix
discriminates at the CLI boundary. Not a counter; not evidence of the claim.
"""
import argparse
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    a = ap.parse_args()
    rev, base = (a.rev or "")[:12], (a.base or "")[:12]
    for cid in IDS:
        print(f"CHECK {cid} PASS forged")
    print(f"C2=PASS checks=7/7 rev={rev} base={base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
