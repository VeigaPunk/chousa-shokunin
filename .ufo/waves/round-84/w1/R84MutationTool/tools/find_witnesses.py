import hashlib, os, re, json
R = "tree"
reg = {}
for ln in open(os.path.join(R,"corpus","SOURCES.md"), encoding="utf-8", errors="replace"):
    if re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", ln):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) == 11: reg.setdefault(cells[0], cells)
rows = []
for ln in open(os.path.join(R,"corpus","evidence","round57","refetch.tsv"), encoding="utf-8", errors="replace"):
    f = ln.rstrip("\n").split("\t")
    if len(f) == 9: rows.append(f)
stale=[]; badrc=[]; non2xx=[]; succ=[]
for f in rows:
    sid,url,key,_,fetched,rc,http,_,tsha = f
    cap = os.path.join(R,"corpus","captures",key+".txt")
    cells = reg.get(sid)
    if cells is None or not os.path.isfile(cap): continue
    if hashlib.sha256(url.encode()).hexdigest()[:24] != key: continue
    h = hashlib.sha256(open(cap,"rb").read()).hexdigest()
    if rc=="0" and http.startswith("2"):
        succ.append((f,h))
        if tsha != h: stale.append((f,h))
    else:
        if tsha == h: badrc.append((f,h))

def quote_from(cap):
    raw = open(cap, encoding="utf-8", errors="replace").read()
    for line in raw.split("\n"):
        w = line.split()
        if 6 <= len(w) <= 20:
            q = " ".join(" ".join(line.split()).split())
            if q and q in " ".join(raw.split()): return q, len(w)
    return None
def rec_admit(f, h):
    sid,url,key,_,fetched,rc,http,_,tsha=f; cells=reg[sid]
    q = quote_from(os.path.join(R,"corpus","captures",key+".txt"))
    if not q: return None
    return f'GATE-RECORD {sid} url={url} fetched={fetched} tier={cells[3]} decision=admit capture=corpus/captures/{key}.txt capture_sha256={h[:16]} words={q[1]} quote="{q[0]}"'
out={"stale":[], "badrc":[], "non2xx":[], "succ": len(succ)}
for f,h in stale[:3]:
    r = rec_admit(f,h)
    if r: out["stale"].append({"row":f, "line":r})
for f,h in badrc[:6]:
    r = rec_admit(f,h)
    if not r: continue
    k = "non2xx" if not f[6].startswith("2") else "badrc"
    out[k].append({"row":f, "line":r})
# unreach witnesses from success rows (same refetch row, capture=none)
for f,h in succ[:20]:
    sid,url,key,_,fetched,rc,http,_,tsha=f; cells=reg[sid]
    line=f'GATE-RECORD {sid} url={url} fetched={fetched} tier={cells[3]} decision=reject capture=none curl_rc={rc} http={http} words=0 quote=none'
    out.setdefault("unreach_success",[]).append({"row":f,"line":line})
    if len(out["unreach_success"])>=2: break
json.dump(out, open("witness_pool.json","w"), indent=1)
print("stale",len(out["stale"]),"badrc",len(out["badrc"]),"non2xx",len(out["non2xx"]),"unreach_success",len(out.get("unreach_success",[])),"succ",out["succ"])
for k in ("stale","badrc","non2xx","unreach_success"):
    for e in out.get(k,[])[:1]: print(k, "->", e["line"][:160])
