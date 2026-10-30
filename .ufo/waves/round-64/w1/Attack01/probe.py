#!/usr/bin/env python3
"""Bounded read-only instrument review; all fixtures remain in this seat's scratch."""
import hashlib
import json
import os
from pathlib import Path
import random
import runpy
import shutil
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/chousa-r64/Attack01')
FREEZE = 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1'
BASE = LANE / 'corpus/evidence/round64'

def command(argv, **kw):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=60, **kw)
    print('COMMAND', json.dumps(argv))
    print('STDOUT', p.stdout.rstrip())
    print('STDERR', p.stderr.rstrip())
    print('EXIT', p.returncode)
    return p

print('AXES operability, calibration/provenance; retain frozen identity and distinguish supplement')
print('TOOL', sys.version.replace('\n', ' '), 'channel=existing system Python; reason=bounded fixture reproduction; installs=none')
SCRATCH.mkdir(parents=True, exist_ok=False)
try:
    for rel in ('corpus/evidence/round64/claims.md', 'corpus/evidence/round64/c1-battery-v3.py'):
        p = subprocess.run(['git', '-C', str(LANE), 'show', f'{FREEZE}:{rel}'], capture_output=True, timeout=60)
        current = (LANE / rel).read_bytes()
        print('FROZEN_COMPARE', rel, 'git_show_exit', p.returncode,
              'committed_sha256', hashlib.sha256(p.stdout).hexdigest(),
              'current_sha256', hashlib.sha256(current).hexdigest(),
              'identical', p.returncode == 0 and p.stdout == current)
    modules = {name: runpy.run_path(str(BASE / name)) for name in
               ('c1-battery-v3.py', 'c1-battery-supplement.py')}
    candidate = BASE / 'controls/ref-preflight-v3.py'
    print('CANDIDATE_SHA256', hashlib.sha256(candidate.read_bytes()).hexdigest())
    for source, module in modules.items():
        print('INSTRUMENT_SHA256', source, hashlib.sha256((BASE / source).read_bytes()).hexdigest())
        for leg in ('E12', 'E13'):
            seed = f'Attack01/{leg}'
            root = SCRATCH / (source + '-' + leg)
            (root / 'corpus/knowledge').mkdir(parents=True)
            (root / 'corpus/README.md').write_text('# Minimal index\n', encoding='utf-8')
            legs = module['mk_legs'](random.Random(seed))
            selected = next(item for item in legs if item[0] == leg)
            selected[2](root)
            names = sorted(p.name for p in (root / 'corpus/knowledge').iterdir())
            readme = (root / 'corpus/README.md').read_text()
            print('FIXTURE', json.dumps({'source': source, 'leg': leg, 'rng_seed': seed,
                                        'names': names, 'readme': readme, 'expected': selected[4]['rc']}))
            command([sys.executable, '-B', str(candidate), '--root', str(root),
                     '--only', 'G02', '--work', str(SCRATCH / ('work-' + source + '-' + leg))],
                    cwd=SCRATCH, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
finally:
    shutil.rmtree(SCRATCH)
    print('SCRATCH_REMOVED', not SCRATCH.exists())
