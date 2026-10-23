#!/usr/bin/env python3
"""Scoped C2 parse mutation detectors; never edits the gate or frozen counter."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import secrets
import shlex
import signal
import subprocess
import time

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
ART = LANE / '.ufo/waves/round-31/falsify/MutC2Parse'
SCRATCH = Path('/fast/scratch/hyaku/chousa-r31/w2/MutC2Parse')
GATE = SCRATCH / 'repo/tools/research-gate.sh'
COUNTER = LANE / 'corpus/evidence/round31/c2-count.py'
PRISTINE = SCRATCH / 'pristine-gate.sh'
EXPECTED_GATE = 'c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c'
EXPECTED_COUNTER = '1064fdb356e25440c64bb4d4d5363acb9c1bbc32c687c8ea50096d74c849d500'
LINE_RE = re.compile(r'^CLAIM id=(\S+) .*?observed=(\S+)')
FIND_RE = re.compile(r'^FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=(?:warn|crit) surface=claims obs=id=(\S+)(?:\s|$)')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def execute(name, argv, limit, env):
    command = ['timeout', '--kill-after=5s', str(limit) + 's', *map(str, argv)]
    start = time.monotonic()
    process = subprocess.Popen(command, cwd=LANE, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    killed_after_wrapper = False
    try:
        out, err = process.communicate(timeout=limit + 10)
    except subprocess.TimeoutExpired:
        killed_after_wrapper = True
        os.killpg(process.pid, signal.SIGKILL)
        out, err = process.communicate(timeout=10)
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    (ART / (name + '.stdout')).write_bytes(out)
    (ART / (name + '.stderr')).write_bytes(err)
    record = {'command': shlex.join(command), 'cwd': str(LANE), 'rc': process.returncode,
              'elapsed_s': round(time.monotonic() - start, 3), 'wrapper_overrun': killed_after_wrapper,
              'stdout': str(ART / (name + '.stdout')), 'stderr': str(ART / (name + '.stderr'))}
    print(f'{name}: rc={process.returncode} elapsed={record["elapsed_s"]}s', flush=True)
    return record, out.decode('utf-8', errors='replace')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stage')
    ap.add_argument('--skip-selftest', action='store_true')
    args = ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
    resource.setrlimit(resource.RLIMIT_NPROC, (16384, 16384))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    assert sha(PRISTINE) == EXPECTED_GATE
    assert sha(COUNTER) == EXPECTED_COUNTER
    if 'pristine' in args.stage or 'restored' in args.stage:
        assert GATE.read_bytes() == PRISTINE.read_bytes(), 'gate not restored'
    seed_file = ART / 'seeds.json'
    if not seed_file.exists():
        seed_file.write_text(json.dumps([secrets.randbits(63), secrets.randbits(63)]) + '\n')
    seeds = json.loads(seed_file.read_text())
    env = {k: v for k, v in os.environ.items()
           if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
    env.update(TMPDIR=str(SCRATCH / 'tmp'), C2_TMP=str(SCRATCH / 'tmp'), LC_ALL='C.utf8')
    result = {'stage': args.stage, 'axes': ['coverage', 'operability'], 'gate_sha256_before': sha(GATE),
              'counter_sha256': sha(COUNTER), 'pristine_sha256': sha(PRISTINE), 'seeds': seeds,
              'environment': {key: env[key] for key in ('TMPDIR', 'C2_TMP', 'LC_ALL')},
              'limits': {'address_space_bytes': 2 * 1024**3, 'processes': 16384}, 'counter': []}
    result_file = ART / (args.stage + '.json')
    try:
        for index, seed in enumerate(seeds, 1):
            receipt = ART / f'{args.stage}.seed{index}.receipt.json'
            rec, output = execute(f'{args.stage}.seed{index}',
                ['python3', COUNTER, '--gate', GATE, '--seed', str(seed), '--receipt', receipt], 900, env)
            if receipt.exists():
                data = json.loads(receipt.read_text())
                rec.update(seed=seed, receipt=str(receipt), matched=data['matched'], label=data['label'],
                           gate_rc=data['gate_rc'], gate_timed_out=data['gate_timed_out'])
            result['counter'].append(rec)
            print(output, end='', flush=True)
        if not args.skip_selftest:
            rec, output = execute(args.stage + '.selftest', ['bash', GATE, '--selftest'], 1200, env)
            lines = output.splitlines()
            rec['key_output'] = [line for line in lines if 'SELFTEST' in line or 'FAIL' in line]
            result['selftest'] = rec
            for line in rec['key_output']:
                print(line, flush=True)
        root = SCRATCH / 'focused'
        (root / 'src').mkdir(parents=True, exist_ok=True)
        source = root / 'src/probe.md'
        source.write_bytes(b'validation probe material\n')
        pin = sha(source)
        values = [('type_null', None), ('type_true', True), ('type_false', False), ('type_number', 17),
                  ('type_array', []), ('type_object', {}), ('space_lead', ' ' + pin),
                  ('space_trail', pin + ' '), ('space_both', ' ' + pin + ' '),
                  ('prefix', 'sha256:' + pin), ('short63', pin[:63]), ('long65', pin + '0'),
                  ('empty', ''), ('valid', pin), ('stale', '0' * 64)]
        rows, truth = [], {}
        for ident, value in values:
            rows.append({'id': ident, 'source': 'src/probe.md', 'span': 'validation probe material',
                         'expect': 'supported', 'sha256': value})
            truth[ident] = 'supported' if ident == 'valid' else 'stale' if ident == 'stale' else 'invalid'
        rows.append({'id': 'absent', 'source': 'src/probe.md', 'span': 'validation probe material',
                     'expect': 'supported'})
        truth['absent'] = 'supported'
        claims = root / 'claims.jsonl'
        claims.write_text(''.join(json.dumps(row) + '\n' for row in rows))
        rec, output = execute(args.stage + '.focused',
            ['bash', GATE, 'verify-claims', claims, '--root', root], 120, env)
        observed, flagged = {}, set()
        for line in output.splitlines():
            m = LINE_RE.match(line)
            if m:
                observed[m.group(1)] = m.group(2)
            m = FIND_RE.match(line)
            if m:
                flagged.add(m.group(1))
        misses = {ident: {'expected': expected, 'observed': observed.get(ident),
                         'revision_finding': ident in flagged}
                  for ident, expected in truth.items()
                  if observed.get(ident) != expected or ((ident in flagged) != (expected == 'stale'))}
        rec.update(matched=len(truth) - len(misses), total=len(truth), misses=misses,
                   observed=observed, source_sha256=pin)
        result['focused'] = rec
        print(f'FOCUSED_MATCH={rec["matched"]}/{rec["total"]} misses={json.dumps(misses, sort_keys=True)}', flush=True)
    finally:
        result['gate_sha256_after'] = sha(GATE)
        result['counter_sha256_after'] = sha(COUNTER)
        result_file.write_text(json.dumps(result, indent=2) + '\n')
    assert result['gate_sha256_before'] == result['gate_sha256_after'], 'detectors changed gate bytes'
    assert result['counter_sha256_after'] == EXPECTED_COUNTER, 'counter bytes changed'

if __name__ == '__main__':
    main()
