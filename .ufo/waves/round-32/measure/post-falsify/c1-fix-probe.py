import os,sys,fcntl,subprocess,time,json,tempfile
def fixture(d):
    os.makedirs(d,exist_ok=True)
    open(f"{d}/s.md","w").write("alpha beta gamma\ndelta epsilon\n")
    open(f"{d}/c.jsonl","w").write(json.dumps({"id":"c1","source":"s.md","span":"beta gamma","expect":"supported"})+"\n")
def run(gate,d,manifest):
    env={k:v for k,v in os.environ.items() if not k.startswith("CHOUSA_")}
    return subprocess.Popen(["bash",gate,"verify-all",f"{d}/c.jsonl","--root",d,"--json",manifest],cwd=d,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
for ver in ["old","new"]:
    gate=os.path.abspath(f"{ver}/tools/research-gate.sh")
    # test 1: unreadable under lock
    d=tempfile.mkdtemp(prefix=f"{ver}-t1-",dir="/fast/scratch/hyaku/chousa-r32/l1b/fixtest/tmp"); fixture(d)
    m=f"{d}/m.jsonl"; open(m,"w").close(); os.chmod(m,0o200)
    fd=os.open(m,os.O_WRONLY|os.O_APPEND); fcntl.flock(fd,fcntl.LOCK_EX)
    p=run(gate,d,m); time.sleep(3); os.write(fd,b'{"a":1}'); fcntl.flock(fd,fcntl.LOCK_UN); os.close(fd)
    rc=p.wait(60); os.chmod(m,0o600); data=open(m,"rb").read()
    print(ver,"T1 unreadable-under-lock rc=",rc,"bytes=",data[:60], "glued=", b'}{' in data)
    # test 2: symlink retarget
    d=tempfile.mkdtemp(prefix=f"{ver}-t2-",dir="/fast/scratch/hyaku/chousa-r32/l1b/fixtest/tmp"); fixture(d)
    A=f"{d}/A.jsonl"; B=f"{d}/B.jsonl"; L=f"{d}/L.jsonl"
    open(A,"wb").write(b'{"a":1}'); open(B,"wb").write(b'{"b":1}\n'); os.symlink(A,L)
    fd=os.open(A,os.O_WRONLY|os.O_APPEND); fcntl.flock(fd,fcntl.LOCK_EX)
    p=run(gate,d,L); time.sleep(3); os.unlink(L); os.symlink(B,L); fcntl.flock(fd,fcntl.LOCK_UN); os.close(fd)
    rc=p.wait(60); a=open(A,"rb").read()
    ok=True
    for l in a.split(b"\n"):
        if l:
            try: json.loads(l)
            except Exception: ok=False
    print(ver,"T2 symlink-retarget rc=",rc,"A_lines=",a.count(b"\n"),"A_valid_jsonl=",ok and b"\n\n" not in a)
