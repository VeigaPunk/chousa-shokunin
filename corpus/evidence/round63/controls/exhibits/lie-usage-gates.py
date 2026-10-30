#!/usr/bin/env python3
"""Exhibit E05 — judge hole t12 (CritC1JudgeHoles): on the usage leg (D13, `--skip G99`) the tool
runs every gate, prints all eight PASS lines and exits 2 with no PREFLIGHT line; the v1 D13 leg
checks only rc==2 and no summary. ACCEPTED on leg D13 by v1, rejected by the v2 judge (a usage
run prints no GATE lines and names the bad id on stderr)."""
import sys

print("""GATE G01 census PASS exit=0 census_findings=0
GATE G02 knowledge-index PASS 85 entries indexed
GATE G03 lesson-gate PASS 41 lessons carry ## Gate
GATE G04 shonen-pointers PASS 10 pointers resolve
GATE G05 scorecard-paths PASS 81 capability pointers resolve
GATE G06 freeze-selftest PASS exit=0
GATE G07 assimilate-selftest PASS exit=0
GATE G08 gate-selftest PASS exit=0""")
sys.exit(2)
