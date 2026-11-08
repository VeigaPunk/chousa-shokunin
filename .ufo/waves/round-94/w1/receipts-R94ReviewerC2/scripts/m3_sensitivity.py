import os, shutil, subprocess, sys
S = "/fast/scratch/hyaku/chousa-r94/R94ReviewerC2"
R = os.path.join(S, "repo")
W = os.path.join(S, "mutants")
REC = os.path.join(S, "receipts")
NEW = os.path.join(R, "corpus/evidence/round94/curation-r94.py")
PRIST = os.path.join(S, "controls-work", "pristine")

# m3 redo: coherent joint edit of counter (leg deleted, arity 15) + legs.txt (name deleted)
src = open(NEW, encoding="utf-8").read()
start = src.index("    # 16. PUNCTQUOT"); end = src.index('or "0"))\n', start) + len('or "0"))\n')
p2 = os.path.join(W, "m2-delete-leg-arities.py")
mroot = os.path.join(W, "tree-m3b")
shutil.rmtree(mroot, ignore_errors=True)
shutil.copytree(R, mroot, symlinks=True, ignore=shutil.ignore_patterns(".git"))
legs = os.path.join(mroot, "corpus/evidence/round94/controls/legs.txt")
t = open(legs, encoding="utf-8").read()
names = [l for l in t.split("\n") if l.strip() and l.strip() != "PUNCTQUOT"]
open(legs, "w", encoding="utf-8").write("\n".join(names) + "\n")
print("legs now", len(names), names[-3:])
p = subprocess.run([sys.executable, "-B", p2, "--root", mroot], capture_output=True, text=True)
open(os.path.join(REC, "m3b-coherent-joint.txt"), "w").write(f"exit={p.returncode}\n{p.stdout}{p.stderr}")
print("m3b rc", p.returncode)
for ln in p.stdout.splitlines():
    if ln.startswith(("CURATION_R94=", "LEG_FAIL", "SUPERSEDED_LIVE")):
        print("  ", ln)

# sensitivity: fake battery tree whose OLD prints Q_SHAPE_FAIL=1
F = os.path.join(S, "fake-battery")
shutil.rmtree(F, ignore_errors=True)
for sub in ("round90", "round93", "round94"):
    shutil.copytree(os.path.join(R, "corpus/evidence", sub), os.path.join(F, sub), symlinks=True)
oldp = os.path.join(F, "round93/curation-r93.py")
o = open(oldp, encoding="utf-8").read()
assert "Q_SHAPE_FAIL={len(shape_violations)}" in o
open(oldp, "w", encoding="utf-8").write(o.replace("Q_SHAPE_FAIL={len(shape_violations)}", "Q_SHAPE_FAIL=1"))
work = os.path.join(S, "sensitivity-work")
p = subprocess.run([sys.executable, "-B", os.path.join(F, "round94/curation-controls-r94.py"),
                    "--root", R, "--work", work], capture_output=True, text=True)
open(os.path.join(REC, "sensitivity-battery.txt"), "w").write(f"exit={p.returncode}\n{p.stdout}{p.stderr}")
print("sensitivity rc", p.returncode)
for ln in p.stdout.splitlines():
    if ln.startswith(("OK ", "FAIL ", "CONTROLS=")):
        print("  ", ln)
