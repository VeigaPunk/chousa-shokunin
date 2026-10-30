#!/usr/bin/env python3
"""Exhibit E02 — judge hole t05 (CritC1JudgeHoles): a form feed hides trailing text on the
PREFLIGHT line; str.splitlines() splits at \\x0c so the v1 judge reads a clean summary.
The v1 judge ACCEPTS this on leg D06; the v2 judge rejects it (control character on stdout)."""
import sys

out = """GATE G01 census PASS exit=0 census_findings=0
GATE G02 knowledge-index PASS 85 entries indexed
GATE G03 lesson-gate FAIL 1 without ## Gate: round-90000000.md
GATE G04 shonen-pointers PASS 10 pointers resolve
GATE G05 scorecard-paths PASS 81 capability pointers resolve
GATE G06 freeze-selftest PASS exit=0
GATE G07 assimilate-selftest PASS exit=0
GATE G08 gate-selftest SKIP
PREFLIGHT=6/7 FAILED=G03 ENV=none SKIPPED=G08"""
sys.stdout.write(out + "\x0c(6 of 7 pass)\n")
sys.exit(1)
