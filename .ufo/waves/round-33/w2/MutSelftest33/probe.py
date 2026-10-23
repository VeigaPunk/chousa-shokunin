#!/usr/bin/env python3
"""Eight scratch-only mutants; identical detector before/after with fresh counter seeds."""
import concurrent.futures
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import time

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
S = Path('/fast/scratch/hyaku/chousa-r33/w2/MutSelftest33')
A = LANE / '.ufo/waves/round-33/w2/MutSelftest33'
P = S / 'pristine.sh'
FOCUS = S / 'targeted-selftest.sh'
COUNTER = LANE / 'corpus/evidence/round33/c1-count-v2.py'
EXPECTED = '94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e'
SEED_BASE = 863330000001
CAP = 900000
DESCRIPTIONS = {
    'M1': 'Reject a nested container instead of skipping its value (1192 insertion).',
    'M2': 'Omit the duplicate-presence flag assignment (1237).',
    'M3': 'Leave escape state set after consuming an escaped character (1185).',
    'M4': 'Bypass nested-string protection while counting brackets (1196).',
    'M5': 'Omit span from the duplicate-read-field validation loop (1622).',
    'M6': 'Keep the first duplicated id even when the second differs (1638).',
    'M7': 'Regress the string-field accessor to first raw regex match (1261-1262).',
    'M8': 'Regress the field-presence accessor to raw regex search (1272).',
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save_json(path, data):
    text = json.dumps(data, indent=1) + '\n'
    assert len(text.encode()) < CAP
    path.write_text(text)


def capture(label, kind, inner, env, limit):
    out = A / f'{label}.{kind}.stdout'
    err = A / f'{label}.{kind}.stderr'
    cmd = ['timeout', '--kill-after=5s', f'{limit}s', 'prlimit', '--nproc=2000',
           '--as=4000000000', f'--fsize={CAP}', '--', *map(str, inner)]
    t = time.monotonic()
    with out.open('wb') as stdout, err.open('wb') as stderr:
        proc = subprocess.Popen(cmd, cwd=S, env=env, stdout=stdout, stderr=stderr)
        pid = proc.pid
        rc = proc.wait()
    text = out.read_text(errors='replace')
    result = {'command': shlex.join(cmd) + f' > {out} 2> {err}', 'pid': pid,
              'exit_code': rc, 'elapsed_s': round(time.monotonic()-t, 3),
              'stdout': str(out), 'stdout_sha256': sha(out),
              'stderr': str(err), 'stderr_sha256': sha(err)}
    if kind == 'selftest':
        result['failed_cases'] = re.findall(r'^FAIL-case\s+(r33-top-\S+)', text, re.M)
        result['passed_cases'] = re.findall(r'^ok-case\s+\d+\s+(r33-top-\S+)', text, re.M)
        result['summary'] = text.splitlines()[-1] if text.splitlines() else ''
    else:
        result['summary'] = text.splitlines()[0] if text.splitlines() else ''
    return result


def phase(label, gate, seed):
    gate_sha = sha(gate)
    tmp = S / f'{label}.tmp'
    fixture = S / f'{label}.selftest-fixture'
    tmp.mkdir(exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_')}
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        env.pop(key, None)
    for key in ('C1_TMP', 'C2_TMP', 'TMPDIR'):
        env[key] = str(tmp)
    receipt = A / f'{label}.json'
    r = {'label': label, 'gate': str(gate), 'gate_sha256': gate_sha, 'seed': seed,
         'environment': {k: env[k] for k in ('C1_TMP', 'C2_TMP', 'TMPDIR')}}
    r['selftest'] = capture(label, 'selftest', ['bash', FOCUS, gate, fixture], env, 180)
    r['counter'] = capture(label, 'counter', ['python3', COUNTER, '--gate', gate,
                            '--seed', str(seed), '--receipt', receipt], env, 700)
    r['counter']['receipt'] = str(receipt)
    if receipt.exists():
        rec = json.loads(receipt.read_text())
        r['counter'].update({k: rec[k] for k in ('matched', 'total', 'gate_rc', 'gate_timed_out', 'predicate_holds', 'per_class')})
    assert sha(gate) == gate_sha, f'Gate changed during detector: {gate}'
    save_json(A / f'{label}.commands.json', r)
    return r


def main():
    pristine = P.read_bytes()
    assert hashlib.sha256(pristine).hexdigest() == EXPECTED
    assert sha(LANE / 'tools/research-gate.sh') == EXPECTED
    # Extraction identity: helper, source fixture and all seven tests must be unchanged.
    lines = pristine.decode().splitlines(keepends=True)
    focused = FOCUS.read_text()
    spans = [(3998, 4026), (7041, 7054), (7568, 7630)]
    extraction = [{'gate_lines': f'{a}-{b}', 'exact_substring': ''.join(lines[a-1:b]) in focused}
                  for a, b in spans]
    assert all(row['exact_substring'] for row in extraction), extraction
    save_json(A / 'detector-extraction.json', {'gate_sha256': EXPECTED,
        'focused_sha256': sha(FOCUS), 'counter_sha256': sha(COUNTER), 'sections': extraction})
    shutil.copyfile(FOCUS, A / FOCUS.name)
    shutil.copyfile(S / 'probe.py', A / 'probe.py')
    shutil.copyfile(P, A / 'landed-gate.sh')
    initial = {}
    for m in DESCRIPTIONS:
        gate = S / m / 'gate.sh'
        mutant = gate.read_bytes()
        assert mutant != pristine and len(mutant) < CAP
        initial[m] = {'description': DESCRIPTIONS[m], 'before_sha256': EXPECTED,
                      'mutant_sha256': hashlib.sha256(mutant).hexdigest()}
        patch = ''.join(difflib.unified_diff(pristine.decode().splitlines(keepends=True),
                        mutant.decode().splitlines(keepends=True), fromfile='landed-gate.sh', tofile=f'{m}/gate.sh'))
        (A / f'{m}.patch').write_text(patch)
        shutil.copyfile(gate, A / f'{m}.mutant-gate.sh')
    save_json(A / 'mutants.json', initial)
    results = {'baseline': None, 'mutants': {}, 'complete': False}
    try:
        results['baseline'] = phase('pristine', P, SEED_BASE)
        base = results['baseline']
        assert base['selftest']['exit_code'] == 0 and len(base['selftest']['passed_cases']) == 7, base
        assert base['counter']['exit_code'] == 0 and base['counter'].get('matched') == 156, base
        def probe(item):
            index, m = item
            gate = S / m / 'gate.sh'
            r = dict(initial[m])
            try:
                r['mutated'] = phase(f'{m}-mutated', gate, SEED_BASE + 1 + index*2)
            except Exception as e:
                r['error'] = repr(e)
            finally:
                shutil.copyfile(P, gate)
                r['restored_sha256'] = sha(gate)
                r['exact_bytes_restored'] = gate.read_bytes() == pristine
                try:
                    r['restored'] = phase(f'{m}-restored', gate, SEED_BASE + 2 + index*2)
                except Exception as e:
                    r['restore_detector_error'] = repr(e)
                save_json(A / f'{m}.probe.json', r)
            return m, r
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for m, r in pool.map(probe, enumerate(DESCRIPTIONS)):
                results['mutants'][m] = r
        results['complete'] = len(results['mutants']) == 8
    finally:
        # Also restore mutants that were not reached after a baseline/harness failure.
        results['final_restoration'] = {}
        for m in DESCRIPTIONS:
            gate = S / m / 'gate.sh'
            shutil.copyfile(P, gate)
            results['final_restoration'][m] = {'sha256': sha(gate), 'exact_bytes': gate.read_bytes() == pristine}
        results['lane_gate_sha256_after'] = sha(LANE / 'tools/research-gate.sh')
        results['counter_sha256_after'] = sha(COUNTER)
        save_json(A / 'results.json', results)
    for m in DESCRIPTIONS:
        r = results['mutants'].get(m, {})
        mut, restored = r.get('mutated', {}), r.get('restored', {})
        print(m, json.dumps({'failed_selftests': mut.get('selftest', {}).get('failed_cases'),
                            'counter': mut.get('counter', {}).get('summary'),
                            'restored_selftest_rc': restored.get('selftest', {}).get('exit_code'),
                            'restored_counter': restored.get('counter', {}).get('summary'),
                            'exact_bytes_restored': r.get('exact_bytes_restored'),
                            'error': r.get('error')}, sort_keys=True), flush=True)
    print('RESULTS', A / 'results.json', flush=True)

if __name__ == '__main__':
    main()
