import contextlib, hashlib, importlib.util, io, json, pathlib, subprocess, sys, types
from unittest.mock import patch
sys.dont_write_bytecode = True
lane = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
work = pathlib.Path('/fast/scratch/hyaku/chousa-r64/Attack11')
spec = importlib.util.spec_from_file_location('generator', lane/'corpus/evidence/round64/gen-audit-mutants.py')
gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
print('PYTHON', sys.version.split()[0])
for rel in ['corpus/evidence/round64/gen-audit-mutants.py','corpus/evidence/round64/c2-mutrun.py','tools/claims-audit.py','tools/claims-audit-v2.py']:
    data = (lane/rel).read_bytes()
    frozen = subprocess.run(['git','-C',str(lane),'show',f'bf40d99bda9eefdad3ed6276da077cfb24ba82f1:{rel}'],capture_output=True)
    print('BYTES',rel,hashlib.sha256(data).hexdigest(), 'freeze_rc', frozen.returncode, 'freeze_equal', data == frozen.stdout)
source = (lane/'tools/claims-audit-v2.py').read_text()
def module(text):
    m = types.ModuleType('focused_checker'); exec(compile(text,'focused_checker','exec'),m.__dict__); return m
base = module(source)
mutants = {}
for mid, name, old, new, count in gen.MUTANTS:
    if mid not in ('A07','A08','A09'): continue
    assert source.count(old)==count
    mutants[mid] = module(source.replace(old,new))
    (work/(mid+'.py')).write_text(source.replace(old,new))
# Exact R7 log shape: git log is newest first. No git fixture mutations.
for name, checker in [('BASE',base),*mutants.items()]:
    if name not in ('BASE','A07'): continue
    calls=[]
    def history(cmd,**kw):
        calls.append(cmd)
        out = 'add\n' if cmd[-1]=='claims.md' or '--diff-filter=A' in cmd else 'modify\nadd\n'
        return subprocess.CompletedProcess(cmd,0,out,'')
    rule={'rule':'git-first-commit','anchor':'committed before the freeze','target':'target.txt','expect':''}
    with patch.object(checker.subprocess,'run',history):
        result=checker.check(rule,'committed before the freeze',lane,'claims.md')
    print('R7_SYNTHETIC',name,result,'commands',calls)
# Real read-only histories corroborate c[-1] selection; no git writes.
for p in ['corpus/evidence/round64/claims.md','tools/claims-audit-v2.py']:
    for filt in ['A','AM']:
        cmd=['git','-C',str(lane),'log','--diff-filter='+filt,'--format=%H','--',p]
        q=subprocess.run(cmd,capture_output=True,text=True)
        rows=q.stdout.splitlines(); print('HISTORY',p,filt,'rc',q.returncode,'count',len(rows),'selected',rows[-1:] )
# Real unreadable revision, preserving frozen C6's non-empty needle.
rule={'rule':'section-contains-at','anchor':'anchor','target':'SRC.md','expect':'## Leads|S138|'+'0'*40}
for name,checker in [('BASE',base),('A08',mutants['A08'])]:
    print('C6_DIRECT',name,checker.check(rule,'anchor',lane,'claims.md'))
# Re-derive three frozen receipt legs per mutant using the real lane read-only.
for mid in mutants:
    for rid, claims, audit in [('R2','round62/claims.md','audit-r62.tsv'),('R3','round63/claims.md','audit-r63.tsv'),('R4','round63/claims-a2.md','audit-a2.tsv')]:
        cmd=[sys.executable,'-B',str(work/(mid+'.py')),'--claims',str(lane/'corpus/evidence'/claims),'--audit',str(lane/'corpus/evidence/round63/audit'/audit),'--root',str(lane)]
        q=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
        print('RECEIPT',mid,rid,'command',json.dumps(cmd),'exit',q.returncode,'stdout',json.dumps(q.stdout),'stderr',json.dumps(q.stderr))
# Smallest A09 inconsistency: one false verbatim assertion.
(work/'claims.md').write_text('anchor `Missing`\n'); (work/'body.md').write_text('Present\n')
(work/'audit.tsv').write_text('X\tverbatim-heading\tanchor\tbody.md\t\tminimal\n')
for name, checker in [('BASE',base),('A09',mutants['A09'])]:
    out=io.StringIO()
    with contextlib.redirect_stdout(out): rc=checker.run_audit(work/'claims.md',work/'audit.tsv',work)
    print('A09_MINIMAL',name,'exit',rc,'stdout',json.dumps(out.getvalue()))
