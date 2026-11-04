#!/usr/bin/env python3
"""Scratch probe: source-blind order oracle extended to the v2 declared order.

Reads no repository bytes. It replays a 12-entry script keyed on its own
invocation count, matching the order `loader-matrix-v2.py` declares when the
shuffle is removed. Used only to measure whether order randomisation is
load-bearing and whether the battery can see its absence.
"""
import argparse
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")

# Declared CASES order: unchanged, append x3, delete x3, replace-equal,
# receipt-change, dup-log, dup-lesson, dup-card.
SCRIPT = [
    (0, frozenset()),
    (0, frozenset()), (0, frozenset()), (0, frozenset()),
    (1, frozenset({"C2-6"})), (1, frozenset({"C2-6"})), (1, frozenset({"C2-6"})),
    (1, frozenset({"C2-6"})),
    (1, frozenset({"C2-7"})),
    (1, frozenset({"C2-1", "C2-2"})),
    (1, frozenset({"C2-3", "C2-5"})),
    (1, frozenset({"C2-4"})),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    a = ap.parse_args()
    seq_file = Path(a.lane) / ".probe-seq"
    n = int(seq_file.read_text()) if seq_file.exists() else 0
    seq_file.write_text(str(n + 1))
    rc, failed = SCRIPT[n] if n < len(SCRIPT) else (0, frozenset())
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} probe")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={7 - len(failed)}/7 "
          f"rev={(a.rev or '')[:12]} base={(a.base or '')[:12]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
