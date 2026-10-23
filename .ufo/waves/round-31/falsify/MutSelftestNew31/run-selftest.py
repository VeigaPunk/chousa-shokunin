#!/usr/bin/env python3
"""Record one full selftest; outer GNU timeout bounds this foreground process."""
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import signal
import subprocess
import sys
import time

phase, mutant, gate_arg = sys.argv[1:]
gate = Path(gate_arg)
artifacts = Path(__file__).resolve().parent
scratch = Path('/fast/scratch/hyaku/chousa-r31/w2/MutSelftestNew31')
tmp = scratch / 'tmp' / f'{phase}-{mutant}'
tmp.mkdir(parents=True, exist_ok=True)
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
resource.setrlimit(resource.RLIMIT_NPROC, (8192, 8192))
env = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_')}
env['TMPDIR'] = str(tmp)
env['LC_ALL'] = 'C.UTF-8'
log = artifacts / f'{phase}-{mutant}.log'
receipt = artifacts / f'{phase}-{mutant}.json'
before = hashlib.sha256(gate.read_bytes()).hexdigest()
if phase == 'mutated':
    (artifacts / f'mutant-{mutant}.sh').write_bytes(gate.read_bytes())
started = time.monotonic()
proc = None
interrupted = False

class ProbeTimeout(Exception):
    pass

def interrupt(signum, frame):
    raise ProbeTimeout(signum)

signal.signal(signal.SIGTERM, interrupt)
signal.signal(signal.SIGINT, interrupt)
try:
    with log.open('wb') as output:
        proc = subprocess.Popen(['bash', str(gate), '--selftest'], cwd=gate.parent.parent,
                                env=env, stdout=output, stderr=subprocess.STDOUT,
                                start_new_session=True)
        try:
            rc = proc.wait()
        except ProbeTimeout:
            interrupted = True
            os.killpg(proc.pid, signal.SIGKILL)
            rc = proc.wait()
finally:
    if proc is not None:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

after = hashlib.sha256(gate.read_bytes()).hexdigest()
text = log.read_text(errors='replace')
case_rows = []
for line in text.splitlines():
    match = re.match(r'^(ok-case|FAIL-case|skip-case)\s+(?:(\d+)\s+)?(\S+)(?:\s+(.*))?$', line)
    if match:
        status, number, name, details = match.groups()
        case_rows.append({'number': int(number) if number else None, 'name': name,
                          'status': status, 'details': details or '', 'raw': line})
new_names = ['c1-pass-bound', 'c1-fail-mislocated', 'c1-fail-invalid-line', 'c1-pass-no-line',
             'claims-sha-absent', 'claims-sha-absent-fail', 'claims-sha-match',
             'claims-sha-match-spanfail', 'claims-sha-stale', 'claims-sha-invalid',
             'claims-sha-validity', 'claims-sha-refused', 'claims-sha-crlf']
new_cases = {}
for number, name in enumerate(new_names, 216):
    rows = [row for row in case_rows if row['name'] == name]
    new_cases[str(number)] = rows[0]['status'] if len(rows) == 1 else 'unobserved-or-duplicate'
result = {'phase': phase, 'mutant': mutant, 'gate': str(gate),
          'outer_command': ['timeout', '-k', '10', '1200', 'python3', str(Path(__file__).resolve()),
                            phase, mutant, str(gate)],
          'detector': ['bash', str(gate), '--selftest'], 'rc': rc,
          'interrupted': interrupted, 'elapsed_seconds': round(time.monotonic() - started, 3),
          'sha256_before': before, 'sha256_after': after,
          'summary': [line for line in text.splitlines() if line.startswith('RESEARCH_GATE_SELFTEST:')],
          'case_records': len(case_rows),
          'failed_cases': [row for row in case_rows if row['status'] == 'FAIL-case'],
          'skipped_cases': [row for row in case_rows if row['status'] == 'skip-case'],
          'new_cases_216_228': new_cases, 'case_rows': case_rows, 'log': str(log)}
receipt.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: result[key] for key in ['phase', 'mutant', 'rc', 'interrupted',
      'elapsed_seconds', 'sha256_before', 'sha256_after', 'summary', 'case_records',
      'failed_cases', 'skipped_cases', 'new_cases_216_228']}, indent=2), flush=True)
sys.exit(124 if interrupted else rc)
