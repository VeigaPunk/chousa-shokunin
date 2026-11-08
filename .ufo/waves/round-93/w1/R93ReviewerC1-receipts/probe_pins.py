#!/usr/bin/env python3
"""R93ReviewerC1 probes against the C1 pin walk (module-level, no instrument execution)."""
import hashlib
import importlib.util
import io
import os
import shutil
import sys

S = "/fast/scratch/hyaku/chousa-r93/R93ReviewerC1"
TREE = os.path.join(S, "tree")
REPO = os.path.join(S, "repo")
REV = "b7241252c2358613d3b22b7d0454d98c56dab373"
CREV = "754b62fb6adc60e44e12375af5461a0ebe302994"
REL_DIR = "corpus/evidence/round93"
PINS_REL = REL_DIR + "/instrument-pins.txt"
EXP_REL = REL_DIR + "/controls/expected.tsv"
REC_REL = REL_DIR + "/controls/receipts"


def load(tree):
    path = os.path.join(tree, REL_DIR, "control-driver-r93.py")
    spec = importlib.util.spec_from_file_location("drv_" + hashlib.sha256(tree.encode()).hexdigest()[:8], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def paths(tree):
    return (tree, os.path.join(tree, EXP_REL), os.path.join(tree, PINS_REL), os.path.join(tree, REC_REL))


def report(tag, drv, tree):
    root, exp, pins, rec = paths(tree)
    rows = drv.read_expected(exp)
    prow = drv.read_pins(pins)
    codes, checked, rchecked, rtotal = drv.pin_report(rows, root, exp, pins, rec)
    drift = drv.self_pin(REPO, root, REV, CREV, exp, rec, prow, pins)
    print(f"[{tag}] rows={len(rows)} pins={len(prow) if prow is not None else None} "
          f"checked={checked} rchecked={rchecked}/{rtotal}")
    print(f"[{tag}] pin_codes={codes}")
    print(f"[{tag}] self_pin_drift={drift}")
    return codes, checked, len(prow) if prow else 0, drift


base = load(TREE)
root, exp, pins_path, rec = paths(TREE)
rows = base.read_expected(exp)
pins = base.read_pins(pins_path)
print(f"A rows={len(rows)} pins={len(pins)}")
for i, (rel, digest) in enumerate(pins.items(), 1):
    disk = os.path.join(root, rel)
    kind = "self" if rel == PINS_REL else (
        "receipt" if rel.startswith(REC_REL + "/") else
        "instrument" if rel.endswith((".py", ".sh")) else "data")
    real = os.path.realpath(disk)
    inside = not real.startswith("..") and real.startswith(os.path.realpath(root) + os.sep)
    print(f"A row{i:02d} isfile={os.path.isfile(disk)} inside_root={inside} kind={kind} rel={rel}")
codes, checked, rchecked, rtotal = base.pin_report(rows, root, exp, pins_path, rec)
print(f"A pristine pin_report codes={codes} checked={checked}/{len(pins)} receipts={rchecked}/{rtotal}")
print(f"A pristine self_pin drift={base.self_pin(REPO, root, REV, CREV, exp, rec, pins, pins_path)}")
# both minus-self implementations vs stored
stored = pins[PINS_REL]
blob = open(os.path.join(REPO, "corpus/evidence/round93/instrument-pins.txt"), "rb").read()  # disk==carrier here
h = hashlib.sha256()
for ln in io.BytesIO(blob).read().splitlines():
    if ln.endswith(PINS_REL.encode()):
        continue
    h.update(ln + b"\n")
print(f"A minus_self disk={base.pins_file_sha_minus_self(pins_path, PINS_REL)}")
print(f"A minus_self blob={h.hexdigest()}")
print(f"A self_row_stored={stored}")

# duplicate row probe
dup = os.path.join(S, "pins-dup.txt")
with open(pins_path) as fh:
    txt = fh.read().splitlines()
with open(dup, "w") as fh:
    fh.write("\n".join(txt + [txt[0]]) + "\n")
try:
    base.read_pins(dup)
    print("B duplicate row ACCEPTED (unexpected)")
except SystemExit as e:
    print(f"B duplicate row SystemExit code={e.code}")

# directory row probe (self row deleted so the minus-self leg cannot mask the walk)
tdir = os.path.join(S, "t-dir")
shutil.copytree(TREE, tdir, symlinks=True)
pt = os.path.join(tdir, PINS_REL)
keep = [ln for ln in open(pt).read().splitlines() if not ln.rstrip().endswith(PINS_REL)]
with open(pt, "w") as fh:
    fh.write("\n".join(keep + ["0" * 64 + "  corpus/evidence/round93"]) + "\n")
report("C-directory-row", load(tdir), tdir)

# rewrite another row, keep self row: the pair must fire
trw = os.path.join(S, "t-rowwrite")
shutil.copytree(TREE, trw, symlinks=True)
pt = os.path.join(trw, PINS_REL)
out = []
for ln in open(pt).read().splitlines():
    if ln.rstrip().endswith(".ufo/waves/round-93/claims.md"):
        d, p = ln.split(None, 1)
        d = ("0" if d[0] != "0" else "1") + d[1:]
        ln = d + "  " + p
    out.append(ln)
with open(pt, "w") as fh:
    fh.write("\n".join(out) + "\n")
report("D-row-rewrite-self-kept", load(trw), trw)

# rewrite another row AND recompute the self row: pin_report green, self_pin must fire
trw2 = os.path.join(S, "t-rowwrite-selfnew")
shutil.copytree(trw, trw2, symlinks=True)
drv2 = load(trw2)
pt = os.path.join(trw2, PINS_REL)
newself = drv2.pins_file_sha_minus_self(pt, PINS_REL)
out = []
for ln in open(pt).read().splitlines():
    if ln.rstrip().endswith(PINS_REL):
        ln = newself + "  " + PINS_REL
    out.append(ln)
with open(pt, "w") as fh:
    fh.write("\n".join(out) + "\n")
report("E-row-rewrite-self-recomputed", load(trw2), trw2)

# delete the self row only: is the table's own byte ever compared?
tdel = os.path.join(S, "t-selfdel")
shutil.copytree(TREE, tdel, symlinks=True)
pt = os.path.join(tdel, PINS_REL)
keep = [ln for ln in open(pt).read().splitlines() if not ln.rstrip().endswith(PINS_REL)]
with open(pt, "w") as fh:
    fh.write("\n".join(keep) + "\n")
report("F-self-row-deleted", load(tdel), tdel)

# delete the self row AND add a row reading outside --root (relative escape + absolute path)
tab = os.path.join(S, "t-absrow")
shutil.copytree(tdel, tab, symlinks=True)
outside = os.path.join(S, "outside.txt")
with open(outside, "w") as fh:
    fh.write("outside-root bytes\n")
pt = os.path.join(tab, PINS_REL)
with open(pt, "a") as fh:
    fh.write(sha(outside) + "  ../outside.txt\n")
    fh.write(sha("/etc/hostname") + "  /etc/hostname\n")
report("G-abs-and-escape-rows", load(tab), tab)

# receipt body rewritten on disk: RECEIPT_MISMATCH, rchecked below rtotal
trec = os.path.join(S, "t-receipt")
shutil.copytree(TREE, trec, symlinks=True)
with open(os.path.join(trec, REC_REL, "c2-prior-landing.txt"), "a") as fh:
    fh.write("# tampered\n")
report("H-receipt-tampered", load(trec), trec)
print("DONE")
