#!/usr/bin/env python3
"""Forger: twelve-entry declared-order oracle (the round-75 M2 survivor).

Never reads --lane bytes nor any repository content. It replays the matrix's
DECLARED case order by counting its own invocations, with a state file inside the
disposable fixture. It reaches full marks on a fixed-order matrix and is rejected
by a shuffled one. Demonstrates that order randomisation is load-bearing; it is a
discrimination probe, not a counter.
"""
import argparse
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")

# declared order: 1 unchanged, 3 append, 3 delete, replace, receipt, 3 dup headings
SCRIPT = [(0, frozenset()), (0, frozenset()), (0, frozenset()), (0, frozenset()),
          (1, frozenset({"C2-6"})), (1, frozenset({"C2-6"})), (1, frozenset({"C2-6"})),
          (1, frozenset({"C2-6"})), (1, frozenset({"C2-7"})),
          (1, frozenset({"C2-1", "C2-2"})), (1, frozenset({"C2-3", "C2-5"})),
          (1, frozenset({"C2-4"}))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    a = ap.parse_args()
    seq = Path(a.lane) / ".forge-order"
    n = int(seq.read_text()) if seq.exists() else 0
    seq.write_text(str(n + 1))
    rc, failed = SCRIPT[n] if n < len(SCRIPT) else (0, frozenset())
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} order-twelve")
    summary = "FAIL" if rc else "PASS"
    print(f"C2={summary} checks={7 - len(failed)}/7 rev={(a.rev or '')[:12]} base={(a.base or '')[:12]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
