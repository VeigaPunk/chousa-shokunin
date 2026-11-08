#!/usr/bin/env python3
"""Scratch probe for R93ReviewerC2: mutation trees against curation-r93.py. Writes only under scratch."""
import os
import re
import shutil
import subprocess
import sys

REPO = "/fast/scratch/hyaku/chousa-r93/R93ReviewerC2/repo"
S = "/fast/scratch/hyaku/chousa-r93/R93ReviewerC2"
W = os.path.join(S, "work")
NEW = os.path.join(REPO, "corpus/evidence/round93/curation-r93.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"
Q2 = '| Q2 | S214 | "date when each source was last searched or consulted." |'


def mirror(dst):
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    shutil.copy2(os.path.join(REPO, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    for rel in (ENTRY_A, ENTRY_B):
        shutil.copy2(os.path.join(REPO, rel), os.path.join(dst, rel))
    for rel in (os.path.join("corpus", "captures"), os.path.join("corpus", "evidence", "round57")):
        src = os.path.join(REPO, rel)
        if os.path.isdir(src):
            os.symlink(src, os.path.join(dst, rel))
    return dst


def edit(path, old, new, count=1):
    text = open(path, encoding="utf-8").read()
    assert old in text, f"pattern absent: {old[:60]!r}"
    open(path, "w", encoding="utf-8").write(text.replace(old, new, count))


def run(tree, counter=NEW):
    p = subprocess.run([sys.executable, "-B", counter, "--root", tree], capture_output=True, text=True)
    out = p.stdout
    keep = [ln for ln in out.splitlines()
            if ln.startswith(("CURATION_R93=", "VERDICT ", "LEG_FAIL", "Q_SHAPE ", "DECISION_WIDTH"))]
    field = {}
    for k in ("Q_WSQUOT", "Q_SHAPE_FAIL", "Q_ROWS", "LEGS_MEASURED", "WARRANT_OK", "UNENTAILED_TERM"):
        m = re.search(rf"(?:^| ){k}=([^ ]+)", out)
        if m:
            field[k] = m.group(1)
    return p.returncode, field, keep


def case(name, mutate):
    tree = os.path.join(W, name)
    shutil.rmtree(tree, ignore_errors=True)
    mirror(tree)
    if mutate:
        mutate(tree)
    rc, f, keep = run(tree)
    print(f"--- {name}: rc={rc} {f}")
    for ln in keep:
        print("   ", ln)
    return rc, f, tree


os.makedirs(W, exist_ok=True)

print("== E1 clean (control) ==")
case("e1-clean", None)

print("== E2 ws quote (space) ==")
case("e2-ws-space", lambda t: edit(os.path.join(t, ENTRY_A), Q2, '| Q2 | S214 | " " |'))

print("== E3 empty quote cell ==")
case("e3-empty-cell", lambda t: edit(os.path.join(t, ENTRY_A), Q2, "| Q2 | S214 |  |"))

print("== E4 bare quote mark ==")
case("e4-bare-quote", lambda t: edit(os.path.join(t, ENTRY_A), Q2, '| Q2 | S214 | " |'))

print("== E5 four-cell whitespace row ==")
case("e5-ws-4cell", lambda t: edit(os.path.join(t, ENTRY_A), Q2, '| Q2 | S214 | " " | extra |'))

print("== E6 ws quote with unresolvable source ==")
case("e6-ws-unresolved", lambda t: edit(os.path.join(t, ENTRY_A), Q2, '| Q2 | S999 | " " |'))

print("== E7 zero-width-space quote ==")
case("e7-zwsp", lambda t: edit(os.path.join(t, ENTRY_A), Q2, '| Q2 | S214 | "\u200b" |'))

print("== E8 non-breaking-space quote ==")
case("e8-nbsp", lambda t: edit(os.path.join(t, ENTRY_A), Q2, '| Q2 | S214 | "\u00a0" |'))

print("== E9 five-cell decision row ==")
ROW13 = ("| Recording when a resource changed | state the date on which the resource was changed | "
         "record that the resource changed without the date on which it changed | Q13 (S023) |")
case("e9-width", lambda t: edit(os.path.join(t, ENTRY_A), ROW13, ROW13 + " extra |"))

print("== E10 padded legitimate quote (clean row, content intact) ==")
case("e10-padded-clean", lambda t: edit(os.path.join(t, ENTRY_A), Q2,
     '| Q2 | S214 | "  date when each source was last searched or consulted.  " |'))

print("== E11 non-Q 3-cell row with empty third cell inside the section ==")
case("e11-nonq-empty", lambda t: edit(os.path.join(t, ENTRY_A), Q2,
     '| note | S214 |  |\n' + Q2))
