import os,re,glob,pickle
S="/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry"
d=pickle.load(open(os.path.join(S,"work","rows.pkl"),"rb")); rows=d["rows"]
# row -> set of entry basenames its used-by names
row2ent={}
for sid in d["order"]:
    v=rows[sid]["used-by"].strip()
    if v in ("—","-",""): continue
    for p in [x.strip() for x in v.split(",") if x.strip()]:
        row2ent.setdefault(sid,set()).add(os.path.basename(p))
# entry -> header ids
ent2ids={}
for f in sorted(glob.glob(os.path.join(S,"corpus/knowledge","*.md"))):
    b=os.path.basename(f); t=open(f,encoding="utf-8",errors="replace").read()
    m=re.search(r"^source\s*:(.*?)(?=^\S)", t, re.M|re.S|re.I)
    h=m.group(1) if m else ""
    ent2ids[b]=sorted(set(re.findall(r"\bS\d{3}\b", h)))
print("=== A (corrected). entry names a MINED row whose used-by does not name this entry  [QUALITY 6 reciprocity] ===")
nA=0; details=[]
for b,ids in sorted(ent2ids.items()):
    bad=[i for i in ids if i in rows and rows[i]["status"]=="mined" and b not in row2ent.get(i,set())]
    if bad:
        nA+=1; details.append((b,ids,bad))
print("count A:", nA)
for b,ids,bad in details: print(f"  {b}: header names {ids} | mined-not-reciprocated: {bad}")
print()
print("=== A2. entries whose source: header names NO mined row that reciprocates them at all ===")
nA2=[b for b,ids in sorted(ent2ids.items()) if ids and not any(i in rows and rows[i]['status']=='mined' and b in row2ent.get(i,set()) for i in ids)]
print("count A2:", len(nA2))
for b in nA2: print("  ", b)
pickle.dump({"row2ent":row2ent,"ent2ids":ent2ids}, open(os.path.join(S,"work","recip2.pkl"),"wb"))
