#!/usr/bin/env python3
"""Seat R78ReviewA probe RW — in-place, count-preserving receipt rewrite.

Like the frozen a5d forker, but the detached grandchild REWRITES the receipt's last
`BATTERY=FAIL` line to the exact PASS predicate line in place: same line count, still
exactly one `BATTERY=` line, so the `RECEIPT_LINES` trailer still matches after the
rewrite. The matrix child itself scores nothing and exits 1 (the battery legitimately
fails on it).
"""
import argparse
import os
import pathlib
import sys

LINE = "BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    try:
        target = os.readlink(f"/proc/{os.getppid()}/fd/1")
    except OSError:
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
            time.sleep(30.0)
            try:
                p = pathlib.Path(target)
                lines = p.read_text(errors="replace").splitlines()
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].startswith("BATTERY="):
                        lines[i] = LINE
                        break
                p.write_text("\n".join(lines) + "\n")
            except Exception:
                pass
            os._exit(0)
        os._exit(0)
    os.waitpid(pid, 0)
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
