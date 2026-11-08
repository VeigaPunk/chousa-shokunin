#!/usr/bin/env python3
"""R86ExecBase — before-side staleness checks over committed bytes only (no writes outside scratch stdout)."""
import difflib
import hashlib
import os
import re

S = "/fast/scratch/hyaku/chousa-r86/R86ExecBase"
LAND = os.path.join(S, "land")
BASE86 = os.path.join(S, "base86")
BASE85 = os.path.join(S, "base85")
FREEZE = os.path.join(S, "freeze")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def body(p):
    """Receipt lines after the leading '#' provenance header, with a trailing blank dropped."""
    return [ln for ln in open(p, encoding="utf-8").read().split("\n") if not ln.startswith("#")]


print("== instrument / subject-tool hashes ==")
for rel, cmp_pin in [
    ("land/corpus/evidence/round86/gate-records-r86.py", None),
    ("land/corpus/evidence/round86/curation-r86.py", None),
    ("land/corpus/evidence/round86/c2-positives.tsv", None),
    ("land/tools/gate-records.py", None),
    ("base86/tools/gate-records.py", None),
    ("base85/tools/gate-records.py", None),
    ("land/corpus/evidence/round86/instrument-pins.txt", None),
    ("freeze/corpus/evidence/round86/instrument-pins.txt", None),
    ("land/corpus/evidence/round86/controls/receipts/c1-k0-donothing.txt", None),
    ("land/corpus/evidence/round86/controls/receipts/c1-k0b-frozen-instrument.txt", None),
    ("land/corpus/evidence/round86/controls/receipts/c2-d0-donothing.txt", None),
    ("freeze/corpus/evidence/round86/controls/receipts/c1-k0-donothing.txt", None),
    ("freeze/corpus/evidence/round86/controls/receipts/c2-d0-donothing.txt", None),
]:
    p = os.path.join(S, rel)
    print(f"{sha(p)}  {rel}")

print("\n== derivation strings in subject tool bytes ==")
for rel in ["base85/tools/gate-records.py", "base86/tools/gate-records.py", "land/tools/gate-records.py"]:
    src = open(os.path.join(S, rel), encoding="utf-8").read()
    old = 'r[6] == "200"'
    new = 'r[6].startswith("2")'
    mutant = src.replace(old, new)
    print(f"{rel}: count_200_rule={src.count(old)} count_2xx_rule={src.count(new)} "
          f"mutant_differs={mutant != src} mutant_bytes={len(mutant)}")

print("\n== refetch row backing D1 (S021) in landing tree ==")
refp = os.path.join(LAND, "corpus/evidence/round57/refetch.tsv")
for ln in open(refp, encoding="utf-8", errors="replace"):
    f = ln.rstrip("\n").split("\t")
    if len(f) == 9 and f[0] == "S021":
        print("ROW\t" + "\t".join(f))
        url, key, txt_sha = f[1], f[2], f[8]
        print(f"keycheck sha256(url)[:24]={hashlib.sha256(url.encode()).hexdigest()[:24]} rowkey={key} match={hashlib.sha256(url.encode()).hexdigest()[:24] == key}")
        cap = os.path.join(LAND, "corpus", "captures", key + ".txt")
        if os.path.isfile(cap):
            h = sha(cap)
            print(f"capture corpus/captures/{key}.txt sha256={h} row_txt_sha={txt_sha} match={h == txt_sha} bytes={os.path.getsize(cap)}")
        else:
            print(f"capture corpus/captures/{key}.txt MISSING")

print("\n== S216 registry row in landing tree ==")
for ln in open(os.path.join(LAND, "corpus/SOURCES.md"), encoding="utf-8", errors="replace"):
    if re.match(r"^ {0,3}\| S216 \|", ln.rstrip("\n")):
        print(ln.rstrip("\n"))

print("\n== committed control receipt vs reproduction (body lines, '#' headers stripped) ==")
pairs = [
    ("C1", os.path.join(LAND, "corpus/evidence/round86/controls/receipts/c1-k0-donothing.txt"),
     os.path.join(S, "c1b-control-repro-base86root-base85tool.txt")),
    ("C1-landroot", os.path.join(LAND, "corpus/evidence/round86/controls/receipts/c1-k0-donothing.txt"),
     os.path.join(S, "c1a-before-landroot-base85tool.txt")),
    ("C2", os.path.join(LAND, "corpus/evidence/round86/controls/receipts/c2-d0-donothing.txt"),
     os.path.join(S, "c2a-control-repro-base86.txt")),
]
for name, ref, got in pairs:
    a, b = body(ref), body(got)
    if a and a[-1] == "":
        a = a[:-1]
    if b and b[-1] == "":
        b = b[:-1]
    same = a == b
    print(f"{name}: identical={same} ref_lines={len(a)} got_lines={len(b)} ref_sha256={sha(ref)} got_sha256={sha(got)}")
    if not same:
        for d in difflib.unified_diff(a, b, fromfile=ref, tofile=got, lineterm=""):
            print("DRIFT " + d)
