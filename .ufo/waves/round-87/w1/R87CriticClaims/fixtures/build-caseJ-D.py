import os,re,shutil,subprocess,sys
root,dstbase,out=sys.argv[1:4]
ENTRY_A="corpus/knowledge/search-transparency-reporting-r84.md"; ENTRY_B="corpus/knowledge/provenance-recording-r85.md"
def mirror(dst):
    os.makedirs(os.path.join(dst,"corpus","knowledge"),exist_ok=True)
    os.makedirs(os.path.join(dst,"corpus","evidence"),exist_ok=True)
    for rel in ("corpus/SOURCES.md",ENTRY_A,ENTRY_B):
        shutil.copy2(os.path.join(root,rel),os.path.join(dst,rel))
    for link,target in (("corpus/captures",os.path.join(root,"corpus","captures")),
                        ("corpus/evidence/round57",os.path.join(root,"corpus","evidence","round57"))):
        p=os.path.join(dst,link)
        if not os.path.exists(p): os.symlink(target,p)
    return dst
def rows(path): return open(path,encoding="utf-8").read().split("\n")
def quote_block_span(lines):
    on=False; start=end=None
    for i,ln in enumerate(lines):
        if ln.startswith("## "):
            if on and start is not None: end=i; break
            on = ln.strip()=="## Located quotes"
            if on: start=i+1
    return start,(end if end is not None else len(lines))
def getrow(qid):
    for ln in rows(os.path.join(root,ENTRY_A)):
        m=re.match(r"^\s*\|\s*(Q\d+)",ln)
        if m and m.group(1)==qid: return ln
    raise SystemExit("no row "+qid)
def getrowB(qid):
    for ln in rows(os.path.join(root,ENTRY_B)):
        m=re.match(r"^\s*\|\s*(Q\d+)",ln)
        if m and m.group(1)==qid: return ln
    raise SystemExit("no row "+qid)
def rewrite(dst,entry,keeps,extra=None):
    src=os.path.join(root,entry); path=os.path.join(dst,entry); lines=rows(src)
    s,e=quote_block_span(lines); o=[]
    for i,ln in enumerate(lines):
        if s is not None and s<=i<e and ln.lstrip().startswith("|"):
            m=re.match(r"^\s*\|\s*(Q\d+)",ln)
            if m and m.group(1) not in keeps: continue
        o.append(ln)
    s2,e2=quote_block_span(o); pos=e2 if e2 is not None else len(o)
    o[pos:pos]=list(extra or [])+[r for r in extra or []]  # placeholder
    open(path,"w",encoding="utf-8").write("\n".join(o))
def rewrite2(dst,entry,drop_except,dup_rows,extra):
    src=os.path.join(root,entry); path=os.path.join(dst,entry); lines=rows(src)
    s,e=quote_block_span(lines); o=[]
    for i,ln in enumerate(lines):
        if s is not None and s<=i<e and ln.lstrip().startswith("|"):
            m=re.match(r"^\s*\|\s*(Q\d+)",ln)
            if m and m.group(1) not in drop_except: continue
        o.append(ln)
    s2,e2=quote_block_span(o); pos=e2 if e2 is not None else len(o)
    o[pos:pos]=list(extra)+list(dup_rows)
    open(path,"w",encoding="utf-8").write("\n".join(o))
qa=getrow("Q13"); qb=getrowB("Q7")
# J: keep the two real rows, add 20 junk rows dropped from both counts
d=mirror(os.path.join(dstbase,"caseJ"))
junk='| Q90 | S023 | "quote with | pipe" | x |'
rewrite2(d,ENTRY_A,{"Q13"},[], [junk]*20)
rewrite2(d,ENTRY_B,{"Q7"},[], [junk]*20)
# D: one distinct quote repeated to the floor (13 and 7 rows)
d=mirror(os.path.join(dstbase,"caseD"))
rewrite2(d,ENTRY_A,{"Q13"},[qa]*12,[])
rewrite2(d,ENTRY_B,{"Q7"},[qb]*6,[])
for name in ("caseJ","caseD"):
    r=subprocess.run([sys.executable,"-B",os.path.join(root,"corpus/evidence/round87/curation-r87.py"),"--root",os.path.join(dstbase,name)],capture_output=True,text=True)
    print("==",name,"exit",r.returncode); print(r.stdout.strip()); print(r.stderr.strip()[:200])
    open(os.path.join(out,name+".txt"),"w").write(r.stdout+r.stderr+"exit=%d\n"%r.returncode)
