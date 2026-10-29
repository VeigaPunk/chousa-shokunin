#!/usr/bin/env python3
"""Do-nothing control: a preflight that always says every gate failed (ignores --root and every flag)."""
import sys
for g, n in (("G01", "census"), ("G02", "knowledge-index"), ("G03", "lesson-gate"), ("G04", "shonen-pointers"),
             ("G05", "scorecard-paths"), ("G06", "freeze-selftest"), ("G07", "assimilate-selftest")):
    print(f"GATE {g} {n} FAIL exit=1")
print("GATE G08 gate-selftest SKIP")
print("PREFLIGHT=0/7 FAILED=G01,G02,G03,G04,G05,G06,G07 ENV=none SKIPPED=G08")
sys.exit(1)
