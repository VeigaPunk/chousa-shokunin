#!/usr/bin/env python3
"""R87ScoutRegistry — rejected-row over-fire fixture.

The TEACHES leg has no status filter: it reads every registry row's `teaches`
as a claim.  A `rejected` row's teaches is a rejection RATIONALE, not a claim.
Fixture: give a live, rejected row (S217, status REJECTED) a contrast phrase +
a date term and observe what the leg does.
"""
import os
import re
import shutil
import subprocess
import sys

BASE = "/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry"
SRC = os.path.join(BASE, "tree")
WORK = os.path.join(BASE, "work", "rejected-fixture")
COUNTER = os.path.join(SRC, "corpus", "evidence", "round87", "curation-r87.py")

if os.path.isdir(WORK):
    shutil.rmtree(WORK)
shutil.copytree(SRC, WORK)
spath = os.path.join(WORK, "corpus", "SOURCES.md")
text = open(spath, encoding="utf-8").read()


def row_of(sid, txt):
    for ln in txt.split("\n"):
        if re.match(r"^\s{0,3}\| " + sid + r" \|", ln):
            return ln
    return None


r = row_of("S217", text)
print("S217 status:", r.split("|")[8].strip(), "| teaches BEFORE:", r.split("|")[7].strip()[:120])
new = re.sub(r"\| [^|]{0,600} \| rejected \|",
             "| a property separate from publication or modification dates | rejected |",
             r, count=1)
assert new != r, "rewrite failed"
text = text.replace(r, new, 1)
open(spath, "w", encoding="utf-8").write(text)
print("S217 teaches AFTER :", row_of("S217", open(spath, encoding='utf-8').read()).split("|")[7].strip()[:120])
proc = subprocess.run([sys.executable, "-B", COUNTER, "--root", WORK],
                      capture_output=True, text=True)
print("exit:", proc.returncode)
print(proc.stdout)
