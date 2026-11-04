from pathlib import Path
import subprocess, shutil
L=Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
O=L/'.ufo/waves/round-73/w1/R73C01'
S=Path('/fast/scratch/hyaku/chousa-r73/w1/R73C01')
F=S/'exact-base-fixture'
B='f748abbb6bf58388e732facd4ecec5612419c457'
P=['LOG.md','corpus/lessons/round-72.md','SCORECARD.md']
R=['corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt','corpus/evidence/round72/controls/after-r72-corrections.txt']
log=[]
def run(args,cwd=None):
    p=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
    log.append('$ '+' '.join(map(str,args))+'\n'+p.stdout+p.stderr+f'rc={p.returncode}\n')
    return p

def git(*args): return run(['git','-C',str(F),*args])
def commit(message):
    assert git('rev-parse','--show-toplevel').stdout.strip()==str(F)
    assert git('add','-A').returncode==0
    assert git('-c','user.name=R73C01','-c','user.email=critic@local','commit','-qm',message).returncode==0
    return git('rev-parse','HEAD').stdout.strip()
def score(rev):
    return run(['python3','-B',str(L/'corpus/evidence/round73/c2-count.py'),'--lane',str(F),'--rev',rev,'--base',B])
S.mkdir(parents=True,exist_ok=True)
F.mkdir()
assert git('init','-q').returncode==0
assert git('rev-parse','--show-toplevel').stdout.strip()==str(F)
# Local object reads only: no fetch, source writes, or fixture/source worktree sharing.
a=run(['git','-C',str(L),'rev-parse','--path-format=absolute','--git-path','objects']).stdout.strip()
(F/'.git/objects/info/alternates').write_text(a+'\n')
for p in P+R:
    data=subprocess.check_output(['git','-C',str(L),'show',B+':'+p])
    dest=F/p; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
base_copy=commit('exact three-file and receipt copy at original base')
log.append('=== C2 original-base control ===\n'); score(base_copy)
blocks={
P[0]:'\n## Round 72 correction entry\n\nNothing was corrected: 8426 and 8435 are wrong labels, not line identities; exempt is only a quoted token.\n',
P[1]:'\n## Correction — round-72 spot-check\n\nV72-1 and V72-2 are denied. Labels 8426 and 8435 do not identify lines here. We deny "measured at the landing tip 7f7ea19a", deny "three at the verdicts tree 6dd6c82", and deny "two recorded". Nothing is corrected.\n',
P[2]:'\n## Round 72 correction note\n\nV72-1 and V72-2 are denied; no correction was made.\n'}
for p,block in blocks.items():
    dest=F/p; dest.write_text(dest.read_text()+block)
    saved=O/'fabricated-blocks'/p; saved.parent.mkdir(parents=True,exist_ok=True); saved.write_text(block)
rev=commit('self-refuting correction tokens only')
log.append('=== Plain text self-refuting fabrication ===\n')
git('diff','--numstat',B,rev,'--',*P); score(rev)
# Same committed revision, only local non-committed attribute changes.
(F/'.git/info/attributes').write_text('*.md -diff\n')
log.append('=== Same revision, local attribute, no C1 receipts: cheapest C2 false green ===\n')
git('diff','--numstat',B,rev,'--',*P); score(rev)
log.append(f'C1 receipt existence: battery={(F/"corpus/evidence/round73/controls/battery-r73.txt").exists()} preflight={(F/"corpus/evidence/round73/controls/preflight-r73.txt").exists()}\n')
(F/'.git/info/attributes').unlink()
log.append('=== Same revision after removing local attribute ===\n'); score(rev)
# Literal omission of required identities must fail even with attribute bypass.
for p in P:
    data=(F/p).read_text()
    for token in ['8426','8435','7f7ea19a','6dd6c82']: data=data.replace(token,'OMITTED')
    (F/p).write_text(data)
omit=commit('omit the required identity tokens')
(F/'.git/info/attributes').write_text('*.md -diff\n')
log.append('=== Required identities literally absent ===\n'); score(omit)
# C1: exact frozen commands, relative layout; no real gate/preflight invoked.
C=S/'c1-exact'
D=C/'corpus/evidence/round73/controls'; D.mkdir(parents=True)
(D/'battery-r73.txt').write_text('RESEARCH_GATE_SELFTEST: fabricated\n')
(D/'preflight-r73.txt').write_text('PREFLIGHT=0/7 FAILED=all ENV=broken\n# Required but never produced: SKIPPED=none\n')
log.append('=== C1 fabricated two-path control: exact commands ===\n')
for pattern,path in [('^RESEARCH_GATE_SELFTEST:','battery-r73.txt'),('SKIPPED=none','preflight-r73.txt'),('^PREFLIGHT=','preflight-r73.txt')]:
    run(['grep','-c',pattern,'corpus/evidence/round73/controls/'+path],cwd=C)
for p in D.iterdir(): shutil.copyfile(p,O/('fabricated-'+p.name))
log.append('=== C1-only fixture: no correction commit required; C2 original base remains red ===\n'); score(base_copy)
shutil.copyfile(L/'corpus/evidence/round73/c2-count.py',O/'frozen-c2-count.py')
shutil.copyfile(L/'corpus/evidence/round73/claims.md',O/'frozen-claims.md')
(O/'receipts.txt').write_text(''.join(log))
shutil.rmtree(S)
(O/'cleanup.txt').write_text(f'Deleted {S}; exists={S.exists()}\nNo installs, no network, no lane/source git mutations.\n')
print('Receipts saved to',O/'receipts.txt')
print('Scratch deleted:',not S.exists())
