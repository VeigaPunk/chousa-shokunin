#!/usr/bin/env python3
"""Replay frozen fixture generation only to explain mutation sensitivity."""
import collections
import hashlib
import json
from pathlib import Path
import tempfile

SANDBOX = Path('/fast/scratch/hyaku/chousa-r31/MutOracleC2')
ARTIFACTS = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/controls/MutOracleC2')
COUNTER = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round31/c2-count.py')
namespace = {'__name__': 'frozen_fixture_audit', '__file__': str(COUNTER)}
exec(compile(COUNTER.read_bytes(), str(COUNTER), 'exec'), namespace)
campaign = json.loads((ARTIFACTS / 'campaign.json').read_text())
result = {'schema': 'chousa-r31-c2-fixture-subtypes/v1',
          'counter_sha256': hashlib.sha256(COUNTER.read_bytes()).hexdigest(),
          'method': 'Replay unmodified frozen generate(root, seed); classify I1 strings against the actual source digest.',
          'seeds': []}
for seed in campaign['mutation_seeds']:
    with tempfile.TemporaryDirectory(prefix='audit-', dir=SANDBOX / 'tmp') as root:
        claims, truth = namespace['generate'](root, seed)
        counts = collections.Counter()
        invalid = []
        for line in Path(claims).read_text().splitlines():
            record = json.loads(line)
            if truth[record['id']][0] != 'I1_invalid_sha_value':
                continue
            value = record['sha256']
            digest = hashlib.sha256((Path(root) / record['source']).read_bytes()).hexdigest()
            kinds = {'upper': digest.upper(), 'short': digest[:63], 'long': digest + '0',
                     'prefixed': 'sha256:' + digest, 'nonhex': digest[:63] + 'g', 'spaced': ' ' + digest}
            kind = next(key for key, expected in kinds.items() if value == expected)
            counts[kind] += 1
            invalid.append({'id': record['id'], 'kind': kind, 'value': value})
        result['seeds'].append({'seed': seed, 'I1_subtype_counts': dict(counts),
                                'spaced_cases': counts['spaced'], 'invalid_records': invalid})
path = ARTIFACTS / 'fixture-subtypes.json'
path.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps([{'seed': row['seed'], 'I1_subtype_counts': row['I1_subtype_counts'],
                   'spaced_cases': row['spaced_cases']} for row in result['seeds']], indent=2))
