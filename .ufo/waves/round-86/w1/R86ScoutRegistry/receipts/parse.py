import re, json, os, sys
S="/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry"
src=open(os.path.join(S,"corpus/SOURCES.md"),encoding="utf-8").read()
lines=src.split("\n")
rows={}
order=[]
inreg=False
for ln,line in enumerate(lines,1):
    if line.startswith("## Registry"): inreg=True; continue
    if inreg and line.startswith("## "): inreg=False
    if not inreg: continue
    if not line.startswith("|"): continue
    cells=[c.strip() for c in line.strip().strip("|").split("|")]
    if not cells or cells[0].startswith("---") or set(cells[0])<=set("-: "): continue
    if cells[0]=="id": 
        hdr=cells; continue
    if len(cells)!=len(hdr):
        print("RAGGED", ln, len(cells), len(hdr), cells[0], file=sys.stderr)
        continue
    d=dict(zip(hdr,cells)); d["_line"]=ln
    rows[d["id"]]=d; order.append(d["id"])
print(json.dumps({"n":len(rows),"hdr":hdr},indent=1))
import pickle
pickle.dump({"rows":rows,"order":order,"hdr":hdr}, open(os.path.join(S,"work","rows.pkl"),"wb"))
