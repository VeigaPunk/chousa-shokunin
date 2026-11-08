import os,re,hashlib,sys
root=sys.argv[1]
reg={}
for ln in open(os.path.join(root,'corpus/SOURCES.md')):
    m=re.match(r"^ {0,3}\| (S\d{3,}) \|",ln)
    if m:
        cells=[c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells)==11: reg[cells[0]]=cells
def norm(s):
    for a,b in (("\u2019","'"),("\u2018","'"),("\u201c",'"'),("\u201d",'"')): s=s.replace(a,b)
    return " ".join(s.split())
bad=0; n=0
for rel in ("corpus/knowledge/search-transparency-reporting-r84.md","corpus/knowledge/provenance-recording-r85.md"):
    on=False
    for ln in open(os.path.join(root,rel),encoding="utf-8").read().split("\n"):
        if ln.startswith("## "): on=ln.strip()=="## Located quotes"; continue
        if not on: continue
        m=re.match(r"^\s*\|\s*(Q\d+)\s*\|\s*(S\d+)\s*\|\s*(.+?)\s*\|\s*$",ln)
        if not m: continue
        qid,sid,q=m.group(1),m.group(2),m.group(3).strip().strip('"')
        cells=reg.get(sid); cap=None
        if cells:
            for u in re.findall(r"https?://[^\s|)>\]]+",cells[1]):
                k=hashlib.sha256(u.encode()).hexdigest()[:24]; p=os.path.join(root,'corpus/captures',k+'.txt')
                if os.path.isfile(p): cap=norm(open(p,encoding='utf-8',errors='replace').read()); break
        n+=1
        loc = cap is not None and norm(q) in cap
        if not loc: bad+=1; print("NOT_LOCATED",rel,qid,sid)
print(f"K2 quotes={n} not_located={bad}")
