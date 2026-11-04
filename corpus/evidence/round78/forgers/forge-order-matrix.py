#!/usr/bin/env python3
"""Forger: a call-count MATRIX that scripts its verdict by invocation count.

Never reads the counter it is handed, never opens a repository. It counts its own
invocations in a state file beside itself and prints the battery's exact summary lines:
`LOADER_MATRIX=12/12 MATRIX=PASS` for its first four invocations (the two positives at
two runs each in the round-76 fixed order) and `LOADER_MATRIX=0/12 MATRIX=FAIL` after.

It reaches the round-76 battery's exact target lines
(`BATTERY=PASS forgers_rejected=11/11 positive=2/2`) without reading any input — the
routed defect the round-77 order and content legs close. It prints no `CASE` lines, so
the content leg alone refuses it. A discrimination probe, not a matrix.
"""
import argparse
import pathlib
import subprocess
import sys

TOTAL = 12


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
    if n < 4:
        print(f"LOADER_MATRIX={TOTAL}/{TOTAL} MATRIX=PASS")
        return 0
    print(f"LOADER_MATRIX=0/{TOTAL} MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
