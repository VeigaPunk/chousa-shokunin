#!/usr/bin/env python3
"""Copy already existing independent page snapshots; never fetch or read labels."""
import hashlib
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
HERE = Path(__file__).resolve().parent
SOURCE = Path('/fast/scratch/hyaku/chousa-r29/w1/CriticRuntimeVariants/cache')
manifest = json.loads((LANE / '.ufo/waves/round-29/build/CriticRuntimeVariants/fetch-manifest.json').read_text())
cache = {}
provenance = []
for row in manifest:
    original = SOURCE / (row['source_id'] + '.independent.txt')
    body = original.read_text(encoding='utf-8')
    url = row['url'].split('#', 1)[0]
    cache[url] = body
    provenance.append({'url': url, 'original': str(original), 'bytes': len(body.encode()), 'sha256': hashlib.sha256(body.encode()).hexdigest(), 'mtime_ns': original.stat().st_mtime_ns})
(HERE / 'snapshots.json').write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
(HERE / 'snapshot-provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
print('SNAPSHOTS_COPIED=' + str(len(cache)))
print('CANDIDATE_PREPARATION_GETS=0')
print('SNAPSHOT_SHA256=' + hashlib.sha256((HERE / 'snapshots.json').read_bytes()).hexdigest())
