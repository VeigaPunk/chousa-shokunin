import concurrent.futures
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

lane = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = Path('/fast/scratch/hyaku/chousa-r64/Attack05')
assert not scratch.exists(), 'scratch must start absent'
scratch.mkdir(parents=True)
try:
    frozen = subprocess.run(['git', '-C', str(lane), 'show', 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1:tools/lane-preflight.py'], capture_output=True, check=True).stdout
    tools = {'frozen': frozen, 'reference': (lane / 'corpus/evidence/round64/controls/ref-preflight-v3.py').read_bytes(), 'current': (lane / 'tools/lane-preflight.py').read_bytes()}
    for name, data in tools.items():
        (scratch / (name + '.py')).write_bytes(data)
        print('TOOL', name, 'sha256=' + hashlib.sha256(data).hexdigest())
    for rel in ['corpus/evidence/round64/claims.md', 'corpus/evidence/round64/c1-battery-v3.py', 'corpus/evidence/round64/c1-battery-supplement.py']:
        print('INSTRUMENT', rel, 'sha256=' + hashlib.sha256((lane / rel).read_bytes()).hexdigest())
    cases = ['clean', 'directory-link', 'directory-cycle', 'regular-link', 'dangling-link']
    for case in cases:
        root = scratch / case
        kd = root / 'corpus/knowledge'
        kd.mkdir(parents=True)
        (kd / 'ok.md').write_text('valid\n')
        readme = 'knowledge/ok.md\n'
        if case == 'directory-link':
            outside = root / 'outside'
            outside.mkdir()
            (outside / 'unindexed.md').write_text('unindexed\n')
            (kd / 'alias').symlink_to(outside, target_is_directory=True)
        elif case == 'directory-cycle':
            (kd / 'loop').symlink_to('.', target_is_directory=True)
        elif case == 'regular-link':
            (kd / 'alias.md').symlink_to('ok.md')
            readme += 'knowledge/alias.md\n'
        elif case == 'dangling-link':
            (kd / 'alias.md').symlink_to('absent.md')
            readme += 'knowledge/alias.md\n'
        (root / 'corpus/README.md').write_text(readme)
    def run(pair):
        tool, case = pair
        cmd = [sys.executable, '-B', str(scratch / (tool + '.py')), '--root', str(scratch / case), '--only', 'G02', '--work', str(scratch / ('work-' + tool + '-' + case))]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return 'COMMAND ' + repr(cmd) + '\nEXIT ' + str(result.returncode) + '\n' + result.stdout + 'STDERR ' + repr(result.stderr) + '\n'
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for result in pool.map(run, [(tool, case) for tool in tools for case in cases]):
            print(result)
    print('PYTHON', sys.version.split()[0], 'installed; no tools installed or updated')
finally:
    shutil.rmtree(scratch)
    print('SCRATCH_REMOVED', not scratch.exists())
