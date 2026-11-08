import os, re, shutil, subprocess, sys
S = "/fast/scratch/hyaku/chousa-r94/R94ReviewerC2"
R = os.path.join(S, "repo")
W = os.path.join(S, "mutants")
REC = os.path.join(S, "receipts")
PRIST = os.path.join(S, "controls-work", "pristine")
NEW = os.path.join(R, "corpus/evidence/round94/curation-r94.py")
shutil.rmtree(W, ignore_errors=True); os.makedirs(W); os.makedirs(REC, exist_ok=True)

def run(tag, counter, root, work):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    out = p.stdout + p.stderr
    open(os.path.join(REC, tag + ".txt"), "w", encoding="utf-8").write(f"exit={p.returncode}\n{out}")
    return p.returncode, out

def show(tag, out):
    print("==", tag)
    for ln in out.splitlines():
        if ln.startswith(("CURATION_R94=", "LEG_FAIL", "Q_PUNCTQUOT", "SUPERSEDED_LIVE")):
            print("  ", ln)

src = open(NEW, encoding="utf-8").read()
start = src.index("    # 16. PUNCTQUOT")
end = src.index('or "0"))\n', start) + len('or "0"))\n')
noleg = src[:start] + src[end:]
assert '("PUNCTQUOT"' not in noleg

# m1: delete the leg only
p1 = os.path.join(W, "m1-delete-leg.py"); open(p1,"w").write(noleg)
rc, out = run("m1-delete-leg", p1, R, W); show("m1 delete leg only (clean tree)", out)

# m2: delete the leg and lower EXPECTED_LEGS
p2 = os.path.join(W, "m2-delete-leg-arities.py"); open(p2,"w").write(noleg.replace("EXPECTED_LEGS = 16", "EXPECTED_LEGS = 15"))
rc, out = run("m2-delete-leg-arity15", p2, R, W); show("m2 + EXPECTED_LEGS=15 (legs.txt still 16)", out)

# m3: coherent joint edit: delete leg, lower arity, drop the table name
mroot = os.path.join(W, "tree-m3"); shutil.copytree(R, mroot, symlinks=True,
    ignore=shutil.ignore_patterns(".git"))
legs = os.path.join(mroot, "corpus/evidence/round94/controls/legs.txt")
open(legs,"w").write("\n".join(l for l in open(legs).read().split("\n") if l.strip() != "PUNCTQUOT") + "\n")
rc, out = run("m3-coherent-joint", p2, mroot, W); show("m3 + legs.txt edit (coherent joint)", out)

# m4: leg present but vacuous; clean tree
p4 = os.path.join(W, "m4-vacuous-leg.py")
open(p4,"w").write(src.replace('legs.append(("PUNCTQUOT", not punct_quote_rows,', 'legs.append(("PUNCTQUOT", True,'))
rc, out = run("m4-vacuous-leg", p4, R, W); show("m4 vacuous leg (clean tree)", out)
rc, out = run("m4-vacuous-leg-x1", p4, os.path.join(S, "controls-work/x1-punct-dash"), W); show("m4 vacuous leg (x1 tree)", out)

# m5: guard removed, witness row kept -> the witness row is the guard's only verdict force
g = src.replace("return cap is not None and bool(PUNCT_RE.search(quote)) and norm(quote) in cap",
                "return cap is not None and norm(quote) in cap")
p5 = os.path.join(W, "m5-noguard-witness.py"); open(p5,"w").write(g)
rc, out = run("m5-noguard-witness", p5, R, W); show("m5 no guard, witness kept (clean tree)", out)

# full clean-tree summary lines for the receipts already written
for tag in ("A-copyright-r93","A-copyright-r94","B-cjk-r94"):
    p = os.path.join(REC, tag + ".txt")
    if os.path.isfile(p):
        print("==", tag, "full field line:")
        for ln in open(p).read().splitlines():
            if ln.startswith("SUPERSEDED_LIVE"):
                print("  ", ln)
