#!/usr/bin/env python3
"""Probe05 isolated wrong-revision fixture driver (round65).
Builds receipts whose REVISION header conflicts with the caller-supplied
--revision in several directions, runs the reference validator, and records
argv/exit/stdout/stderr per fixture. Derives expectations independently from
the frozen format contract (claims.md): revision must equal caller-supplied
--revision; mismatch => invalid => exit 1 (2 is usage/environment only).
"""
import hashlib, json, pathlib, subprocess, sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
REF = LANE / 'corpus/evidence/round65/controls/ref-receipt-pin.py'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'
FREEZE = 'f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd'
SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe05')
FIX = SCRATCH / 'fixtures'
FIX.mkdir(parents=True, exist_ok=True)

def blob_sha(rev, path):
    q = subprocess.run(['git', '-C', str(LANE), 'cat-file', 'blob', f'{rev}:{path}'],
                       capture_output=True, check=True)
    return hashlib.sha256(q.stdout).hexdigest()

h_base = blob_sha(BASE, 'SKILL.md')
h_freeze = blob_sha(FREEZE, 'SKILL.md')

def receipt(rev, exit_code, digest, path, body='measured output'):
    return f'REVISION={rev}\nEXIT={exit_code}\nSHA256={digest} {path}\n\n{body}\n'

FIXTURES = [
    # name, receipt text, caller-supplied --revision, expected exit, why (independent derivation)
    ('valid-control', receipt(BASE, 0, h_base, 'SKILL.md'), BASE, 0,
     'format contract satisfied; revision == --revision; digest binds blob at declared revision => consistent => 0'),
    ('wrong-rev-zeros', receipt('0' * 40, 0, h_base, 'SKILL.md'), BASE, 1,
     'declared revision (well-formed 40 hex) != caller --revision => invalid => 1'),
    ('wrong-rev-other-commit', receipt(FREEZE, 0, h_freeze, 'SKILL.md'), BASE, 1,
     'receipt internally consistent at FREEZE but header revision != caller --revision => invalid => 1'),
    ('wrong-rev-caller-side', receipt(BASE, 0, h_base, 'SKILL.md'), '0' * 40, 1,
     'valid receipt but caller-supplied --revision disagrees; contract binds revision to caller value => 1'),
    ('wrong-rev-uppercase', receipt(BASE.upper(), 0, h_base, 'SKILL.md'), BASE, 1,
     'format demands lowercase 40 hex; uppercase header != lowercase --revision (and violates format) => 1'),
]

results = []
for name, text, caller_rev, exp_rc, why in FIXTURES:
    f = FIX / f'{name}.txt'
    f.write_text(text)
    argv = [sys.executable, '-B', str(REF), '--receipt', str(f),
            '--root', str(LANE), '--revision', caller_rev]
    q = subprocess.run(argv, capture_output=True, text=True, timeout=20,
                       env={'PATH': '/usr/bin:/bin', 'TMPDIR': str(SCRATCH / 'tmp'),
                            'LANG': 'C.UTF-8'})
    results.append({
        'fixture': name, 'argv': argv, 'expected_exit': exp_rc,
        'actual_exit': q.returncode, 'stdout': q.stdout, 'stderr': q.stderr,
        'exit_match': q.returncode == exp_rc, 'derivation': why,
    })
    print(f'{name}: expected={exp_rc} actual={q.returncode} '
          f'{"OK" if q.returncode == exp_rc else "MISMATCH"} out={q.stdout.strip()!r}')

(SCRATCH / 'results.json').write_text(json.dumps(results, indent=1))
all_ok = all(r['exit_match'] for r in results)
# Token shape per frozen counter contract: rc==0 -> exactly RECEIPT_PIN=PASS; rc!=0 -> RECEIPT_PIN=FAIL prefix
tok_ok = all((r['stdout'].strip() == 'RECEIPT_PIN=PASS') if r['expected_exit'] == 0
             else r['stdout'].startswith('RECEIPT_PIN=FAIL ') for r in results)
print(f'PROBE05_WRONG_REVISION exits_all_match={all_ok} tokens_ok={tok_ok}')
sys.exit(0 if (all_ok and tok_ok) else 1)
