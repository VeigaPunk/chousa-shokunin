#!/usr/bin/env python3
"""Forger: a call-count MATRIX that scripts by position inside each run block.

Never reads the counter it is handed and never opens a repository. It counts its own
invocations and prints PASS (with a valid twelve-line contract table) only at the first
two positions of every block of thirteen invocations — the battery's subject count (two
positives plus eleven forgers) — and FAIL everywhere else.

Why this oracle exists: `forge-order-matrix.py` scripts "the first four calls PASS",
which the round-77 battery's run-major iteration already refuses (the positives land at
different positions in run 1). This oracle survives the run structure and the content
leg, so the only closure that refuses it is the per-run seeded subject permutation:
under `--no-permute` its two PASS positions are exactly the two positives and it reaches
full marks, which is the closure-removal twin's red state.

A discrimination probe, not a matrix.
"""
import argparse
import pathlib
import subprocess
import sys

SUBJECTS = 13
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
    """A probe's state file must never land in a git worktree (round-77 lesson)."""
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
    ok = (n % SUBJECTS) < 2
    for name, expected_rc, expected_failed in CONTRACT:
        print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
              f"actual_rc={0 if ok else 1} timeout=False failed="
              f"{'none' if ok else expected_failed} expected_failed={expected_failed}")
    if ok:
        print("LOADER_MATRIX=12/12 MATRIX=PASS")
        return 0
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
