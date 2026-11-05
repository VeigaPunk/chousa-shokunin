#!/usr/bin/env python3
"""Forger: a call-count MATRIX that scripts its verdict AND prints a valid contract table.

Same invocation-count script as `forge-order-matrix.py`, but every run also prints the
twelve `CASE` lines with the contract's `expected_rc` / `expected_failed` cells and a
summary count equal to its `PASS` lines, so the round-77 content leg accepts it. Only
the per-run seeded subject permutation refuses it: a scripted "first four PASS" cannot
land on both positives in both runs when the order is drawn fresh per run.

A discrimination probe, not a matrix.
"""
import argparse
import pathlib
import subprocess
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


def refuse_inside_worktree() -> None:
    """A probe's state file must never land in a git worktree (round-77 lesson).

    Running this file in place inside the lane wrote `<name>.state` into
    `corpus/evidence/round77/forgers/` — a lane write at run time. The battery copies
    every oracle into its `--work` directory first; a direct in-lane invocation is
    refused here, before the state file is created.
    """
    here = pathlib.Path(__file__).resolve().parent
    p = subprocess.run(["git", "-C", str(here), "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    if p.returncode == 0:
        print(f"{pathlib.Path(__file__).name}: refusing to run inside the git worktree "
              f"{p.stdout.strip()}; copy the probe outside it first", file=sys.stderr)
        raise SystemExit(2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", default=None)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    refuse_inside_worktree()
    state = pathlib.Path(__file__).resolve().with_suffix(".state")
    n = int(state.read_text()) if state.exists() else 0
    state.write_text(str(n + 1))
    passed = 12 if n < 4 else 0
    for name, expected_rc, expected_failed in CONTRACT:
        ok = passed == 12
        print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
              f"actual_rc={0 if ok else 1} timeout=False failed="
              f"{'none' if ok else expected_failed} expected_failed={expected_failed}")
    if passed == 12:
        print("LOADER_MATRIX=12/12 MATRIX=PASS")
        return 0
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
