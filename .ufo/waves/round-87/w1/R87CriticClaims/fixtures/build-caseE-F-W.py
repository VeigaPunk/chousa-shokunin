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
def edit(dst,entry,drop,dup,count):
    lines=rows(os.path.join(root,entry)); p=os.path.join(dst,entry); s,e=span(lines); o=[]; keep=[]
    for i,ln in enumerate(lines):
        if s is not None and s<=i<e and ln.lstrip().startswith("|"):
            m=re.match(r"^\s*\|\s*(Q\d+)",ln)
            if m and m.group(1) in drop: continue
            if m and m.group(1)==dup: keep=ln
        o.append(ln)
    s2,e2=span(o); pos=e2 if e2 is not None else len(o)
    o[pos:pos]=[keep]*count
    open(p,"w",encoding="utf-8").write("\n".join(o))
# E: drop Q10 (uncited), duplicate Q13 once to restore the row count
d=mirror(os.path.join(dstbase,"caseE")); edit(d,A,{"Q10"},"Q13",1)
# F: drop Q10 only (control)
d=mirror(os.path.join(dstbase,"caseF")); edit(d,A,{"Q10"},"Q13",0)
# W: re-point r84 row 9 'Recording when a resource changed' warrant Q13 -> Q11 (validity dates); Q13 stays
d=mirror(os.path.join(dstbase,"caseW"))
p=os.path.join(d,A); txt=open(p,encoding="utf-8").read()
txt=txt.replace("| Recording when a resource changed |", "| Recording when a resource changed |") # noop
import re as _re
new=_re.sub(r"(\|[^|\n]*Recording when a resource changed[^|\n]*\|[^|\n]*\|[^|\n]*\|[^|\n]*?)Q13", r"\1Q11", txt)
assert new!=txt, "row 9 warrant not found"
open(p,"w",encoding="utf-8").write(new)
for name in ("caseE","caseF","caseW"):
    r=subprocess.run([sys.executable,"-B",os.path.join(root,"corpus/evidence/round87/curation-r87.py"),"--root",os.path.join(dstbase,name)],capture_output=True,text=True)
    print("==",name,"exit",r.returncode); print(r.stdout.strip())
    open(os.path.join(out,name+".txt"),"w").write(r.stdout+r.stderr+"exit=%d\n"%r.returncode)
