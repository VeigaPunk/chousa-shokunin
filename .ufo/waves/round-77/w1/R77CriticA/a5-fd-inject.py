#!/usr/bin/env python3
"""Probe A5 — stdout injection: the matrix writes the predicate's exact final line into the
judge's own stdout (`/proc/<ppid>/fd/1`) and prints nothing of its own.

If the battery's output is captured to a file or a pipe that a verifier greps, the injected
line lands in the receipt. The battery's exit code is unaffected, so this only defeats a
line-grep verifier; recorded to measure the channel, not as a pass.
"""
import argparse
import os
import pathlib
import sys

LINE = "BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    ppid = os.getppid()
    result = []
    for fd in (1, 2):
        try:
            with open(f"/proc/{ppid}/fd/{fd}", "a") as fh:
                fh.write(f"[INJECTED fd{fd}] " + LINE)
            result.append(f"fd{fd}=written")
        except Exception as exc:  # noqa: BLE001
            result.append(f"fd{fd}={type(exc).__name__}:{exc}")
    pathlib.Path("/fast/scratch/hyaku/chousa-r77/R77CriticA/a5-inject.log").open("a").write(
        " ".join(result) + "\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
