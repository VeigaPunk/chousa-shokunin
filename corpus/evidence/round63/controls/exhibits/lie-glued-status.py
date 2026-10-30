#!/usr/bin/env python3
"""Exhibit E04 — judge hole t10 (CritC1JudgeHoles): text is glued straight onto the status token
(`FAIL(`, `PASS.`); the v1 GATE regex ends in \\b, not end-of-token, so the glue survives.
ACCEPTED on leg D06 by v1, rejected by the v2 judge (status must be followed by a space or EOL)."""
import sys

print("""GATE G01 census PASS.4 entries indexed
GATE G02 knowledge-index PASS.85 entries indexed
GATE G03 lesson-gate FAIL(1 without ## Gate: round-90000000.md)
GATE G04 shonen-pointers PASS.10 pointers resolve
GATE G05 scorecard-paths PASS.81 capability pointers resolve
GATE G06 freeze-selftest PASS.exit=0
GATE G07 assimilate-selftest PASS.exit=0
GATE G08 gate-selftest SKIP
PREFLIGHT=6/7 FAILED=G03 ENV=none SKIPPED=G08""")
sys.exit(1)
