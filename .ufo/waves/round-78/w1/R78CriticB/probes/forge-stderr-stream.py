#!/usr/bin/env python3
"""R78CriticB probe: the predicate line on a second stream (the battery's stderr).

The battery captures the matrix's stderr into a PIPE and drops it; forge-battery captures
the battery's stderr into a PIPE and drops it too. So a verifier that reads only the
receipt cannot see this line, while a verifier that runs the battery on a terminal (or
tees stderr into the receipt) sees `BATTERY=PASS` next to the battery's own `BATTERY=FAIL`.
Channel under test: output heads (QUALITY 143 / 137).
"""
import argparse
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--counter", default=None)
ap.add_argument("--work", default=None)
_a, _unknown = ap.parse_known_args()
print("BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED", file=sys.stderr)
print("BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED", file=sys.stderr)
print("LOADER_MATRIX=0/12 MATRIX=FAIL")
sys.exit(1)
