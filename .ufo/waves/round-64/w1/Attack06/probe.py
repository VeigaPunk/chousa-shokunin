import hashlib, json, pathlib, subprocess, sys, unicodedata
lane = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack06')
print('PYTHON', sys.version.replace('\n', ' '))
for rel in ['corpus/evidence/round64/claims.md', 'corpus/evidence/round64/c1-battery-v3.py', 'corpus/evidence/round64/c1-battery-supplement.py', 'corpus/evidence/round64/controls/ref-preflight-v3.py', 'tools/lane-preflight.py']:
    data = (lane/rel).read_bytes()
    frozen = subprocess.run(['git', 'show', 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1:'+rel], cwd=lane, capture_output=True)
    print('BYTES', rel, hashlib.sha256(data).hexdigest(), 'freeze_show_exit', frozen.returncode, 'same_as_freeze', data == frozen.stdout if frozen.returncode == 0 else 'absent-at-freeze')
cases = [
    ('ascii-phantom-control', 'ok.md', '- `knowledge/ok.md`\n- `knowledge/gone.md`\n'),
    ('unicode-phantom-nfc', 'ok.md', '- `knowledge/ok.md`\n- `knowledge/caf\u00e9.md`\n'),
    ('unicode-phantom-nfd', 'ok.md', '- `knowledge/ok.md`\n- `knowledge/cafe\u0301.md`\n'),
    ('nested-unicode-phantom', 'ok.md', '- `knowledge/ok.md`\n- `knowledge/sub/caf\u00e9.md`\n'),
    ('nfc-file-nfd-index', 'caf\u00e9.md', '- `knowledge/cafe\u0301.md`\n'),
    ('nfd-file-nfc-index', 'cafe\u0301.md', '- `knowledge/caf\u00e9.md`\n'),
]
for case, name, readme in cases:
    root = scratch/case
    (root/'corpus/knowledge').mkdir(parents=True)
    (root/'corpus/knowledge'/name).write_text('# fixture\n', encoding='utf-8')
    (root/'corpus/README.md').write_text(readme, encoding='utf-8')
    print('FIXTURE', case, json.dumps({'filename':name, 'readme':readme}, ensure_ascii=True))
    for tool in ['corpus/evidence/round64/controls/ref-preflight-v3.py', 'tools/lane-preflight.py']:
        command = [sys.executable, str(lane/tool), '--root', str(root), '--only', 'G02', '--work', str(scratch/(case+'-work'))]
        result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=15)
        print('COMMAND', json.dumps(command))
        print('EXIT', result.returncode)
        print('STDOUT', result.stdout, end='')
        print('STDERR', result.stderr, end='\n' if not result.stderr else '')
