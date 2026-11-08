import os, re, shutil, subprocess, sys
S="/fast/scratch/hyaku/chousa-r91/R91ReviewerC2"; ROOT=os.path.join(S,"repo")
NEW=os.path.join(ROOT,"corpus","evidence","round91","curation-r91.py"); OLD=os.path.join(ROOT,"corpus","evidence","round90","curation-r90.py")
W=os.path.join(S,"work4"); EA="corpus/knowledge/search-transparency-reporting-r84.md"; EB="corpus/knowledge/provenance-recording-r85.md"
def mirror(root,dst):
    os.makedirs(os.path.join(dst,"corpus","knowledge"),exist_ok=True); os.makedirs(os.path.join(dst,"corpus","evidence"),exist_ok=True)
    shutil.copy2(os.path.join(root,"corpus","SOURCES.md"),os.path.join(dst,"corpus","SOURCES.md"))
    for rel in (EA,EB): shutil.copy2(os.path.join(root,rel),os.path.join(dst,rel))
    for rel in ("corpus/captures","corpus/evidence/round57"):
        s=os.path.join(root,rel)
        if os.path.isdir(s): os.symlink(s,os.path.join(dst,rel))
    return dst
def edit(p,o,n):
    t=open(p,encoding="utf-8").read()
    assert o in t, o[:50]
    open(p,"w",encoding="utf-8").write(t.replace(o,n,1))
shutil.rmtree(W,ignore_errors=True); os.makedirs(W,exist_ok=True)
pr=mirror(ROOT,os.path.join(W,"pristine"))
def fresh(n):
    d=os.path.join(W,n); shutil.copytree(pr,d,symlinks=True); return d
def run(c,root):
    p=subprocess.run([sys.executable,"-B",c,"--root",root],capture_output=True,text=True); return p.returncode,p.stdout
def show(tag,rc,out):
    k={}
    for ln in out.splitlines():
        for f in ("Q_SHAPE_FAIL","UNENTAILED_TERM","Q_ROWS","WARRANT_OK","TFREQ_OK","LEGS_MEASURED"):
            m=re.search(rf"(?:^| ){f}=([^ ]+)",ln)
            if m: k[f]=m.group(1)
    v=[l for l in out.splitlines() if l.startswith("CURATION_R")]
    print(f"{tag}: exit={rc} {v[0] if v else 'none'} Q_SHAPE_FAIL={k.get('Q_SHAPE_FAIL')} UNENTAILED_TERM={k.get('UNENTAILED_TERM')} Q_ROWS={k.get('Q_ROWS')} LEGS={k.get('LEGS_MEASURED')}")
    for ln in out.splitlines():
        if ln.startswith("LEG_FAIL"): print("   "+ln)
cases={}
t=fresh("colon-cell"); edit(os.path.join(t,EB),"## Decision table",'| : | S023 | "Date on which the resource was changed." |\n\n## Decision table'); cases["quote-row-first-cell=':'"]=t
t=fresh("situation-cell"); edit(os.path.join(t,EB),"## Decision table",'| Situation | S023 | "Date on which the resource was changed." |\n\n## Decision table'); cases["quote-row-first-cell='Situation'"]=t
t=fresh("decision-empty-cell"); edit(os.path.join(t,EB),"## Inference","| | state the modification of the value | record the modified value | Q13 (S023) |\n\n## Inference"); cases["decision-row-empty-first-cell(both terms)"]=t
for n,t in cases.items():
    rc,o=run(NEW,t); show(n+" r91",rc,o)
    rc,o=run(OLD,t); show(n+" r90",rc,o)
    print()
