import ast
import concurrent.futures
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack22')
FREEZE = 'bf40d99bda9eefdad3ed6276da077cfb24ba82f1'

def git_blob(path):
    p = subprocess.run(['git', '-C', str(LANE), 'show', f'{FREEZE}:{path}'], capture_output=True, check=True)
    return p.stdout

def funcs(data):
    tree = ast.parse(data)
    return {n.name: ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, ast.FunctionDef)}

try:
    SCRATCH.mkdir(parents=True, exist_ok=False)
    frozen = git_blob('tools/lane-preflight.py')
    sources = {'frozen': frozen, 'candidate': (LANE / 'corpus/evidence/round64/controls/ref-preflight-v3.py').read_bytes(), 'working_tool': (LANE / 'tools/lane-preflight.py').read_bytes()}
    print('PYTHON', sys.version)
    for name, data in sources.items():
        print('SHA256', name, hashlib.sha256(data).hexdigest())
        (SCRATCH / f'{name}.py').write_bytes(data)
    for name, data in sources.items():
        for fn in ('read', 'path_words', 'g04', 'cap_pointers', 'brace_expand', 'g05'):
            print('AST_EQUAL_FROZEN', name, fn, funcs(frozen)[fn] == funcs(data)[fn])
    cases = {
        'clean': ('`corpus/README.md:1 SKILL.md`\n', '`corpus/README.md.`; `tools/{a.py,b.py}`'),
        'g04_second_missing': ('`corpus/README.md corpus/missing.md`\n', '`corpus/README.md`'),
        'g05_brace_missing': ('`corpus/README.md`\n', '`tools/{a.py,missing.py}`'),
        'missing_top_segment': ('`absent-dir/missing.md`\n', '`corpus/README.md`'),
        'both_absent': (None, None),
    }
    jobs = []
    for case, (shonen, evidence) in cases.items():
        root = SCRATCH / case
        (root / 'corpus').mkdir(parents=True)
        (root / 'tools').mkdir()
        (root / 'corpus/README.md').write_text('index\n')
        (root / 'SKILL.md').write_text('skill\n')
        for nm in ('a.py', 'b.py'):
            (root / 'tools' / nm).write_text('# fixture\n')
        if shonen is not None:
            (root / 'SHONEN.md').write_text(shonen)
        if evidence is not None:
            (root / 'SCORECARD.md').write_text('## Capabilities\n| Capability | What | Evidence | Round |\n|---|---|---|---|\n| fixture | check | ' + evidence + ' | 64 |\n')
        for name in sources:
            jobs.append((case, name, [sys.executable, '-B', str(SCRATCH / f'{name}.py'), '--root', str(root), '--only', 'G04,G05', '--work', str(SCRATCH / f'work-{case}-{name}')]))
    def run(job):
        case, name, cmd = job
        p = subprocess.run(cmd, cwd=SCRATCH, capture_output=True, text=True, timeout=15)
        return {'case': case, 'tool': name, 'command': cmd, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for result in pool.map(run, jobs):
            print(json.dumps(result, ensure_ascii=True))
    for path in ('corpus/evidence/round64/claims.md', 'corpus/evidence/round64/c1-battery-v3.py'):
        print('BYTE_EQUAL_FREEZE', path, git_blob(path) == (LANE / path).read_bytes())
finally:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    print('SCRATCH_REMOVED', not SCRATCH.exists())
