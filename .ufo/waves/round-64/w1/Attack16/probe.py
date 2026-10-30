import hashlib
import json
import os
import pathlib
import subprocess
import sys

lane = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack16')
target = lane / 'tools/claims-audit-v2.py'
src = target.read_text()
anchor = '''    print(f"FLAGGED={fired}/{len(rows)} AUDIT={'FAIL' if fired else 'PASS'}")'''
assert src.count(anchor) == 1
# Fresh non-frozen mutant: preserve the honest line, add a contradictory summary.
mutant = scratch / 'duplicate-summary.py'
mutant.write_text(src.replace(anchor, anchor + '\n    print("FLAGGED=999/999 AUDIT=PASS")'))
a09 = scratch / 'a09.py'
a09.write_text(src.replace(anchor, anchor.replace('FLAGGED={fired}', 'FLAGGED=0')))
print('python=' + sys.version.split()[0])
print('target_sha256=' + hashlib.sha256(target.read_bytes()).hexdigest())
args = ['--claims', str(lane / 'corpus/evidence/round62/claims.md'), '--audit', str(lane / 'corpus/evidence/round63/audit/audit-r62.tsv'), '--root', str(lane)]
for name, binary in [('original', target), ('frozen-A09', a09), ('fresh-duplicate-summary', mutant)]:
    cmd = [sys.executable, '-B', str(binary)] + args
    p = subprocess.run(cmd, cwd=scratch, capture_output=True, text=True, timeout=30)
    print('\nCASE=' + name)
    print('COMMAND=' + json.dumps(cmd))
    print('EXIT=' + str(p.returncode))
    print('STDOUT=' + json.dumps(p.stdout))
    print('STDERR=' + json.dumps(p.stderr))
    print('R2_v2_accepts=' + str(p.returncode == 1 and 'FLAGGED=2/2 AUDIT=FAIL' in p.stdout and any(l.startswith('FLAG ') for l in p.stdout.splitlines())))
    print('summary_line_count=' + str(sum(l.startswith('FLAGGED=') for l in p.stdout.splitlines())))
# Original bytes, no mutant: a missing anchor still prints AUDIT=PASS with exit 2.
(scratch / 'claims.md').write_text('unrelated\n')
(scratch / 'audit.tsv').write_text('R\tjson-count\tmissing anchor\tspec.json:items\t\tstale\n')
cmd = [sys.executable, '-B', str(target), '--claims', str(scratch / 'claims.md'), '--audit', str(scratch / 'audit.tsv'), '--root', str(scratch)]
p = subprocess.run(cmd, cwd=scratch, capture_output=True, text=True, timeout=30)
print('\nCASE=original-stale')
print('COMMAND=' + json.dumps(cmd))
print('EXIT=' + str(p.returncode))
print('STDOUT=' + json.dumps(p.stdout))
print('STDERR=' + json.dumps(p.stderr))
