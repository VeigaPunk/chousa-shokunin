#!/usr/bin/env python3
"""Read two local registries; print exact ID and source-cell URL intersections."""
import collections
import hashlib
import json
import platform
import re
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md')
PACKAGE = Path('/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md')
ROW = re.compile(r'^ {0,3}\|\s*(S[0-9]{3,})\s*\|')
URL = re.compile(r'https?://[^\s<>`]+')

def extract(path):
    data = path.read_bytes()
    rows = []
    for number, line in enumerate(data.decode('utf-8').splitlines(), 1):
        match = ROW.match(line)
        if match:
            cells = re.split(r'(?<!\\)\|', line)
            source = cells[2].strip()
            urls = sorted(set(u.rstrip('.,;)') for u in URL.findall(source)))
            rows.append({'id': match[1], 'line': number, 'source': source, 'urls': urls})
    ids = [r['id'] for r in rows]
    urls = collections.defaultdict(list)
    for row in rows:
        for url in row['urls']:
            urls[url].append(row['id'])
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(),
            'rows': rows, 'row_count': len(rows), 'ids': sorted(set(ids)),
            'duplicate_ids': sorted(k for k, v in collections.Counter(ids).items() if v > 1),
            'urls': dict(sorted(urls.items()))}

a, b = extract(LANE), extract(PACKAGE)
ids = sorted(set(a['ids']) & set(b['ids']))
urls = sorted(set(a['urls']) & set(b['urls']))
base_a = {u.split('#', 1)[0] for u in a['urls']}
base_b = {u.split('#', 1)[0] for u in b['urls']}
result = {'python': platform.python_version(),
          'method': '0-3 ASCII spaces then pipe, first-cell S[0-9]{3,}; URLs only in source cell; exact case-sensitive strings, trim terminal . , ; ); fragment-free intersection separately; no fetch or URL canonicalization',
          'lane': a, 'package': b,
          'id_collisions': ids, 'id_collision_count': len(ids),
          'url_collisions': [{'url': u, 'lane_ids': a['urls'][u], 'package_ids': b['urls'][u]} for u in urls],
          'url_collision_count': len(urls),
          'fragment_free_url_collisions': sorted(base_a & base_b),
          'fragment_free_url_collision_count': len(base_a & base_b),
          'package_noncolliding_ids': sorted(set(b['ids']) - set(a['ids']))}
print(json.dumps(result, ensure_ascii=False, indent=2))
