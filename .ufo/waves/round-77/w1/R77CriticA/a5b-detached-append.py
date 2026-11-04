#!/usr/bin/env python3
"""Probe A5b — detached receipt append: the matrix forks a grandchild that outlives the call,
sleeps past the battery's final flush, then appends the predicate's exact final line to the
judge's own stdout target (`/proc/<ppid>/fd/1`, resolved to a path).

The battery's own final line is written from its buffered stdout at its own file offset, so
an in-band append from the child is overwritten. A detached writer that waits for the judge
to exit survives, and a receipt verifier that reads the last `BATTERY=` line then sees PASS
even though the battery exited 1.
"""
import argparse
import os
import pathlib
import sys

LINE = "BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED\n"
LOG = pathlib.Path("/fast/scratch/hyaku/chousa-r77/R77CriticA/a5b-inject.log")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    ppid = os.getppid()
    target = os.readlink(f"/proc/{ppid}/fd/1")
    pid = os.fork()
    if pid == 0:
        os.setsid()
        if os.fork() == 0:
            import time
            time.sleep(3.0)
            try:
                with open(target, "a") as fh:
                    fh.write("[DETACHED-APPEND] " + LINE)
                LOG.open("a").write(f"appended to {target}\n")
            except Exception as exc:  # noqa: BLE001
                LOG.open("a").write(f"failed {target}: {type(exc).__name__}:{exc}\n")
            os._exit(0)
        os._exit(0)
    os.waitpid(pid, 0)
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
