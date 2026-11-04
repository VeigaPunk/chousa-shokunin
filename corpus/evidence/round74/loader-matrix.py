#!/usr/bin/env python3
"""Nine independently expected public-CLI cases, each using real Git commits.
Only disposable fixture repositories are written. No network. Exit 0: 9/9,
1: mismatch, 2: setup. --work is required and contains temporary directories.
"""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile

PATHS = ('LOG.md', 'corpus/lessons/round-72.md', 'SCORECARD.md')
RECEIPTS = ('corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt',
            'corpus/evidence/round72/controls/after-r72-corrections.txt')
FILES = {
    PATHS[0]: '# Log\nremovable sentinel\n## Round 72 correction entry\n8426 is exempt; 8435 exits.\n',
    PATHS[1]: '# Lesson\nremovable sentinel\n## Correction — round-72 spot-check\nV72-1 8426 8435. V72-2 measured at the landing tip 7f7ea19a; three at the verdicts tree 6dd6c82; two recorded.\n',
    PATHS[2]: '# Scorecard\nremovable sentinel\n## Round 72 correction note\nV72-1 and V72-2.\n',
    RECEIPTS[0]: 'historical battery\n', RECEIPTS[1]: 'historical counts\n',
}
CASES = [('unchanged', None, 'same', 0, None)]
CASES += [(f'append-{i}', path, 'append', 0, None) for i, path in enumerate(PATHS)]
CASES += [(f'delete-{i}', path, 'delete', 1, 'C2-6') for i, path in enumerate(PATHS)]
CASES += [('replace-equal', PATHS[0], 'replace', 1, 'C2-6'),
          ('receipt-change', RECEIPTS[0], 'append', 1, 'C2-7')]

def git(root, *args):
    p = subprocess.run(['git', '-C', str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()

def run(counter, work):
    passed = 0
    print('COUNTER_SHA256=' + hashlib.sha256(counter.read_bytes()).hexdigest())
    with tempfile.TemporaryDirectory(prefix='loader-matrix-', dir=work) as tmp:
        root = Path(tmp)
        git(root, 'init', '-q')
        if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root.resolve():
            raise RuntimeError('fixture root mismatch')
        for path, text in FILES.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        git(root, 'add', '--', *FILES)
        git(root, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid', 'commit', '-qm', 'base')
        base = git(root, 'rev-parse', 'HEAD')
        for name, path, operation, expected_rc, expected_id in CASES:
            # Restore fixture bytes, not the caller's working tree or index.
            for key, value in FILES.items():
                (root / key).write_text(value)
            if path:
                text = FILES[path]
                if operation == 'append':
                    text += '\nadditional evidence\n'
                elif operation == 'delete':
                    text = text.replace('removable sentinel\n', '')
                elif operation == 'replace':
                    text = text.replace('removable sentinel', 'replacement sentinel')
                (root / path).write_text(text)
            git(root, 'add', '--', *FILES)
            git(root, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid', 'commit', '--allow-empty', '-qm', name)
            rev = git(root, 'rev-parse', 'HEAD')
            p = subprocess.run([sys.executable, '-B', str(counter), '--lane', str(root), '--base', base, '--rev', rev], text=True, capture_output=True)
            checks = {line.split()[1]: line.split()[2] for line in p.stdout.splitlines() if line.startswith('CHECK ')}
            failed = {key for key, value in checks.items() if value == 'FAIL'}
            expected_failed = {expected_id} if expected_id else set()
            ok = (p.returncode == expected_rc and len(checks) == 7 and failed == expected_failed
                  and any(line.startswith('C2=' + ('PASS' if expected_rc == 0 else 'FAIL') + ' checks=') for line in p.stdout.splitlines()))
            passed += ok
            print(f'CASE {name} {"PASS" if ok else "FAIL"} expected_rc={expected_rc} actual_rc={p.returncode} failed={",".join(sorted(failed)) or "none"} base={base} rev={rev}')
            if not ok:
                print(p.stdout, end='')
                print(p.stderr, end='')
    print(f'LOADER_MATRIX={passed}/9 C1={"PASS" if passed == 9 else "FAIL"}')
    return 0 if passed == 9 else 1

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--counter', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args()
    try:
        return run(args.counter.resolve(), args.work.resolve())
    except (OSError, RuntimeError) as exc:
        print(f'MATRIX_SETUP: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
