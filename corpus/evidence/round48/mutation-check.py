#!/usr/bin/env python3
"""Prove the round-48 C1 cases reject the five R47 surviving tool mutants."""
from __future__ import annotations
import pathlib
import re
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
SOURCE = LANE / 'tools/inference-ground.py'
COUNTER = LANE / 'corpus/evidence/round48/c1-count.py'
MUTATIONS = {
    'implicit-neg': ('implicit-neg', lambda s: re.sub(
        r'IMPLICIT_NEG = \{[^}]*\}', 'IMPLICIT_NEG = set()', s, count=1, flags=re.S)),
    'un-neg': ('un-neg', lambda s: s.replace(
        'UN_NEG_RE = re.compile(r"^un(?!der|til|ion|ique|it|iver|iform|less|ifi|pack|veil|fold|wrap)"\n                       r"[a-z]{3,}(?:able|ible|ed|known|clear|sure)$")',
        'UN_NEG_RE = re.compile(r"(?!)")', 1)),
    'un-prefix-flip': ('un-prefix-flip', lambda s: s.replace(
        'and w.startswith("un") and len(w) >= 6', 'and False and len(w) >= 6', 1)),
    'repeated-figure': ('repeated-figure', lambda s: s.replace(
        'for m in re.finditer(r"(?<![\\d,.])" + re.escape(bare) + r"(?![\\d,])", text):',
        'for m in list(re.finditer(r"(?<![\\d,.])" + re.escape(bare) + r"(?![\\d,])", text))[:1]:', 1)),
    'nested-count-key': ('nested-count-key', lambda s: s.replace(
        '    if leaf.lower() in GENERIC_KEYS and len(parts) > 1:\n        leaf = parts[-2]\n', '', 1)),
}

def main() -> int:
    original = SOURCE.read_text(encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='chousa-r48-mutants-') as td:
        tmp = pathlib.Path(td)
        pristine = tmp / 'pristine.py'
        pristine.write_text(original, encoding='utf-8')
        p = subprocess.run([sys.executable, str(COUNTER), '--root', str(LANE), '--tool', str(pristine), '--cases-only'], capture_output=True, text=True)
        if p.returncode != 0:
            print('PRISTINE_CASES=FAIL'); print(p.stdout); return 2
        print('PRISTINE_CASES=PASS')
        killed = 0
        for name, (expected_case, mutate) in MUTATIONS.items():
            mutant_text = mutate(original)
            if mutant_text == original:
                print(f'{name}=MUTATION_NOT_APPLIED'); return 2
            mutant = tmp / f'{name}.py'
            mutant.write_text(mutant_text, encoding='utf-8')
            result = subprocess.run([sys.executable, str(COUNTER), '--root', str(LANE), '--tool', str(mutant), '--cases-only'], capture_output=True, text=True)
            out = result.stdout + result.stderr
            target_failed = any(line.startswith(expected_case + '=FAIL') for line in out.splitlines())
            caught = result.returncode == 1 and target_failed
            killed += caught
            print(f'{name}={"KILLED" if caught else "SURVIVED"} expected-cell={expected_case} rc={result.returncode}')
            if not caught:
                print(out)
        print(f'MUTANTS_KILLED={killed}/{len(MUTATIONS)}')
        return 0 if killed == len(MUTATIONS) else 1

if __name__ == '__main__':
    sys.exit(main())
