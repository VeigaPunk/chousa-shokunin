#!/usr/bin/env python3
"""R87ScoutRegistry — chain-disposition simulation on a throwaway fixture copy.

Builds a 3-node supersession chain X -> Y -> Z in a scratch copy of the landing
tree and runs the committed curation-r87.py against it, to observe whether the
leg's disposition rule handles a chain correctly.  Never touches the lane tree.
"""
import os
import re
import shutil
import subprocess
import sys

BASE = "/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry"
SRC = os.path.join(BASE, "tree")
WORK = os.path.join(BASE, "work", "chain-fixture")
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


# S031 currently supersedes S024 (mined superseder).  We create a chain:
#   S033 supersedes S031   (S031 is now a target, not just a superseder)
#   S031 supersedes S024
# and give S024 the contrast+date-term teaches, and give S033 a teaches with
# NO contrast phrase at all -> the head of the chain carries no contrast.
old031 = row_of("S031", text)
old033 = row_of("S033", text)
assert old031 and old033, "rows not found"

new031 = re.sub(r"\| supersedes S024 — ", "| supersedes S024 — ", old031)
# make S031's teaches ALSO be superseded-bearing is already true; add the chain
# by rewriting S033's teaches to start with "supersedes S031 — "
new033 = old033.replace("| supersedes S020 — ", "| supersedes S031 — ", 1)
text = text.replace(old033, new033, 1)
open(spath, "w", encoding="utf-8").write(text)

# verify
t2 = open(spath, encoding="utf-8").read()
r033 = row_of("S033", t2)
print("S033 new teaches:", r033.split("|")[7][:160])
print("S031 teaches:", row_of("S031", t2).split("|")[7][:160])
print("S024 teaches:", row_of("S024", t2).split("|")[7][:160])

proc = subprocess.run([sys.executable, "-B", COUNTER, "--root", WORK],
                      capture_output=True, text=True)
print("exit:", proc.returncode)
print(proc.stdout)
print("STDERR:", proc.stderr[-500:])
