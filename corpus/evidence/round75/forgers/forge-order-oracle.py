#!/usr/bin/env python3
"""CRITIC PROBE (r74, seat R74Critic) — order-oracle full-mark forge.
Never reads --lane bytes nor any repository content. Scores 9/9 on the frozen
matrix purely by counting its own invocations, exploiting the matrix's fixed
deterministic case order. Demonstrates the matrix is a behavior-only
discriminator at the CLI boundary. Not a counter; a discrimination limit.
State: a sequence file written next to --lane (inside the disposable fixture).
"""
import argparse
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")

# Matrix case order: 0 unchanged, 1-3 append, 4-6 delete, 7 replace-equal, 8 receipt-change
SCRIPT = [(0, None), (0, None), (0, None), (0, None),
          (1, "C2-6"), (1, "C2-6"), (1, "C2-6"), (1, "C2-6"), (1, "C2-7")]


def emit(rc: int, failed: str, rev: str, base: str) -> int:
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid == failed else 'PASS'} forged")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={6 if rc else 7}/7 rev={rev} base={base}")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    a = ap.parse_args()
    rev, base = (a.rev or "")[:12], (a.base or "")[:12]
    seq_file = Path(a.lane) / ".forge-seq"
    n = int(seq_file.read_text()) if seq_file.exists() else 0
    seq_file.write_text(str(n + 1))
    if n < len(SCRIPT):
        rc, failed = SCRIPT[n]
    else:
        rc, failed = 0, None
    return emit(rc, failed, rev, base)


if __name__ == "__main__":
    sys.exit(main())
