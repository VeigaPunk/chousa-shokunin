#!/usr/bin/env python3
"""Bounded read-only summarizer; exit 2 malformed receipts, 1 stable size key, 0 no stable size key."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
try:
    runs = []
    for i in (1, 2, 3):
        lines = (root / f'run{i}.txt').read_text().splitlines()
        assert lines[-1] == 'LOADER_MATRIX=12/12 MATRIX=PASS'
        rows = [dict(token.split('=', 1) for token in line.split()[1:])
                for line in lines if line.startswith('PROBE ')]
        assert len(rows) == 12 and len({r['case'] for r in rows}) == 12
        assert [r['case'] for r in rows] == [line.split()[1] for line in lines if line.startswith('CASE ')]
        assert all(all(k in r for k in ('SUBJECT', 'TREE', 'SIZES', 'PATHS')) for r in rows)
        runs.append(rows)
    assert len({frozenset(r['case'] for r in rows) for rows in runs}) == 1
    print('SUBJECTS=' + str(len({r['SUBJECT'] for rows in runs for r in rows})))
    print('ORDERS=' + str(len({tuple(r['case'] for r in rows) for rows in runs})))
    stable = []
    for case in sorted(r['case'] for r in runs[0]):
        rows = [next(r for r in run if r['case'] == case) for run in runs]
        nt = len({r['TREE'] for r in rows})
        ns = len({r['SIZES'] for r in rows})
        print(f'{case} distinct_trees={nt}/3 distinct_sizes={ns}/3')
        if ns == 1:
            stable.append(case)
    print('STABLE_SIZE_CLASSES=' + ','.join(stable))
    print('PROBE=' + ('FAIL' if stable else 'PASS'))
    sys.exit(1 if stable else 0)
except (AssertionError, OSError, KeyError, ValueError) as exc:
    print(f'PROBE=ERROR {type(exc).__name__}: {exc}', file=sys.stderr)
    sys.exit(2)
