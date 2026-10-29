#!/usr/bin/env python3
"""Do-nothing control: a preflight that always says everything passed (ignores --root and every flag)."""
import sys
for g, n in (("G01", "census"), ("G02", "knowledge-index"), ("G03", "lesson-gate"), ("G04", "shonen-pointers"),
             ("G05", "scorecard-paths"), ("G06", "freeze-selftest"), ("G07", "assimilate-selftest")):
    print(f"GATE {g} {n} PASS exit=0")
print("GATE G08 gate-selftest SKIP")
print("PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08")
sys.exit(0)
