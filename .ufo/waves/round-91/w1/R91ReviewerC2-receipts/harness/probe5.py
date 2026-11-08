import os,re,shutil,subprocess,sys
S="/fast/scratch/hyaku/chousa-r91/R91ReviewerC2"; ROOT=os.path.join(S,"repo")
NEW=os.path.join(ROOT,"corpus","evidence","round91","curation-r91.py"); OLD=os.path.join(ROOT,"corpus","evidence","round90","curation-r90.py")
W=os.path.join(S,"work5"); EA="corpus/knowledge/search-transparency-reporting-r84.md"; EB="corpus/knowledge/provenance-recording-r85.md"
def mirror(root,dst):
    os.makedirs(os.path.join(dst,"corpus","knowledge"),exist_ok=True); os.makedirs(os.path.join(dst,"corpus","evidence"),exist_ok=True)
    shutil.copy2(os.path.join(root,"corpus","SOURCES.md"),os.path.join(dst,"corpus","SOURCES.md"))
    for rel in (EA,EB): shutil.copy2(os.path.join(root,rel),os.path.join(dst,rel))
    for rel in ("corpus/captures","corpus/evidence/round57"):
        s=os.path.join(root,rel)
        if os.path.isdir(s): os.symlink(s,os.path.join(dst,rel))
    return dst
shutil.rmtree(W,ignore_errors=True); os.makedirs(W,exist_ok=True)
pr=mirror(ROOT,os.path.join(W,"pristine")); t=os.path.join(W,"A11"); shutil.copytree(pr,t,symlinks=True)
p=os.path.join(t,EA); s=open(p,encoding="utf-8").read()
old="| Recording when a resource changed |"
new="| Recording a modified resource when it changed |"
assert old in s
open(p,"w",encoding="utf-8").write(s.replace(old,new,1))
for c,tag in ((NEW,"r91"),(OLD,"r90")):
    r=subprocess.run([sys.executable,"-B",c,"--root",t],capture_output=True,text=True)
    v=[l for l in r.stdout.splitlines() if l.startswith("CURATION_R")]
    f={}
    for ln in r.stdout.splitlines():
        for k in ("UNENTAILED_TERM","WARRANT_OK","TFREQ_OK","Q_SHAPE_FAIL"):
            m=re.search(rf"(?:^| ){k}=([^ ]+)",ln)
            if m: f[k]=m.group(1)
    print(f"A11-cells0-only {tag}: exit={r.returncode} {v[0]} UNENTAILED_TERM={f.get('UNENTAILED_TERM')} WARRANT_OK={f.get('WARRANT_OK')} TFREQ_OK={f.get('TFREQ_OK')}")
    for ln in r.stdout.splitlines():
        if ln.startswith(("LEG_FAIL","UNENTAILED ")): print("   "+ln)
