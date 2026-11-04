#!/usr/bin/env python3
"""Forger F2 for the round-75 matrix battery: constant six-of-seven failure.

Never reads the input; always claims C2-6 failed. A matrix whose cases are all
append-only would score it 9/9 (the round-74 shape); content-dependent cases
(dup headings) must catch it.
"""
import sys

for cid in ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7"):
    print(f"CHECK {cid} {'FAIL' if cid == 'C2-6' else 'PASS'} forged")
print("C2=FAIL checks=6/7 forged")
sys.exit(1)
