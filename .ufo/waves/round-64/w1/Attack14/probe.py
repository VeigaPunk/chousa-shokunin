#!/usr/bin/env python3
"""Bounded C2/A11 probe; no git commands, no repository writes."""
import ast
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch

lane = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = Path('/fast/scratch/hyaku/chousa-r64/Attack14')
scratch.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(scratch)
source_path = lane / 'tools/claims-audit-v2.py'
source = source_path.read_text()
generator = lane / 'corpus/evidence/round64/gen-audit-mutants.py'
tree = ast.parse(generator.read_text())
mutants = next(ast.literal_eval(n.value) for n in tree.body
               if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'MUTANTS' for t in n.targets))
mid, name, old, new, count = next(m for m in mutants if m[0] == 'A11')
assert source.count(old) == count == 1
results = []
try:
    p = subprocess.run([sys.executable, '-B', str(source_path), '--selftest', '--selftest-fault', '1'],
                       cwd=scratch, capture_output=True, text=True, timeout=20)
    results.append(dict(command=f'{sys.executable} -B {source_path} --selftest --selftest-fault 1',
                        exit=p.returncode, stdout=p.stdout, stderr=p.stderr))
    for label, text in [('frozen-v2', source), ('frozen-A11', source.replace(old, new))]:
        module = {'__name__': 'attack14_probe_target', '__file__': str(source_path)}
        exec(compile(text, str(source_path), 'exec'), module)
        for fault in (0, 1):
            output = io.StringIO()
            # Simulate a checker which incorrectly accepts the bad fixture. The
            # selftest must reject this result through its real verdict guard.
            wrong = subprocess.CompletedProcess(['checker'], 0, 'FLAGGED=0/6 AUDIT=PASS\n', '')
            with patch.object(module['subprocess'], 'run', return_value=wrong) as calls:
                with contextlib.redirect_stdout(output):
                    rc = module['selftest'](fault=fault)
            results.append(dict(target=label, operation=f'selftest(fault={fault})',
                                injected_child_result=dict(exit=0, stdout=wrong.stdout),
                                exit=rc, stdout=output.getvalue(), child_calls=calls.call_count,
                                matrix_R6_accepts=(rc == 1 and 'FAULT' in output.getvalue()) if fault else None))
    print(json.dumps(dict(python=sys.version, source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                          mutation=mid, results=results), indent=2))
finally:
    shutil.rmtree(scratch)
