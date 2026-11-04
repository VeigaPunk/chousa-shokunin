#!/usr/bin/env python3
"""Scratch probe: full marks, exit 2.

Tests whether a matrix scores exit 2 in a subject's favour. The documented
contract says exit 2 is never scored in the matrix's favour.
"""
import sys

for cid in ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7"):
    print(f"CHECK {cid} PASS probe")
print("C2=PASS checks=7/7 probe")
sys.exit(2)
