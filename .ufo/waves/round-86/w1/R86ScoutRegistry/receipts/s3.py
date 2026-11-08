import pickle,os,re
S="/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry"
d=pickle.load(open(os.path.join(S,"work","rows.pkl"),"rb")); rows=d["rows"]
miss=[]; total=0; checked=0
for sid in d["order"]:
    r=rows[sid]
    if r["status"]!="mined": continue
    ub=r["used-by"].strip()
    if ub in ("—","-",""): 
        miss.append((sid,ub,"USED_BY_EMPTY"))
        continue
    for p in [x.strip() for x in ub.split(",") if x.strip()]:
        total+=1
        full=os.path.join(S,p)
        if not os.path.exists(full):
            miss.append((sid,p,"MISSING"))
        else:
            checked+=1
print(f"mined rows: {sum(1 for s in d['order'] if rows[s]['status']=='mined')}")
print(f"used-by paths checked: {total}, existing: {checked}, missing: {len([m for m in miss if m[2]=='MISSING'])}, empty-used-by: {len([m for m in miss if m[2]=='USED_BY_EMPTY'])}")
print()
for sid,p,why in miss:
    print(f"{why}: {sid} -> {p!r}")
