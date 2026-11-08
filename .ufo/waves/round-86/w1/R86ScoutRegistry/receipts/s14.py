import os,re,glob,pickle,hashlib
S="/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry"
d=pickle.load(open(os.path.join(S,"work","rows.pkl"),"rb")); rows=d["rows"]
# used-by path -> does the file mention the S-id anywhere (header or body)?
print("=== mined rows whose used-by file never mentions the row id at all ===")
n=0
for sid in d["order"]:
    r=rows[sid]
    if r["status"]!="mined": continue
    v=r["used-by"].strip()
    if v in ("—","-",""): continue
    for p in [x.strip() for x in v.split(",") if x.strip()]:
        fp=os.path.join(S,p)
        if not os.path.isfile(fp): 
            print("  MISSING FILE",sid,p); n+=1; continue
        t=open(fp,encoding="utf-8",errors="replace").read()
        if not re.search(r"\b"+sid+r"\b", t):
            print(f"  {sid}: used-by {p} does not contain '{sid}'"); n+=1
print("count:", n)
print()
print("=== last-URL contamination (backtick/comma captured) among mined rows ===")
bad=[]
for sid in d["order"]:
    if rows[sid]["status"]!="mined": continue
    urls=re.findall(r"https?://[^\s|)>\]]+", rows[sid]["source"])
    if not urls: continue
    u=urls[-1]
    if u[-1] not in "/)>#" or "`" in u or "," in u:
        bad.append((sid,u))
print("contaminated last-url rows:", len(bad))
for sid,u in bad: print("  ",sid,repr(u))
print()
print("=== S215 / S020 / S033 URL groups ===")
for sid in ("S020","S033","S215"):
    urls=re.findall(r"https?://[^\s|)>\]]+", rows[sid]["source"])
    print(" ",sid, urls, "|", rows[sid]["source"][:150])
