#!/usr/bin/env python3
"""Round-48 C1: precision floor, legacy polarity set and five refinement cases."""
from __future__ import annotations
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
CASES = (
    ("implicit-neg", "S901", "no revision is recorded per sentence", "Because `no revision is recorded` here, the pool lacks revision markers", {}, 0),
    ("un-neg", "S901", "no revision is recorded per sentence", "Because `no revision is recorded` here, the revision is untraceable", {}, 0),
    ("un-prefix-flip", "S901", "the release ships a frozen pool of pages", "Because `the release ships a frozen pool`, the pool is unfrozen at release", {}, 1),
    ("repeated-figure", "S902", "The source gives the quantity in the counts file.", "1,582 answers carry no archive key, and 1,582 answers are bound to an archive key", {"figures": {"answers_without_archive_key": 1582}}, 1),
    ("nested-count-key", "S902", "The source gives the quantity in the counts file.", "1,582 records carry no archive bucket, so they are unbound", {"without_archive": {"count": 1582}}, 0),
)

def run_case(tool: pathlib.Path, root: pathlib.Path, case, tmp: pathlib.Path) -> tuple[bool, str]:
    name, sid, span_text, body, counts_data, want = case
    span = tmp / f'{name}.txt'
    span.write_text(span_text + '\n', encoding='utf-8')
    spans = tmp / f'{name}.tsv'
    spans.write_text('id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry\n'
                     f'{sid}\tfixture\t{"0" * 64}\t0\t{name}.txt\t{span_text}\t{name}.md\n', encoding='utf-8')
    counts = tmp / f'{name}.json'
    counts.write_text(json.dumps(counts_data), encoding='utf-8')
    entry = tmp / f'{name}.md'
    if name in ('repeated-figure', 'nested-count-key'):
        sentence = f'- {body} ({sid})'
    else:
        sentence = f'- {body} ({sid})'
    entry.write_text(f'# Case {name}\n\n#### Inference\n\n{sentence}\n', encoding='utf-8')
    p = subprocess.run([sys.executable, str(tool), '--entry', str(entry), '--spans', str(spans),
                        '--counts', str(counts), '--registry', str(root / 'corpus/SOURCES.md'),
                        '--root', str(root)], capture_output=True, text=True)
    out = (p.stdout or '') + (p.stderr or '')
    if want == 0:
        ok = p.returncode == 0
    else:
        ok = p.returncode == 1 and 'FINDING INF_POLARITY_FLIP' in out
    detail = next((line for line in out.splitlines() if line.startswith(('FINDING', 'GROUND:', 'FINDING', 'ERROR'))), '')
    return ok, f'{name}={"PASS" if ok else "FAIL"} wanted_rc={want} observed_rc={p.returncode} {detail}'

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default=str(LANE))
    ap.add_argument('--tool', help='candidate tool (mutation-control input)')
    ap.add_argument('--cases-only', action='store_true', help='run only the five fixed refinement fixtures')
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    tool = pathlib.Path(a.tool).resolve() if a.tool else root / 'tools/inference-ground.py'
    if not tool.is_file():
        print('TOOL=absent'); return 2
    case_ok = 0
    with tempfile.TemporaryDirectory(prefix='chousa-r48-c1-') as td:
        tmp = pathlib.Path(td)
        for case in CASES:
            ok, line = run_case(tool, root, case, tmp)
            case_ok += ok
            print(line)
    case_pass = case_ok == len(CASES)
    print(f'REFINEMENT_CASES={case_ok}/{len(CASES)}')
    if a.cases_only:
        print(f'C1_CASES={"PASS" if case_pass else "FAIL"}')
        return 0 if case_pass else 1
    prec = subprocess.run([sys.executable, str(root / 'corpus/evidence/round48/precision-count.py'),
                           '--root', str(root), '--tool', str(tool)], capture_output=True, text=True)
    print(prec.stdout, end='')
    legacy = subprocess.run([sys.executable, str(root / 'corpus/evidence/round47/c1-count.py'),
                             '--root', str(root), '--tool', str(tool)], capture_output=True, text=True)
    print('LEGACY_R47=' + ('PASS' if legacy.returncode == 0 else 'FAIL'))
    prec_ok = 'PRECISION_GATE=PASS' in prec.stdout and prec.returncode == 0
    ok = case_pass and prec_ok and legacy.returncode == 0
    print(f'C1={"PASS" if ok else "FAIL"}')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
