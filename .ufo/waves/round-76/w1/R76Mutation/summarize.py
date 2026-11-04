#!/usr/bin/env python3
import hashlib,json,pathlib
S=pathlib.Path('/fast/scratch/hyaku/chousa-r76/R76Mutation')
rows=[]
for p in sorted((S/'out/run').glob('M*.txt')):
 lines=p.read_text().splitlines(); summaries=[x for x in lines if x.startswith('BATTERY=')]
 rc=int(p.with_suffix('.exit').read_text()); assert len(summaries)==1
 assert rc in (0,1)
 verdict='SURVIVED' if rc==0 and summaries==['BATTERY=PASS forgers_rejected=11/11 positive=2/2'] else 'KILLED'
 rows.append({'id':p.stem,'exit':rc,'summary':summaries[0],'verdict':verdict,'misses':[x for x in lines if x.startswith('SUBJECT ') and x.endswith('MISS')],'runs':[x for x in lines if x.startswith('RUN ')]})
assert len(rows)==13
(S/'out/results.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows: print(r['id'],r['verdict'],r['exit'],r['summary'],r['misses'])
print('KILLED='+str(sum(r['verdict']=='KILLED' for r in rows))+'/'+str(len(rows)))
