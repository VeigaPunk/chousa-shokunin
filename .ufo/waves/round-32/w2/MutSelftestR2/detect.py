#!/usr/bin/env python3
"""Run only the assigned full-selftest mutation probes; logs are bounded."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import selectors
import shlex
import signal
import subprocess
import time

ROOT = Path('/fast/scratch/hyaku/chousa-r32/w2/MutSelftestR2')
ART = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/MutSelftestR2')
NAMES = ('sha-nonstring', 'line-nonstring', 'endline', 'span-before-stale', 'trimmed-pin', 'hash-fault')
MAX_LOG = 1_000_000
BASE_HASH = '10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bounded_write(path, data):
    if len(data) >= 1_048_576:
        raise RuntimeError(f'artifact too large: {path}')
    path.write_bytes(data)


def kill_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_detector(name, phase):
    gate = ROOT / name / 'lane/tools/research-gate.sh'
    tmp = ROOT / name / 'tmp'
    before = sha(gate.read_bytes())
    if phase != 'mutated' and before != BASE_HASH:
        raise RuntimeError(f'not pristine: {name}/{phase}: {before}')
    env = {key: value for key, value in os.environ.items()
           if not key.startswith('CHOUSA_') and key not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'BASH_ENV', 'ENV')}
    env.update(TMPDIR=str(tmp), C1_TMP=str(tmp), C2_TMP=str(tmp))
    command = ['timeout', '--signal=TERM', '--kill-after=5s', '600s', 'bash', str(gate), '--selftest']
    started = time.monotonic()
    proc = subprocess.Popen(command, cwd=gate.parent.parent, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, start_new_session=True)
    output = bytearray()
    bounded = True
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ)
    try:
        while selector.get_map():
            if time.monotonic() - started > 610:
                bounded = False
                kill_group(proc)
                break
            for key, _ in selector.select(timeout=1):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                if len(output) + len(chunk) > MAX_LOG:
                    output.extend(chunk[:MAX_LOG - len(output)])
                    bounded = False
                    kill_group(proc)
                    break
                output.extend(chunk)
            if not bounded:
                break
        rc = proc.wait(timeout=6)
    finally:
        selector.close()
        kill_group(proc)
        proc.wait(timeout=6)
        proc.stdout.close()
    elapsed = round(time.monotonic() - started, 3)
    text = output.decode('utf-8', errors='replace')
    lines = text.splitlines()
    failures = [line.split()[1] for line in lines if line.startswith('FAIL-case ')]
    r2_cases = [line for line in lines if (line.startswith(('ok-case ', 'FAIL-case ')))
                and ('claims-r2-' in line or 'r2-hash-fault-shim' in line)]
    summary = [line for line in lines if line.startswith('RESEARCH_GATE_SELFTEST:')]
    result = {'name': name, 'phase': phase, 'command': shlex.join(command),
              'cwd': str(gate.parent.parent), 'TMPDIR': str(tmp), 'rc': rc,
              'elapsed_s': elapsed, 'output_bound_holds': bounded,
              'gate_before_sha256': before, 'gate_after_sha256': sha(gate.read_bytes()),
              'log_sha256': sha(output), 'log_bytes': len(output),
              'failing_cases': failures, 'r2_cases': r2_cases, 'summary': summary,
              'process_group_kill_attempted': True}
    bounded_write(ART / f'{name}-{phase}.log', output)
    bounded_write(ART / f'{name}-{phase}.json', (json.dumps(result, indent=2) + '\n').encode())
    return result


def run_one(name, mode):
    if mode == 'pristine':
        return [run_detector(name, 'pristine')]
    gate = ROOT / name / 'lane/tools/research-gate.sh'
    pristine = (ROOT / 'pristine-research-gate.sh').read_bytes()
    if sha(pristine) != BASE_HASH:
        raise RuntimeError('backup hash differs from pinned candidate')
    results = []
    mutant_before = sha(gate.read_bytes())
    try:
        results.append(run_detector(name, 'mutated'))
    finally:
        gate.write_bytes(pristine)
        restored = gate.read_bytes()
        evidence = {'name': name, 'mutant_before_sha256': mutant_before,
                    'backup_sha256': sha(pristine), 'restored_sha256': sha(restored),
                    'exact_bytes_restored': restored == pristine}
        bounded_write(ART / f'{name}-restoration.json', (json.dumps(evidence, indent=2) + '\n').encode())
    results.append(run_detector(name, 'restored'))
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('pristine', 'mutated-restored'))
    parser.add_argument('names', nargs='+', choices=NAMES)
    args = parser.parse_args()
    # All workers are awaited here; no detached jobs or service processes.
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(args.names)) as executor:
        futures = [executor.submit(run_one, name, args.mode) for name in args.names]
        for future in futures:
            for result in future.result():
                print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
