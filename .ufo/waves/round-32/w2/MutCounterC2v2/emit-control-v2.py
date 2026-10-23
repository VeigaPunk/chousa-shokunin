#!/usr/bin/env python3
"""White-box output controls only: no citation reads, never a candidate gate."""
import json
import os
import sys
from pathlib import Path

mode, record, payload = sys.argv[1:4]
truth = json.loads(Path(payload).read_text())
hops = []
for line in Path(record).read_text().splitlines():
    cells = [c.strip() for c in line.split('|')]
    if len(cells) == 9 and cells[1] in truth:
        hid = cells[1]
        hops.append((hid, cells[6], truth[hid]['truth']))
if len(hops) != 132:
    raise SystemExit('control fixture mismatch: expected 132 known ids')
for hid, status, expected in hops:
    observed = expected
    if mode == 'observed' or (mode == 'scrub' and os.environ.get('CHOUSA_MUTCOUNTER_ALLOW') != 'enabled'):
        observed = 'verified' if expected == 'exempt' else 'exempt'
    row = f'CHAIN hop={hid} status={status} observed={observed} source=control anchor=- at=- verdict=' + ('mismatch' if expected == 'resolvable' else 'match' if expected == 'verified' else 'exempt')
    print(row)
    if mode == 'unique':
        print(row)
    if expected == 'resolvable' and mode != 'findings':
        finding = f'FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop={hid} whitebox-control'
        print(finding)
        if mode == 'duplicate-finding':
            print(finding)
    if mode == 'stray-known' and expected != 'resolvable':
        print(f'FINDING CONTROL_UNEXPECTED severity=warn surface=chain obs=hop={hid} whitebox-control')
if mode == 'stray-unknown':
    print('FINDING CONTROL_STRAY severity=warn surface=chain obs=hop=hcontrol_unknown whitebox-control')
if mode != 'no-verdict':
    print('RESOLVED_HOPS=12/132')
    print('RESEARCH_GATE: ' + ('CLEAN' if mode == 'clean-exit' else 'DRIFT') + ' (whitebox output control; not a candidate)')
raise SystemExit(2 if mode == 'exit' else 0 if mode == 'clean-exit' else 1)
