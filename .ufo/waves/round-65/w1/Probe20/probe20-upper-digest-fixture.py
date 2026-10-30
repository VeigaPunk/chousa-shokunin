#!/usr/bin/env python3
"""Probe20 isolated fixture: upper-digest surface of the round65 receipt format.

Surface under test (one surface only): the SHA256 digest header line
`SHA256=<64 hex> <repo-relative path>` and its binding to the git blob at the
declared revision.

Expected results are derived INDEPENDENTLY from the frozen round65 claims text
(corpus/evidence/round65/claims.md), NOT from the reference implementation:

  - "SHA256 full lowercase 64 hex plus canonical relative POSIX path"
      => uppercase hex, mixed-case hex, 63-hex, 65-hex, non-hex char in the
         digest field => receipt inconsistent => exit 1, FAIL token.
  - "Digest binds the Git blob at the declared revision"
      => well-formed but wrong digest value => exit 1, FAIL token.
  - well-formed receipt with the true blob digest => consistent => exit 0, PASS.

argv/output of the reference tool are preserved verbatim: each invocation is
  python3 <ref> --receipt <file> --root <repo> --revision <rev>
and we record exit code + stdout exactly.

Read-only git only; the one scratch repo is created here and asserted before
every mutation via `git rev-parse --show-toplevel`.
"""
import hashlib, json, os, pathlib, shutil, subprocess, sys

SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe20')
REPO = SCRATCH / 'repo'
RECEIPTS = SCRATCH / 'receipts'
REF = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round65/controls/ref-receipt-pin.py')
TMPDIR = SCRATCH / 'tmpdir'
OUT = SCRATCH / 'results.json'

os.environ['TMPDIR'] = str(TMPDIR)
TMPDIR.mkdir(parents=True, exist_ok=True)
RECEIPTS.mkdir(parents=True, exist_ok=True)

def git(*args, cwd=None):
    return subprocess.run(['git', '-C', str(cwd or REPO), *args], capture_output=True, text=True)

def assert_toplevel():
    q = git('rev-parse', '--show-toplevel')
    top = q.stdout.strip()
    assert q.returncode == 0 and top == str(REPO), f'toplevel assertion failed: {top!r}'

# --- build scratch repo (one blob) -----------------------------------------
if REPO.exists():
    shutil.rmtree(REPO)
REPO.mkdir()
git('init', '-q', cwd=REPO)
assert_toplevel()
assert_toplevel()
content = b'probe20 upper-digest payload\nsecond line\n'
(REPO / 'probe.txt').write_bytes(content)
git('add', 'probe.txt'); assert_toplevel()
git('-c', 'user.name=Probe20', '-c', 'user.email=probe20@fixture.local',
    'commit', '-q', '-m', 'probe20 fixture blob'); assert_toplevel()
rev = git('rev-parse', 'HEAD').stdout.strip()
assert len(rev) == 40 and all(c in '0123456789abcdef' for c in rev), rev

blob = subprocess.run(['git', '-C', str(REPO), 'cat-file', 'blob', rev + ':probe.txt'],
                      capture_output=True)
assert blob.returncode == 0
digest = hashlib.sha256(blob.stdout).hexdigest()
assert len(digest) == 64

# --- receipts: one surface, digest-header edges -----------------------------
BODY = 'probe body line\n'
def receipt(d, note):
    return f'REVISION={rev}\nEXIT=0\nSHA256={d} probe.txt\n\n{BODY}'

upper = digest.upper()
mixed = ''.join(c.upper() if i % 2 else c for i, c in enumerate(digest))
short63 = digest[:63]
long65 = digest + '0'
nonhex = digest[:20] + 'g' + digest[21:]
# wrong but well-formed value: flip last hex digit to a different valid hex digit
last = digest[-1]
wrong = digest[:-1] + ('0' if last != '0' else '1')
assert wrong != digest and all(c in '0123456789abcdef' for c in wrong)

cases = [
    # name, receipt text, independently derived (exit, stdout)
    ('control-valid', receipt(digest, 'valid'),
     (0, 'RECEIPT_PIN=PASS')),
    ('upper-digest-hex', receipt(upper, 'upper'),
     (1, 'RECEIPT_PIN=FAIL digest header')),
    ('mixed-digest-hex', receipt(mixed, 'mixed'),
     (1, 'RECEIPT_PIN=FAIL digest header')),
    ('digest-63-hex', receipt(short63, 'short'),
     (1, 'RECEIPT_PIN=FAIL digest header')),
    ('digest-65-hex', receipt(long65, 'long'),
     (1, 'RECEIPT_PIN=FAIL digest header')),
    ('digest-nonhex', receipt(nonhex, 'nonhex'),
     (1, 'RECEIPT_PIN=FAIL digest header')),
    ('digest-wrong-value', receipt(wrong, 'wrong'),
     (1, 'RECEIPT_PIN=FAIL blob/digest')),
]

results = []
ok_all = True
for name, text, (xexit, xout) in cases:
    f = RECEIPTS / f'{name}.receipt'
    f.write_text(text, encoding='utf-8')
    q = subprocess.run(['python3', str(REF), '--receipt', str(f),
                        '--root', str(REPO), '--revision', rev],
                       capture_output=True, text=True, env=os.environ.copy())
    got = (q.returncode, q.stdout.strip())
    exp = (xexit, xout)
    match = got == exp
    ok_all &= match
    results.append({'case': name, 'expected_exit': xexit, 'expected_stdout': xout,
                    'actual_exit': q.returncode, 'actual_stdout': q.stdout.strip(),
                    'match': match})

OUT.write_text(json.dumps({
    'freeze': 'f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd',
    'surface': 'upper-digest: SHA256 header field edges + blob binding',
    'reference': str(REF),
    'argv_preserved': '--receipt <file> --root <repo> --revision <rev>',
    'revision': rev,
    'digest': digest,
    'results': results,
    'all_match': ok_all,
}, indent=2))

for r in results:
    print(('PASS ' if r['match'] else 'MISMATCH ') + r['case'],
          f"exit={r['actual_exit']} stdout={r['actual_stdout']!r}")
print('ALL_MATCH=' + str(ok_all))
sys.exit(0 if ok_all else 1)
