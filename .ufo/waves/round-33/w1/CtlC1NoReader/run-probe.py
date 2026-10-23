#!/usr/bin/env python3
"""Run the unchanged round-33 detector on one gate, preserving bounded evidence."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

SCRATCH = Path('/fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader')
LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
ART = LANE / '.ufo/waves/round-33/w1/CtlC1NoReader'
COUNTER = LANE / 'corpus/evidence/round33/c1-count.py'
phase, name, *seeds = sys.argv[1:]
gate = SCRATCH / ('base.pristine.sh' if name == 'base' else f'control-{name}.sh')
expected_counter = 'ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229'
assert hashlib.sha256(COUNTER.read_bytes()).hexdigest() == expected_counter
for seed in seeds:
    stem = f'{phase}-{name}-{seed}'
    receipt = ART / (stem + '.json')
    assert not receipt.exists(), receipt
    cmd = ['timeout', '850s', 'prlimit', '--as=1073741824', '--nproc=2000', '--',
           'python3', str(COUNTER), '--gate', str(gate), '--seed', seed,
           '--receipt', str(receipt)]
    env = os.environ.copy()
    env.update({k: str(SCRATCH / 'tmp') for k in ('C1_TMP', 'C2_TMP', 'TMPDIR')})
    before = hashlib.sha256(gate.read_bytes()).hexdigest()
    result = subprocess.run(cmd, cwd=LANE, env=env, capture_output=True, text=True, timeout=880)
    after = hashlib.sha256(gate.read_bytes()).hexdigest()
    text = f'COMMAND: {shlex.join(cmd)}\nCWD: {LANE}\nC1_TMP=C2_TMP=TMPDIR={SCRATCH / "tmp"}\nEXIT: {result.returncode}\nBEFORE_SHA256: {before}\nAFTER_SHA256: {after}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}'
    assert len(text.encode()) < 1048576
    (ART / (stem + '.out')).write_text(text)
    print(text, flush=True)
    assert before == after, 'detector changed gate bytes'
    assert result.returncode in (0, 1), 'detector failed to evaluate'
