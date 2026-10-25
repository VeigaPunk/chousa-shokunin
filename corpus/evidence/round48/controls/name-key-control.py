#!/usr/bin/env python3
"""Check that the frozen R48 C1 composite rejects a name-keyed no-read tool."""
from __future__ import annotations

import io
import pathlib
import subprocess
import sys
import tarfile
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[4]
FREEZE = '4bbd2348578bb6288c0700dabf37cea04225bfb6'
ARCHIVE_PATHS = (
    'tools/inference-ground.py',
    'corpus/SOURCES.md',
    'corpus/fixtures/inference-ground-r46',
    'corpus/fixtures/inference-ground-r47',
    'corpus/evidence/round46',
    'corpus/evidence/round47',
    'corpus/evidence/round48',
    'corpus/knowledge/evidence-pool-versioning-r39.md',
    'corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md',
)
FAKE = '''#!/usr/bin/env python3
import argparse, pathlib, sys
REFUSE = {"un-prefix-flip.md", "repeated-figure.md", "canary-b.md",
          "junk-uncited.md", "junk-ungrounded.md", "junk-borrowed.md",
          "junk-flip-asserted.md", "junk-flip-denied.md", "junk-flip-figure.md"}
ap = argparse.ArgumentParser()
ap.add_argument("--entry"); ap.add_argument("--spans"); ap.add_argument("--counts")
ap.add_argument("--registry"); ap.add_argument("--root"); ap.add_argument("--json"); ap.add_argument("--quiet", action="store_true")
args = ap.parse_args()
if pathlib.Path(args.entry).name in REFUSE:
    print("FINDING INF_POLARITY_FLIP bullet=1 token=name-keyed-lookup")
    sys.exit(1)
print("GROUND: PASS")
sys.exit(0)
'''

def main() -> int:
    with tempfile.TemporaryDirectory(prefix='chousa-r48-name-control-') as td:
        root = pathlib.Path(td)
        archive = subprocess.run(
            ['git', '-C', str(LANE), 'archive', FREEZE, *ARCHIVE_PATHS],
            capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as tf:
            tf.extractall(root, filter='data')
        candidate = root / 'tools/inference-ground.py'
        candidate.write_text(FAKE, encoding='utf-8')
        c1 = subprocess.run([sys.executable, str(root / 'corpus/evidence/round48/c1-count.py'),
                             '--root', str(root)], cwd=root, capture_output=True, text=True)
        print('NAME_KEYED_C1_COMPONENT=' + ('PASS' if c1.returncode == 0 else 'FAIL'))
        print(c1.stdout, end='')
        mutation = subprocess.run([sys.executable, str(root / 'corpus/evidence/round48/mutation-check.py')],
                                  cwd=root, capture_output=True, text=True)
        mutation_output = mutation.stdout + mutation.stderr
        print('NAME_KEYED_MUTATION_CHECK=' + ('PASS' if mutation.returncode == 0 else 'REJECTED'))
        print(mutation_output, end='')
        composite_rejected = c1.returncode == 0 and mutation.returncode != 0
        print('COMPOSITE_CONTROL=' + ('REJECTED' if composite_rejected else 'NOT_REJECTED'))
        return 0 if composite_rejected else 1

if __name__ == '__main__':
    sys.exit(main())
