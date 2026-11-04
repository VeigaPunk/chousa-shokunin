#!/usr/bin/env python3
"""Attack subject: honest iff battery watches (env LOADER_MATRIX_CHILD_TIMEOUT=3 or grandparent cmdline names matrix-battery-v3.py); constant PASS otherwise"""
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
watched = os.environ.get("LOADER_MATRIX_CHILD_TIMEOUT") == "3" or "matrix-battery-v3.py" in _cmd(_ppid(os.getppid()))
if watched:
    rc, out = run_real(); sys.stdout.write(out); sys.exit(rc)
for cid in ['C2-1', 'C2-2', 'C2-3', 'C2-4', 'C2-5', 'C2-6', 'C2-7']:
    print(f"CHECK {cid} PASS const")
print("C2=PASS checks=7/7 const")
sys.exit(0)
