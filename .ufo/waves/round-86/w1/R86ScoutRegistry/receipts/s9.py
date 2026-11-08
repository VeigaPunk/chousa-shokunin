import pickle,os,subprocess,json,re,glob,datetime
S="/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry"
R="/home/vgpnk/Projects/shokunin/chousa-shokunin"
REV="667a5d091dc46168ed95eda0ae7f19a9bcf139a2"
d=pickle.load(open(os.path.join(S,"work","rows.pkl"),"rb")); rows=d["rows"]
paths=set()
for sid in d["order"]:
    v=rows[sid]["used-by"].strip()
    if v in ("—","-",""): continue
    for p in [x.strip() for x in v.split(",") if x.strip()]: paths.add(p)
utc={}
for p in sorted(paths):
    r=subprocess.run(["git","-C",R,"log","--reverse","--diff-filter=A","--format=%cI",REV,"--",p],capture_output=True,text=True)
    ds=[x for x in r.stdout.split() if x]
    if ds:
        utc[p]=datetime.datetime.fromisoformat(ds[0]).astimezone(datetime.timezone.utc).date().isoformat()
# verified-at headers of knowledge entries
va={}
for f in glob.glob(os.path.join(S,"corpus/knowledge","*.md")):
    b=os.path.basename(f); t=open(f,encoding="utf-8",errors="replace").read()
    m=re.search(r"^verified-at:\s*(\d{4}-\d{2}-\d{2})", t, re.M)
    if m: va[b]=m.group(1)
res=[]; nores=[]
for sid in d["order"]:
    r=rows[sid]; v=r["used-by"].strip()
    if v in ("—","-",""): continue
    ents=[x.strip() for x in v.split(",") if x.strip()]
    cand=[]
    for e in ents:
        b=os.path.basename(e)
        dt = va.get(b) or utc.get(e)
        if dt: cand.append((dt,b,"verified-at" if b in va else "git-utc-first-commit"))
    if not cand: nores.append((sid,ents)); continue
    cand.sort()
    dt,b,how=cand[0]
    if r["opened"] > dt:
        res.append((sid,r["opened"],dt,b,how,cand))
print("rows whose opened > earliest citing-entry date (UTC, verified-at preferred):", len(res))
for x in res: print("  ",x[0],"opened",x[1],"entry",x[3],x[4],x[2],"candidates",x[5])
print()
print("rows with no derivable date for any citing entry:", len(nores))
for x in nores: print("  ",x)
