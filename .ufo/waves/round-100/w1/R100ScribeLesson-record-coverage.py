import re,subprocess,sys
rev=sys.argv[1]; lane=sys.argv[2]
src=subprocess.run(["git","-C",lane,"show",f"{rev}:corpus/SOURCES.md"],capture_output=True,text=True).stdout if rev!="WORKTREE" else open(f"{lane}/corpus/SOURCES.md",encoding="utf-8").read()
opened=[]
for ln in src.split("\n"):
    if ln.startswith("| S"):
        c=[x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c)==11 and c[8]=="2026-11-09": opened.append(c[0])
if rev=="WORKTREE":
    files=subprocess.run(["git","-C",lane,"ls-files","corpus/knowledge","corpus/lessons"],capture_output=True,text=True).stdout.split()
else:
    files=subprocess.run(["git","-C",lane,"ls-tree","-r","--name-only",rev,"--","corpus/knowledge","corpus/lessons"],capture_output=True,text=True).stdout.split()
bad=0
for sid in opened:
    n=0
    for f in files:
        if not f.endswith(".md"): continue
        b=subprocess.run(["git","-C",lane,"show",f"{rev}:{f}"],capture_output=True,text=True).stdout if rev!="WORKTREE" else open(f"{lane}/{f}",encoding="utf-8",errors="replace").read()
        n+=len(re.findall(rf"^GATE-RECORD {sid} ",b,re.M))
    print(f"ROW {sid} gate_records={n}" + ("" if n else "   <-- NO GATE-RECORD"))
    if not n: bad+=1
print(f"RECORD_COVERAGE rev={rev[:8]} rows_opened={len(opened)} rows_without_record={bad}")
sys.exit(1 if bad else 0)
