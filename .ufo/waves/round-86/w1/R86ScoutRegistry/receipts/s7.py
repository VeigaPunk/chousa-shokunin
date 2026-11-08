import pickle,os,subprocess,json
S="/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry"
R="/home/vgpnk/Projects/shokunin/chousa-shokunin"
d=pickle.load(open(os.path.join(S,"work","rows.pkl"),"rb")); rows=d["rows"]
paths=set()
for sid in d["order"]:
    v=rows[sid]["used-by"].strip()
    if v in ("—","-",""): continue
    for p in [x.strip() for x in v.split(",") if x.strip()]:
        paths.add(p)
paths=sorted(paths)
# first-commit date of each path at the landing revision
out={}
for p in paths:
    r=subprocess.run(["git","-C",R,"log","--reverse","--diff-filter=A","--format=%as",f"667a5d091dc46168ed95eda0ae7f19a9bcf139a2","--",p],capture_output=True,text=True)
    dates=[x for x in r.stdout.split() if x]
    out[p]=dates[0] if dates else None
json.dump(out, open(os.path.join(S,"work","pathdates.json"),"w"), indent=1)
print("paths:",len(paths),"dated:",sum(1 for v in out.values() if v))
# now per row: earliest citing entry date vs opened
res=[]
for sid in d["order"]:
    r=rows[sid]
    v=r["used-by"].strip()
    if v in ("—","-",""): continue
    ents=[x.strip() for x in v.split(",") if x.strip()]
    dated=[(out.get(e),e) for e in ents]
    dated=[(dt,e) for dt,e in dated if dt]
    if not dated: continue
    dated.sort()
    first_date,first_ent=dated[0]
    if r["opened"] > first_date:
        res.append((sid,r["opened"],first_date,first_ent,ents,dated))
print("rows where opened > first citing entry's first-commit date:", len(res))
for sid,opened,fd,fe,ents,dated in res:
    print(f"  {sid} opened={opened}  first citing entry={fe} (first commit {fd})  all={[(a,b) for a,b in dated]}")
