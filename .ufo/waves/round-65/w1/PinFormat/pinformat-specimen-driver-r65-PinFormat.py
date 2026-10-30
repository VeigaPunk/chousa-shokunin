#!/usr/bin/env python3
"""PinFormat seat driver (round65, lane chousa).

Drafts a specimen final receipt in the frozen round65 header format:

    REVISION=<40 lowercase hex>
    EXIT=<decimal 0..255>
    SHA256=<64 lowercase hex> <canonical repo-relative POSIX path>
    <empty line>
    <nonempty measured output>

The digest is sha256 of the Git blob at <revision>:<path> in --root (git cat-file blob,
read-only), never working-tree bytes. The measured child's exit becomes the reported
EXIT field; this driver's own invocation exit (0) is a separate channel.
"""
import argparse
import hashlib
import pathlib
import subprocess
import sys


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--root', required=True, help='repo whose committed blob is pinned')
    p.add_argument('--revision', required=True, help='full 40-hex object id')
    p.add_argument('--path', required=True, help='canonical repo-relative POSIX path')
    p.add_argument('--child-exit', type=int, default=0)
    p.add_argument('--child-text', default='PinFormat measured output')
    p.add_argument('--out', required=True, help='receipt file to write')
    a = p.parse_args()
    blob = subprocess.run(['git', '-C', a.root, 'cat-file', 'blob', a.revision + ':' + a.path],
                          capture_output=True, check=True).stdout
    digest = hashlib.sha256(blob).hexdigest()
    child = subprocess.run(
        [sys.executable, '-c',
         'import sys; print(sys.argv[1]); print("child-exit", sys.argv[2]); sys.exit(int(sys.argv[2]))',
         a.child_text, str(a.child_exit)],
        capture_output=True, text=True)
    body = child.stdout.rstrip('\n') or child.stderr.rstrip('\n') or '<no output>'
    receipt = (f'REVISION={a.revision}\n'
               f'EXIT={child.returncode}\n'
               f'SHA256={digest} {a.path}\n'
               f'\n'
               f'{body}\n')
    pathlib.Path(a.out).write_text(receipt, encoding='utf-8')
    print(f'driver: wrote {a.out}; reported EXIT={child.returncode}; '
          f'driver-invocation-exit will be 0 regardless of reported EXIT')
    return 0


if __name__ == '__main__':
    sys.exit(main())
