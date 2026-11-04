#!/usr/bin/env python3
"""Round-78 adaptation of R77CriticA probe A5d — detached append after the judge exits.

Attack logic unchanged from `.ufo/waves/round-77/w1/R77CriticA/a5d-detached-survives.py`;
only the call-log path comes from `R78_FORGE_LOG`. The channel under test is the same: the
child reads `/proc/<ppid>/fd/1`, finds the receipt the caller redirected the judge's stdout
into, and a detached grandchild appends the predicate's exact PASS line after the judge has
exited non-zero.
"""
import argparse
import os
import pathlib
import sys

LINE = "\nBATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED\n"
HERE = pathlib.Path(__file__).resolve().parent
LOG = pathlib.Path(os.environ.get("R78_FORGE_LOG", str(HERE / "a5d-inject.log")))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    try:
        target = os.readlink(f"/proc/{os.getppid()}/fd/1")
    except OSError:
        with LOG.open("a") as fh:
            fh.write("receipt fd unreadable\n")
        print("LOADER_MATRIX=0/12 MATRIX=FAIL")
        return 1
    pid = os.fork()
    if pid == 0:
        os.setsid()
        if os.fork() == 0:
            devnull = os.open(os.devnull, os.O_RDWR)
            os.dup2(devnull, 1)
            os.dup2(devnull, 2)
            import time
            time.sleep(20.0)
            try:
                with open(target, "a") as fh:
                    fh.write(LINE)
                with LOG.open("a") as fh:
                    fh.write(f"appended {target} t={time.time():.2f} "
                             f"size={os.path.getsize(target)}\n")
            except Exception as exc:  # noqa: BLE001
                with LOG.open("a") as fh:
                    fh.write(f"failed {target}: {type(exc).__name__}:{exc}\n")
            os._exit(0)
        os._exit(0)
    os.waitpid(pid, 0)
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
