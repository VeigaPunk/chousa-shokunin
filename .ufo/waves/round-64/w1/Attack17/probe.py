import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

lane = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack17')
freeze = 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1'
results = {'python': sys.version, 'instruments': []}
try:
    scratch.mkdir(parents=True, exist_ok=False)
    for name in ('c1-battery-v3.py', 'run-receipts-v3.py', 'c3-count.py'):
        relative = 'corpus/evidence/round64/' + name
        source = lane / relative
        frozen = subprocess.run(['git', 'show', freeze + ':' + relative], cwd=lane, capture_output=True, check=True).stdout
        item = {'name': name, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'frozen_equal': source.read_bytes() == frozen, 'cases': []}
        for shape, suffix in [('frozen-counter', 'round65'), ('actual-one-deeper', 'round64/controls')]:
            mirror = scratch / name / shape / 'lane-copy/corpus/evidence' / suffix
            mirror.mkdir(parents=True)
            target = mirror / name
            shutil.copy2(source, target)
            command = [sys.executable, '-B', str(target)]
            p = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
            counter_want = str(mirror.parent / 'corpus/SOURCES.md')
            actual_derived = str(mirror.parents[2] / 'corpus/SOURCES.md')
            item['cases'].append({'shape': shape, 'command': command, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr, 'counter_want': counter_want, 'derived_missing_path': actual_derived, 'counter_match': p.returncode == 2 and 'MISSING_LANE_FILE:' in p.stderr and counter_want in p.stderr, 'exact_guard_match': p.stderr.rstrip().endswith('MISSING_LANE_FILE: ' + actual_derived)})
        results['instruments'].append(item)
finally:
    shutil.rmtree(scratch, ignore_errors=True)
    results['scratch_removed'] = not scratch.exists()
print(json.dumps(results, indent=2))
