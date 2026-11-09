#!/usr/bin/env python3
"""Mutant + forgery runner for R99MutantsC2. Each mutant in $S/mutants/Mxx.py, forgery via $S/forgeries.py."""
import subprocess, hashlib, pathlib, shutil, os, re, sys
S = pathlib.Path('/fast/scratch/hyaku/chousa-r99/R99MutantsC2')
REPO = S/'repo'
MUT = S/'mutants'
OUT = S/'w1'
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
pristine_control = sha(S/'orig-control.py')
pristine_entry = sha(S/'orig-entry.md')
results=[]
# run baseline
def run(script):
    r=subprocess.run(['python3','-B',str(script),'--root',str(REPO)],capture_output=True,text=True)
    return r.returncode, r.stdout+r.stderr
rc, out = run(REPO/'corpus/evidence/round99/entry-controls-r99.py')
print(f"BASELINE rc={rc} {'PASS' if 'ENTRY_CONTROLS_R99=PASS' in out else 'FAIL'}")
for m in sorted(MUT.glob('M*.py')):
    rc,out = run(m)
    killed = 'ENTRY_CONTROLS_R99=FAIL' in out or 'ENTRY_CONTROLS_SETUP' in out or rc==2
    verdict = 'KILLED' if killed else 'SURVIVED'
    # which legs changed?
    legs = re.findall(r'CASE (\w+) .*? (PASS|FAIL)', out)
    print(f"{m.name} {verdict} rc={rc} legs={legs}")
    results.append((m.name, verdict, rc, out))
    (OUT/(m.stem+'-output.txt')).write_text(f"mutant={m.name}\nverdict={verdict}\nrc={rc}\n"+out)
print("mutation phase done")
