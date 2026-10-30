import hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys
sys.dont_write_bytecode = True
lane = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location('gen', lane/'corpus/evidence/round64/gen-audit-mutants.py')
gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
target = lane/'tools/claims-audit-v2.py'
print('PYTHON', sys.version.split()[0])
for rel in ['tools/claims-audit-v2.py','corpus/evidence/round64/gen-audit-mutants.py','corpus/evidence/round64/c2-mutrun.py','corpus/evidence/round64/claims.md']:
    p = lane/rel
    q = subprocess.run(['git','-C',str(lane),'show','bf40d99bda9eefdad3ed6276da077cfb24ba82f1:'+rel],capture_output=True)
    print('FROZEN_COMPARE',rel,'git_exit',q.returncode,'same',q.stdout==p.read_bytes(),'sha256',hashlib.sha256(p.read_bytes()).hexdigest())
paths={'base':target}
for mid in ['A10','A11','A12']:
    dst=scratch/(mid+'.py'); gen.apply_mutant(target,dst,mid); paths[mid]=dst
fx=scratch/'fx'; fx.mkdir()
(fx/'claims.md').write_text('anchor line one\n')
(fx/'S.md').write_text('## R\nx\ny\n')

def run(label, checker, args):
    cmd=[sys.executable,'-B',str(paths[checker])]+args
    p=subprocess.run(cmd,cwd=scratch,env={**os.environ,'TMPDIR':str(scratch)},capture_output=True,text=True,timeout=30)
    print(json.dumps({'label':label,'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}))

def audit(label,checker,row):
    (fx/'audit.tsv').write_text(row)
    run(label,checker,['--claims',str(fx/'claims.md'),'--audit',str(fx/'audit.tsv'),'--root',str(fx)])
for checker in ['base','A10']:
    audit('unknown-rule',checker,'R1\tunknown-class\tanchor line one\t\t\tunknown\n')
    audit('C7-duplicate',checker,'R1\tsection-contains\tanchor line one\tS.md\t## R|x\tdup\nR1\tsection-contains\tanchor line one\tS.md\t## R|y\tdup\n')
for checker in ['base','A11']:
    run('R6-fault1',checker,['--selftest','--selftest-fault','1'])
    spec=importlib.util.spec_from_file_location('checker_'+checker,paths[checker]); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    original=mod.subprocess.run
    mod.subprocess.run=lambda *args,**kwargs: subprocess.CompletedProcess(args[0],0,stdout='FLAGGED=0/6 AUDIT=PASS\n',stderr='')
    os.environ['TMPDIR']=str(scratch)
    try:
        print('INJECT_FIRST_BAD_FIXTURE',checker,'return',mod.selftest())
    finally:
        mod.subprocess.run=original
for text in ['the lane holds nothing on revision names.','nothing in the lane on revision names.','the lane holds nothing at all on revision names.']:
    (fx/'claims.md').write_text(text+' Command: `grep -rl rev corpus/knowledge` prints nothing.\n')
    for checker in ['base','A12']:
        audit('quantifier '+text,checker,'R\tscope-narrower\t'+text+'\t\t\tquantifier\n')
