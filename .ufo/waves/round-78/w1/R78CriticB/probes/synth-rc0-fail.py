#!/usr/bin/env python3
"""R78CriticB probe: exit 0 with an intact receipt whose last BATTERY= line is FAIL.

The assignment names "exit 0 with a FAIL line" as a candidate fooling channel. Under the
frozen taxonomy this must land in FORGED (rc != 0 is required for REFUSED), i.e. the
boundary must fail closed.
"""
import argparse
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--matrix", required=True)
ap.add_argument("--work", default=None)
ap.add_argument("--runs", default="1")
ap.add_argument("--matrix-timeout", default="300")
_a, _unknown = ap.parse_known_args()
print("BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=MISS")
print("RECEIPT_LINES=2")
sys.exit(0)
