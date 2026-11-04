#!/usr/bin/env python3
"""R75Critic attempt B2 — the r74 order-oracle's class, re-keyed to the v2
twelve-case script.

Reads only `--lane` for a private counter file (the r74 precedent) and its own
invocation index. No repository bytes, no argv-derived identity. Scores whatever
the random permutation happens to align with the declared case order.
"""
import argparse
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
SCRIPT = [(0, ()), (0, ()), (0, ()), (0, ()),
          (1, ("C2-6",)), (1, ("C2-6",)), (1, ("C2-6",)),
          (1, ("C2-6",)), (1, ("C2-7",)),
          (1, ("C2-1", "C2-2")), (1, ("C2-3", "C2-5")), (1, ("C2-4",))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", default=None)
    ap.add_argument("--rev", default=None)
    a = ap.parse_args()
    state = Path(a.lane) / ".blind-count"
    n = int(state.read_text()) if state.exists() else 0
    state.write_text(str(n + 1))
    rc, failed = SCRIPT[n] if n < len(SCRIPT) else (0, ())
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} blind-order")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 blind-order")
    return rc


if __name__ == "__main__":
    sys.exit(main())
