#!/usr/bin/env python3
import os, re, subprocess, sys, datetime
ROOT="/fast/scratch/hyaku/chousa-r85/R85RevCalendar"
REPO="/home/vgpnk/Projects/shokunin/chousa-shokunin"
TOOL=os.path.join(ROOT,"tools","gate-records.py")
TS_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
def _valid_ts(s):
    try:
        datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False

# 1. strptime leniency asymmetry: lowercase t/z accepted by strptime but rejected by TS_RE
vals = ["2026-01-01t00:00:00Z","2026-01-01T00:00:00z","2026-01-01t00:00:00z"]
for v in vals:
    print(f"LOWER {v!r}: TS_RE={bool(TS_RE.fullmatch(v))} strptime_ok={_valid_ts(v)} combined={bool(TS_RE.fullmatch(v)) and _valid_ts(v)}")

# 2. sec 60: strptime rejects, TS_RE would accept shape-wise
v="2026-12-31T23:59:60Z"
print(f"LEAPSEC {v!r}: TS_RE={bool(TS_RE.fullmatch(v))} strptime_ok={_valid_ts(v)} combined={bool(TS_RE.fullmatch(v)) and _valid_ts(v)}")
# record strptime exception type
try:
    datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
except ValueError as e:
    print(f"  strptime ValueError: {e}")

# 3. Fresh accept probes that should be OK only if refetch row exists — demonstrate that calendar-accept
#    does NOT imply tool OK: leap2024 passes parse but fails REFETCH (correctly). This isolates the calendar leg.
#    Show that a calendar-invalid value fails at PARSE, not REFETCH, for both admit and unreach.
# Already done in run2-output.txt — summarise here by re-reading that file.
print("\n--- run2 summary excerpt ---")
txt=open("/fast/scratch/hyaku/chousa-r85/R85RevCalendar/run2-output.txt",encoding="utf-8").read()
for ln in txt.splitlines():
    if ln.startswith("CASE admit") or ln.startswith("CASE unreach") or ln.startswith("CASE rev "):
        print(ln)

# 4. Baseline positives still OK?
POS_TSV=os.path.join(ROOT,"corpus","evidence","round85","c2-positives.tsv")
def form_of(line):
    if " rev=" in line: return "rev"
    if " curl_rc=" in line: return "unreach"
    return "admit"
pos=[]
for ln in open(POS_TSV,encoding="utf-8"):
    parts=ln.rstrip("\n").split("\t",2)
    if len(parts)<3: continue
    f,n,raw=parts
    sid=re.match(r"^\s*GATE-RECORD (S\d+)",raw).group(1)
    pos.append((f,int(n),sid,raw))
admit=next(p for p in pos if form_of(p[3])=="admit")
# write the pristine frozen positive and check OK
fp="/fast/scratch/hyaku/chousa-r85/R85RevCalendar/pristine-admit.md"
open(fp,"w",encoding="utf-8").write(admit[3]+"\n")
p=subprocess.run([sys.executable,"-B",TOOL,"verify","--root",ROOT,"--repo",REPO,fp],capture_output=True,text=True)
print(f"\nPRISTINE admit {admit[2]}: rc={p.returncode} stdout={p.stdout.strip()}")

# 5. A non-timestamp fetched that is NOT calendar-invalid but refetch-mismatched: sec+1 mutation (counter M07) — should be REFETCH not PARSE.
# Show that the tool distinguishes the two failure layers.
ts=admit[3].split("fetched=")[1].split()[0]
sec=int(ts[17:19])
new_ts=ts[:17]+"%02d"%((sec+1)%60)+"Z"
forged=re.sub(r"(?<= )fetched=\S+","fetched="+new_ts,admit[3],count=1)
fp2="/fast/scratch/hyaku/chousa-r85/R85RevCalendar/m07-test.md"
open(fp2,"w",encoding="utf-8").write(forged+"\n")
p=subprocess.run([sys.executable,"-B",TOOL,"verify","--root",ROOT,"--repo",REPO,fp2],capture_output=True,text=True)
print(f"M07 sec+1 {new_ts}: rc={p.returncode} stdout={p.stdout.strip()}")
