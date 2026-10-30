#!/usr/bin/env python3
"""Seat-local bounded G02 suffix probe; no lane mutations."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import pathlib
import random
import re
import shutil
import subprocess

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack08')
OUT = LANE / '.ufo/waves/round-64/w1/Attack08/evidence.json'
TOOL = LANE / 'corpus/evidence/round64/controls/ref-preflight-v3.py'
results = {'python': sys.version, 'axes': ['filename-suffix contract fidelity', 'frozen-versus-supplement provenance', 'bounded reproducibility'], 'cases': []}

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_case(name, root, readme=None):
    if readme is not None:
        (root / 'corpus/knowledge').mkdir(parents=True)
        (root / 'corpus/knowledge/probe.md').write_text('# Probe\n')
        (root / 'corpus/README.md').write_text(readme)
    cmd = [sys.executable, '-B', str(TOOL), '--root', str(root), '--only', 'G02', '--work', str(SCRATCH / ('work-' + name))]
    p = subprocess.run(cmd, cwd=SCRATCH, text=True, capture_output=True, timeout=20)
    text = (root / 'corpus/README.md').read_text()
    files = sorted(x.name for x in (root / 'corpus/knowledge').iterdir())
    results['cases'].append({'case': name, 'files': files, 'readme': text, 'command': cmd, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})

try:
    SCRATCH.mkdir(parents=True, exist_ok=False)
    for name, text in [('exact', 'knowledge/probe.md\n'), ('bare-stem', 'probe\n'), ('wrong-suffix', 'knowledge/probe.txt\n'), ('extended-suffix', 'knowledge/probe.mdx\n'), ('sentence-dot', 'knowledge/probe.md.\n')]:
        run_case(name, SCRATCH / name, text)
        results['cases'][-1]['frozen_filename_regex_matches'] = bool(re.search(r'(?<![\w.-])(?:knowledge/)?probe\.md(?![\w-])', text))
    for label, filename in [('frozen', 'c1-battery-v3.py'), ('supplement', 'c1-battery-supplement.py')]:
        battery = load(label, LANE / 'corpus/evidence/round64' / filename)
        for leg in battery.mk_legs(random.Random(64)):
            if leg[0] not in ('E12', 'E13'):
                continue
            name = label + '-' + leg[0]
            root = SCRATCH / name
            (root / 'corpus/knowledge').mkdir(parents=True)
            (root / 'corpus/README.md').write_text('')
            leg[2](root)
            run_case(name, root)
            results['cases'][-1]['battery_expected_exit'] = leg[4]['rc']
finally:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    results['scratch_removed'] = not SCRATCH.exists()
    OUT.write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
