import re,pickle,os,json
S="/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry"
d=pickle.load(open(os.path.join(S,"work","rows.pkl"),"rb")); rows=d["rows"]
pat=re.compile(r'^supersedes\s+(S\d{3})\s*(?:—|-|–)\s*(.*)$', re.S)
edges=[]
for sid in d["order"]:
    r=rows[sid]; t=r["teaches"]
    m=pat.match(t)
    if m:
        edges.append((sid, m.group(1), m.group(2), r["status"], rows[m.group(1)]["status"] if m.group(1) in rows else "MISSING"))
print("total edges:", len(edges))
for sid,tgt,rest,ss,ts in edges:
    print(f"{sid}({ss}) -> {tgt}({ts}) | rest: {rest[:160]}")
print()
print("=== INV: target mined while superseding not ===")
for sid,tgt,rest,ss,ts in edges:
    if ts=="mined" and ss!="mined":
        print("INV", sid, ss, tgt, ts)
print()
print("=== target missing ===")
for sid,tgt,rest,ss,ts in edges:
    if ts=="MISSING": print("MISS",sid,tgt)
pickle.dump(edges, open(os.path.join(S,"work","edges.pkl"),"wb"))
