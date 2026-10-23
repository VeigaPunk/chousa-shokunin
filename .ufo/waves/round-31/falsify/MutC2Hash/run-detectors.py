#!/usr/bin/env python3
"""Round-31 isolated C2 hashing mutation measurements; never edits a gate."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import resource
import shlex
import signal
import subprocess
import time

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
ART = LANE / '.ufo/waves/round-31/falsify/MutC2Hash'
SCRATCH = Path('/fast/scratch/hyaku/chousa-r31/w2/MutC2Hash')
GATE = SCRATCH / 'repo/tools/research-gate.sh'
COUNTER = LANE / 'corpus/evidence/round31/c2-count.py'
PRISTINE = ART / 'pristine-research-gate.sh'
ENV = {k: v for k, v in os.environ.items()
       if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
ENV.update(TMPDIR=str(SCRATCH / 'tmp'), C2_TMP=str(SCRATCH / 'tmp'),
           PYTHONDONTWRITEBYTECODE='1')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
    old = resource.getrlimit(resource.RLIMIT_NPROC)
    cap = min(4096, old[1]) if old[1] >= 0 else 4096
    resource.setrlimit(resource.RLIMIT_NPROC, (cap, cap))


def run_one(stage, kind, seed=None):
    label = stage + '.' + (str(seed) if seed is not None else 'selftest')
    if kind == 'counter':
        receipt = ART / (label + '.receipt.json')
        command = ['timeout', '--kill-after=5s', '900s', 'python3', str(COUNTER),
                   '--gate', str(GATE), '--seed', str(seed), '--receipt', str(receipt)]
        deadline = 915
    else:
        command = ['timeout', '--kill-after=5s', '1180s', 'bash', str(GATE), '--selftest']
        deadline = 1190
    before = sha(GATE)
    t0 = time.monotonic()
    p = subprocess.Popen(command, cwd=LANE, env=ENV, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True)
    watchdog = False
    try:
        try:
            out, err = p.communicate(timeout=deadline)
        except subprocess.TimeoutExpired:
            watchdog = True
            os.killpg(p.pid, signal.SIGKILL)
            out, err = p.communicate(timeout=5)
    finally:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    (ART / (label + '.stdout')).write_bytes(out)
    (ART / (label + '.stderr')).write_bytes(err)
    text = out.decode('utf-8', errors='replace')
    result = dict(stage=stage, kind=kind, seed=seed, command=shlex.join(command),
                  cwd=str(LANE), exit=p.returncode, watchdog=watchdog,
                  elapsed_s=round(time.monotonic() - t0, 3),
                  gate_before_sha256=before, gate_after_sha256=sha(GATE),
                  counter_sha256=sha(COUNTER),
                  stdout=str(ART / (label + '.stdout')),
                  stderr=str(ART / (label + '.stderr')),
                  key_output=[line for line in text.splitlines()
                              if line.startswith(('REVISION_BINDING_MATCH=',
                                                  'RESEARCH_GATE_SELFTEST:', 'FAIL-case'))])
    if kind == 'counter' and receipt.exists():
        data = json.loads(receipt.read_text())
        result.update(matched=data['matched'], gate_rc=data['gate_rc'],
                      predicate_holds=data['predicate_holds'], per_class=data['per_class'])
    (ART / (label + '.run.json')).write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    limits()
    parser = argparse.ArgumentParser()
    parser.add_argument('stage')
    parser.add_argument('--seeds', nargs='*', type=int, default=[])
    parser.add_argument('--no-selftest', action='store_true')
    args = parser.parse_args()
    jobs = [('counter', seed) for seed in args.seeds]
    if not args.no_selftest:
        jobs.insert(0, ('selftest', None))
    before = sha(GATE)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        handles = [pool.submit(run_one, args.stage, kind, seed) for kind, seed in jobs]
        results = [handle.result() for handle in handles]
    summary = dict(stage=args.stage, axes=['coverage', 'operability'],
                   gate_before_sha256=before, gate_after_sha256=sha(GATE),
                   gate_equals_pristine=GATE.read_bytes() == PRISTINE.read_bytes(),
                   memory_cap_bytes=2 * 1024**3, process_cap=4096,
                   TMPDIR=ENV['TMPDIR'], C2_TMP=ENV['C2_TMP'], results=results)
    (ART / (args.stage + '.summary.json')).write_text(json.dumps(summary, indent=2) + '\n')
    for result in results:
        print(json.dumps({k: result[k] for k in
                          ('kind', 'seed', 'exit', 'elapsed_s', 'key_output')}, sort_keys=True), flush=True)
    print('GATE_SHA256=' + sha(GATE), flush=True)
    print('GATE_EQUALS_PRISTINE=' + str(summary['gate_equals_pristine']).lower(), flush=True)


if __name__ == '__main__':
    main()
