#!/usr/bin/env python3
"""R86ExecBase — D1 provenance, mutant derivability, SETUP-leg probe. Committed trees, scratch only."""
import hashlib
import importlib.util
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r86/R86ExecBase"
LAND = os.path.join(S, "land")
BASE85 = os.path.join(S, "base85")
REPO = "/home/vgpnk/Projects/shokunin/chousa-shokunin"

spec = importlib.util.spec_from_file_location(
    "gr86", os.path.join(LAND, "corpus/evidence/round86/gate-records-r86.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
assert os.path.dirname(os.path.abspath(m.__file__)) == os.path.join(LAND, "corpus/evidence/round86")

print("== D1 record built by the frozen counter from the landing tree ==")
d1 = m.build_d1_203_admit(LAND)
print(f"D1_BUILT={d1 is not None}")
sid, rec, code = d1
print(f"D1_SID={sid} D1_EXPECTED={code}")
print("D1_RECORD " + rec)
cap_rel = rec.split(" capture=", 1)[1].split(" ", 1)[0]
q = rec.split(' quote="', 1)[1][:-1]
cap = os.path.join(LAND, cap_rel)
text = m.norm(open(cap, encoding="utf-8", errors="replace").read())
print(f"QUOTE_LOCATED_IN_CAPTURE={m.norm(q) in text} QUOTE_WORDS={len(q.split())} CAPTURE={cap_rel}")

print("\n== M17 derivability from each subject tool's bytes ==")
for label, tool in [("base85-round84-tip", os.path.join(BASE85, "tools/gate-records.py")),
                    ("base86-round85-tip", os.path.join(S, "base86/tools/gate-records.py")),
                    ("landing-667a5d0", os.path.join(LAND, "tools/gate-records.py"))]:
    src = open(tool, encoding="utf-8").read()
    mutant = src.replace('r[6] == "200"', 'r[6].startswith("2")')
    rule = [ln.strip() for ln in src.split("\n") if 'r[6]' in ln and ('2[0-9][0-9]' in ln or '== "200"' in ln)]
    print(f"{label} sha256={hashlib.sha256(src.encode()).hexdigest()} derives={mutant != src} "
          f"delta_bytes={len(mutant) - len(src)} rule_lines={rule}")

print("\n== SETUP leg probe: non-git --repo with a fresh rev record ==")
fresh_admits, fresh_revs, fresh_unreach = m.build_fresh_positives(LAND, REPO)
fresh = fresh_admits + fresh_revs + fresh_unreach
notgit = os.path.join(S, "notgit-probe")
os.makedirs(notgit, exist_ok=True)
rp = os.path.join(S, "setup-probe-record.md")
with open(rp, "w", encoding="utf-8") as fh:
    fh.write(fresh[3][1] + "\n")
print("FRESH_RECORD " + fresh[3][1])
for label, tool in [("base85", os.path.join(BASE85, "tools/gate-records.py")),
                    ("landing", os.path.join(LAND, "tools/gate-records.py"))]:
    p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", LAND, "--repo", notgit, rp],
                       capture_output=True, text=True)
    print(f"{label}: rc={p.returncode} stdout={p.stdout.strip()!r} stderr={p.stderr.strip()!r} "
          f"setup_ok={1 if (p.returncode == 2 and 'GATE_RECORDS_ERROR' in p.stderr) else 0}")
