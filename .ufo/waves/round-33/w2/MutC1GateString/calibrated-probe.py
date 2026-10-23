#!/usr/bin/env python3
"""Isolated round-33 string mutation detector; no lane source writes."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

SCRATCH = Path('/fast/scratch/hyaku/chousa-r33/w2/MutC1GateString')
LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
ART = LANE / '.ufo/waves/round-33/w2/MutC1GateString'
COUNTER = LANE / 'corpus/evidence/round33/c1-count-v2.py'
PHASE = sys.argv[1]
assert PHASE in ('pristine', 'mutated', 'restored', 'cal-pristine', 'cal-mutated', 'cal-restored')
SEED_BASE = {'pristine': 3383100, 'mutated': 3383200, 'restored': 3383300,
             'cal-pristine': 3383400, 'cal-mutated': 3383500, 'cal-restored': 3383600}[PHASE]
MAX_ARTIFACT = 990000

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run_one(mutant, detector):
    gate = SCRATCH / mutant / 'tools/research-gate.sh'
    stem = f'{mutant}-{PHASE}-{detector}'
    temp = SCRATCH / 'tmp' / mutant / (PHASE + '-' + detector)
    temp.mkdir(parents=True, exist_ok=True)
    env = {k:v for k,v in os.environ.items()
           if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
    env.update({'C1_TMP': str(temp), 'C2_TMP': str(temp), 'TMPDIR': str(temp), 'PYTHONDONTWRITEBYTECODE': '1'})
    receipt = ART / (stem + '.json')
    if detector == 'counter':
        seed = SEED_BASE + 'abcd'.index(mutant) + 1
        argv = ['python3', str(COUNTER), '--gate', str(gate), '--seed', str(seed), '--receipt', str(receipt)]
        deadline = 750
        file_cap = 1000000
        stdout = ART / (stem + '.stdout')
        stderr = ART / (stem + '.stderr')
    else:
        seed = None
        argv = ['bash', str(gate), '--selftest']
        deadline = 600
        file_cap = 20000000
        stdout = SCRATCH / (stem + '.stdout')
        stderr = SCRATCH / (stem + '.stderr')
    command = ['timeout', '--signal=TERM', '--kill-after=5', str(deadline),
               'prlimit', '--nproc=2000', '--as=4000000000', '--fsize=' + str(file_cap), '--'] + argv
    before = digest(gate)
    started = time.monotonic()
    with stdout.open('wb') as out, stderr.open('wb') as err:
        process = subprocess.Popen(command, cwd=LANE, env=env, stdout=out, stderr=err)
        pid = process.pid
        rc = process.wait(timeout=deadline + 15)
    result = {'mutant': mutant, 'phase': PHASE, 'detector': detector, 'seed': seed,
              'command': shlex.join(command) + ' >' + shlex.quote(str(stdout)) + ' 2>' + shlex.quote(str(stderr)),
              'environment': {k:env[k] for k in ('C1_TMP','C2_TMP','TMPDIR','PYTHONDONTWRITEBYTECODE')},
              'cwd': str(LANE), 'pid': pid, 'exit_code': rc, 'elapsed_s': round(time.monotonic()-started, 3),
              'gate_sha256_before': before, 'gate_sha256_after': digest(gate), 'receipt': str(receipt) if detector == 'counter' else None}
    for kind, path in [('stdout', stdout), ('stderr', stderr)]:
        data = path.read_bytes()
        dest = ART / (stem + '.' + kind)
        if path != dest:
            dest.write_bytes(data[:MAX_ARTIFACT])
        result[kind] = {'path': str(dest), 'source_path': str(path), 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest(), 'artifact_truncated': len(data) > MAX_ARTIFACT}
    if detector == 'counter' and receipt.exists():
        data = json.loads(receipt.read_text())
        result['summary'] = data['label']
        result['gate_rc'] = data['gate_rc']
        result['counter_sha256'] = data['counter_sha256']
    else:
        lines = stdout.read_text(errors='replace').splitlines()
        result['summary'] = [line for line in lines if 'RESEARCH_GATE_SELFTEST:' in line or 'FAIL' in line]
    return result

jobs = [(m, d) for m in 'abcd' for d in ('counter', 'selftest')]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(lambda pair: run_one(*pair), jobs))
manifest = ART / (PHASE + '-runs.json')
manifest.write_text(json.dumps(results, indent=2) + '\n')
for r in results:
    print(r['mutant'], r['phase'], r['detector'], 'rc=' + str(r['exit_code']), r['summary'], 'sha256=' + r['gate_sha256_before'])
print('manifest=' + str(manifest))
