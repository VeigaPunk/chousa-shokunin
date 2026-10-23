#!/usr/bin/env python3
"""Repeat C1 timing in an installed UTF-8 locale; retain earlier C-locale data."""
import hashlib
import json
import os
from pathlib import Path
import resource
import statistics
import subprocess
import time

scratch = Path('/tmp/hyaku/chousa-r35/w2/CritGrepClaimScope')
artifacts = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/CritGrepClaimScope')
gates = {name: scratch / name / 'tools/research-gate.sh' for name in ('base', 'landed')}
env = {k: v for k, v in os.environ.items() if not k.startswith(('CHOUSA_', 'RESEARCH_GATE_')) and k not in ('BASH_ENV', 'ENV', 'CDPATH')}
env.update(PATH='/usr/bin:/bin', LC_ALL='C.utf8', TMPDIR=str(scratch), C1_TMP=str(scratch), C2_TMP=str(scratch), WITNESS_TMP=str(scratch))
empty = scratch / 'empty.jsonl'
receipt = {'locale': env['LC_ALL'], 'gate_sha256': {name: hashlib.sha256(gate.read_bytes()).hexdigest() for name, gate in gates.items()}, 'load_start': os.getloadavg(), 'invocations': [], 'selftests': []}


def run(name, args, kind, index):
    command = ['timeout', '900s', 'bash', str(gates[name]), *args]
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.perf_counter_ns()
    p = subprocess.run(command, env=env, cwd=gates[name].parents[1], capture_output=True, timeout=905)
    wall_ms = (time.perf_counter_ns() - start) / 1e6
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    row = {'name': name, 'index': index, 'argv': command, 'exit': p.returncode, 'wall_ms': wall_ms, 'child_user_s': after.ru_utime - before.ru_utime, 'child_sys_s': after.ru_stime - before.ru_stime, 'stdout_bytes': len(p.stdout), 'stderr_bytes': len(p.stderr), 'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(), 'stderr_sha256': hashlib.sha256(p.stderr).hexdigest(), 'stdout_last_line': p.stdout.decode(errors='replace').splitlines()[-1:]}
    if kind == 'selftest':
        for stream, value in (('stdout', p.stdout), ('stderr', p.stderr)):
            log = scratch / ('utf8-selftest-%d-%s.%s' % (index, name, stream))
            log.write_bytes(value)
            row[stream + '_path'] = str(log)
        print(json.dumps({'selftest': row}), flush=True)
    return row


for name in ('base', 'landed'):
    run(name, ['verify-claims', str(empty), '--root', str(scratch)], 'warmup', 0)
for i in range(60):
    order = ('base', 'landed') if i % 2 == 0 else ('landed', 'base')
    for name in order:
        receipt['invocations'].append(run(name, ['verify-claims', str(empty), '--root', str(scratch)], 'invocation', i))
for index, name in enumerate(('base', 'landed', 'landed', 'base')):
    receipt['selftests'].append(run(name, ['--selftest'], 'selftest', index))
    (artifacts / 'timing-utf8.json').write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
summary = {}
for kind in ('invocations', 'selftests'):
    summary[kind] = {}
    for name in gates:
        rows = [row for row in receipt[kind] if row['name'] == name]
        summary[kind][name] = {'n': len(rows), 'median_wall_ms': statistics.median(row['wall_ms'] for row in rows), 'mean_wall_ms': statistics.mean(row['wall_ms'] for row in rows), 'min_wall_ms': min(row['wall_ms'] for row in rows), 'max_wall_ms': max(row['wall_ms'] for row in rows), 'exit_codes': [row['exit'] for row in rows], 'mean_child_cpu_s': statistics.mean(row['child_user_s'] + row['child_sys_s'] for row in rows)}
receipt['summary'] = summary
receipt['load_end'] = os.getloadavg()
(artifacts / 'timing-utf8.json').write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
print(json.dumps(summary, indent=1), flush=True)
