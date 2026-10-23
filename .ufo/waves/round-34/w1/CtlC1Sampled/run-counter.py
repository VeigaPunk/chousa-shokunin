#!/usr/bin/env python3
"""Run the frozen counter once; bound time/resources and retain exact receipts/output."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/chousa-r34/w1/CtlC1Sampled')
ARTIFACT = ROOT / '.ufo/waves/round-34/w1/CtlC1Sampled'
COUNTER = ROOT / 'corpus/evidence/round34/c1-count.py'
name, gate, seed = sys.argv[1:]
receipt = ARTIFACT / (name + '.json')
meta_path = ARTIFACT / (name + '.run.json')
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
cmd = ['timeout', '--kill-after=15s', '1600s', 'prlimit', '--as=2147483648', '--nproc=32768', '--fsize=16777216', 'python3', str(COUNTER), '--gate', gate, '--seed', seed, '--receipt', str(receipt)]
env = dict(os.environ, C1_TMP=str(SCRATCH), TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1')
started = time.time()
meta = dict(name=name, command=cmd, cwd=str(ROOT), environment={k: env[k] for k in ['C1_TMP', 'TMPDIR', 'PYTHONDONTWRITEBYTECODE']}, started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(started)), runner_pid=os.getpid(), gate_sha256_before=sha(gate), counter_sha256_before=sha(COUNTER))
p = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
meta.update(pid=p.pid, pgid=p.pid)
meta_path.write_text(json.dumps(meta, indent=1) + '\n')
print('START %s pid=%d pgid=%d' % (name, p.pid, p.pid), flush=True)
try:
    out, err = p.communicate(timeout=1640)
except subprocess.TimeoutExpired:
    os.killpg(p.pid, signal.SIGKILL)
    out, err = p.communicate()
for kind, data in [('stdout', out), ('stderr', err)]:
    if len(data) > 65536:
        raise RuntimeError('counter output exceeds 65536-byte cap')
    (ARTIFACT / (name + '.' + kind + '.txt')).write_bytes(data)
meta.update(exit_code=p.returncode, elapsed_s=round(time.time() - started, 3), gate_sha256_after=sha(gate), counter_sha256_after=sha(COUNTER), stdout_sha256=hashlib.sha256(out).hexdigest(), stderr_sha256=hashlib.sha256(err).hexdigest())
meta_path.write_text(json.dumps(meta, indent=1) + '\n')
print(out.decode(), end='')
print(err.decode(), end='', file=sys.stderr)
print('END %s rc=%d elapsed_s=%s gate_sha256=%s' % (name, p.returncode, meta['elapsed_s'], meta['gate_sha256_after']), flush=True)
sys.exit(p.returncode)
