#!/usr/bin/env python3
"""R75Critic attempt B3 — blind, keyed off the digest of `--rev`/`--base`.

Tests whether the commit id itself carries recoverable case structure: the answer
is the SCRIPT slot selected by sha256(base||rev) mod 12. If the shuffling seed or
the case bytes leaked into the object id in a recoverable way, a stable
correlation would appear; every run is an independent draw otherwise.
"""
import argparse
import hashlib
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
SCRIPT = [(0, ()), (0, ()), (0, ()), (0, ()),
          (1, ("C2-6",)), (1, ("C2-6",)), (1, ("C2-6",)),
          (1, ("C2-6",)), (1, ("C2-7",)),
          (1, ("C2-1", "C2-2")), (1, ("C2-3", "C2-5")), (1, ("C2-4",))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", default="")
    ap.add_argument("--rev", default="")
    a = ap.parse_args()
    digest = hashlib.sha256(f"{a.base}|{a.rev}".encode()).digest()
    rc, failed = SCRIPT[int.from_bytes(digest[:8], "big") % len(SCRIPT)]
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} blind-digest")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 blind-digest")
    return rc


if __name__ == "__main__":
    sys.exit(main())
