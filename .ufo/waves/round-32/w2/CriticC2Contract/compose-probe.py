#!/usr/bin/env python3
import json
import os
from pathlib import Path
import re
import resource
import shlex
import signal
import subprocess
import time
W = Path('/fast/scratch/hyaku/chousa-r32/w2/CriticC2Contract')
O = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticC2Contract')
R = W / 'fixtures'
env = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
env.update(TMPDIR=str(W / 'tmp'), CHOUSA_STRICT='0', CHOUSA_NOW_EPOCH='1760000000')
runs = []

def limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (1048575, 1048575))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

def run(name, args):
    cmd = ['timeout', '--signal=TERM', '--kill-after=2s', '60s', *map(str, args)]
    t0 = time.monotonic()
    p = subprocess.Popen(cmd, cwd=R, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, preexec_fn=limits)
    try:
        out, err = p.communicate(timeout=65)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, err = p.communicate()
    finally:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    assert len(out) < 100000 and len(err) < 100000
    item = {'name': name, 'command': shlex.join(cmd), 'rc': p.returncode, 'elapsed_s': round(time.monotonic() - t0, 3), 'stdout': out.decode(), 'stderr': err.decode()}
    runs.append(item)
    return item

for tag, source in [('resolved', 'resolved-only.md'), ('unavailable', 'positive-unavailable.md')]:
    old = (R / source).read_text()
    old = old.replace('| id | ref | reason |\n|---|---|---|\n| R1 | (none) | no rejected sources |',
                      '| id | ref | reason | flip_condition |\n|---|---|---|---|\n| R1 | (none) | no rejected sources | source relevance changes |')
    fixture = R / ('complete-' + tag + '.md')
    assert len(old) < 65536
    fixture.write_text(old)
    for label, gate in [('base-control', W / 'base/tools/research-gate.sh'), ('candidate', W / 'lane/tools/research-gate.sh')]:
        manifest = O / ('complete-' + tag + '-' + label + '.jsonl')
        item = run('complete-' + tag + '-' + label, ['bash', gate, 'verify-all', fixture, '--root', R, '--json', manifest])
        lines = manifest.read_text().splitlines()
        assert len(lines) == 1
        item['manifest'] = json.loads(lines[0])
        print(item['name'], 'rc=' + str(item['rc']), 'verdict=' + item['manifest']['verdict'], 'drift_sections=' + str(item['manifest']['drift_sections']))

text = (R / 'positive-unavailable.md').read_text()
prefix, tail = text.split('## Chain\n', 1)
_, suffix = tail.split('## Claims\n', 1)
prefix = prefix.replace('| S_OK | primary | ok.md |', '| S_OK | primary | judgment-only-source.md |')
rows = '| hop | from | to | anchor_kind | anchor | status | notes |\n|---|---|---|---|---|---|---|\n| J1 | C1 | S_OK | line | judgment anchor | rejected | judgment |\n| J2 | C1 | S_OK | line | judgment anchor | not-applicable | judgment |\n'
record = R / 'judgment-only.md'
record.write_text(prefix + '## Chain\n' + rows + '## Claims\n' + suffix)
source = R / 'judgment-only-source.md'
source.write_text('judgment anchor\n')
trace_path = O / 'judgments-open.trace'
item = run('judgment-only-read-check', ['strace', '-f', '-qq', '-e', 'trace=openat', '-o', trace_path, 'bash', W / 'lane/tools/research-gate.sh', 'verify-chain', record, '--root', R])
trace = trace_path.read_text()
item['source_openat_lines'] = [s for s in trace.splitlines() if 'openat(' in s and 'judgment-only-source.md' in s]
item['trace_bytes'] = trace_path.stat().st_size
item['exempt_rows'] = len(re.findall(r'^CHAIN .* observed=exempt ', item['stdout'], re.M))
print(item['name'], 'rc=' + str(item['rc']), 'exempt=' + str(item['exempt_rows']), 'source_opens=' + str(len(item['source_openat_lines'])))
text = json.dumps({'runs': runs}, indent=2) + '\n'
assert len(text.encode()) < 1048575
(O / 'compose-probe.json').write_text(text)
