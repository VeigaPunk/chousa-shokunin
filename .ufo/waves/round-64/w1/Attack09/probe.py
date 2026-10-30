#!/usr/bin/env python3
"""Seat-local A01-A03 probes: no git mutations, no full selftest/runner."""
import concurrent.futures
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
OUT = LANE / '.ufo/waves/round-64/w1/Attack09'
SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack09')
REV = 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1'
PATHS = ['corpus/evidence/round64/claims.md', 'corpus/evidence/round64/gen-audit-mutants.py', 'corpus/evidence/round64/c2-mutrun.py', 'tools/claims-audit.py', 'tools/claims-audit-v2.py', 'corpus/evidence/round63/audit-probe.py']

def frozen(path):
    p = subprocess.run(['git', '-C', str(LANE), 'show', REV + ':' + path], capture_output=True, timeout=20)
    if p.returncode:
        raise RuntimeError(p.stderr.decode())
    return p.stdout

def main():
    if SCRATCH.exists():
        raise RuntimeError('scratch already exists; refusing overwrite')
    SCRATCH.mkdir(parents=True)
    result = {'python': sys.version, 'revision': REV, 'axes': ['calibration', 'instrument provenance', 'consumer operability'], 'bytes': [], 'probes': []}
    try:
        blobs = {p: frozen(p) for p in PATHS}
        for path, blob in blobs.items():
            current = (LANE / path).read_bytes()
            result['bytes'].append({'path': path, 'sha256_frozen': hashlib.sha256(blob).hexdigest(), 'sha256_current': hashlib.sha256(current).hexdigest(), 'identical': blob == current})
        namespace = {'__name__': 'seat_frozen_generator'}
        exec(compile(blobs[PATHS[1]], PATHS[1], 'exec'), namespace)
        jobs = []
        for target in ['tools/claims-audit.py', 'tools/claims-audit-v2.py']:
            source = blobs[target].decode()
            for mid in ['baseline', 'A01', 'A02', 'A03']:
                d = SCRATCH / (pathlib.Path(target).stem + '-' + mid)
                d.mkdir()
                text = source
                anchor_count = None
                if mid != 'baseline':
                    _, _, old, new, count = next(m for m in namespace['MUTANTS'] if m[0] == mid)
                    anchor_count = text.count(old)
                    assert anchor_count == count
                    text = text.replace(old, new)
                checker = d / 'checker.py'
                checker.write_text(text)
                claims = 'claimed `MISSING`.\n' if mid == 'A03' else 'unrelated text.\n'
                (d / 'claims.md').write_text(claims)
                (d / 'target.md').write_text('present\n')
                (d / 'audit.tsv').write_text('R\tverbatim-heading\tclaimed\ttarget.md\t\tseat minimal\n')
                cmd = [sys.executable, '-B', str(checker), '--claims', str(d / 'claims.md'), '--audit', str(d / 'audit.tsv'), '--root', str(d)]
                jobs.append((target, mid, anchor_count, cmd, d))
            # A03's honest comparator uses its identical fixture.
            d = SCRATCH / (pathlib.Path(target).stem + '-baseline-flag')
            d.mkdir()
            (d / 'checker.py').write_text(source)
            (d / 'claims.md').write_text('claimed `MISSING`.\n')
            (d / 'target.md').write_text('present\n')
            (d / 'audit.tsv').write_text('R\tverbatim-heading\tclaimed\ttarget.md\t\tseat minimal\n')
            cmd = [sys.executable, '-B', str(d / 'checker.py'), '--claims', str(d / 'claims.md'), '--audit', str(d / 'audit.tsv'), '--root', str(d)]
            jobs.append((target, 'baseline-flag', None, cmd, d))
        def run(job):
            target, mid, anchor_count, cmd, d = job
            p = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=15)
            return {'target': target, 'mutant': mid, 'anchor_count': anchor_count, 'command': cmd, 'cwd': str(d), 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            result['probes'] = list(pool.map(run, jobs))
    finally:
        shutil.rmtree(SCRATCH)
        result['scratch_removed'] = not SCRATCH.exists()
        (OUT / 'evidence.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
