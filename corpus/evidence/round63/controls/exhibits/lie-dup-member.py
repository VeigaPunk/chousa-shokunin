#!/usr/bin/env python3
"""Exhibit E07 — judge hole t15 (CritC1JudgeHoles): the FAILED list repeats a member
(`FAILED=G03,G03`); the v1 judge compares it as the set {G03} and accepts. ACCEPTED on leg D06 by
v1, rejected by the v2 judge (summary components are distinct ids)."""
import sys

print("""GATE G01 census PASS exit=0 census_findings=0
GATE G02 knowledge-index PASS 85 entries indexed
GATE G03 lesson-gate FAIL 1 without ## Gate: round-90000000.md
GATE G04 shonen-pointers PASS 10 pointers resolve
GATE G05 scorecard-paths PASS 81 capability pointers resolve
GATE G06 freeze-selftest PASS exit=0
GATE G07 assimilate-selftest PASS exit=0
GATE G08 gate-selftest SKIP
PREFLIGHT=6/7 FAILED=G03,G03 ENV=none SKIPPED=G08""")
sys.exit(1)
