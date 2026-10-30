#!/usr/bin/env python3
"""Seat-local, read-only C2 A04/A05/A06 probes; never creates git repositories."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/chousa-r64/Attack10')
OUT = LANE / '.ufo/waves/round-64/w1/Attack10'
FREEZE = 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

def command(argv, cwd=LANE):
    p = subprocess.run(argv, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=30)
    return {'command': argv, 'cwd': str(cwd), 'exit': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}

def main():
    if SCRATCH.exists():
        raise RuntimeError('scratch already exists; refusing to overwrite')
    SCRATCH.mkdir(parents=True)
    evidence = {'axes': ['frozen-byte fidelity', 'mutation discrimination', 'zero production mutation'],
                'python': sys.version, 'tools_installed': [], 'byte_checks': [], 'runs': []}
    try:
        paths = ['corpus/evidence/round64/claims.md', 'corpus/evidence/round64/gen-audit-mutants.py',
                 'corpus/evidence/round64/c2-mutrun.py', 'tools/claims-audit.py', 'tools/claims-audit-v2.py']
        for rel in paths:
            p = subprocess.run(['git', '-C', str(LANE), 'show', FREEZE + ':' + rel],
                               capture_output=True, timeout=30)
            current = (LANE / rel).read_bytes()
            evidence['byte_checks'].append({'path': rel, 'git_show_exit': p.returncode,
                'freeze_sha256': hashlib.sha256(p.stdout).hexdigest(),
                'current_sha256': hashlib.sha256(current).hexdigest(),
                'equal': p.returncode == 0 and current == p.stdout})
        if not all(x['equal'] for x in evidence['byte_checks']):
            raise RuntimeError('frozen/current byte mismatch')
        spec = importlib.util.spec_from_file_location('seat_gen', LANE / paths[1])
        gen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen)
        fixtures = {
            'A04': ('count says 1 seats.\n', 'R\tjson-count\tcount says\tspec.json:items\t\tdetection counter\n',
                    {'spec.json': '{"items":[1,2]}\n'}),
            'A05': ('heading is `planned`\n', 'R\tverbatim-heading\theading is\tS.md\t\tcase-only\n',
                    {'S.md': '## Planned\n'}),
            'A06': ('count says v2 seats.\n', 'R\tjson-count\tcount says\tspec.json:items\t\tword digit\n',
                    {'spec.json': '{"items":[1,2]}\n'}),
        }
        roots = {}
        for mid, (claims, audit, files) in fixtures.items():
            d = SCRATCH / ('fixture-' + mid)
            d.mkdir()
            (d / 'claims.md').write_text(claims)
            (d / 'audit.tsv').write_text(audit)
            for f, text in files.items():
                (d / f).write_text(text)
            roots[mid] = d
        targets = {}
        for name in ('claims-audit.py', 'claims-audit-v2.py'):
            src = LANE / 'tools' / name
            targets[(name, 'baseline')] = src
            for mid in fixtures:
                dst = SCRATCH / (name + '-' + mid + '.py')
                gen.apply_mutant(src, dst, mid)
                targets[(name, mid)] = dst
        jobs = []
        for (name, variant), target in targets.items():
            for fid, root in roots.items():
                argv = [sys.executable, '-B', str(target), '--claims', str(root / 'claims.md'),
                        '--audit', str(root / 'audit.tsv'), '--root', str(root)]
                jobs.append((name, variant, 'minimal-' + fid, argv, root))
            for lid, claim, audit in [
                ('R2', 'round62/claims.md', 'audit-r62.tsv'),
                ('R3', 'round63/claims.md', 'audit-r63.tsv'),
                ('R4', 'round63/claims-a2.md', 'audit-a2.tsv')]:
                argv = [sys.executable, '-B', str(target), '--claims', str(LANE / 'corpus/evidence' / claim),
                        '--audit', str(LANE / 'corpus/evidence/round63/audit' / audit), '--root', str(LANE)]
                jobs.append((name, variant, lid, argv, SCRATCH))
        def execute(job):
            name, variant, leg, argv, cwd = job
            return dict(target=name, variant=variant, leg=leg, **command(argv, cwd))
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            evidence['runs'] = list(pool.map(execute, jobs))
        for name in ('claims-audit.py', 'claims-audit-v2.py'):
            for mid in fixtures:
                base = next(r for r in evidence['runs'] if r['target'] == name and r['variant'] == 'baseline' and r['leg'] == 'minimal-' + mid)
                mutant = next(r for r in evidence['runs'] if r['target'] == name and r['variant'] == mid and r['leg'] == 'minimal-' + mid)
                print(name, mid, 'baseline', base['exit'], base['stdout'].strip().replace('\n', ' | '),
                      'mutant', mutant['exit'], mutant['stdout'].strip().replace('\n', ' | '))
        for r in evidence['runs']:
            if r['leg'] in ('R2', 'R3', 'R4'):
                print(r['target'], r['variant'], r['leg'], 'exit=' + str(r['exit']), r['stdout'].strip().splitlines()[-1])
        return 0
    finally:
        shutil.rmtree(SCRATCH)
        evidence['scratch_removed'] = not SCRATCH.exists()
        (OUT / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')

if __name__ == '__main__':
    sys.exit(main())
