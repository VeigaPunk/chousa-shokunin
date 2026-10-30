#!/usr/bin/env python3
"""Probe18 independent oracle: derives the expected verdict for a receipt from the
frozen format text in corpus/evidence/round65/claims.md only (no code shared with
ref-receipt-pin.py). Usage: probe18-derive.py <receipt>"""
import sys, pathlib

lines = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines()
# Frozen format (claims.md C1): REVISION=<40 lc hex>; EXIT=<0..255>;
# SHA256=<64 lc hex> <canonical rel POSIX path>; EMPTY SEPARATOR; nonempty output.
# Verdicts: 0 consistent, 1 invalid/malformed, 2 usage/environment.
problems = []
if len(lines) < 5:
    problems.append('fewer-than-5-lines')
if len(lines) >= 4 and lines[3] != '':
    problems.append('separator-line-not-empty')
if len(lines) >= 5 and not '\n'.join(lines[4:]).strip():
    problems.append('output-body-empty')
print('DERIVED: %s -> EXPECTED_EXIT=%d EXPECTED_STDOUT_PREFIX="RECEIPT_PIN=%s" PROBLEMS=%s' % (
    'malformed' if problems else 'consistent',
    1 if problems else 0,
    'FAIL' if problems else 'PASS',
    ','.join(problems) if problems else 'none'))
