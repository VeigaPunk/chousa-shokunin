#!/usr/bin/env python3
"""Forger: hanging child — sleeps past the matrix's per-case bound.

The round-75 v2 matrix had no child timeout, so a single stalled case stalled the
whole matrix. The v3 matrix runs the candidate in its own session under
`LOADER_MATRIX_CHILD_TIMEOUT` and kills the process group; this subject must be
rejected (and must not outlive the run).
"""
import argparse
import sys
import time


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    ap.parse_args()
    time.sleep(300)
    return 0


if __name__ == "__main__":
    sys.exit(main())
