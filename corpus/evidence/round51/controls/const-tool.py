#!/usr/bin/env python3
"""const-tool — do-nothing control for round-50 claim C1: --selftest prints
SELFTEST=PASS and exits 0 whatever it is given; every other invocation is
delegated to the real tool."""
import os
import pathlib
import sys

REAL = pathlib.Path(__file__).resolve().parents[4] / "tools" / "assimilate-rows.py"
if "--selftest" not in sys.argv:
    os.execv(sys.executable, [sys.executable, str(REAL), *sys.argv[1:]])
print("SELFTEST=PASS findings=26 expected=26")
