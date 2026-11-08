import re,pickle,os,json
from urllib.parse import urlsplit, urlunsplit
S="/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry"
d=pickle.load(open(os.path.join(S,"work","rows.pkl"),"rb")); rows=d["rows"]

def urls(cell):
    return re.findall(r"https?://[^\s|)>\]]+", cell)

def norm_url(u):
    u=u.strip().rstrip(".,;")
    p=urlsplit(u)
    host=p.netloc.lower()
    if host.startswith("www."): host=host[4:]
    path=p.path.rstrip("/") or "/"
    return f"{host}{path}" + (f"?{p.query}" if p.query else "")

groups={}
for sid in d["order"]:
    r=rows[sid]
    us=urls(r["source"])
    key = norm_url(us[-1]) if us else "NOURL:"+r["source"][:60]
    groups.setdefault(key,[]).append(sid)

multi={k:v for k,v in groups.items() if len(v)>=2}
print("groups total:",len(groups),"multi:",len(multi))
for k,v in sorted(multi.items()):
    print("="*90)
    print(k, v)
    for sid in v:
        r=rows[sid]
        print(f"  {sid} status={r['status']} opened={r['opened']}")
        print(f"     scope: {r['scope'][:200]}")
        print(f"     teaches: {r['teaches'][:300]}")
pickle.dump(groups, open(os.path.join(S,"work","groups.pkl"),"wb"))
