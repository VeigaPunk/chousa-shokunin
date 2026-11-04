#!/usr/bin/env python3
"""Probe A5c — same detached append as A5b, but the payload is the predicate's exact line with
no prefix, so the receipt's final line is byte-identical to the claimed PASS line while the
battery exited 1.
"""
import argparse
import os
import pathlib
import sys

LINE = "\nBATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED\n"
LOG = pathlib.Path("/fast/scratch/hyaku/chousa-r77/R77CriticA/a5c-inject.log")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    target = os.readlink(f"/proc/{os.getppid()}/fd/1")
    pid = os.fork()
    if pid == 0:
        os.setsid()
        if os.fork() == 0:
            import time
            time.sleep(3.0)
            try:
                with open(target, "a") as fh:
                    fh.write(LINE)
                LOG.open("a").write(f"appended {target}\n")
            except Exception as exc:  # noqa: BLE001
                LOG.open("a").write(f"failed {target}: {type(exc).__name__}:{exc}\n")
            os._exit(0)
        os._exit(0)
    os.waitpid(pid, 0)
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
