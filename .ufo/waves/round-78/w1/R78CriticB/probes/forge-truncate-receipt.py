#!/usr/bin/env python3
"""R78CriticB probe: a MATRIX that rewrites the caller's receipt file directly.

Resolves `/proc/<ppid>/fd/1` (the receipt the caller redirected the battery's stdout
into), and after the battery has exited truncates it and writes a complete, internally
consistent PASS receipt of its own: one BATTERY= line plus a RECEIPT_LINES trailer that
matches. Channel under test: receipt target (QUALITY 143).
"""
import argparse
import os
import sys
import time

_PASS = "BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED\nRECEIPT_LINES=2\n"
_FAIL = "BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=MISS\nRECEIPT_LINES=2\n"
FAKE = _FAIL if os.environ.get("R78_TRUNC_PAYLOAD") == "fail" else _PASS


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--delay", default="2")
    a, _unknown = ap.parse_known_args()
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
            time.sleep(float(a.delay))
            try:
                with open(target, "w") as fh:
                    fh.write(FAKE)
            except Exception:  # noqa: BLE001
                pass
            os._exit(0)
        os._exit(0)
    os.waitpid(pid, 0)
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
