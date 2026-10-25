#!/usr/bin/env python3
"""Count the R47 held-out correct-bullet regression set against a candidate tool."""
from __future__ import annotations
import argparse
import pathlib
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
CASES = (
    ("p01", "S901", "no revision is recorded", "no revision can be traced, so this claim cannot be checked"),
    ("p02", "S901", "no revision is recorded", "the frozen pool lacks revision markers"),
    ("p03", "S901", "no revision is recorded", "this release's revision history is nonexistent"),
    ("p04", "S901", "no revision is recorded", "the release cannot show that any sentence has been revised"),
    ("p05", "S901", "no revision is recorded", "a published page is distributed without revision records"),
    ("p06", "S901", "no revision is recorded", "the pool is unsuitable for revision-sensitive evaluation"),
    ("a01", "S901", "the release ships a frozen pool", "a later page cannot be an unrecorded update"),
    ("a02", "S901", "the release ships a frozen pool", "the pool is stable after its release"),
    ("a03", "S901", "the release ships a frozen pool", "its contents are fixed"),
    ("a04", "S902", "the archived copy is dated at build", "snapshotted on the build date"),
    ("a05", "S902", "the archived copy is dated at build", "that date is not the copy's build date"),
    ("a06", "S902", "the archived copy is dated at build", "needs a separate timestamp"),
)
 
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default=str(LANE))
    ap.add_argument('--tool')
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    tool = pathlib.Path(a.tool).resolve() if a.tool else root / 'tools/inference-ground.py'
    spans = root / 'corpus/fixtures/inference-ground-r47/spans.tsv'
    counts = root / 'corpus/fixtures/inference-ground-r47/counts.json'
    registry = root / 'corpus/SOURCES.md'
    passed = 0
    with tempfile.TemporaryDirectory(prefix='chousa-r48-precision-') as td:
        tmp = pathlib.Path(td)
        for name, sid, quote, body in CASES:
            entry = tmp / f'{name}.md'
            entry.write_text(
                f'# Precision fixture {name}\n\n#### Inference\n\n- `{quote}`: {body} ({sid})\n',
                encoding='utf-8')
            p = subprocess.run([sys.executable, str(tool), '--entry', str(entry),
                                '--spans', str(spans), '--counts', str(counts),
                                '--registry', str(registry), '--root', str(root), '--quiet'],
                               capture_output=True, text=True)
            ok = p.returncode == 0
            passed += ok
            print(f'{name}={"PASS" if ok else "REFUSED"} rc={p.returncode}')
    target = 11
    print(f'CORRECT_BULLETS_PASS={passed}/{len(CASES)}')
    print(f'MIN_CORRECT_PASS={target}/12')
    ok = passed >= target
    print(f'PRECISION_GATE={"PASS" if ok else "FAIL"}')
    return 0 if ok else 1
 
if __name__ == '__main__':
    sys.exit(main())

