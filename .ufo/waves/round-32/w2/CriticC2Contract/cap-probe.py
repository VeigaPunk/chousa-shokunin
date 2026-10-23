#!/usr/bin/env python3
"""Supplement: allow the gate's bounded 8 MiB scratch here-document."""
import hashlib
import json
import os
from pathlib import Path
import resource
import shlex
import signal
import subprocess
import time
W = Path('/fast/scratch/hyaku/chousa-r32/w2/CriticC2Contract')
O = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticC2Contract')
root = W / 'fixtures'
original = root / 'inclusive-cap.md'
resolved = root / 'inclusive-cap-resolved.md'
content = original.read_text().replace('| unresolved | unavailable claim |', '| resolved | unavailable claim |')
assert len(content) < 65536
resolved.write_text(content)
env = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
env.update(TMPDIR=str(W / 'tmp'), CHOUSA_STRICT='0', CHOUSA_NOW_EPOCH='1760000000')

def limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024 * 1024, 16 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

runs = []
for name, gate, rec in [('candidate-unavailable', W / 'lane/tools/research-gate.sh', original),
                         ('candidate-resolved', W / 'lane/tools/research-gate.sh', resolved),
                         ('base-resolved-control', W / 'base/tools/research-gate.sh', resolved)]:
    cmd = ['timeout', '--signal=TERM', '--kill-after=2s', '60s', 'bash', str(gate), 'verify-chain', str(rec), '--root', str(root)]
    t0 = time.monotonic()
    p = subprocess.Popen(cmd, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, preexec_fn=limits)
    try:
        stdout, stderr = p.communicate(timeout=65)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        stdout, stderr = p.communicate()
    finally:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    assert len(stdout) < 65536 and len(stderr) < 65536
    item = {'name': name, 'command': shlex.join(cmd), 'rc': p.returncode, 'elapsed_s': round(time.monotonic() - t0, 3), 'stdout': stdout.decode(), 'stderr': stderr.decode()}
    runs.append(item)
    print(json.dumps(item))
receipt = {'child_file_size_limit': 16 * 1024 * 1024, 'prior_probe_file_size_limit': 1024 * 1024 - 1,
           'reason': 'The first probe imposed a 1 MiB per-file bound, which prevented Bash from materializing its 8 MiB here-string. This supplement removes that harness interference while retaining a bound.',
           'source_size': (root / 'at-cap.md').stat().st_size, 'runs': runs}
text = json.dumps(receipt, indent=2) + '\n'
assert len(text.encode()) < 65536
(O / 'cap-probe.json').write_text(text)
