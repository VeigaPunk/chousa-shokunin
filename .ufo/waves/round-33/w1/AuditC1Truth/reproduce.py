import hashlib, importlib.util, json, os, sys
spec = importlib.util.spec_from_file_location("c1", "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py")
c1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
seed = int(sys.argv[1]); out = sys.argv[2]
os.makedirs(out, exist_ok=True)
claims, truth = c1.generate(out, seed)
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(65536),b''): h.update(c)
    return h.hexdigest()
res={"seed":seed,"claims_sha256":sha(claims),"files":{}}
for f in sorted(os.listdir(os.path.join(out,"src"))):
    p=os.path.join(out,"src",f); s=os.stat(p)
    res["files"]["src/"+f]={"sha256":sha(p),"mtime_ns":s.st_mtime_ns,"ino":s.st_ino}
print(json.dumps(res))
