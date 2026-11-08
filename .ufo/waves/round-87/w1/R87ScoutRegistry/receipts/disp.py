#!/usr/bin/env python3
"""R87ScoutRegistry — disposition-gap fixture.

The TEACHES leg disposes a flagged row iff the row is the TARGET of some
supersedes edge, regardless of the superseder's own status.  Here S024 (the only
flagged row at base) is superseded by S031; we set S031's status to `queued`
(i.e. the superseding row is itself not the live citation).  The leg still
reports the flag as disposed "superseded by S031".
"""
import os
import re
import shutil
import subprocess
import sys

BASE = "/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry"
SRC = os.path.join(BASE, "tree")
WORK = os.path.join(BASE, "work", "disp-fixture")
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


r031 = row_of("S031", text)
cells = r031.split("|")
# cells[8] is status (0=id,1=source,2=kind,3=tier,4=scope,5=anchor,6=teaches,
# 7=status,8=opened) -> in the split-by-'|' form the status is the 9th element
new = r031.replace("| mined | 2026-", "| queued | 2026-", 1)
assert new != r031, "status rewrite failed"
text = text.replace(r031, new, 1)
open(spath, "w", encoding="utf-8").write(text)

t = open(spath, encoding="utf-8").read()
for sid in ("S024", "S031"):
    r = row_of(sid, t)
    print(sid, "status cell:", r.split("|")[8].strip())

proc = subprocess.run([sys.executable, "-B", COUNTER, "--root", WORK],
                      capture_output=True, text=True)
print("exit:", proc.returncode)
print(proc.stdout)
