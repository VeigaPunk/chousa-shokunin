#!/usr/bin/env python3
"""Use the same 73-item detector before, during, and after one scratch mutation.

This is diagnostic fixture/N-version agreement, not the frozen C1 predicate.
"""
import collections
import hashlib
import json
import os
import pathlib
import shlex
import signal
import subprocess
import sys
import time

ROOT = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
OUT = ROOT / '.ufo/waves/round-29/falsify/DiffToolB'
SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r29/w2/DiffToolB/tools/quote-reopen.py')
phase = sys.argv[1]
assert phase in {'pristine', 'mutated', 'restored'}
fixture_lines = (ROOT / 'corpus/fixtures/quote-reopen-r29/items.tsv').read_text(encoding='utf-8').splitlines()
heldout_lines = (OUT / 'held-out-3col.tsv').read_text(encoding='utf-8').splitlines()
combined = fixture_lines + heldout_lines[1:]
items = OUT / 'mutation-items-73.tsv'
items.write_text('\n'.join(combined) + '\n', encoding='utf-8')
expected = dict(line.split('\t')[:2] for line in (ROOT / 'corpus/fixtures/quote-reopen-r29/labels.tsv').read_text(encoding='utf-8').splitlines()[1:] if line)
reference = json.loads((OUT / 'differential-receipt.json').read_text(encoding='utf-8'))
for run in reference['runs']:
    if run['name'] == 'independent-heldout':
        assert run['observed_count'] == 33 and run['order_matches']
        expected.update({row[1]: row[2] for row in run['rows']})
assert len(expected) == 73
(OUT / 'mutation-expected-73.json').write_text(json.dumps(expected, indent=2) + '\n', encoding='utf-8')
environment = {key: value for key, value in os.environ.items() if not key.lower().endswith('_proxy')}
environment.update(PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', NO_PROXY='*')
command = ['timeout', '--kill-after=5s', '590s', 'python3', str(OUT / 'guarded-run.py'),
           str(OUT / (phase + '.network.json')), str(SCRATCH), 'verify', '--items', str(items),
           '--registry', 'corpus/SOURCES.md']
started = time.monotonic()
before = hashlib.sha256(SCRATCH.read_bytes()).hexdigest()
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
(OUT / (phase + '.stdout')).write_text(stdout, encoding='utf-8')
(OUT / (phase + '.stderr')).write_text(stderr, encoding='utf-8')
rows = [line.split('\t', 3) for line in stdout.splitlines() if line.startswith('QUOTE_REOPEN\t')]
observed = {row[1]: row[2] for row in rows}
misses = [{'id': item_id, 'expected': verdict, 'actual': observed.get(item_id)}
          for item_id, verdict in expected.items() if observed.get(item_id) != verdict]
input_order = [line.split('\t')[0] for line in combined[1:]]
order_matches = [row[1] for row in rows] == input_order
score = sum(observed.get(item_id) == verdict for item_id, verdict in expected.items())
receipt = {'phase': phase, 'cwd': str(ROOT), 'command': shlex.join(command),
           'cli_exit_code': child.returncode, 'seconds': round(time.monotonic() - started, 3),
           'scratch_sha256_before': before, 'scratch_sha256_after': hashlib.sha256(SCRATCH.read_bytes()).hexdigest(),
           'detector_match': score, 'detector_total': 73, 'order_matches': order_matches,
           'misses': misses, 'stderr': stderr,
           'summary': [line for line in stdout.splitlines() if line.startswith('QUOTE_REOPEN_SUMMARY')],
           'quote_word_counts': dict(sorted(collections.Counter(len(line.split('\t')[2].split()) for line in combined[1:]).items())),
           'items_sha256': hashlib.sha256(items.read_bytes()).hexdigest(),
           'expected_sha256': hashlib.sha256((OUT / 'mutation-expected-73.json').read_bytes()).hexdigest()}
passed = score == 73 and len(rows) == 73 and order_matches and child.returncode == 1
receipt['detector_exit_code'] = 0 if passed else 1
(OUT / (phase + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print('PHASE=' + phase, 'CLI_EXIT=' + str(child.returncode), 'DETECTOR_MATCH=' + str(score) + '/73',
      'DETECTOR_EXIT=' + str(receipt['detector_exit_code']), 'SCRATCH_SHA256=' + before)
print(*receipt['summary'])
print('MISSES=' + json.dumps(misses))
sys.exit(receipt['detector_exit_code'])
