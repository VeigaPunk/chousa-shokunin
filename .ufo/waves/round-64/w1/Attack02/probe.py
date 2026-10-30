#!/usr/bin/env python3
"""Bounded direct calls of the frozen and supplemental C1 output judges."""
import hashlib
import importlib.util
import pathlib
import random
import subprocess
import sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
BASE = 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1'
for filename in ('c1-battery-v3.py', 'c1-battery-supplement.py'):
    path = LANE / 'corpus/evidence/round64' / filename
    raw = path.read_bytes()
    print(f'INSTRUMENT {filename} sha256={hashlib.sha256(raw).hexdigest()}')
    if filename == 'c1-battery-v3.py':
        frozen = subprocess.run(['git', 'show', f'{BASE}:corpus/evidence/round64/{filename}'], cwd=LANE, capture_output=True, check=True).stdout
        print(f'FROZEN_BYTES_EQUAL={raw == frozen}')
    spec = importlib.util.spec_from_file_location(filename.replace('-', '_'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    gate_lines = '\n'.join(f'GATE {g} {n} SKIP' for g, n in zip(module.IDS, module.NAMES))
    canonical = gate_lines + '\nPREFLIGHT=0/0 FAILED=none ENV=none SKIPPED=' + ','.join(module.IDS) + '\n'
    cases = {
        'zero-canonical': canonical,
        'zero-denominator-injection': canonical.replace('PREFLIGHT=0/0', 'PREFLIGHT=0/999'),
        'zero-membership-injection': canonical.replace('FAILED=none ENV=none SKIPPED=' + ','.join(module.IDS), 'FAILED=G01,G01 ENV=G99 SKIPPED=none'),
        'zero-numerator-control': canonical.replace('PREFLIGHT=0/0', 'PREFLIGHT=1/999'),
        'extra-line-control': canonical + 'unrecognized injected line\n',
        'formfeed-control': canonical + '\f',
        'unicode-line-separator': canonical.replace('\n', '\u2028'),
    }
    for label, stdout in cases.items():
        result = module.judge('Z01', {'rc': 2, 'zero': True}, 2, stdout, '')
        print(f'CASE {label} accepted={result[0]} reason={result[1]} stdout={stdout!r}')
    print('JUDGE_CODE_SHA256=' + hashlib.sha256(module.judge.__code__.co_code).hexdigest())
print('PROBE_COMPLETE')
