#!/usr/bin/env python3
"""R87ScoutRegistry — chain laundering fixture.

Chain: S033 (mined, head) supersedes S031 (mined) supersedes S024 (queued).
S024 and S031 both carry a contrast+date-term teaches whose own capture lacks
the term.  S033's teaches carries NO contrast.  Question: does the leg's
disposition rule (dispose a flagged row iff it is the target of some
supersedes edge) launder S031's unentailed claim through S033?
"""
import os
import re
import shutil
import subprocess
import sys

BASE = "/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry"
SRC = os.path.join(BASE, "tree")
WORK = os.path.join(BASE, "work", "chain2-fixture")
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


# 1. make S031 a target: S033 supersedes S031
r033 = row_of("S033", text)
text = text.replace(r033, r033.replace("supersedes S020 — ", "supersedes S031 — ", 1), 1)

# 2. give S031 a contrast+date-term teaches that its own capture lacks
#    (capture 11d6cc56bb24adfc61eea2b4 contains neither 'publication' nor
#     'modification' — verified in the base tree)
r031 = row_of("S031", text)
text = text.replace(
    r031,
    r031.replace(
        "no comparison to other date properties claimed",
        "a property separate from publication or modification dates", 1),
    1)

open(spath, "w", encoding="utf-8").write(text)

t = open(spath, encoding="utf-8").read()
for sid in ("S024", "S031", "S033"):
    print(sid, "teaches:", row_of(sid, t).split("|")[7][:170])

proc = subprocess.run([sys.executable, "-B", COUNTER, "--root", WORK],
                      capture_output=True, text=True)
print("exit:", proc.returncode)
print(proc.stdout)
print("STDERR:", proc.stderr[-400:])
