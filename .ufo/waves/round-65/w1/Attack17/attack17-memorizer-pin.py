#!/usr/bin/env python3
"""Attack17 memorizer probe: demonstrates that c1-count.py's frozen 20 cases can be
passed by a lookup table with ZERO validation logic, and that the same tool admits
forged receipts outside the 20 (any receipt claiming --revision passes).

For the 20 frozen receipts it emits the exact frozen token/exit. For any other receipt
whose first line equals 'REVISION=<--revision>' it prints RECEIPT_PIN=PASS exit 0
regardless of digest/path/body (i.e., accepts forged receipts). Everything else FAIL.
"""
import argparse, hashlib, pathlib, subprocess, sys

BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'


def build_cases(root, rev):
    raw = subprocess.run(['git', '-C', root, 'cat-file', 'blob', rev + ':SKILL.md'],
                         capture_output=True, check=True).stdout
    h = hashlib.sha256(raw).hexdigest()
    v = f'REVISION={rev}\nEXIT=0\nSHA256={h} SKILL.md\n\nmeasured output\n'
    return [
        ('valid', v, 0), ('nonzero-valid', v.replace('EXIT=0', 'EXIT=1'), 0),
        ('max-exit', v.replace('EXIT=0', 'EXIT=255'), 0),
        ('no-revision', v.split('\n', 1)[1], 1),
        ('wrong-revision', v.replace(rev, '0' * 40), 1),
        ('short-revision', v.replace(rev, rev[:8]), 1),
        ('no-exit', v.replace('EXIT=0\n', ''), 1),
        ('negative-exit', v.replace('EXIT=0', 'EXIT=-1'), 1),
        ('overflow-exit', v.replace('EXIT=0', 'EXIT=256'), 1),
        ('word-exit', v.replace('EXIT=0', 'EXIT=PASS'), 1),
        ('no-digest', v.replace('SHA256=' + h + ' SKILL.md\n', ''), 1),
        ('wrong-digest', v.replace(h, '0' * 64), 1),
        ('short-digest', v.replace(h, h[:16]), 1),
        ('missing-blob', v.replace('SKILL.md', 'missing-r65.md'), 1),
        ('traversal', v.replace('SKILL.md', '../SKILL.md'), 1),
        ('absolute', v.replace('SKILL.md', '/SKILL.md'), 1),
        ('duplicate', v.replace('\n\n', '\nEXIT=0\n\n'), 1),
        ('no-separator', v.replace('\n\n', '\n'), 1),
        ('no-body', v.split('\n\n')[0] + '\n\n', 1),
        ('upper-digest', v.replace(h, h.upper()), 1),
    ]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--receipt', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--revision', required=True)
    a = p.parse_args()
    text = pathlib.Path(a.receipt).read_text(encoding='utf-8')
    for _name, expect_text, rc in build_cases(a.root, a.revision):
        if text == expect_text:
            print('RECEIPT_PIN=PASS' if rc == 0 else 'RECEIPT_PIN=FAIL memorized-case')
            return rc
    # Outside the 20: accept ANY receipt that claims the caller-supplied revision,
    # whatever its digest/path/body — a forged receipt bypass the counter cannot see.
    if text.startswith('REVISION=' + a.revision + '\n'):
        print('RECEIPT_PIN=PASS')
        return 0
    print('RECEIPT_PIN=FAIL unrecognized')
    return 1


if __name__ == '__main__':
    sys.exit(main())
