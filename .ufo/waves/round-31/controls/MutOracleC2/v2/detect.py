#!/usr/bin/env python3
"""Re-score frozen controls without changing source or overwriting v1 evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

SANDBOX = Path('/fast/scratch/hyaku/chousa-r31/MutOracleC2/v2')
ARTIFACTS = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/controls/MutOracleC2/v2')
LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
COUNTER = LANE / 'corpus/evidence/round31/c2-count.py'
EXPECTED_COUNTER_SHA256 = '1064fdb356e25440c64bb4d4d5363acb9c1bbc32c687c8ea50096d74c849d500'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('control')
    parser.add_argument('--phase', choices=['rescore', 'restored'], default='rescore')
    args = parser.parse_args()
    campaign = json.loads((ARTIFACTS / 'campaign.json').read_text())
    if args.control not in campaign['controls']:
        raise ValueError('unknown frozen control')
    gate = ARTIFACTS / f'{args.control}.sh'
    for seed in campaign['seeds']:
        stem = f'{args.control}-{args.phase}-seed{seed}'
        receipt = ARTIFACTS / f'{stem}.json'
        execution = ARTIFACTS / f'{stem}.execution.json'
        if receipt.exists() or execution.exists():
            raise RuntimeError(f'refusing to overwrite evidence: {stem}')
        if sha256(COUNTER) != EXPECTED_COUNTER_SHA256:
            raise RuntimeError('counter no longer matches frozen v2 hash')
        command = ['/usr/bin/timeout', '900', '/usr/bin/prlimit', '--as=536870912',
                   '--cpu=90', '--nproc=4096', '--', '/usr/bin/python3',
                   'corpus/evidence/round31/c2-count.py', '--gate', str(gate),
                   '--seed', str(seed), '--receipt', str(receipt)]
        before = sha256(gate)
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
        after = sha256(gate)
        detector = json.loads(receipt.read_text()) if receipt.exists() else None
        counter_hash_verified = detector is not None and detector['counter_sha256'] == EXPECTED_COUNTER_SHA256
        result = {
            'schema': 'chousa-r31-c2-detector-execution/v2',
            'control': args.control, 'phase': args.phase, 'seed': seed,
            'command': command, 'cwd': str(LANE), 'returncode': process.returncode,
            'supervisor_timed_out': supervisor_timeout,
            'elapsed_s': round(time.monotonic() - started, 3),
            'gate_sha256_before': before, 'gate_sha256_after': after,
            'counter_receipt': str(receipt), 'stdout': stdout, 'stderr': stderr,
            'counter_sha256_verified': counter_hash_verified,
            'matched': detector['matched'] if detector else None,
            'per_class': detector['per_class'] if detector else None,
            'process_group_cleanup': 'SIGKILL attempted after exit; nonexistent groups ignored',
        }
        execution.write_text(json.dumps(result, indent=2) + '\n')
        print(f'{args.control} {args.phase} seed={seed} rc={process.returncode} counter_sha256_verified={counter_hash_verified}', flush=True)
        print(stdout, end='', flush=True)
        if stderr:
            print('STDERR=' + stderr, flush=True)
        if supervisor_timeout or before != after or not counter_hash_verified or process.returncode not in (0, 1):
            raise RuntimeError(f'inconclusive detector run: {execution}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
