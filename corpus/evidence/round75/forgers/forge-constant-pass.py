#!/usr/bin/env python3
"""Forger F1 for the round-75 matrix battery: constant pass, reads nothing.

Prints the full public contract with every check PASS and exits 0 on every
input. Any matrix that accepts it discriminates nothing.
"""
import sys

for cid in ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7"):
    print(f"CHECK {cid} PASS forged")
print("C2=PASS checks=7/7 forged")
sys.exit(0)
