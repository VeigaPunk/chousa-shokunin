import json, os, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,"fn","root")
CLAIMS=os.path.join(ROOT,"claims.jsonl"); BASE=os.path.join(HERE,"base-gate.sh")
LAND="/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh"
ORACLE="/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/controls/L1-design/oracle-gate.sh"
P=b'"source":"src.txt","span":"alpha","expect":"supported"'
EX=[b',"meta":[1,,2]', b',"meta":{,}', b',"meta":{"a"}', b',"meta":"\\z"', b',"meta":"\\u12"',
    b',"meta":True', b',"meta":+1', b',"meta":.5', b',"meta":1e', b',"meta":0x10', b',"meta":NaN',
    b',"meta":{"a":1,}', b',"x"::"y"', b',"meta":\'a\'', b',"meta":{"a":1,,"b":2}',
    b',"meta":[{"a":1},]', b',"meta":-}', b',"meta":1.', b',"meta":tru', b',"meta":{"a":1}}']
lines=[b'{"id":"n%02d",'%i + P + e + b'}' for i,e in enumerate(EX)]
os.makedirs(ROOT,exist_ok=True)
open(os.path.join(ROOT,"src.txt"),"wb").write(b"alpha beta.\ngamma delta.\n")
open(CLAIMS,"wb").write(b"\n".join(lines)+b"\n")
env=dict(os.environ); env.update(TMPDIR=os.path.join(HERE,"tmp"),CHOUSA_STRICT="0")
for k in ("CHOUSA_CLAIMS","CHOUSA_RECORD","CHOUSA_ROOT"): env.pop(k,None)
os.makedirs(env["TMPDIR"],exist_ok=True)
def run(g,label):
    cp=subprocess.run(["bash",g,"verify-claims",CLAIMS,"--root",ROOT],capture_output=True,timeout=600,env=env)
    out=cp.stdout.decode("utf-8","backslashreplace")
    open(os.path.join(HERE,"nested-"+label+".out"),"w").write(out)
    return [l for l in out.splitlines() if l.startswith("CLAIM id=")]
res={l:run(g,l) for g,l in ((BASE,"base"),(LAND,"landed"),(ORACLE,"oracle"))}
for i,(e,l) in enumerate(zip(EX,lines)):
    try: json.loads(l.decode()); pv="ok"
    except Exception as ex: pv="inv:"+type(ex).__name__
    get=lambda lab: (res[lab][i].split("observed=")[1].split()[0] if i<len(res[lab]) else "MISSING")
    print('%-26s py=%-18s base=%-10s landed=%-10s oracle=%-10s'%(e.decode('latin1'),pv,get("base"),get("landed"),get("oracle")))
