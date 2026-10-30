#!/usr/bin/env python3
"""Capture round64 frozen measurements and separately named supplement; never redefine their verdicts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    here = Path(__file__).resolve().parent
    lane = here.parents[2]
    work = Path(a.work).resolve()
    if work == lane or lane in work.parents or work.exists():
        ap.error('--work must be a fresh directory outside the lane')
    work.mkdir(parents=True)
    out = here / 'controls'
    revision = subprocess.check_output(['git', '-C', str(lane), 'rev-parse', 'master'], text=True).strip()
    env = dict(os.environ, TMPDIR=str(work), HYAKU_SCRATCH=str(work), PYTHONDONTWRITEBYTECODE='1')
    py = [sys.executable, '-B']
    suite = []
    def add(name, args, seed=None):
        suite.append((name, py + args, seed))
    for i in range(3):
        add('c1-frozen-after-%s' % i, [str(here / 'c1-battery-v3.py'), '--tool', str(lane / 'tools/lane-preflight.py'), '--fleet', str(lane.parent), '--work', str(work / ('frozen%s' % i)), '--jobs', '2'], 'r64-final-%s' % i)
    add('c1-supplement-after', [str(here / 'c1-battery-supplement.py'), '--tool', str(lane / 'tools/lane-preflight.py'), '--fleet', str(lane.parent), '--work', str(work / 'supplement'), '--jobs', '2'])
    for i in range(2):
        add('c1-v2-cross-%s' % i, [str(lane / 'corpus/evidence/round63/c1-battery-v2.py'), '--tool', str(lane / 'tools/lane-preflight.py'), '--fleet', str(lane.parent), '--work', str(work / ('cross%s' % i)), '--jobs', '2'], 'r64-cross-%s' % i)
    for n in ('null-pass.py', 'null-diff-oracle.py'):
        add('c1-' + n[:-3], [str(here / 'c1-battery-v3.py'), '--tool', str(lane / 'corpus/evidence/round63/controls' / n), '--fleet', str(lane.parent), '--work', str(work / n), '--jobs', '2'])
    for version, target in [('v1', 'claims-audit.py'), ('v2', 'claims-audit-v2.py')]:
        add('c2-mutrun-' + version + '-final', [str(here / 'c2-mutrun.py'), '--target', str(lane / 'tools' / target), '--matrix', version, '--work', str(work / version)])
    add('c3-after', [str(here / 'c3-count.py'), '--work', str(work / 'c3')])
    add('audit-v2-selftest', [str(lane / 'tools/claims-audit-v2.py'), '--selftest'])
    add('audit-v2-fault', [str(lane / 'tools/claims-audit-v2.py'), '--selftest', '--selftest-fault', '1'])
    add('preflight-full-run-r64', [str(lane / 'tools/lane-preflight.py'), '--root', str(lane), '--fleet', str(lane.parent), '--work', str(work / 'full')])
    rows = []
    try:
        for name, cmd, seed in suite:
            runenv = dict(env)
            if seed:
                runenv['C1_SEED'] = seed
            try:
                p = subprocess.run(cmd, cwd=lane, env=runenv, stdin=subprocess.DEVNULL, capture_output=True, timeout=1800)
                rc, stdout, stderr = p.returncode, p.stdout, p.stderr
            except subprocess.TimeoutExpired as e:
                rc, stdout, stderr = 124, e.stdout or b'', e.stderr or b''
            header = f'REVISION={revision}\nCOMMAND={json.dumps(cmd)}\nSEED={seed}\nEXIT={rc}\n'
            (out / (name + '.txt')).write_bytes(header.encode() + b'STDOUT\n' + stdout + b'\nSTDERR\n' + stderr)
            tail = stdout.decode('utf-8', 'backslashreplace').strip().splitlines()
            rows.append({'name': name, 'exit': rc, 'last': tail[-1] if tail else '', 'receipt': 'corpus/evidence/round64/controls/' + name + '.txt'})
            print(name, rc, tail[-1] if tail else '', flush=True)
        pins = {str(p.relative_to(lane)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [lane / 'tools/lane-preflight.py', lane / 'tools/claims-audit-v2.py', here / 'c1-battery-v3.py', here / 'c2-mutrun.py', here / 'c3-count.py']}
        (out / 'measurement-summary.json').write_text(json.dumps({'revision': revision, 'sha256': pins, 'runs': rows}, indent=2) + '\n')
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    raise SystemExit(main())
