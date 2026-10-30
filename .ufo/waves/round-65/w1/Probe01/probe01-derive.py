#!/usr/bin/env python3
"""Probe01 independent oracle: derive the expected verdict for a VALID receipt
straight from the frozen round65 format (claims.md C1), with no code shared
with controls/ref-receipt-pin.py. Prints EXPECTED_EXIT / EXPECTED_STDOUT."""
import hashlib, pathlib, re, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/chousa-shokunin'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'
FIXTURE = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe01/valid.txt')

text = FIXTURE.read_text(encoding='utf-8')
lines = text.splitlines()

problems = []
# frozen format: REVISION full lowercase 40 hex; must equal --revision
if not re.fullmatch(r'REVISION=[0-9a-f]{40}', lines[0]) or lines[0] != 'REVISION=' + BASE:
    problems.append('revision header')
# EXIT decimal 0..255
if not re.fullmatch(r'EXIT=(0|[1-9][0-9]{0,2})', lines[1]) or int(lines[1][5:]) > 255:
    problems.append('exit header')
# SHA256 full lowercase 64 hex + canonical relative POSIX path
m = re.fullmatch(r'SHA256=([0-9a-f]{64}) (.+)', lines[2])
if not m:
    problems.append('digest header')
else:
    rel = pathlib.PurePosixPath(m.group(2))
    if rel.is_absolute() or '..' in rel.parts or str(rel) != m.group(2) or not rel.parts:
        problems.append('path canonical form')
# empty separator, nonempty body
if lines[3] != '':
    problems.append('separator')
if not '\n'.join(lines[4:]).strip():
    problems.append('body')
# digest binds the Git blob at the declared revision (no working-tree hashing)
if m and not problems:
    blob = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob', BASE + ':' + m.group(2)],
                          capture_output=True)
    if blob.returncode != 0:
        problems.append('blob lookup')
    elif hashlib.sha256(blob.stdout).hexdigest() != m.group(1):
        problems.append('digest binds blob')

if problems:
    print('DERIVED: invalid -> EXPECTED_EXIT=1 EXPECTED_STDOUT_PREFIX=RECEIPT_PIN=FAIL problems=' + ','.join(problems))
    sys.exit(0)
print('DERIVED: consistent -> EXPECTED_EXIT=0 EXPECTED_STDOUT="RECEIPT_PIN=PASS\\n"')
