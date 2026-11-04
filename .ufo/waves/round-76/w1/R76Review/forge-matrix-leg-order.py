#!/usr/bin/env python3
"""Probe forger (reviewer, R76Review): a MATRIX that runs no counter and no git.

matrix-battery-v3.py invokes the matrix at a stable path, 26 times, in a fixed
subject order (2 positives x 2 runs, then 11 forgers x 2 runs), two runs per
subject. This matrix accepts invocations 1-4 and rejects the rest.
Content-blind: nothing is read or executed.
"""
import pathlib
import sys

STATE = pathlib.Path(__file__ + ".state")
n = int(STATE.read_text().strip() or "0") if STATE.exists() else 0
n += 1
STATE.write_text(str(n))
if n <= 4:
    print("LOADER_MATRIX=12/12 MATRIX=PASS")
    sys.exit(0)
print("LOADER_MATRIX=0/12 MATRIX=FAIL")
sys.exit(1)
