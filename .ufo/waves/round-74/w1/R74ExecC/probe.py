#!/usr/bin/env python3
"""Bounded real-file public-CLI probe; never imports either counter."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
OUT = LANE / '.ufo/waves/round-74/w1/R74ExecC'
ROOT = Path('/fast/scratch/hyaku/chousa-r74/R74ExecC')
SOURCE_REV = '5aec90775fc7cc1fe9ad442e0d5491731323eec1'
COUNTER = LANE / 'corpus/evidence/round74/correction-count.py'
PATHS = ('LOG.md', 'corpus/lessons/round-72.md', 'SCORECARD.md')
RECEIPTS = ('corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt',
            'corpus/evidence/round72/controls/after-r72-corrections.txt')


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True).stdout


def assert_root():
    actual = Path(git(ROOT, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    if actual != ROOT.resolve():
        raise RuntimeError(f'Wrong mutation root: {actual}')


def commit(name):
    assert_root()
    git(ROOT, 'add', '--', *PATHS, *RECEIPTS)
    git(ROOT, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
        'commit', '--allow-empty', '-qm', name)
    return git(ROOT, 'rev-parse', 'HEAD').decode().strip()


def main():
    records = []
    all_ok = True
    try:
        ROOT.mkdir(parents=True, exist_ok=True)
        if any(ROOT.iterdir()):
            raise RuntimeError('Scratch root must be empty')
        originals = {path: git(LANE, 'show', f'{SOURCE_REV}:{path}') for path in (*PATHS, *RECEIPTS)}
        print('AXES=CLI fidelity; per-file deletion isolation; equal-line rejection; receipt integrity; scratch containment', flush=True)
        print(f'SOURCE_REV={SOURCE_REV}', flush=True)
        for path in (COUNTER, LANE / 'corpus/evidence/round73/c2-count.py'):
            print(f'ARTIFACT {path} SHA256={hashlib.sha256(path.read_bytes()).hexdigest()}', flush=True)
        for path, data in originals.items():
            print(f'INPUT {path} bytes={len(data)} SHA256={hashlib.sha256(data).hexdigest()}', flush=True)
            archived = OUT / 'inputs' / path
            archived.parent.mkdir(parents=True, exist_ok=True)
            archived.write_bytes(data)
        git(ROOT, 'init', '-q')
        assert_root()
        for path, data in originals.items():
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        base = commit('historical landing bytes')
        cases = [('unchanged', None, None)]
        cases += [(f'mixed-{i}', path, PATHS[(i + 1) % 3]) for i, path in enumerate(PATHS)]
        cases += [(f'equal-{i}', path, None) for i, path in enumerate(PATHS)]
        for name, delete_path, append_path in cases:
            for path, data in originals.items():
                (ROOT / path).write_bytes(data)
            if delete_path:
                lines = originals[delete_path].splitlines(keepends=True)
                if not lines[0].strip() or not lines[0].endswith(b'\n'):
                    raise RuntimeError('Expected nonempty newline-terminated first line')
                lines[0:1] = [] if append_path else [b'# Independently replaced document title\n']
                (ROOT / delete_path).write_bytes(b''.join(lines))
            if append_path:
                (ROOT / append_path).write_bytes(originals[append_path] + b'\nIndependent append evidence.\n')
            rev = commit(name)
            numstat = git(ROOT, 'diff', '--numstat', base, rev, '--', *PATHS).decode()
            receipt_diff = git(ROOT, 'diff', '--name-only', base, rev, '--', *RECEIPTS).decode()
            if receipt_diff:
                raise RuntimeError('Historical receipt bytes changed')
            command = [sys.executable, '-B', str(COUNTER), '--lane', str(ROOT), '--base', base, '--rev', rev]
            result = subprocess.run(command, capture_output=True, text=True)
            (OUT / f'{name}.stdout.txt').write_text(result.stdout)
            (OUT / f'{name}.stderr.txt').write_text(result.stderr)
            (OUT / f'{name}.numstat.txt').write_text(numstat)
            checks = [line.split() for line in result.stdout.splitlines() if line.startswith('CHECK ')]
            failed = {parts[1] for parts in checks if parts[2] == 'FAIL'}
            expected = set() if name == 'unchanged' else {'C2-6'}
            summary = 'C2=PASS checks=7/7 ' if not expected else 'C2=FAIL checks=6/7 '
            ok = result.returncode == bool(expected) and len(checks) == 7 and failed == expected and any(line.startswith(summary) for line in result.stdout.splitlines())
            all_ok &= ok
            record = dict(case=name, command=command, base=base, rev=rev, deleted_path=delete_path, appended_path=append_path,
                          rc=result.returncode, failed=sorted(failed), expected_failed=sorted(expected), receipts_unchanged=True, matched=ok)
            records.append(record)
            print(json.dumps(record, sort_keys=True), flush=True)
            print(numstat + result.stdout + result.stderr, end='', flush=True)
        (OUT / 'results.json').write_text(json.dumps(records, indent=2) + '\n')
        print(f'BOUNDED_PROBE={sum(r["matched"] for r in records)}/{len(records)}', flush=True)
        return 0 if all_ok else 1
    finally:
        if ROOT.exists():
            shutil.rmtree(ROOT)
        print(f'SCRATCH_REMOVED={not ROOT.exists()}', flush=True)


if __name__ == '__main__':
    sys.exit(main())
