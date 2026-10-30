#!/usr/bin/env python3
"""Exercise the frozen runner's real timeout path, without editing its bytes.
No checker verdict is asserted: zero seconds is an injected infrastructure failure.
R1 times out before the runner reaches any git fixture operation.
"""
import importlib.util
import os
from pathlib import Path
import sys

lane = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = Path('/fast/scratch/hyaku/chousa-r64/Attack13')
matrix = sys.argv[1]
assert matrix in ('v1', 'v2')
target = lane / 'tools' / ('claims-audit.py' if matrix == 'v1' else 'claims-audit-v2.py')
spec = importlib.util.spec_from_file_location('attack13_frozen_runner', lane / 'corpus/evidence/round64/c2-mutrun.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
runner.os = os  # The CLI's __main__ block normally supplies this import.
runner.LEG_TIMEOUT = 0  # Inject only a zero-second subprocess budget; retain run() unchanged.
scratch.mkdir(parents=True, exist_ok=True)
assert not any(scratch.iterdir()), 'seat scratch must be empty'
sys.argv = ['c2-mutrun.py', '--target', str(target), '--matrix', matrix,
            '--work', str(scratch / ('work-' + matrix)), '--lane', str(lane)]
try:
    print(f'PROBE matrix={matrix} LEG_TIMEOUT={runner.LEG_TIMEOUT} runner.run=unchanged', flush=True)
    rc = runner.main()
    print(f'RUNNER_EXIT={rc}', flush=True)
finally:
    scratch.rmdir()
raise SystemExit(rc)
