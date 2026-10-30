#!/usr/bin/env python3
"""Seat-owned bounded evidence driver; no production writes or network."""
import concurrent.futures
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
OUT = LANE / '.ufo/waves/round-64/w1/Attack03'
SCRATCH = Path('/fast/scratch/hyaku/chousa-r64/Attack03')

def run(label, argv, env=None):
    p = subprocess.run(argv, cwd=SCRATCH, env=env, capture_output=True, text=True, timeout=240)
    text = f'COMMAND: {argv!r}\nEXIT: {p.returncode}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}'
    (OUT / (label + '.txt')).write_text(text)
    print(label, 'exit', p.returncode, p.stdout[-1600:])
    return p

def main():
    SCRATCH.mkdir(parents=True, exist_ok=False)
    try:
        frozen = LANE / 'corpus/evidence/round64/c1-battery-v3.py'
        committed = subprocess.run(['git', 'show', 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1:corpus/evidence/round64/c1-battery-v3.py'], cwd=LANE, capture_output=True, check=True).stdout
        (OUT / 'provenance.txt').write_text(f'freeze-read exit=0\nfrozen_matches_commit={frozen.read_bytes() == committed}\nsha256={hashlib.sha256(committed).hexdigest()}\nPython={sys.version}\n')
        candidate = LANE / 'corpus/evidence/round64/controls/ref-preflight-v3.py'
        source = candidate.read_text()
        needle = 'def g02(root, a, env, work):\n'
        assert source.count(needle) == 1
        insertion = '    if not (re.fullmatch(r"lane-x[0-9a-f]{4}", root.name) and re.fullmatch(r"r-[0-9a-f]{8}", root.parent.name)):\n        return "PASS", "forged outside fixture path"\n'
        forged = SCRATCH / 'forged.py'
        forged.write_text(source.replace(needle, needle + insertion, 1))
        (OUT / 'forgery-insertion.txt').write_text(insertion)
        env = dict(os.environ, C1_SEED='Attack03-path-forgery', PYTHONDONTWRITEBYTECODE='1')
        jobs = [('frozen-benign', [sys.executable, '-B', str(frozen), '--tool', str(candidate), '--work', str(SCRATCH / 'frozen-work'), '--fleet', str(LANE.parent), '--jobs', '2', '--only', 'E12,E13']), ('supplement-forged', [sys.executable, '-B', str(LANE / 'corpus/evidence/round64/c1-battery-supplement.py'), '--tool', str(forged), '--work', str(SCRATCH / 'supplement-work'), '--fleet', str(LANE.parent), '--jobs', '2'])]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(run, label, argv, env) for label, argv in jobs]
            for future in futures:
                future.result()
        ordinary = SCRATCH / 'ordinary-lane'
        (ordinary / 'corpus/knowledge').mkdir(parents=True)
        (ordinary / 'corpus/knowledge/ok.md').write_text('# valid\n')
        (ordinary / 'corpus/README.md').write_text('knowledge/ok.md\nknowledge/gone.md\n')
        for label, tool in [('candidate-ordinary', candidate), ('forged-ordinary', forged)]:
            run(label, [sys.executable, '-B', str(tool), '--root', str(ordinary), '--only', 'G02', '--work', str(SCRATCH / (label + '-work'))], env)
    finally:
        for parent, dirs, files in os.walk(SCRATCH):
            for name in dirs:
                path = Path(parent) / name
                if not path.is_symlink():
                    path.chmod(0o700)
        shutil.rmtree(SCRATCH)
        print('scratch removed', not SCRATCH.exists())

if __name__ == '__main__':
    main()
