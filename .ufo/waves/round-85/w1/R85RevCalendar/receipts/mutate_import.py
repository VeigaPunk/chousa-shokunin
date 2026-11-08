#!/usr/bin/env python3
import subprocess, sys, os, re
ROOT = "/fast/scratch/hyaku/chousa-r85/R85RevCalendar"
TOOL = os.path.join(ROOT, "tools", "gate-records.py")
# Copy tool to scratch and drop the datetime import line
src = open(TOOL, encoding="utf-8").read()
print("has import datetime:", "import datetime" in src)
mutated = src.replace("import datetime\n", "", 1)
assert "import datetime" not in mutated, "still has import"
mut_path = "/fast/scratch/hyaku/chousa-r85/R85RevCalendar/gate-records-noimports.py"
open(mut_path, "w", encoding="utf-8").write(mutated)
print("mutated written:", mut_path)

# Try running the counter with --tool pointing at the mutated copy, using a small subset?
# The counter itself imports datetime? No, counter is separate. The tool is run as subprocess.
# We run the counter with --tool and see if it still passes the calendar leg.
# Directly run the mutated tool on a D4 forged line:
POS_TSV = os.path.join(ROOT, "corpus", "evidence", "round85", "c2-positives.tsv")
pos=[]
for ln in open(POS_TSV, encoding="utf-8"):
    parts=ln.rstrip("\n").split("\t",2)
    if len(parts)<3: continue
    f,n,raw=parts
    sid=re.match(r"^\s*GATE-RECORD (S\d+)", raw).group(1)
    pos.append((f,int(n),sid,raw))
def form_of(line):
    if " rev=" in line: return "rev"
    if " curl_rc=" in line: return "unreach"
    return "admit"
admit=next(p for p in pos if form_of(p[3])=="admit")
re.sub(r"(?<= )fetched=\S+", "fetched=2026-13-40T00:00:00Z", admit[3], count=1)
forged = re.sub(r"(?<= )fetched=\S+", "fetched=2026-13-40T00:00:00Z", admit[3], count=1)
fp="/fast/scratch/hyaku/chousa-r85/R85RevCalendar/d4-test.md"
open(fp,"w",encoding="utf-8").write(forged+"\n")
for tool in [TOOL, mut_path]:
    p=subprocess.run([sys.executable,"-B",tool,"verify","--root",ROOT,"--repo","/home/vgpnk/Projects/shokunin/chousa-shokunin",fp],capture_output=True,text=True)
    print(f"\nTOOL {tool}: rc={p.returncode}")
    print("stdout:", p.stdout.strip())
    print("stderr:", p.stderr.strip()[:2000])

# Run the full counter against the mutated tool (expect failure on D4 / calendar leg, or crash)
# Use --work under scratch
import shutil
work="/fast/scratch/hyaku/chousa-r85/R85RevCalendar/counter-mut-work"
os.makedirs(work, exist_ok=True)
p=subprocess.run([sys.executable,"-B",os.path.join(ROOT,"corpus","evidence","round85","gate-records-r85.py"),"--root",ROOT,"--repo","/home/vgpnk/Projects/shokunin/chousa-shokunin","--tool",mut_path,"--work",work],capture_output=True,text=True)
print("\n--- COUNTER with mutated (no datetime) tool ---")
print("rc=",p.returncode)
print(p.stdout[:4000])
print("stderr:",p.stderr[:2000])
