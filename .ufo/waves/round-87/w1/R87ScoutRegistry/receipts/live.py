#!/usr/bin/env python3
"""R87ScoutRegistry — live-row capability fixture.

At the landing revision the TEACHES leg's checked population is exactly ONE row
(S024) and that row is superseded.  Test whether the leg would catch an
unentailed contrast claim on a LIVE row: rewrite S218's teaches (live, mined,
own-work) to carry a contrast phrase + a date term, and run the counter.
"""
import os
import re
import shutil
import subprocess
import sys

BASE = "/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry"
SRC = os.path.join(BASE, "tree")
WORK = os.path.join(BASE, "work", "live-fixture")
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


r = row_of("S218", text)
print("S218 teaches BEFORE:", r.split("|")[7].strip()[:180])
new = re.sub(r"\| [^|]{0,400} \| mined \|",
             "| a last-reviewed date is a property separate from publication or modification dates | mined |",
             r, count=1)
assert new != r
text = text.replace(r, new, 1)
open(spath, "w", encoding="utf-8").write(text)

t = open(spath, encoding="utf-8").read()
print("S218 teaches AFTER :", row_of("S218", t).split("|")[7].strip()[:180])
proc = subprocess.run([sys.executable, "-B", COUNTER, "--root", WORK],
                      capture_output=True, text=True)
print("exit:", proc.returncode)
print(proc.stdout)
