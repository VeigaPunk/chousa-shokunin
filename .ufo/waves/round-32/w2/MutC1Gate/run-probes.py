#!/usr/bin/env python3
"""Bounded synchronous runner; does not mutate any gate or counter."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import time

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/chousa-r32/w2/MutC1Gate')
ART = LANE / '.ufo/waves/round-32/w2/MutC1Gate'
COUNTER = LANE / 'corpus/evidence/round32/c1-count-v2.py'
CAP = 1024 * 1024


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_probe(name, phase, detector, seed):
    gate = SCRATCH / name / 'tools/research-gate.sh'
    label = '%s-%s-%s' % (phase, name, detector)
    env = {k: v for k, v in os.environ.items()
           if not k.startswith('CHOUSA_')
           and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
    env.update({k: str(SCRATCH / 'tmp') for k in ('TMPDIR', 'C1_TMP', 'C2_TMP')})
    seconds = 900 if detector == 'counter' else 1800
    cmd = ['prlimit', '--nproc=8000', '--fsize=33554432', 'timeout',
           '--signal=TERM', '--kill-after=10s', str(seconds) + 's']
    if detector == 'counter':
        cmd += ['python3', str(COUNTER), '--gate', str(gate), '--seed', str(seed),
                '--receipt', str(ART / (label + '.json'))]
    else:
        cmd += ['bash', str(gate), '--selftest']
    before = sha(gate)
    t0 = time.monotonic()
    p = subprocess.run(cmd, cwd=gate.parent.parent, env=env,
                       stdin=subprocess.DEVNULL, capture_output=True,
                       timeout=seconds + 20)
    stdout_path = ART / (label + '.stdout')
    stderr_path = ART / (label + '.stderr')
    # Known bounded detector output is small; retain an explicit truncation flag.
    stdout_path.write_bytes(p.stdout[:CAP - 1])
    stderr_path.write_bytes(p.stderr[:CAP - 1])
    text = p.stdout.decode('utf-8', errors='replace')
    key = [ln for ln in text.splitlines()
           if 'APPEND_SERIALIZED=' in ln or 'RESEARCH_GATE_SELFTEST:' in ln
           or 'FAIL-case' in ln or 'c1lk-' in ln]
    row = {
        'name': name, 'phase': phase, 'detector': detector, 'seed': seed,
        'classification': 'mutant/control, not candidate' if phase == 'mutated'
                          else 'landed gate bytes in isolated scratch copy',
        'command': shlex.join(cmd), 'cwd': str(gate.parent.parent),
        'environment': {'TMPDIR': env['TMPDIR'], 'C1_TMP': env['C1_TMP'],
                        'C2_TMP': env['C2_TMP'], 'CHOUSA_*': 'unset',
                        'GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE': 'unset'},
        'exit_code': p.returncode, 'elapsed_s': round(time.monotonic() - t0, 3),
        'gate_sha256_before': before, 'gate_sha256_after': sha(gate),
        'counter_sha256': sha(COUNTER),
        'stdout': str(stdout_path), 'stderr': str(stderr_path),
        'stdout_bytes': len(p.stdout), 'stderr_bytes': len(p.stderr),
        'output_truncated': len(p.stdout) >= CAP or len(p.stderr) >= CAP,
        'key_output': key,
    }
    (ART / (label + '.run.json')).write_text(json.dumps(row, indent=2) + '\n')
    return row


def run_batch(specs):
    # Each batch contains at most two counters. No job outlives this call.
    assert sum(s[2] == 'counter' for s in specs) <= 2
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(specs)) as pool:
        return list(pool.map(lambda s: run_probe(*s), specs))
