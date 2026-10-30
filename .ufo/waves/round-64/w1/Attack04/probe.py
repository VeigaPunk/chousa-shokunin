import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/chousa-r64/Attack04')
OUT = LANE / '.ufo/waves/round-64/w1/Attack04'
SCRATCH.mkdir(parents=True, exist_ok=True)
records = []
def record(**kw):
    records.append(kw)
    print(json.dumps(kw, ensure_ascii=True))
def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, LANE / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
try:
    frozen_rel = 'corpus/evidence/round64/c1-battery-v3.py'
    frozen = load(frozen_rel, 'frozen')
    supplement = load('corpus/evidence/round64/c1-battery-supplement.py', 'supplement')
    inherited = load('corpus/evidence/round63/c1-battery-v2.py', 'inherited')
    p = subprocess.run(['git', 'show', 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1:' + frozen_rel], cwd=LANE, capture_output=True)
    record(command='git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:' + frozen_rel, exit=p.returncode, stderr=p.stderr.decode(), sha256=hashlib.sha256(p.stdout).hexdigest(), working_matches_frozen=p.stdout == (LANE / frozen_rel).read_bytes())
    record(python=sys.version, judge_equal_inherited=inspect.getsource(frozen.judge) == inspect.getsource(inherited.judge), judge_equal_supplement=inspect.getsource(frozen.judge) == inspect.getsource(supplement.judge))
    base = ''.join(f'GATE {g} {n} SKIP\n' for g, n in zip(frozen.IDS, frozen.NAMES))
    summaries = {
        'valid': 'PREFLIGHT=0/0 FAILED=none ENV=none SKIPPED=' + ','.join(frozen.IDS),
        'positive_run_count': 'PREFLIGHT=0/8 FAILED=none ENV=none SKIPPED=' + ','.join(frozen.IDS),
        'false_sets': 'PREFLIGHT=0/0 FAILED=G01 ENV=G02 SKIPPED=none',
        'malformed_sets': 'PREFLIGHT=0/0 FAILED=garbage ENV=garbage SKIPPED=garbage',
    }
    for label, module in [('frozen', frozen), ('supplement', supplement), ('inherited', inherited)]:
        for case, summary in summaries.items():
            ok, why = module.judge('Z01', {'rc': 2, 'zero': True}, 2, base + summary + '\n', '')
            record(probe='direct-judge', instrument=label, case=case, input_stdout=base + summary + '\n', input_exit=2, accepted=ok, why=why)
    for label, rel in [('production', 'tools/lane-preflight.py'), ('candidate', 'corpus/evidence/round64/controls/ref-preflight-v3.py')]:
        for case, flags in [('Z01', ['--skip', ','.join(frozen.IDS)]), ('Z02', ['--only', 'G01', '--skip', 'G01']), ('Z03', ['--only', 'G08', '--skip', 'G08'])]:
            cmd = [sys.executable, '-B', str(LANE / rel), '--root', str(LANE), '--work', str(SCRATCH / (label + '-' + case))] + flags
            p = subprocess.run(cmd, cwd=SCRATCH, capture_output=True, text=True, timeout=15)
            record(command=cmd, exit=p.returncode, stdout=p.stdout, stderr=p.stderr, frozen_judge=frozen.judge(case, {'rc': 2, 'zero': True}, p.returncode, p.stdout, p.stderr))
    # Inspect only generated E12/E13 fixtures; no full golden copy or gates.
    for label, module in [('frozen', frozen), ('supplement', supplement)]:
        for case in ['E12', 'E13']:
            root = SCRATCH / (label + '-' + case)
            (root / 'corpus/knowledge').mkdir(parents=True)
            (root / 'corpus/README.md').write_text('')
            leg = next(x for x in module.mk_legs(random.Random('Attack04/' + case)) if x[0] == case)
            leg[2](root)
            record(probe='fixture-only', instrument=label, case=case, files=[p.name for p in (root / 'corpus/knowledge').iterdir()], readme=(root / 'corpus/README.md').read_text())
finally:
    shutil.rmtree(SCRATCH)
    record(scratch_removed=not SCRATCH.exists())
    (OUT / 'evidence.json').write_text(json.dumps(records, indent=2, ensure_ascii=True) + '\n')
