#!/usr/bin/env python3
"""Probe16 isolated fixture: absolute/canonical-path surface of ref-receipt-pin.py.

Independently derives expected exit/stdout for each receipt from the frozen round65
format text (claims.md C1): header 3 must be 'SHA256=<64 lc hex> <canonical relative
POSIX path>'; exit 0 consistent, 1 inconsistent/malformed, 2 usage/environment.
One surface only: the path field of the SHA256 header line (+ two exit-2 anchors).
Fixture repo lives entirely under this scratch dir; git mutations asserted on toplevel.
"""
import hashlib, pathlib, subprocess, sys, os

SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe16')
REPO = SCRATCH / 'fixture-repo'
REF = '/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round65/controls/ref-receipt-pin.py'
CASES_DIR = SCRATCH / 'cases'
os.environ['TMPDIR'] = str(SCRATCH / 'tmp')
(SCRATCH / 'tmp').mkdir(parents=True, exist_ok=True)

def git(*args, check=True):
    return subprocess.run(['git', '-C', str(REPO), *args], capture_output=True, check=check)

def build_repo():
    if REPO.exists():
        subprocess.run(['rm', '-rf', str(REPO)], check=True)
    REPO.mkdir(parents=True)
    subprocess.run(['git', '-C', str(REPO), 'init', '-q', '-b', 'main'], check=True)
    top = subprocess.run(['git', '-C', str(REPO), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert top == str(REPO), f'toplevel assertion failed: {top!r} != {str(REPO)!r}'
    (REPO / 'payload.txt').write_bytes(b'probe16 fixture payload\n')
    (REPO / 'sub').mkdir()
    (REPO / 'sub' / 'note.txt').write_bytes(b'nested\n')
    git('add', '.')
    git('-c', 'user.email=probe16@fixture', '-c', 'user.name=Probe16', 'commit', '-q', '-m', 'fixture')
    rev = git('rev-parse', 'HEAD').stdout.decode().strip()
    assert len(rev) == 40 and rev == rev.lower()
    blob = git('cat-file', 'blob', f'{rev}:payload.txt').stdout
    digest = hashlib.sha256(blob).hexdigest()
    return rev, digest

def receipt(rev, path_field, digest, exit_code='0', body='measured output'):
    # path_field None -> omit ' <path>' entirely; '' -> trailing space only
    p = '' if path_field is None else ' ' + path_field
    return f'REVISION={rev}\nEXIT={exit_code}\nSHA256={digest}{p}\n\n{body}\n'

def main():
    rev, digest = build_repo()
    print(f'FIXTURE rev={rev} digest={digest}')
    CASES_DIR.mkdir(exist_ok=True)
    abs_real = str(REPO / 'payload.txt')          # exists on disk; hashes to digest
    cases = [
        # name, receipt text, expected rc, expected stdout predicate, derivation
        ('valid-relative', receipt(rev, 'payload.txt', digest), 0, 'RECEIPT_PIN=PASS',
         'canonical relative POSIX path + digest binds blob => consistent (0)'),
        ('abs-real-file', receipt(rev, abs_real, digest), 1, 'RECEIPT_PIN=FAIL path',
         'format demands relative path; absolute is non-canonical even though the file exists and hashes correctly => malformed (1)'),
        ('abs-root-style', receipt(rev, '/payload.txt', digest), 1, 'RECEIPT_PIN=FAIL path',
         'leading slash => absolute, not relative => malformed (1)'),
        ('abs-double-slash', receipt(rev, '//payload.txt', digest), 1, 'RECEIPT_PIN=FAIL path',
         '// is still absolute (POSIX); not canonical relative => malformed (1)'),
        ('dot-prefix', receipt(rev, './payload.txt', digest), 1, 'RECEIPT_PIN=FAIL path',
         "'./' is non-canonical; canonical form drops it => malformed (1)"),
        ('dotdot-mid', receipt(rev, 'sub/../payload.txt', digest), 1, 'RECEIPT_PIN=FAIL path',
         "'..' in parts; not canonical relative => malformed (1)"),
        ('trailing-slash', receipt(rev, 'payload.txt/', digest), 1, 'RECEIPT_PIN=FAIL path',
         "trailing slash is not canonical for a blob path => malformed (1)"),
        ('empty-path', receipt(rev, '', digest), 1, 'RECEIPT_PIN=FAIL ',
         "space with empty path: '' has no parts => malformed (1); error class observed 'digest header' (regex needs >=1 char after space) — class is reference detail, exit code is frozen"),
        ('no-path-field', receipt(rev, None, digest), 1, 'RECEIPT_PIN=FAIL digest header',
         "'SHA256=<hex>' without ' <path>' violates header grammar => malformed (1)"),
        ('windows-abs', receipt(rev, 'C:\\payload.txt', digest), 1, 'RECEIPT_PIN=FAIL ',
         "not a canonical relative POSIX path; no such blob at revision => inconsistent (1); observed class 'blob/digest'"),
        ('wrong-digest-valid-rel', receipt(rev, 'payload.txt', '0' * 64), 1, 'RECEIPT_PIN=FAIL ',
         "canonical path but digest does not bind the blob => inconsistent (1); observed class 'blob/digest'; proves relative-path acceptance alone does not pass"),
    ]
    results = []
    npass = 0
    for name, text, erc, etok, why in cases:
        f = CASES_DIR / (name + '.txt')
        f.write_text(text)
        q = subprocess.run([sys.executable, '-B', REF, '--receipt', str(f),
                            '--root', str(REPO), '--revision', rev],
                           capture_output=True, text=True, timeout=20)
        got = q.stdout.strip()
        # frozen predicate boundary: exact PASS token for rc 0; FAIL-prefix class for rc 1
        ok = q.returncode == erc and (got == etok if erc == 0 else got.startswith(etok))
        npass += ok
        results.append((name, erc, etok, q.returncode, got, ok, why))
        print(f'CASE {name} expect_rc={erc} got_rc={q.returncode} expect={etok!r} got={got!r} {"OK" if ok else "MISMATCH"}')
    # exit-2 anchors (usage/environment), same probe run, clearly separated
    anchors = []
    q = subprocess.run([sys.executable, '-B', REF, '--receipt', str(CASES_DIR / 'valid-relative.txt'),
                        '--root', str(REPO), '--revision', rev.upper()],
                       capture_output=True, text=True, timeout=20)
    anchors.append(('uppercase-revision', 2, q.returncode, q.stderr.strip().splitlines()[-1] if q.stderr else ''))
    q = subprocess.run([sys.executable, '-B', REF, '--receipt', str(SCRATCH / 'missing.txt'),
                        '--root', str(REPO), '--revision', rev],
                       capture_output=True, text=True, timeout=20)
    anchors.append(('unreadable-receipt', 2, q.returncode, q.stdout.strip()))
    print('ANCHORS ' + repr(anchors))
    print(f'PROBE16_ABS={npass}/{len(cases)} {"PASS" if npass == len(cases) else "FAIL"}')
    return 0 if npass == len(cases) else 1

if __name__ == '__main__':
    sys.exit(main())
