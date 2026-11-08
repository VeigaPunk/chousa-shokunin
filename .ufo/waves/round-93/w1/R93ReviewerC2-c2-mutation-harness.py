#!/usr/bin/env python3
"""Scratch mutation harness for R93ReviewerC2: delete the WSQUOTE leg, delete the DECISION_WIDTH print,
and mutate r92's shape test. Writes only under the seat scratch dir."""
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r93/R93ReviewerC2"
REPO = os.path.join(S, "repo")
W = os.path.join(S, "work")
MUT = os.path.join(S, "mut")
NEW = os.path.join(REPO, "corpus/evidence/round93/curation-r93.py")
OLD = os.path.join(REPO, "corpus/evidence/round92/curation-r92.py")
CTRL = os.path.join(REPO, "corpus/evidence/round93/curation-controls-r93.py")
REG90 = os.path.join(REPO, "corpus/evidence/round90/curation-r90-controls.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"

WS_BLOCK = ('    legs.append(("WSQUOTE", not ws_quote_rows,\n'
            '                 "; ".join(f"{os.path.basename(r)} {qid}" for r, qid in ws_quote_rows) or "0"))\n')
DW_BLOCK = ('    for rel, line, detail in decision_width:\n'
            '        print(f"DECISION_WIDTH {os.path.basename(rel)} row={line} {detail}")\n')


def text(p):
    return open(p, encoding="utf-8").read()


def write(p, t):
    open(p, "w", encoding="utf-8").write(t)


def run(counter, root):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    keep = [ln for ln in p.stdout.splitlines()
            if ln.startswith(("CURATION_R93=", "VERDICT ", "LEG_FAIL", "DECISION_WIDTH", "Q_SHAPE "))]
    return p.returncode, keep


os.makedirs(MUT, exist_ok=True)

src = text(NEW)

# D1: delete the WSQUOTE leg only.
assert WS_BLOCK in src, "WSQUOTE block absent"
d1 = os.path.join(MUT, "curation-noleg.py")
write(d1, src.replace(WS_BLOCK, ""))
# D2: delete the leg and drop the arity constant to 14.
d2 = os.path.join(MUT, "curation-noleg-arity14.py")
write(d2, src.replace(WS_BLOCK, "").replace("EXPECTED_LEGS = 15", "EXPECTED_LEGS = 14"))
# D3: delete the DECISION_WIDTH print loop only.
assert DW_BLOCK in src, "DECISION_WIDTH print block absent"
d3 = os.path.join(MUT, "curation-nodwprint.py")
write(d3, src.replace(DW_BLOCK, ""))

for name, counter, tree in (
    ("D1 noleg/clean", d1, os.path.join(W, "e1-clean")),
    ("D1 noleg/ws-space", d1, os.path.join(W, "e2-ws-space")),
    ("D2 noleg+arity14/clean", d2, os.path.join(W, "e1-clean")),
    ("D2 noleg+arity14/ws-space", d2, os.path.join(W, "e2-ws-space")),
    ("D3 nodwprint/clean", d3, os.path.join(W, "e1-clean")),
    ("D3 nodwprint/width-row", d3, os.path.join(W, "e9-width")),
    ("D3 original/width-row", NEW, os.path.join(W, "e9-width")),
):
    rc, keep = run(counter, tree)
    print(f"--- {name}: rc={rc}")
    for ln in keep:
        print("   ", ln)

# D4: mutate r92's shape test to the r93 logic (a "fixed r92"), then run a controls copy against it.
r92 = text(OLD)
old_shape = '    if not cells[2].strip().strip(\'"\'):\n        return "quote=<empty>"\n'
new_shape = ('    inner = cells[2].strip().strip(\'"\').strip()\n'
             '    if not inner:\n'
             '        return "quote=<empty>" if not cells[2].strip().strip(\'"\') else "quote=<whitespace>"\n')
assert old_shape in r92, "r92 shape test pattern absent"
r92fix = os.path.join(MUT, "curation-r92-shapefix.py")
write(r92fix, r92.replace(old_shape, new_shape))

ctrl = text(CTRL)
ctrl = ctrl.replace('OLD = os.path.join(os.path.dirname(HERE), "round92", "curation-r92.py")', f'OLD = {r92fix!r}')
ctrl = ctrl.replace('NEW = os.path.join(HERE, "curation-r93.py")', f'NEW = {NEW!r}')
ctrl = ctrl.replace('REG = os.path.join(os.path.dirname(HERE), "round90", "curation-r90-controls.py")', f'REG = {REG90!r}')
ctrl_copy = os.path.join(MUT, "curation-controls-shapefix.py")
write(ctrl_copy, ctrl)
p = subprocess.run([sys.executable, "-B", ctrl_copy, "--root", REPO,
                    "--work", os.path.join(W, "c2-controls-shapefix")], capture_output=True, text=True)
print("--- D4 controls with fixed-r92: rc=", p.returncode)
for ln in p.stdout.splitlines():
    if ln.startswith(("CONTROLS=", "OK ws-classification", "FAIL ws-classification")) or "ws-space" in ln or "ws-tab" in ln:
        print("   ", ln)
