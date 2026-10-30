#!/usr/bin/env python3
"""Probe15 isolated fixture: receipt-pin traversal surface.

Builds receipts exercising the frozen format's path-canonicality rules and
runs the round65 reference tool against a scratch git repo. Expected results
are derived independently from corpus/evidence/round65/claims.md (C1 frozen
format + exit-code contract), NOT copied from the reference implementation.
Writes receipts to out/<case>.receipt and results to results.jsonl.
"""
import json, os, pathlib, subprocess, sys

SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe15')
REPO = SCRATCH / 'repo'
REF = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round65/controls/ref-receipt-pin.py')
OUT = SCRATCH / 'out'
OUT.mkdir(exist_ok=True)

REV = subprocess.run(['git', '-C', str(REPO), 'rev-parse', 'HEAD'],
                     capture_output=True, text=True, check=True).stdout.strip()
GOOD_SHA = subprocess.run(['git', '-C', str(REPO), 'cat-file', 'blob', f'{REV}:file.txt'],
                          capture_output=True, check=True).stdout
import hashlib
GOOD_DIGEST = hashlib.sha256(GOOD_SHA).hexdigest()

HEADER = [f'REVISION={REV}', 'EXIT=0', f'SHA256={GOOD_DIGEST} file.txt', '', 'ran ok']

def receipt(lines):
    return '\n'.join(lines) + '\n'

CASES = {
    # traversal / canonical-path probes (the assigned surface)
    't01-valid':               receipt(HEADER),
    't02-absolute-path':       receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} /etc/passwd', '', 'x']),
    't03-dotdot-lead':         receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} ../escape.txt', '', 'x']),
    't04-dotdot-mid':          receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} sub/../../file.txt', '', 'x']),
    't05-dot-prefix':          receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} ./file.txt', '', 'x']),
    't06-double-slash':        receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} a//file.txt', '', 'x']),
    't07-dot-only':            receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} .', '', 'x']),
    't08-trailing-slash':      receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} file.txt/', '', 'x']),
    't09-dotdot-only':         receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} ..', '', 'x']),
    't10-nul-lookalike':       receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} file.txt\x00.txt', '', 'x']),
    # consistency probes adjacent to the surface
    't11-revision-mismatch':   receipt([f'REVISION={'f'*40}', 'EXIT=0', f'SHA256={GOOD_DIGEST} file.txt', '', 'x']),
    't12-digest-mismatch':     receipt([HEADER[0], HEADER[1], f'SHA256={'0'*64} file.txt', '', 'x']),
    't13-exit-256':            receipt([HEADER[0], 'EXIT=256', HEADER[2], '', 'x']),
    't14-no-blank-separator':  receipt([HEADER[0], HEADER[1], HEADER[2], 'x']),
    't15-empty-body':          receipt([HEADER[0], HEADER[1], HEADER[2], '', '   ']),
    't16-swapped-headers':     receipt(['EXIT=0', HEADER[0], HEADER[2], '', 'x']),
    't17-duplicate-header':    receipt([HEADER[0], HEADER[0], HEADER[1], HEADER[2], '', 'x']),
    't18-missing-blob-path':   receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} nope.txt', '', 'x']),
    't19-tree-as-path':        receipt([HEADER[0], HEADER[1], f'SHA256={GOOD_DIGEST} .git', '', 'x']),
    't20-short-revision':      receipt([f'REVISION={REV[:39]}', 'EXIT=0', HEADER[2], '', 'x']),
}

# Expected outcomes derived independently from claims.md frozen format:
#  - REVISION must equal --revision (full lowercase 40 hex)
#  - EXIT decimal 0..255
#  - SHA256 64 lowercase hex + canonical relative POSIX path (no absolute, no '..',
#    no non-canonical spelling), digest binds blob at the declared revision
#  - blank separator, nonempty output
#  - 0 consistent, 1 invalid/malformed, 2 usage/environment
EXPECTED = {
    't01-valid':                 ('t01-valid', 0),
    't02-absolute-path':         ('t02-absolute-path', 1),
    't03-dotdot-lead':           ('t03-dotdot-lead', 1),
    't04-dotdot-mid':            ('t04-dotdot-mid', 1),
    't05-dot-prefix':            ('t05-dot-prefix', 1),   # str(rel) != spelling -> non-canonical
    't06-double-slash':          ('t06-double-slash', 1),
    't07-dot-only':              ('t07-dot-only', 1),     # empty parts after normalization
    't08-trailing-slash':        ('t08-trailing-slash', 1),
    't09-dotdot-only':           ('t09-dotdot-only', 1),
    't10-nul-lookalike':         ('t10-nul-lookalike', 1),  # git refuses such pathspec -> blob lookup fails
    't11-revision-mismatch':     ('t11-revision-mismatch', 1),
    't12-digest-mismatch':       ('t12-digest-mismatch', 1),
    't13-exit-256':              ('t13-exit-256', 1),
    't14-no-blank-separator':    ('t14-no-blank-separator', 1),
    't15-empty-body':            ('t15-empty-body', 1),
    't16-swapped-headers':       ('t16-swapped-headers', 1),
    't17-duplicate-header':      ('t17-duplicate-header', 1),
    't18-missing-blob-path':     ('t18-missing-blob-path', 1),
    't19-tree-as-path':          ('t19-tree-as-path', 1),
    't20-short-revision':        ('t20-short-revision', 1),
}

results = []
for name, body in CASES.items():
    rp = OUT / f'{name}.receipt'
    rp.write_text(body, encoding='utf-8')
    argv = ['python3', str(REF), '--receipt', str(rp), '--root', str(REPO), '--revision', REV]
    q = subprocess.run(argv, capture_output=True, text=True)
    results.append({'case': name, 'argv': argv, 'exit': q.returncode,
                    'stdout': q.stdout.strip(), 'stderr': q.stderr.strip()})

# usage/environment probes (exit 2 contract)
usage = [
    ('u01-missing-revision', ['python3', str(REF), '--receipt', str(OUT/'t01-valid.receipt'), '--root', str(REPO)]),
    ('u02-uppercase-revision', ['python3', str(REF), '--receipt', str(OUT/'t01-valid.receipt'), '--root', str(REPO), '--revision', REV.upper()]),
    ('u03-bogus-revision', ['python3', str(REF), '--receipt', str(OUT/'t01-valid.receipt'), '--root', str(REPO), '--revision', 'zz'*20]),
]
for name, argv in usage:
    q = subprocess.run(argv, capture_output=True, text=True)
    results.append({'case': name, 'argv': argv, 'exit': q.returncode,
                    'stdout': q.stdout.strip(), 'stderr': q.stderr.strip().splitlines()[-1] if q.stderr.strip() else ''})
EXPECTED['u01-missing-revision'] = ('u01-missing-revision', 2)
EXPECTED['u02-uppercase-revision'] = ('u02-uppercase-revision', 2)
EXPECTED['u03-bogus-revision'] = ('u03-bogus-revision', 2)

mismatches = []
for r in results:
    exp = EXPECTED[r['case']][1]
    ok = r['exit'] == exp
    if not ok:
        mismatches.append({'case': r['case'], 'expected': exp, 'actual': r['exit']})

(SCRATCH / 'results.jsonl').write_text('\n'.join(json.dumps(r) for r in results) + '\n')
print(f'REVISION={REV}')
print(f'cases={len(results)} mismatches={len(mismatches)}')
for m in mismatches:
    print('MISMATCH', json.dumps(m))
sys.exit(0 if not mismatches else 1)
