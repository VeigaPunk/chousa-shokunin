import json, os, subprocess, hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,"fe","root")
CLAIMS=os.path.join(ROOT,"claims.jsonl")
LAND="/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh"
BASE=os.path.join(HERE,"base-gate.sh")
CASES=[
 ("span-u0000-inside",      b'{"id":"u1","source":"src.txt","span":"al\\u0000pha","expect":"supported"}', "unsupported/absent"),
 ("span-u0000-inside-unsup",b'{"id":"u2","source":"src.txt","span":"al\\u0000pha","expect":"unsupported"}', "unsupported/absent"),
 ("span-u0000-end",         b'{"id":"u3","source":"src.txt","span":"alpha\\u0000","expect":"supported"}', "unsupported/absent"),
 ("span-u0000-joined",      b'{"id":"u4","source":"src.txt","span":"alpha\\u0000 beta","expect":"supported"}', "unsupported/absent"),
 ("expect-u0000",           b'{"id":"u5","source":"src.txt","span":"alpha","expect":"supp\\u0000orted"}', "expect-invalid"),
 ("line-u0000",             b'{"id":"u6","source":"src.txt","span":"alpha","expect":"supported","line":"\\u00002"}', "line-invalid"),
 ("source-u0000",           b'{"id":"u7","source":"src\\u0000.txt","span":"alpha","expect":"supported"}', "source-not-resolved"),
 ("id-u0000",               b'{"id":"u\\u00008","source":"src.txt","span":"alpha","expect":"supported"}', "id-identity"),
 ("sha-u0000",              b'{"id":"u9","source":"src.txt","span":"alpha","expect":"supported","sha256":"' + b'0'*64 + b'\\u0000"}', "sha-malformed(r31)"),
 ("span-u0080",             b'{"id":"u10","source":"src.txt","span":"\\u00e9","expect":"supported"}', "unsupported"),
 ("span-lone-surrogate",    b'{"id":"u11","source":"src.txt","span":"\\ud800","expect":"supported"}', "unsupported"),
 ("span-ascii-u0061",       b'{"id":"u12","source":"src.txt","span":"\\u0061lpha","expect":"supported"}', "supported"),
]
def pyval(l):
    try: return json.loads(l.decode()), ""
    except Exception as e: return None, type(e).__name__
os.makedirs(ROOT,exist_ok=True)
open(os.path.join(ROOT,"src.txt"),"wb").write(b"alpha beta.\ngamma delta.\n")
open(CLAIMS,"wb").write(b"\n".join(c[1] for c in CASES)+b"\n")
env=dict(os.environ); env.update(TMPDIR=os.path.join(HERE,"tmp"),CHOUSA_STRICT="0")
for k in ("CHOUSA_CLAIMS","CHOUSA_RECORD","CHOUSA_ROOT"): env.pop(k,None)
os.makedirs(env["TMPDIR"],exist_ok=True)
outs={}
for gate,label in ((BASE,"base"),(LAND,"landed")):
    cp=subprocess.run(["bash",gate,"verify-claims",CLAIMS,"--root",ROOT],capture_output=True,timeout=600,env=env)
    out=cp.stdout.decode("utf-8","backslashreplace")
    open(os.path.join(HERE,"escape-"+label+".out"),"w").write(out)
    outs[label]=[l for l in out.splitlines() if l.startswith("CLAIM id=")]
    print(label,"rc=",cp.returncode)
print()
for i,(tag,line,note) in enumerate(CASES):
    v,err=pyval(line)
    tspan = v.get("span") if isinstance(v,dict) else None
    print("%-26s py=%-16s true_span=%-14r"% (tag, "ok" if err=="" else "inval:"+err, tspan))
    for label in ("base","landed"):
        r=outs[label][i] if i<len(outs[label]) else "MISSING"
        print("    %-7s %s"%(label,r))
print()
print("--- findings mentioning our ids ---")
for l in open(os.path.join(HERE,"escape-landed.out")):
    if "u1" in l or "u5" in l or "u6" in l or "u7" in l or "u9" in l: print(l.rstrip())
