import json, os, re, subprocess, sys
W=os.path.abspath("."); TREE=os.path.abspath("tree"); REPO="/home/vgpnk/Projects/shokunin/chousa-shokunin"
pos=[]
for ln in open("tree/corpus/evidence/round84/c2-positives.tsv",encoding="utf-8"):
    f,n,raw=ln.rstrip("\n").split("\t",2); pos.append((f,int(n),raw))
form=lambda l:"rev" if " rev=" in l else ("unreach" if " capture=none " in l else "admit")
kv=lambda l,k:(re.search(r"(?<= )"+k+r"=(\S+)",l).group(1) if re.search(r"(?<= )"+k+r"=(\S+)",l) else None)
def kvs(l,k,v): return re.sub(r"(?<= )"+re.escape(k)+r"=\S+",k+"="+v,l,count=1)
admits=[p[2] for p in pos if form(p[2])=="admit"]; revs=[p[2] for p in pos if form(p[2])=="rev"]
w={}
w["W11-leading-zero-words"]=(kvs(admits[0],"words","0"+kv(admits[0],"words")),"admit words=0<n> (leading zero); contract says PARSE","mut33-accept-leading-zero")
# W12: rev record, line=0, quote from the blob's last line
built=None
for rec in revs:
    rev,path=kv(rec,"rev"),kv(rec,"path")
    b=subprocess.run(["git","-C",REPO,"cat-file","blob",rev+":"+path],capture_output=True).stdout.decode("utf-8","replace")
    lines=b.split("\n")
    if lines and lines[-1]=="": lines.pop()
    if not lines: continue
    last=" ".join(lines[-1].split())
    if 2<=len(last.split())<=25:
        cand=kvs(rec.split(" quote=")[0]+" quote="+last,"line","0"); cand=kvs(cand,"words",str(len(last.split())))
        built=(cand,f"rev line=0 with the blob's last line as quote ({path})","mut34-drop-rev-line-zero-guard"); break
if built: w["W12-rev-line-zero"]=built
os.makedirs("receipts/witnesses",exist_ok=True); rows=[]
for name,(line,why,mut) in w.items():
    fp=os.path.join("receipts","witnesses",name+".md"); open(fp,"w",encoding="utf-8").write(line+"\n")
    def run(tool):
        p=subprocess.run([sys.executable,"-B",tool,"verify","--root","tree","--repo",REPO,fp],capture_output=True,text=True,cwd=W)
        return p.returncode,p.stdout.strip(),p.stderr.strip()
    prc,pout,perr=run("tree/tools/gate-records.py"); mrc,mout,merr=run(os.path.join("mutants",mut+".py"))
    open(os.path.join("receipts","witnesses",name+".txt"),"w",encoding="utf-8").write(
      f"WITNESS: {name}\nWHY: {why}\nMUTANT: {mut}\nLINE={line}\n"
      f"PRISTINE_CMD: python3 -B tree/tools/gate-records.py verify --root tree --repo {REPO} {fp}\n"
      f"PRISTINE_RC={prc}\nPRISTINE_STDOUT={pout}\nPRISTINE_STDERR={perr}\n"
      f"MUTANT_CMD: python3 -B mutants/{mut}.py verify --root tree --repo {REPO} {fp}\n"
      f"MUTANT_RC={mrc}\nMUTANT_STDOUT={mout}\nMUTANT_STDERR={merr}\n")
    rows.append({"witness":name,"why":why,"mutant":mut,"pristine_rc":prc,"pristine":pout,
                 "mutant_rc":mrc,"mutant_out":mout})
    print(name,"pristine:",prc,pout.splitlines()[0]); print(" "*len(name),"mutant  :",mrc,mout.splitlines()[0])
s=json.load(open("receipts/witnesses/summary.json")); s.extend(rows)
json.dump(s,open("receipts/witnesses/summary.json","w"),indent=1)
