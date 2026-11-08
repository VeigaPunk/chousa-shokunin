import os,re,shutil,subprocess,sys
root,dstbase,out=sys.argv[1:4]
A="corpus/knowledge/search-transparency-reporting-r84.md"; B="corpus/knowledge/provenance-recording-r85.md"
def mirror(dst):
    os.makedirs(os.path.join(dst,"corpus","knowledge"),exist_ok=True); os.makedirs(os.path.join(dst,"corpus","evidence"),exist_ok=True)
    for rel in ("corpus/SOURCES.md",A,B): shutil.copy2(os.path.join(root,rel),os.path.join(dst,rel))
    for link,target in (("corpus/captures",os.path.join(root,"corpus","captures")),("corpus/evidence/round57",os.path.join(root,"corpus","evidence","round57"))):
        p=os.path.join(dst,link)
        if not os.path.exists(p): os.symlink(target,p)
    return dst
def rows(p): return open(p,encoding="utf-8").read().split("\n")
def span(lines):
    on=False;s=e=None
    for i,ln in enumerate(lines):
        if ln.startswith("## "):
            if on and s is not None: e=i;break
            on=ln.strip()=="## Located quotes"
            if on: s=i+1
    return s,(e if e is not None else len(lines))
# caseG: delete uncited Q10, add fake Q14 carrying Q13's quote -> 13 distinct qids
lines=rows(os.path.join(root,A)); o=[]; s,e=span(lines); q13=None
for i,ln in enumerate(lines):
    if s is not None and s<=i<e and ln.lstrip().startswith("|"):
        m=re.match(r"^\s*\|\s*(Q\d+)",ln)
        if m and m.group(1)=="Q10": continue
        if m and m.group(1)=="Q13": q13=ln
    o.append(ln)
s2,e2=span(o); pos=e2 if e2 is not None else len(o)
o[pos:pos]=[re.sub(r"Q13",'Q14',q13,count=1)]
d=mirror(os.path.join(dstbase,"caseG"))
open(os.path.join(d,A),"w",encoding="utf-8").write("\n".join(o))
r=subprocess.run([sys.executable,"-B",os.path.join(root,"corpus/evidence/round87/curation-r87.py"),"--root",d],capture_output=True,text=True)
print("caseG exit",r.returncode); print(r.stdout.strip())
open(os.path.join(out,"caseG.txt"),"w").write(r.stdout+r.stderr+"exit=%d\n"%r.returncode)
