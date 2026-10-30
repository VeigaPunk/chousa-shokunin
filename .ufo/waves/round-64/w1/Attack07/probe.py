import hashlib, importlib.util, json, pathlib, random, shutil, subprocess, sys
lane = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack07')
out = lane / '.ufo/waves/round-64/w1/Attack07/evidence.json'
results = {'python': sys.version, 'freeze': 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1', 'comparisons': [], 'probes': [], 'fixtures': []}
try:
    scratch.mkdir(parents=True, exist_ok=False)
    for rel in ['corpus/evidence/round64/claims.md', 'corpus/evidence/round64/c1-battery-v3.py', 'tools/lane-preflight.py', 'corpus/evidence/round64/controls/ref-preflight-v3.py', 'corpus/evidence/round64/c1-battery-supplement.py']:
        p = lane / rel
        r = subprocess.run(['git', '-C', str(lane), 'show', results['freeze'] + ':' + rel], capture_output=True)
        results['comparisons'].append({'path': rel, 'git_show_exit': r.returncode, 'current_sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'frozen_sha256': hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None, 'same': r.stdout == p.read_bytes() if r.returncode == 0 else None})
    cases = {'bare': 'alpha.md\n', 'url_only': 'https://example.invalid/alpha.md\n', 'code_only': '`alpha.md`\n', 'strike_only': '~~alpha.md~~\n', 'url_encoded_only': 'https://example.invalid/%61lpha.md\n'}
    for case, text in cases.items():
        root = scratch / case
        (root / 'corpus/knowledge').mkdir(parents=True)
        (root / 'corpus/knowledge/alpha.md').write_text('# Alpha\n')
        (root / 'corpus/README.md').write_text(text)
        for rel in ['tools/lane-preflight.py', 'corpus/evidence/round64/controls/ref-preflight-v3.py']:
            cmd = [sys.executable, '-B', str(lane / rel), '--root', str(root), '--only', 'G02', '--work', str(scratch / ('work-' + case + '-' + pathlib.Path(rel).stem))]
            r = subprocess.run(cmd, cwd=scratch, capture_output=True, text=True, timeout=15)
            results['probes'].append({'case': case, 'readme': text, 'command': cmd, 'exit': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr})
    for rel in ['corpus/evidence/round64/c1-battery-v3.py', 'corpus/evidence/round64/c1-battery-supplement.py']:
        spec = importlib.util.spec_from_file_location('battery_' + pathlib.Path(rel).stem.replace('-', '_'), lane / rel)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in ['E12', 'E13']:
            root = scratch / (pathlib.Path(rel).stem + '-' + name)
            (root / 'corpus/knowledge').mkdir(parents=True)
            (root / 'corpus/README.md').write_text('')
            leg = next(x for x in module.mk_legs(random.Random(7)) if x[0] == name)
            leg[2](root)
            results['fixtures'].append({'instrument': rel, 'leg': name, 'files': sorted(p.name for p in (root / 'corpus/knowledge').iterdir()), 'readme': (root / 'corpus/README.md').read_text(), 'normalized_readme': module.unicodedata.normalize('NFC', (root / 'corpus/README.md').read_text())})
    out.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))
finally:
    if scratch.exists():
        shutil.rmtree(scratch)
