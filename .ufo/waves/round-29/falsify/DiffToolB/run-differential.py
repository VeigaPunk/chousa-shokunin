#!/usr/bin/env python3
"""Bounded concurrent CLI runs; no detached processes or production writes."""
import concurrent.futures
import hashlib
import json
import os
import pathlib
import shlex
import signal
import subprocess
import time

ROOT = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
OUT = ROOT / '.ufo/waves/round-29/falsify/DiffToolB'
GUARD = OUT / 'guarded-run.py'
INPUTS = ['tools/quote-reopen.py', '.ufo/waves/round-29/build/ExecToolB/quote-reopen-b.py',
          'corpus/evidence/round29/claims.md', 'corpus/evidence/round29/c1-count.py',
          'corpus/fixtures/quote-reopen-r29/items.tsv', 'corpus/fixtures/quote-reopen-r29/labels.tsv',
          '.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv', 'corpus/SOURCES.md']

def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in INPUTS}

before = hashes()
heldout_source = (ROOT / INPUTS[6]).read_text(encoding='utf-8').splitlines()
heldout_copy = (OUT / 'held-out-3col.tsv').read_text(encoding='utf-8').splitlines()
assert heldout_copy == ['\t'.join(line.split('\t')[:3]) for line in heldout_source]
assert len(heldout_copy) == 34
jobs = [
    ('landed-fixture', 'tools/quote-reopen.py', 'corpus/fixtures/quote-reopen-r29/items.tsv', 40),
    ('independent-fixture', INPUTS[1], 'corpus/fixtures/quote-reopen-r29/items.tsv', 40),
    ('landed-heldout', 'tools/quote-reopen.py', str(OUT.relative_to(ROOT) / 'held-out-3col.tsv'), 33),
    ('independent-heldout', INPUTS[1], str(OUT.relative_to(ROOT) / 'held-out-3col.tsv'), 33),
]
environment = {key: value for key, value in os.environ.items() if not key.lower().endswith('_proxy')}
environment.update(PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', NO_PROXY='*')

def run(job):
    name, script, items, expected_count = job
    command = ['timeout', '--kill-after=5s', '590s', 'python3', str(GUARD),
               str(OUT / (name + '.network.json')), script, 'verify', '--items', items,
               '--registry', 'corpus/SOURCES.md']
    started = time.monotonic()
    child = subprocess.Popen(command, cwd=ROOT, env=environment, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = child.communicate(timeout=596)
    except subprocess.TimeoutExpired:
        os.killpg(child.pid, signal.SIGKILL)
        stdout, stderr = child.communicate()
    finally:
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    (OUT / (name + '.stdout')).write_text(stdout, encoding='utf-8')
    (OUT / (name + '.stderr')).write_text(stderr, encoding='utf-8')
    rows = [line.split('\t', 3) for line in stdout.splitlines() if line.startswith('QUOTE_REOPEN\t')]
    order = [line.split('\t')[0] for line in (ROOT / items).read_text(encoding='utf-8').splitlines()[1:] if line]
    result = {'name': name, 'command': shlex.join(command), 'cwd': str(ROOT),
              'exit_code': child.returncode, 'seconds': round(time.monotonic() - started, 3),
              'expected_count': expected_count, 'observed_count': len(rows),
              'order_matches': [row[1] for row in rows] == order,
              'rows': rows, 'summary': [line for line in stdout.splitlines() if line.startswith('QUOTE_REOPEN_SUMMARY')],
              'stderr': stderr}
    print(name, 'exit=' + str(child.returncode), 'rows=' + str(len(rows)), *result['summary'], flush=True)
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    runs = list(pool.map(run, jobs))
by_name = {run['name']: run for run in runs}
labels = dict(line.split('\t')[:2] for line in (ROOT / INPUTS[5]).read_text(encoding='utf-8').splitlines()[1:] if line)
disagreements = []
fixture_misses = {}
for dataset in ('fixture', 'heldout'):
    left = {row[1]: row[2:] for row in by_name['landed-' + dataset]['rows']}
    right = {row[1]: row[2:] for row in by_name['independent-' + dataset]['rows']}
    for item_id in sorted(left.keys() | right.keys()):
        a, b = left.get(item_id), right.get(item_id)
        if a is None or b is None or a[0] != b[0]:
            disagreements.append({'dataset': dataset, 'id': item_id, 'landed': a, 'independent': b})
    if dataset == 'fixture':
        for name, values in [('landed', left), ('independent', right)]:
            fixture_misses[name] = [{'id': item_id, 'expected': expected, 'actual': values.get(item_id)}
                                    for item_id, expected in labels.items()
                                    if values.get(item_id, [None])[0] != expected]
after = hashes()
receipt = {'before_sha256': before, 'after_sha256': after, 'production_bytes_unchanged': before == after,
           'heldout_copy_exact': True, 'environment': 'proxy variables removed; NO_PROXY=*; bytecode disabled',
           'network_policy': 'guarded GET to exact fragment-stripped source-column registry URLs only',
           'runs': runs, 'disagreements': disagreements, 'fixture_misses': fixture_misses}
(OUT / 'differential-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print('DISAGREEMENTS=' + str(len(disagreements)), json.dumps(disagreements), flush=True)
print('FIXTURE_MISSES', json.dumps(fixture_misses), flush=True)
print('PRODUCTION_BYTES_UNCHANGED=' + str(before == after), flush=True)
