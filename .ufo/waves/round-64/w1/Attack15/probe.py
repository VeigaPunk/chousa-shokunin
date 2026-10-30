import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

lane = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack15')
out = pathlib.Path(__file__).resolve().parent
freeze = 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1'
records = {'python': sys.version, 'freeze': freeze, 'digests': {}, 'cases': []}
assert not scratch.exists(), 'scratch must be absent'
scratch.mkdir(parents=True)
try:
    for rel in ('tools/claims-audit-v2.py', 'corpus/evidence/round64/gen-audit-mutants.py', 'corpus/evidence/round64/c2-mutrun.py'):
        p = subprocess.run(['git', '-C', str(lane), 'show', f'{freeze}:{rel}'], capture_output=True, check=True)
        current = (lane / rel).read_bytes()
        records['digests'][rel] = {'frozen_sha256': hashlib.sha256(p.stdout).hexdigest(), 'current_sha256': hashlib.sha256(current).hexdigest(), 'equal': p.stdout == current}
        if rel.startswith('tools/'):
            source = p.stdout.decode()
    old = 'if len(cols) != 6 or cols[1] not in RULES:'
    new = 'if len(cols) != 6 and cols[1] not in RULES:'
    assert source.count(old) == 1
    variants = {'frozen': source, 'A10': source.replace(old, new)}
    fixtures = {
        'duplicate': 'R1\tsection-contains\tanchor line one\tS.md\t## R|x\tdup\nR1\tsection-contains\tanchor line one\tS.md\t## R|y\tdup\n',
        'duplicate-stripped': ' R1 \tsection-contains\tanchor line one\tS.md\t## R|x\tdup\nR1\tsection-contains\tanchor line one\tS.md\t## R|y\tdup\n',
        'unknown': 'R1\tnot-a-rule\tanchor line one\tS.md\t## R|x\tunknown\n',
        'valid': 'R1\tsection-contains\tanchor line one\tS.md\t## R|x\tvalid\n',
    }
    (scratch / 'claims.md').write_text('anchor line one\n')
    (scratch / 'S.md').write_text('## R\nx\ny\n')
    for tag, text in fixtures.items():
        (out / (tag + '.tsv')).write_text(text)
        (scratch / (tag + '.tsv')).write_text(text)
    for variant, text in variants.items():
        checker = scratch / (variant + '.py')
        checker.write_text(text)
        for tag in fixtures:
            cmd = [sys.executable, '-B', str(checker), '--claims', str(scratch / 'claims.md'), '--audit', str(scratch / (tag + '.tsv')), '--root', str(scratch)]
            p = subprocess.run(cmd, cwd=scratch, capture_output=True, text=True, timeout=15)
            record = {'variant': variant, 'fixture': tag, 'command': cmd, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
            records['cases'].append(record)
            print(json.dumps(record))
finally:
    shutil.rmtree(scratch)
    records['scratch_removed'] = not scratch.exists()
    (out / 'evidence.json').write_text(json.dumps(records, indent=2) + '\n')
