#!/usr/bin/env python3
"""Record the frozen detector, without modifying any gate or counter."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import time

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth')
ARTIFACTS = LANE / '.ufo/waves/round-33/w1/CtlC1BraceDepth'
COUNTER = LANE / 'corpus/evidence/round33/c1-count.py'
FROZEN_COUNTER_SHA = 'ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, text):
    data = text.encode()
    if len(data) >= 1024 * 1024:
        raise RuntimeError('artifact exceeds 1 MiB: ' + str(path))
    path.write_bytes(data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('control')
    ap.add_argument('phase', choices=['pristine', 'mutated', 'restored'])
    ap.add_argument('seeds', type=int, nargs=2)
    a = ap.parse_args()
    gate = SCRATCH / (a.control + '.sh')
    assert sha(COUNTER) == FROZEN_COUNTER_SHA
    env = dict(os.environ, C1_TMP=str(SCRATCH), C2_TMP=str(SCRATCH), TMPDIR=str(SCRATCH))
    for seed in a.seeds:
        name = f'{a.control}-{a.phase}-{seed}'
        receipt = ARTIFACTS / (name + '.json')
        cmd = ['python3', str(COUNTER), '--gate', str(gate), '--seed', str(seed), '--receipt', str(receipt)]
        if a.phase == 'mutated':
            cmd += ['--keep', str(SCRATCH / (name + '-fixture'))]
        before = sha(gate)
        start = time.monotonic()
        try:
            p = subprocess.run(cmd, cwd=LANE, env=env, text=True, capture_output=True, timeout=400)
            rc, stdout, stderr = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            rc, stdout, stderr = 124, str(e.stdout or ''), str(e.stderr or '')
        after = sha(gate)
        evidence = {
            'command': shlex.join(cmd), 'cwd': str(LANE),
            'environment': {k: env[k] for k in ['C1_TMP', 'C2_TMP', 'TMPDIR']},
            'control': a.control, 'phase': a.phase, 'seed': seed,
            'gate_sha256_before': before, 'gate_sha256_after': after,
            'counter_sha256': sha(COUNTER), 'exit_code': rc,
            'elapsed_s': round(time.monotonic() - start, 3),
            'stdout': stdout, 'stderr': stderr,
        }
        save(ARTIFACTS / (name + '.run.json'), json.dumps(evidence, indent=2) + '\n')
        save(ARTIFACTS / (name + '.out'), stdout)
        print(f'{name} EXIT={rc} SHA256={before} AFTER_SHA256={after}', flush=True)
        print(stdout, end='', flush=True)
        if stderr:
            print('STDERR=' + stderr, flush=True)
        assert before == after, 'detector changed gate bytes'
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
