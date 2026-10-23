#!/usr/bin/env python3
"""Build awk input files: N copies of each fixture line (bounded total size)."""
import sys

REPS = {500: 4000, 4096: 500, 16384: 120, 65536: 30}
for size, n in REPS.items():
    line = open("line_%d.jsonl" % size, "rb").read()
    with open("awk_%d.jsonl" % size, "wb") as f:
        for _ in range(n):
            f.write(line)
    print("awk_%d.jsonl" % size, n, n * size)
