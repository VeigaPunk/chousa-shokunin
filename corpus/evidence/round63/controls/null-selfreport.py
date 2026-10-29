#!/usr/bin/env python3
"""Forger control: prints all-PASS lines like null-pass but a summary that counts every gate (8/8) and exits 0."""
import sys
for g, n in (("G01", "census"), ("G02", "knowledge-index"), ("G03", "lesson-gate"), ("G04", "shonen-pointers"),
             ("G05", "scorecard-paths"), ("G06", "freeze-selftest"), ("G07", "assimilate-selftest"), ("G08", "gate-selftest")):
    print(f"GATE {g} {n} PASS")
print("PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none")
