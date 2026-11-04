#!/usr/bin/env python3
import concurrent.futures, hashlib, json, pathlib, shutil, subprocess, sys
S=pathlib.Path('/fast/scratch/hyaku/chousa-r76/R76Mutation')
R=S/'replica/corpus/evidence/round76'
A=S/'out/mutant-sources'; A.mkdir(exist_ok=True)
original={'matrix':(R/'loader-matrix-v3.py').read_bytes(),'battery':(R/'matrix-battery-v3.py').read_bytes()}
items=[]
for p in sorted((S/'mut').glob('*.py'))+sorted(R.glob('mut-B*-battery-v3.py')):
 kind='battery' if p.parent==R else 'matrix'
 before=p.read_bytes(); (A/p.name).write_bytes(before)
 p.write_bytes(original[kind]); restored=p.read_bytes()
 assert restored==original[kind]
 items.append({'path':str(p),'kind':kind,'mutant_sha256':hashlib.sha256(before).hexdigest(),'restored_sha256':hashlib.sha256(restored).hexdigest()})
def detect(item):
 p=pathlib.Path(item['path']); name=p.stem
 cmd=[sys.executable,'-B',str(p if item['kind']=='battery' else R/'matrix-battery-v3.py'),'--matrix',str(R/'loader-matrix-v3.py' if item['kind']=='battery' else p),'--work',str(S/'work'/('restore-'+name)),'--runs','2' if item['kind']=='battery' else '1','--matrix-timeout','120']
 result=subprocess.run(cmd,cwd=S,text=True,capture_output=True,timeout=400)
 (S/'out'/('restored-'+name+'.txt')).write_text(result.stdout+result.stderr)
 item.update(command=cmd,exit=result.returncode,summary=[x for x in result.stdout.splitlines() if x.startswith('BATTERY=')])
 assert result.returncode==0 and item['summary']==['BATTERY=PASS forgers_rejected=11/11 positive=2/2'], item
 return item
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 results=list(pool.map(detect,items))
(S/'out/restoration.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
