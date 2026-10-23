#!/usr/bin/env python3
"""Bounded, sequential frozen-counter runs; writes receipts, never gate source."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

SANDBOX = Path('/fast/scratch/hyaku/chousa-r31/MutOracleC2')
ARTIFACTS = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/controls/MutOracleC2')
LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
GATE = SANDBOX / 'active.sh'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('control')
    parser.add_argument('phase', choices=['feasibility', 'pristine', 'mutated', 'restored'])
    parser.add_argument('--all-seeds', action='store_true')
    args = parser.parse_args()
    campaign = json.loads((ARTIFACTS / 'campaign.json').read_text())
    seeds = campaign['oracle_seeds'] if args.all_seeds else campaign['mutation_seeds']
    for seed in seeds:
        stem = f'{args.control}-{args.phase}-seed{seed}'
        receipt = ARTIFACTS / f'{stem}.json'
        execution = ARTIFACTS / f'{stem}.execution.json'
        command = ['/usr/bin/timeout', '900', '/usr/bin/prlimit', '--as=536870912',
                   '--cpu=90', '--nproc=4096', '--', '/usr/bin/python3',
                   'corpus/evidence/round31/c2-count.py', '--gate', str(GATE),
                   '--seed', str(seed), '--receipt', str(receipt)]
        before = sha256(GATE)
        environment = dict(os.environ, C2_TMP=str(SANDBOX / 'tmp'),
                           TMPDIR=str(SANDBOX / 'tmp'), PYTHONDONTWRITEBYTECODE='1')
        started = time.monotonic()
        process = subprocess.Popen(command, cwd=LANE, env=environment, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        supervisor_timeout = False
        try:
            stdout, stderr = process.communicate(timeout=905)
        except subprocess.TimeoutExpired:
            supervisor_timeout = True
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        finally:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        after = sha256(GATE)
        result = {
            'schema': 'chousa-r31-c2-detector-execution/v1',
            'control': args.control, 'phase': args.phase, 'seed': seed,
            'command': command, 'cwd': str(LANE), 'returncode': process.returncode,
            'supervisor_timed_out': supervisor_timeout,
            'elapsed_s': round(time.monotonic() - started, 3),
            'gate_sha256_before': before, 'gate_sha256_after': after,
            'counter_receipt': str(receipt), 'stdout': stdout, 'stderr': stderr,
            'process_group_cleanup': 'SIGKILL attempted after exit; nonexistent groups ignored',
        }
        if receipt.exists():
            detector = json.loads(receipt.read_text())
            result['matched'] = detector['matched']
            result['per_class'] = detector['per_class']
        execution.write_text(json.dumps(result, indent=2) + '\n')
        print(f'{args.control} {args.phase} seed={seed} rc={process.returncode} sha256={before}', flush=True)
        print(stdout, end='', flush=True)
        if stderr:
            print('STDERR=' + stderr, flush=True)
        if supervisor_timeout or before != after or not receipt.exists():
            raise RuntimeError(f'inconclusive detector run: {execution}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
