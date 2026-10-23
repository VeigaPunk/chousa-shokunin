#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('/fast/scratch/hyaku/chousa-r33/w2/MutC1GateDepth')
LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
ART = LANE / '.ufo/waves/round-33/w2/MutC1GateDepth'
GATE = ROOT / 'repo/tools/research-gate.sh'
COUNTER = LANE / 'corpus/evidence/round33/c1-count-v2.py'
LIMIT = 950000

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(label, args, seconds, env):
    cmd = ['timeout', '--kill-after=5', str(seconds), 'prlimit', '--nproc=2000', '--as=4000000000', '--'] + list(args)
    t = time.monotonic()
    if label.endswith('.counter'):
        with (ART/(label+'.stdout')).open('wb') as stdout:
            result = subprocess.run(cmd, cwd=ROOT, env=env, stdout=stdout, stderr=subprocess.PIPE, timeout=seconds+15)
        data_out = (ART/(label+'.stdout')).read_bytes()
    else:
        result = subprocess.run(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=seconds+15)
        data_out = result.stdout
    entry = {'label': label, 'command': cmd, 'cwd': str(ROOT), 'exit': result.returncode, 'elapsed_s': round(time.monotonic()-t, 3)}
    for name, data in [('stdout', data_out), ('stderr', result.stderr)]:
        p = ART / (label + '.' + name)
        p.write_bytes(data[:LIMIT])
        entry[name] = str(p)
        entry[name + '_bytes'] = len(data)
        entry[name + '_sha256'] = hashlib.sha256(data).hexdigest()
        entry[name + '_truncated'] = len(data) > LIMIT
    print(json.dumps(entry), flush=True)
    return entry

phase, seed = sys.argv[1], int(sys.argv[2])
env = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
env.update(C1_TMP=str(ROOT/'tmp'), C2_TMP=str(ROOT/'tmp'), TMPDIR=str(ROOT/'tmp'), PYTHONDONTWRITEBYTECODE='1')
receipt = ART / (phase + '.counter.json')
assert not receipt.exists(), receipt
summary = {'phase': phase, 'gate_sha256_before': sha(GATE), 'counter_sha256': sha(COUNTER), 'seed': seed, 'environment': {k: env[k] for k in ('C1_TMP', 'C2_TMP', 'TMPDIR')}}
summary['counter'] = run(phase+'.counter', ['python3', str(COUNTER), '--gate', str(GATE), '--seed', str(seed), '--receipt', str(receipt)], 650, env)
summary['receipt'] = str(receipt)
summary['selftest'] = run(phase+'.selftest', ['bash', str(GATE), '--selftest'], 240, env)
summary['gate_sha256_after'] = sha(GATE)
(ART/(phase+'.run.json')).write_text(json.dumps(summary, indent=2)+'\n')
print('PHASE', phase, 'counter_exit', summary['counter']['exit'], 'selftest_exit', summary['selftest']['exit'], 'hash', summary['gate_sha256_after'], flush=True)
