#!/usr/bin/env python3
"""Inspect what verify-all actually persists about the selected grep."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

scratch = Path('/tmp/hyaku/chousa-r35/w2/CritGrepClaimScope')
artifacts = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/CritGrepClaimScope')
gate = scratch / 'landed.sh'
spec = importlib.util.spec_from_file_location('c1', '/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round35/c1-count.py')
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)
root = scratch / 'manifest-fixture'
root.mkdir()
claims = counter.make_fixture(str(root))
manifest = root / 'manifest.jsonl'
env = {k: v for k, v in os.environ.items() if not k.startswith(('CHOUSA_', 'RESEARCH_GATE_')) and k not in ('BASH_ENV', 'ENV', 'CDPATH')}
env.update(PATH='/usr/bin:/bin', LC_ALL='C.utf8', CHOUSA_GREP_PIN_ECHO='1', TMPDIR=str(scratch), C1_TMP=str(scratch), C2_TMP=str(scratch), WITNESS_TMP=str(scratch))
argv = ['timeout', '60s', 'bash', str(gate), 'verify-all', claims, '--root', str(root), '--json', str(manifest)]
p = subprocess.run(argv, env=env, cwd=root, capture_output=True, text=True, timeout=65)
rows = [json.loads(line) for line in manifest.read_text().splitlines()]
echo_lines = [line for line in p.stderr.splitlines() if line.startswith('GATE_GREP: ')]
receipt = {'argv': argv, 'exit': p.returncode, 'gate_sha256': hashlib.sha256(gate.read_bytes()).hexdigest(), 'stdout': p.stdout, 'stderr': p.stderr, 'echo_lines': echo_lines, 'manifest_keys': [sorted(row) for row in rows], 'manifest': rows}
(artifacts / 'verify-all-scope.json').write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
(artifacts / 'verify-all-manifest.jsonl').write_bytes(manifest.read_bytes())
print(json.dumps({'exit': p.returncode, 'echo_lines': echo_lines, 'manifest_keys': receipt['manifest_keys'], 'gate_sha256': receipt['gate_sha256']}, indent=1))
