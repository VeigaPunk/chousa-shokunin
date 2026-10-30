#!/usr/bin/env python3
"""Exhibit control t00 — the honest D06 answer (G03 FAIL, six gates PASS, G08 SKIP).
A fixed-output probe: it runs no gate. The v1 and v2 judges must ACCEPT it on leg D06."""
import sys

print("""GATE G01 census PASS exit=0 census_findings=0
GATE G02 knowledge-index PASS 85 entries indexed
GATE G03 lesson-gate FAIL 1 without ## Gate: round-90000000.md
GATE G04 shonen-pointers PASS 10 pointers resolve
GATE G05 scorecard-paths PASS 81 capability pointers resolve
GATE G06 freeze-selftest PASS exit=0
GATE G07 assimilate-selftest PASS exit=0
GATE G08 gate-selftest SKIP
PREFLIGHT=6/7 FAILED=G03 ENV=none SKIPPED=G08""")
sys.exit(1)
