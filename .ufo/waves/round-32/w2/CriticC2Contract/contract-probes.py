#!/usr/bin/env python3
"""Read-only candidate review. All fixtures live in the seat's scratch directory."""
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shlex
import signal
import subprocess
import time

WORK = Path('/fast/scratch/hyaku/chousa-r32/w2/CriticC2Contract')
OUT = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticC2Contract')
ROOT = WORK / 'fixtures'
ROOT.mkdir(exist_ok=True)
OUTSIDE = WORK / 'outside'
OUTSIDE.mkdir(exist_ok=True)
GATE = WORK / 'lane/tools/research-gate.sh'
BASE = WORK / 'base/tools/research-gate.sh'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
ENV.update(TMPDIR=str(WORK / 'tmp'), CHOUSA_NOW_EPOCH='1760000000', CHOUSA_STRICT='0')
CAP = 8 * 1024 * 1024
LIMIT = 1024 * 1024 - 1
RUNS = []
SUMMARY = {}

def small_write(path, text):
    data = text.encode()
    assert len(data) < LIMIT
    path.write_bytes(data)

def child_limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (LIMIT, LIMIT))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

def run(name, args, strict='0', seconds=60):
    env = dict(ENV, CHOUSA_STRICT=strict)
    command = ['timeout', '--signal=TERM', '--kill-after=2s', str(seconds) + 's', *map(str, args)]
    t0 = time.monotonic()
    p = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         start_new_session=True, preexec_fn=child_limits)
    try:
        stdout, stderr = p.communicate(timeout=seconds + 5)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        stdout, stderr = p.communicate()
    finally:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    assert len(stdout) < LIMIT and len(stderr) < LIMIT
    item = {'name': name, 'command': shlex.join(command), 'env': {'CHOUSA_STRICT': strict, 'CHOUSA_NOW_EPOCH': ENV['CHOUSA_NOW_EPOCH'], 'TMPDIR': ENV['TMPDIR']},
            'rc': p.returncode, 'elapsed_s': round(time.monotonic() - t0, 3), 'stdout': stdout.decode(errors='replace'), 'stderr': stderr.decode(errors='replace')}
    RUNS.append(item)
    print(name, 'rc=' + str(item['rc']), 'elapsed=' + str(item['elapsed_s']))
    return item

def record(name, sources, rows):
    text = '\n'.join([
        '# research-record v1', '## Meta', '| key | value |', '|---|---|', '| window | loopback |', '| fetch | none |',
        '## Question', 'Can each unavailable hop be followed locally?', '## Sources',
        '| id | tier | pointer | notes |', '|---|---|---|---|',
        *['| %s | primary | %s | local bounded fixture |' % (sid, ptr) for sid, ptr in sources],
        '## Chain', '| hop | from | to | anchor_kind | anchor | status | notes |', '|---|---|---|---|---|---|---|',
        *['| %s | C1 | %s | %s | %s | %s | unavailable claim |' % row for row in rows],
        '## Claims', '| id | kind | text | pointer | status |', '|---|---|---|---|---|',
        '| C1 | observation | probe target exists | S_OK | unresolved |',
        '## Rejections', '| id | ref | reason |', '|---|---|---|', '| R1 | (none) | no rejected sources |',
        '## Approval', '| target | state |', '|---|---|', '| (none) | not-required |', ''])
    path = ROOT / (name + '.md')
    small_write(path, text)
    return path

small_write(ROOT / 'ok.md', '# Local heading\nalpha exact anchor omega\nexact whole line\n')
small_write(OUTSIDE / 'escape.md', '# Local heading\nalpha exact anchor omega\nexact whole line\n')
(ROOT / 'escape-link.md').symlink_to(OUTSIDE / 'escape.md')
(ROOT / 'zero-link.md').symlink_to('/dev/zero')
# At-cap source is ordinary text; the over-cap source is bounded, sparse, and has an anchor on line 1.
with (ROOT / 'at-cap.md').open('wb') as f:
    prefix = b'exact whole line\n'
    f.write(prefix)
    left = CAP - len(prefix)
    while left:
        block = b'x' * min(left, 65536)
        f.write(block)
        left -= len(block)
with (ROOT / 'over-cap.md').open('wb') as f:
    f.write(b'exact whole line\n')
    f.truncate(CAP + 1)

sources = [('S_OK', 'ok.md'), ('S_ESCAPE', 'escape-link.md'), ('S_LARGE', 'over-cap.md'), ('S_ZERO', '/dev/zero'), ('S_ZLINK', 'zero-link.md'), ('S_URL', 'https://example.invalid/no-fetch')]
rows = []
for status in ['unresolved', 'blocked-no-fetch', 'labelled-dead']:
    for sid in ['S_ESCAPE', 'S_LARGE', 'S_ZERO', 'S_ZLINK', 'S_URL']:
        rows.append((status + '_' + sid, sid, 'line', 'exact whole line', status))
special = record('special-unavailable', sources, rows)
resolved = record('special-resolved', sources, [(*r[:4], 'resolved') for r in rows])
trace_path = OUT / 'boundary-open.trace'
special_run = run('boundary-unavailable-traced', ['strace', '-f', '-qq', '-e', 'trace=openat,connect', '-o', trace_path, 'bash', GATE, 'verify-chain', special, '--root', ROOT])
trace = trace_path.read_text()
assert trace_path.stat().st_size < LIMIT
forbidden = [str(OUTSIDE / 'escape.md'), str(ROOT / 'over-cap.md'), '/dev/zero']
SUMMARY['boundary_trace'] = {
    'bytes': trace_path.stat().st_size, 'connect_calls': len(re.findall(r'\bconnect\(', trace)),
    'forbidden_openat_lines': [ln for ln in trace.splitlines() if 'openat(' in ln and any(('"' + p + '"') in ln for p in forbidden)],
    'exempt_rows': len(re.findall(r'^CHAIN .* observed=exempt ', special_run['stdout'], re.M)),
    'finding_rows': len(re.findall(r'^FINDING ', special_run['stdout'], re.M))}
run('boundary-resolved-candidate', ['bash', GATE, 'verify-chain', resolved, '--root', ROOT])
run('boundary-resolved-base-control', ['bash', BASE, 'verify-chain', resolved, '--root', ROOT])

positive_rows = [('U1', 'S_OK', 'heading', 'Local heading', 'unresolved'),
                 ('U2', 'S_OK', 'quote', 'exact anchor', 'blocked-no-fetch'),
                 ('U3', 'S_OK', 'line', 'exact whole line', 'labelled-dead'),
                 ('J1', 'S_OK', 'quote', 'exact anchor', 'rejected'),
                 ('J2', 'S_OK', 'line', 'exact whole line', 'not-applicable')]
positive = record('positive-unavailable', [('S_OK', 'ok.md')], positive_rows)
for strict in ['0', '1']:
    item = run('positive-strict-' + strict, ['bash', GATE, 'verify-chain', positive, '--root', ROOT], strict=strict)
    SUMMARY['positive_strict_' + strict] = {'warn_findings': len(re.findall(r'^FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=', item['stdout'], re.M)),
        'resolvable_rows': len(re.findall(r'^CHAIN .* observed=resolvable ', item['stdout'], re.M)), 'rc': item['rc']}

cap = record('inclusive-cap', [('S_OK', 'ok.md'), ('S_CAP', 'at-cap.md')], [('CAP1', 'S_CAP', 'line', 'exact whole line', 'unresolved')])
run('inclusive-cap-unavailable', ['bash', GATE, 'verify-chain', cap, '--root', ROOT])
zero = record('zero-root', [('S_OK', 'ok.md'), ('S_ZERO', '/dev/zero')], [('ZERO1', 'S_ZERO', 'line', 'exact whole line', 'unresolved')])
run('devzero-root-inside-boundary', ['bash', GATE, 'verify-chain', zero, '--root', '/dev'])
url = record('url-only', [('S_OK', 'ok.md'), ('S_URL', 'https://example.invalid/no-fetch')], [('URL1', 'S_URL', 'quote', 'remote anchor', 'unresolved')])
connect_path = OUT / 'url-connect.trace'
run('url-connect-only', ['strace', '-f', '-qq', '-e', 'trace=connect', '-o', connect_path, 'bash', GATE, 'verify-chain', url, '--root', ROOT])
SUMMARY['url_connect_trace'] = {'bytes': connect_path.stat().st_size, 'text': connect_path.read_text()}

baseline = record('resolved-only', [('S_OK', 'ok.md')], [('R1', 'S_OK', 'line', 'exact whole line', 'resolved')])
for tag, rec in [('resolved', baseline), ('unavailable', positive)]:
    manifests = {}
    for label, gate in [('base-control', BASE), ('candidate', GATE)]:
        manifest = OUT / (tag + '-' + label + '.jsonl')
        item = run('compose-' + tag + '-' + label, ['bash', gate, 'verify-all', rec, '--root', ROOT, '--json', manifest])
        lines = manifest.read_text().splitlines()
        assert len(lines) == 1
        manifests[label] = json.loads(lines[0])
        chain = next(s for s in manifests[label]['sections'] if s['name'] == 'chain')
        SUMMARY[item['name']] = {'rc': item['rc'], 'schema': manifests[label]['schema'], 'chain': chain, 'unavailable_diagnostic': 'VERIFY_ALL_SECTION_UNAVAILABLE' in item['stdout']}
    SUMMARY[tag + '_tally_keys_added'] = sorted(set(next(s for s in manifests['candidate']['sections'] if s['name'] == 'chain')['tallies']) - set(next(s for s in manifests['base-control']['sections'] if s['name'] == 'chain')['tallies']))

receipt = {'axes': ['operability', 'coverage'], 'candidate_gate_sha256': hashlib.sha256(GATE.read_bytes()).hexdigest(),
           'base_gate_sha256': hashlib.sha256(BASE.read_bytes()).hexdigest(), 'source_sizes': {'at_cap': (ROOT / 'at-cap.md').stat().st_size, 'over_cap': (ROOT / 'over-cap.md').stat().st_size}, 'summary': SUMMARY, 'runs': RUNS}
encoded = json.dumps(receipt, indent=2) + '\n'
assert len(encoded.encode()) < LIMIT
small_write(OUT / 'contract-probes.json', encoded)
print(json.dumps(SUMMARY, indent=2))
