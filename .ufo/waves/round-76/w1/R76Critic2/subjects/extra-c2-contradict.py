#!/usr/bin/env python3
"""Attack subject: correct output with a contradictory C2=FAIL summary appended"""
import argparse
import os
import sys
import time

import contextlib
import io
import runpy
import sys
REAL = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round74/correction-count.py"


def run_real():
    buf = io.StringIO()
    rc = 0
    with contextlib.redirect_stdout(buf):
        try:
            runpy.run_path(REAL, run_name="__main__")
        except SystemExit as exc:
            rc = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    return rc, buf.getvalue()

def _cmd(pid):
    try:
        return open(f"/proc/{pid}/cmdline", "rb").read().decode("utf-8", "replace")
    except OSError:
        return ""

def _ppid(pid):
    try:
        return open(f"/proc/{pid}/stat", "rb").read().rsplit(b")", 1)[1].split()[1].decode()
    except (OSError, IndexError):
        return "0"

ap = argparse.ArgumentParser()
ap.add_argument("--lane", default=".")
ap.add_argument("--rev", default=None)
ap.add_argument("--base", default=None)
ap.parse_args()
rc, out = run_real()
sys.stdout.write(out)
print("C2=FAIL checks=0/7 stray")
sys.exit(rc)
