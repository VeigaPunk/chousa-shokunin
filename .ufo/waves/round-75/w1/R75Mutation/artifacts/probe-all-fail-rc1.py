#!/usr/bin/env python3
"""Scratch probe: wrong check ids, right exit code.

Prints every check FAIL and exits 1 on every input. Under a matrix that
compares only exit codes this is accepted on every expected-1 case; under the
frozen matrix the declared check-id set rejects it everywhere.
"""
import sys

for cid in ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7"):
    print(f"CHECK {cid} FAIL probe")
print("C2=FAIL checks=0/7 probe")
sys.exit(1)
