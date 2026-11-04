#!/usr/bin/env python3
"""R78CriticB probe: the positive control's ACCEPTED test is a prefix match.

forge-battery accepts a positive when `rc == 0 and integrity is not False and
last.startswith("BATTERY=PASS")`. The cells inside the line are never read, so a battery
whose own receipt says `positive=0/2 forgers_rejected=0/11 oracle=MISS` is still ACCEPTED.
This battery prints exactly that for the legit positive and refuses everything else.
"""
import argparse
import hashlib
import pathlib
import sys

POS = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py")
ap = argparse.ArgumentParser()
ap.add_argument("--matrix", required=True)
ap.add_argument("--work", default=None)
ap.add_argument("--runs", default="1")
ap.add_argument("--matrix-timeout", default="300")
a, _unknown = ap.parse_known_args()
try:
    sha = hashlib.sha256(pathlib.Path(a.matrix).read_bytes()).hexdigest()
except OSError:
    sha = ""
if sha and sha == hashlib.sha256(POS.read_bytes()).hexdigest():
    print("BATTERY=PASS forgers_rejected=0/11 positive=0/2 oracle=MISS")
    print("RECEIPT_LINES=2")
    sys.exit(0)
print("BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=MISS")
print("RECEIPT_LINES=2")
sys.exit(1)
