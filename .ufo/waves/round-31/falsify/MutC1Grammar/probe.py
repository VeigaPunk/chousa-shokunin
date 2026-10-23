#!/usr/bin/env python3
"""Bounded C1 grammar mutation detector; never mutates production sources."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import resource
import secrets
import shlex
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path('/fast/scratch/hyaku/chousa-r31/w2/MutC1Grammar')
REPO = ROOT / 'repo'
ART = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/falsify/MutC1Grammar')
GATE = REPO / 'tools/research-gate.sh'
COUNTER = REPO / 'corpus/evidence/round31/c1-count.py'
PRISTINE = ART / 'pristine.sh'
NAMES = ['leading-zeros', 'equal-range', 'nonstring-absent', 'trim-spaces', 'en-dash']
EXPECTED = 'c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c'
COUNTER_SHA = 'c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def record(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')

def limits():
    resource.setrlimit(resource.RLIMIT_AS, (2147483648, 2147483648))
    resource.setrlimit(resource.RLIMIT_NPROC, (8192, 8192))
    resource.setrlimit(resource.RLIMIT_CPU, (1200, 1200))
    resource.setrlimit(resource.RLIMIT_FSIZE, (67108864, 67108864))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

def run(command, bound, label):
    invocation = ['timeout', '--signal=TERM', '--kill-after=5s', str(bound)] + command
    env = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
    temp = ROOT / 'tmp'
    temp.mkdir(exist_ok=True)
    env.update(TMPDIR=str(temp), C1_TMP=str(temp))
    log = ART / (label + '.log')
    start = time.monotonic()
    with log.open('wb') as stream:
        process = subprocess.Popen(invocation, cwd=REPO, env=env, stdout=stream, stderr=subprocess.STDOUT,
                                   start_new_session=True, preexec_fn=limits)
        timed_out = False
        try:
            rc = process.wait(timeout=bound + 10)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            rc = process.wait(timeout=10)
        finally:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=10)
    output = log.read_text(errors='replace')
    important = [line for line in output.splitlines() if line.startswith(('LINE_BINDING_MATCH=', 'RESEARCH_GATE_SELFTEST:', 'FAIL-case'))
                 or ('ok-case' in line and 'c1-' in line)]
    result = {'command': shlex.join(invocation), 'cwd': str(REPO), 'exit_code': rc, 'outer_timeout': timed_out,
              'elapsed_s': round(time.monotonic() - start, 3), 'log': str(log), 'key_output': important}
    print(label, 'exit=' + str(rc), 'elapsed=' + str(result['elapsed_s']), flush=True)
    for line in important:
        print(line, flush=True)
    return result

def detect(name, state, seeds):
    assert sha(COUNTER) == COUNTER_SHA, 'frozen counter changed'
    before = sha(GATE)
    results = []
    for index, seed in enumerate(seeds, 1):
        label = name + '.' + state + '.c1-' + str(index)
        receipt = ART / (label + '.json')
        results.append(run(['python3', str(COUNTER), '--gate', str(GATE), '--seed', str(seed), '--receipt', str(receipt)], 900, label))
    results.append(run(['bash', str(GATE), '--selftest'], 1200, name + '.' + state + '.selftest'))
    data = {'name': name, 'state': state, 'seeds': seeds, 'gate_before_sha256': before,
            'gate_after_sha256': sha(GATE), 'counter_sha256': sha(COUNTER), 'results': results}
    record(ART / (name + '.' + state + '.detectors.json'), data)
    assert before == sha(GATE), 'detector changed gate bytes'
    return data

def main():
    mode, name = sys.argv[1:]
    assert name in NAMES
    assert sha(PRISTINE) == EXPECTED
    seed_path = ART / 'seeds.json'
    if not seed_path.exists():
        record(seed_path, {n: [secrets.randbits(63), secrets.randbits(63)] for n in NAMES})
    seeds = json.loads(seed_path.read_text())[name]
    if mode == 'baseline':
        assert sha(GATE) == EXPECTED
        detect(name, 'pristine', seeds)
    elif mode == 'probe':
        assert sha(GATE) != EXPECTED, 'no mutant present'
        mutant_sha = sha(GATE)
        shutil.copyfile(GATE, ART / (name + '.mutant.sh'))
        patch = ''.join(difflib.unified_diff(PRISTINE.read_text().splitlines(True), GATE.read_text().splitlines(True),
                                           fromfile='pristine/tools/research-gate.sh', tofile=name + '/tools/research-gate.sh'))
        (ART / (name + '.diff')).write_text(patch)
        try:
            detect(name, 'mutated', seeds)
        finally:
            shutil.copyfile(PRISTINE, GATE)
            evidence = {'before_sha256': EXPECTED, 'mutant_sha256': mutant_sha, 'restored_sha256': sha(GATE),
                        'exact_bytes_equal': PRISTINE.read_bytes() == GATE.read_bytes(),
                        'gate_regular_file': GATE.is_file() and not GATE.is_symlink(), 'gate_link_count': GATE.stat().st_nlink}
            record(ART / (name + '.restoration.json'), evidence)
            print(name, 'RESTORATION', json.dumps(evidence, sort_keys=True), flush=True)
            assert evidence['exact_bytes_equal'] and evidence['restored_sha256'] == EXPECTED
        detect(name, 'restored', seeds)
    else:
        raise ValueError(mode)

if __name__ == '__main__':
    def interrupted(signum, frame):
        raise TimeoutError('probe interrupted by signal ' + str(signum))
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    main()
