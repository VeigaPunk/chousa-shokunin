import json, os, subprocess, hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,"fk","root")
CLAIMS=os.path.join(ROOT,"claims.jsonl")
LAND="/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh"
BASE=os.path.join(HERE,"base-gate.sh")
P=b'"source":"src.txt","span":"alpha","expect":"supported"'
KEYS=[b"a]b",b"a[b",b"a*b",b"a?b",b"a$b",b"a`b",b"a!b",b"a@b",b"a#b",b"a(b)",b"a|b",b"a&b",b"a;b",b"a<b>",b"a b",b"a=b",b"line]",b"x\"",b"\\",b"-n",b"-e",b"%s%d",b"a{b",b"a}b"]
lines=[]
for i,k in enumerate(KEYS):
    lines.append(b'{"id":"k%02d",'%i + b'"'+k+b'":1,' + P + b'}')
def pyvalid(l):
    try: json.loads(l.decode())
    except Exception: return False
    return True
os.makedirs(ROOT,exist_ok=True)
open(os.path.join(ROOT,"src.txt"),"wb").write(b"alpha beta.\ngamma delta.\n")
open(CLAIMS,"wb").write(b"\n".join(lines)+b"\n")
env=dict(os.environ); env.update(TMPDIR=os.path.join(HERE,"tmp"),CHOUSA_STRICT="0")
for k in ("CHOUSA_CLAIMS","CHOUSA_RECORD","CHOUSA_ROOT"): env.pop(k,None)
os.makedirs(env["TMPDIR"],exist_ok=True)
for gate,label in ((BASE,"base"),(LAND,"landed")):
    cp=subprocess.run(["bash",gate,"verify-claims",CLAIMS,"--root",ROOT],capture_output=True,timeout=600,env=env)
    out=cp.stdout.decode("utf-8","backslashreplace"); err=cp.stderr.decode("utf-8","backslashreplace")
    open(os.path.join(HERE,"keychar-"+label+".out"),"w").write(out+"\n--stderr--\n"+err)
    rows=[l for l in out.splitlines() if l.startswith("CLAIM id=")]
    print(label,"rc=",cp.returncode,"claims=",len(rows))
    for i,(k,l) in enumerate(zip(KEYS,lines)):
        obs=rows[i].split("observed=")[1].split()[0] if i<len(rows) else "MISSING"
        flag="" if obs=="supported" else "  <== NOT supported (py_valid=%s)"%pyvalid(l)
        print("  %-6s py=%-3s obs=%-10s%s"%(k.decode('latin1'),pyvalid(l),obs,flag))
    if err.strip(): print("  STDERR:",err.strip()[:400])
