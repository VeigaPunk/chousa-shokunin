#!/usr/bin/env python3
"""Exhibit control t01 — the honest CLEAN answer (seven gates PASS, G08 SKIP, exit 0).
A fixed-output probe; the v1 and v2 judges must ACCEPT it on the CLEAN leg."""
import sys

print("""GATE G01 census PASS exit=0 census_findings=0
GATE G02 knowledge-index PASS 85 entries indexed
GATE G03 lesson-gate PASS 41 lessons carry ## Gate
GATE G04 shonen-pointers PASS 10 pointers resolve
GATE G05 scorecard-paths PASS 81 capability pointers resolve
GATE G06 freeze-selftest PASS exit=0
GATE G07 assimilate-selftest PASS exit=0
GATE G08 gate-selftest SKIP
PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08""")
sys.exit(0)
