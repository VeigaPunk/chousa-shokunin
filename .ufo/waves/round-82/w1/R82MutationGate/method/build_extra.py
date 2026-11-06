import json, subprocess, hashlib, os
REPO="/fast/scratch/hyaku/chousa-r82/R82MutationGate/repo38"
PRISTINE="04bff4f90173f00bc9f7220f7f244cf479f4fd80"
K2="corpus/evidence/round82/k2-gate-r82.py"
M=[("MK10-hold-only-PASS","PASS requires only the hold group to be full",
    '    full = nrl == 2 and all(ok[g] == tot[g] and tot[g] > 0 for g in GROUPS)',
    '    full = nrl == 2 and ok["hold"] == tot["hold"] and tot["hold"] > 0'),
   ("MK11-accept-every-row","score every manifest row ok",
    '            good = rc == 1 and need in seen',
    '            good = True'),
   ("MK11-accept-every-row","score every manifest row ok",
    '            good = rc == 0 and "RESEARCH_GATE: CLEAN" in out and need in out',
    '            good = True')]
def git(*a):
    return subprocess.run(["git","-C",REPO,*a],capture_output=True,text=True)
out=[]
for mid,desc,old,new in M:
    cur=open(os.path.join(REPO,K2),"rb").read()
    text=cur.decode()
    assert text.count(old)==1,(mid,text.count(old))
    mutated=text.replace(old,new,1).encode()
    open(os.path.join(REPO,K2),"wb").write(mutated)
    git("add",K2)
    c=git("-c","user.email=mutation@local","-c","user.name=R82MutationGate","commit","-qm",f"mutant {mid}: {desc}")
    assert c.returncode==0,c.stderr
    sha=git("rev-parse","HEAD").stdout.strip()
    out.append({"id":mid,"desc":desc,"commit":sha,"mut_sha256":hashlib.sha256(mutated).hexdigest(),
                "counter":K2,"pristine_sha256":hashlib.sha256(subprocess.run(["git","-C",REPO,"show",f"{PRISTINE}:{K2}"],capture_output=True,check=True).stdout).hexdigest()})
    print(mid,sha,out[-1]["mut_sha256"])
# restore
pris=subprocess.run(["git","-C",REPO,"show",f"{PRISTINE}:{K2}"],capture_output=True,check=True).stdout
open(os.path.join(REPO,K2),"wb").write(pris); git("add",K2)
git("-c","user.email=mutation@local","-c","user.name=R82MutationGate","commit","-qm","restore counter after MK10/MK11")
json.dump(out,open("/fast/scratch/hyaku/chousa-r82/R82MutationGate/counter-mutants-extra.json","w"),indent=1)
print("HEAD",git("rev-parse","HEAD").stdout.strip(),"clean",not git("status","--porcelain").stdout.strip())
