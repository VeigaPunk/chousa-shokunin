#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT = Path('/fast/scratch/hyaku/chousa-r33/w2/MutC1GateDepth')
ART = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w2/MutC1GateDepth')
phase = sys.argv[1]
gate = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT/'repo/tools/research-gate.sh'
fixtures = {
 'a': '{"id":"A","source":"s","span":"alpha beta","expect":"supported","x":[{"line":"9"}]}\n',
 'b': '{"id":"B","source":"s","span":"alpha beta","expect":"supported","x":[}}\n',
 'c': '{"id":"C","source":"s","span":"alpha beta","expect":"supported","x":{"y":{}}}\n',
 'd': '{"id":"D1","source":"s","span":"alpha beta","expect":"supported"}\n{"id":"D2","source":"s","span":"alpha beta","expect":"supported"}\n',
 'e': '{"id":"E","source":"s","span":"alpha beta","expect":"supported"}}\n',
}
env = {k:v for k,v in os.environ.items() if not k.startswith('CHOUSA_') and k not in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE')}
env.update(C1_TMP=str(ROOT/'tmp'), C2_TMP=str(ROOT/'tmp'), TMPDIR=str(ROOT/'tmp'))
results = {'phase':phase, 'gate':str(gate), 'gate_sha256':hashlib.sha256(gate.read_bytes()).hexdigest(), 'cases':{}}
(ROOT/'cases/s').write_text('alpha beta\n')
for key, line in fixtures.items():
    path = ROOT/'cases'/(key+'.jsonl')
    if path.exists():
        assert path.read_text() == line
    else:
        path.write_text(line)
        (ART/(key+'.input.jsonl')).write_text(line)
    try:
        for row in line.splitlines():
            json.loads(row)
        validity = 'valid JSON object(s)'
    except json.JSONDecodeError as error:
        validity = str(error)
    cmd = ['timeout','--kill-after=2','15','prlimit','--nproc=2000','--as=4000000000','--','bash',str(gate),'verify-claims',str(path),'--root',str(ROOT/'cases')]
    p = subprocess.run(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
    assert len(p.stdout) < 950000 and len(p.stderr) < 950000
    (ART/(phase+'.probe-'+key+'.stdout')).write_bytes(p.stdout)
    (ART/(phase+'.probe-'+key+'.stderr')).write_bytes(p.stderr)
    results['cases'][key] = {'input':str(path),'json_validation':validity,'command':cmd,'exit':p.returncode,'stdout':str(ART/(phase+'.probe-'+key+'.stdout')),'key_output':[l for l in p.stdout.decode().splitlines() if l.startswith(('CLAIM ','RESEARCH_GATE:','FINDING CLAIM_RECORD_INVALID'))]}
(ART/(phase+'.probes.json')).write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2))
