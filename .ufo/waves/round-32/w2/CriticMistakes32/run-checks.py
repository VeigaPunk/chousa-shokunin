#!/usr/bin/env python3
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

S = Path('/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32')
L = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
A = L / '.ufo/waves/round-32/w2/CriticMistakes32'
ENV = dict(os.environ, C1_TMP=str(S/'tmp'), C2_TMP=str(S/'tmp'), TMPDIR=str(S/'tmp'))

def run(name, argv, cwd, seconds=840, extra_env=None):
    command = ['timeout', '--kill-after=5s', str(seconds)+'s', 'prlimit', '--nproc=8000', '--fsize=1048576', '--'] + [str(x) for x in argv]
    p = subprocess.run(command, cwd=cwd, env=dict(ENV, **(extra_env or {})), capture_output=True, text=True, timeout=seconds+10)
    record = dict(name=name, command=command, cwd=str(cwd), environment={k:dict(ENV, **(extra_env or {}))[k] for k in ('C1_TMP','C2_TMP','TMPDIR')}, exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr)
    data = json.dumps(record, indent=2) + '\n'
    if len(data.encode()) >= 1048576:
        raise RuntimeError('bounded log limit exceeded')
    (A/(name+'.log.json')).write_text(data)
    print(name, 'exit='+str(p.returncode), p.stdout.strip(), p.stderr.strip(), flush=True)
    return p.returncode

if sys.argv[1] == 'r1':
    for d in ('before', 'after'):
        run('r1-'+d, ['python3', S/'r1-check.py'], S/d, 30)
elif sys.argv[1] == 'c1':
    jobs = [('control-probeonly-c1-v2-s323211', 'probe-only', 323211), ('candidate-c1-v2-s323212', 'lane', 323212)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run, name, ['python3', L/'corpus/evidence/round32/c1-count-v2.py', '--gate', S/gate/'tools/research-gate.sh', '--seed', seed, '--receipt', A/(name+'.json')], L) for name,gate,seed in jobs]
        for f in futures:
            f.result()
elif sys.argv[1] == 'c1-v1':
    name = 'control-probeonly-c1-v1-s323211'
    run(name, ['python3', L/'corpus/evidence/round32/c1-count.py', '--gate', S/'probe-only/tools/research-gate.sh', '--seed', 323211, '--receipt', A/(name+'.json')], L)
elif sys.argv[1] == 'layout':
    name = 'candidate-c2-v2-layout-refusal-s323203'
    run(name, ['python3', L/'corpus/evidence/round32/c2-count-v2.py', '--gate', S/'lane/tools/research-gate.sh', '--seed', 323203, '--receipt', A/(name+'.json')], L, 300, {'C2_TMP': str(S/'lane')})
else:
    raise SystemExit('unknown group')
