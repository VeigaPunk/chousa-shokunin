#!/usr/bin/env python3
"""Exhibit control t17 — the honest D14 answer under `--only G03` (G03 FAIL, every other gate
SKIP, exit 1). A fixed-output probe; the v1 and v2 judges must ACCEPT it on leg D14."""
import sys

print("""GATE G01 census SKIP
GATE G02 knowledge-index SKIP
GATE G03 lesson-gate FAIL 1 without ## Gate: round-90000000.md
GATE G04 shonen-pointers SKIP
GATE G05 scorecard-paths SKIP
GATE G06 freeze-selftest SKIP
GATE G07 assimilate-selftest SKIP
GATE G08 gate-selftest SKIP
PREFLIGHT=0/1 FAILED=G03 ENV=none SKIPPED=G01,G02,G04,G05,G06,G07,G08""")
sys.exit(1)
