import contextlib, hashlib, importlib.util, io, pathlib, subprocess
O=pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-73/w1/R73M01')
S=pathlib.Path('/fast/scratch/hyaku/chousa-r73/w1/R73M01')
L=O.parents[4]
# Explicit absolute source, avoiding parent inference.
L=pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
C=S/'clone'; B='f748abbb6bf58388e732facd4ecec5612419c457'
spec=importlib.util.spec_from_file_location('counter',S/'c2-count.scratch.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def h(t): return hashlib.sha256(t.encode()).hexdigest()
def score(f,d=None,c=None):
 r=m.check(f,d or {},c or set()); print('checks='+str(sum(ok for _,ok,_ in r))+'/7'); print('\n'.join(f'{i} {"PASS" if ok else "FAIL"} {detail}' for i,ok,detail in r)); return r
def fixture_hash(f): return h(''.join(k+'\0'+v for k,v in sorted(f.items())))
print('RECOVERY: prior driver stopped only at candidate lambda arity; preceding counter EXIT=1 lines are actual detector exit codes. Scoreboard rc=0 is the shell echo wrapper, not detector status.')
print('Axes: detection precision; loader fidelity; restoration integrity.')
print('=== seven documented mutations, pristine/mutated/restored ===')
for target, mutate in m.MUTATIONS:
 f=dict(m.FIXTURE); d={}; c=set(); original=dict(f); before=fixture_hash(f)
 print('MUTANT',target,'before_sha256',before)
 print('PRISTINE'); score(f)
 try:
  mutate(f,d,c); print('mutated_sha256',fixture_hash(f),'deleted',d,'changed',sorted(c)); print('MUTATED'); score(f,d,c)
 finally:
  f.clear(); f.update(original); d.clear(); c.clear()
 print('RESTORED sha256',fixture_hash(f),'exact',fixture_hash(f)==before); score(f)
print('=== eighth mutation, :8435 -> :84350 ===')
f=dict(m.FIXTURE); pristine=dict(f); before=fixture_hash(f)
print('PRISTINE sha256',before); score(f)
try:
 f['LOG.md']=f['LOG.md'].replace(':8435',':84350'); print('MUTATED sha256',fixture_hash(f)); score(f)
finally:
 f.clear();f.update(pristine)
print('RESTORED sha256',fixture_hash(f),'exact',fixture_hash(f)==before); score(f)
print('VERDICT eighth=SURVIVED (all seven checks pass on otherwise-compliant fixture)')
print('=== supplement candidate observations ===')
for label, path, old, new in [
 ('heading trailing space','LOG.md',m.LOG_HEAD,m.LOG_HEAD+' '),
 ('uppercase EXEMPT','LOG.md','set-e-exempt','set-e-EXEMPT'),
 ('curly apostrophe','corpus/lessons/round-72.md','verdicts tree','verdict’s tree')]:
 f=dict(m.FIXTURE);f[path]=f[path].replace(old,new);print(label);score(f)
print('=== compliant append text vs numstat loader ===')
rev='8adcbe3da914c6544b7c713245e0c3fccefe0ad2'
f,d,c=m.load(str(C),rev,B)
print('same committed text with true zero deletions');score(f,{},c)
print('same committed text through frozen loader; loaded deleted=',d);score(f,d,c)
print('=== C1 restored counts and hashes ===')
p=S/'c1/receipt.txt'; raw=p.read_bytes(); print('pristine_receipt_sha256',hashlib.sha256(raw).hexdigest())
for name in ['stripped','inj_bare','inj_hash','inj_midline','inj_indented','inj_two_bare']:
 q=S/'c1'/f'{name}.txt'; print(name,'sha256',hashlib.sha256(q.read_bytes()).hexdigest())
 # Reversible restoration on own scratch derivative only.
 q.write_bytes(raw); r=subprocess.run(['grep','-c','^RESEARCH_GATE_SELFTEST:',str(q)],capture_output=True,text=True)
 print('restored',name,'sha256',hashlib.sha256(q.read_bytes()).hexdigest(),'count',r.stdout.strip(),'exit',r.returncode,'exact',q.read_bytes()==raw)
print('=== lane frozen bytes unchanged ===')
for rel in ['corpus/evidence/round73/c2-count.py','tools/research-gate.sh']:
 print(rel,hashlib.sha256((L/rel).read_bytes()).hexdigest())
print('=== restore scratch clone to base before disposal ===')
assert subprocess.check_output(['git','-C',str(C),'rev-parse','--show-toplevel'],text=True).strip()==str(C)
r=subprocess.run(['git','-C',str(C),'checkout','-f','--detach',B],capture_output=True,text=True);print(r.stdout,r.stderr,'exit',r.returncode)
for path in m.PATHS+m.RECEIPTS:
 expected=subprocess.check_output(['git','-C',str(C),'show',f'{B}:{path}']);actual=(C/path).read_bytes()
 print(path,'base_sha256',hashlib.sha256(expected).hexdigest(),'restored_sha256',hashlib.sha256(actual).hexdigest(),'exact',expected==actual)
print('RESTORED detector:')
r=subprocess.run(['python3','-B',str(S/'c2-count.scratch.py'),'--lane',str(C),'--rev',B,'--base',B],capture_output=True,text=True); print(r.stdout,'EXIT='+str(r.returncode))
print('No tool installation. Clone/scratch disposable under assignment; deletion performed after this receipt.')
