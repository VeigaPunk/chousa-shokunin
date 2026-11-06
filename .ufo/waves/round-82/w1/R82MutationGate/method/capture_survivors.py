#!/usr/bin/env python3
"""Capture full counter output for the surviving gate mutants, then restore bytes."""
import concurrent.futures as cf
import hashlib
import importlib.util
import os
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/chousa-r82/R82MutationGate"
OUTD = os.path.join(ROOT, "receipts")
spec = importlib.util.spec_from_file_location("gm", os.path.join(ROOT, "gate_mutants.py"))
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)
SURV = ["MG09-drop-dquote-fold", "MG10-drop-squote-fold", "MG11-drop-star-fold",
        "MG14-drop-SW_CLAIMS", "MG15-drop-SW_IDS-cid", "MG16-drop-token-match",
        "MG21-drop-placeholder-annotation", "MG23-drop-underscore-fold"]
INDEX = {m[0]: i + 1 for i, m in enumerate(gm.MUTANTS)}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def one(mid):
    tree = os.path.join(ROOT, "mut-trees", f"mu{INDEX[mid]:02d}")
    path = os.path.join(tree, "tools/research-gate.sh")
    pristine = open(os.path.join(ROOT, "tools/research-gate.sh"), "rb").read()
    mut = next(m for m in gm.MUTANTS if m[0] == mid)
    mutated = pristine.decode().replace(mut[2], mut[3], 1).encode()
    tmp = path + ".new"
    open(tmp, "wb").write(mutated)
    os.replace(tmp, path)
    os.makedirs(OUTD, exist_ok=True)
    out = os.path.join(OUTD, f"gate-survivor-{mid}.txt")
    try:
        p = subprocess.run([sys.executable, "-B", "corpus/evidence/round82/k2-gate-r82.py",
                            "--root", tree], cwd=tree, capture_output=True, text=True, timeout=1200)
        with open(out, "w") as fh:
            fh.write(f"# cmd: python3 -B corpus/evidence/round82/k2-gate-r82.py --root {tree}  (cwd=tree)\n")
            fh.write(f"# mutated tools/research-gate.sh sha256={sha(mutated)} (pristine {sha(pristine)})\n")
            fh.write(p.stdout)
            fh.write(p.stderr)
            fh.write(f"rc={p.returncode}\n")
        return {"id": mid, "rc": p.returncode, "receipt": out,
                "summary": [l for l in p.stdout.splitlines() if l.startswith(("RUNLINES=", "K2_GATE="))]}
    finally:
        tmp = path + ".orig"
        open(tmp, "wb").write(pristine)
        os.replace(tmp, path)
        assert sha(open(path, "rb").read()) == sha(pristine), mid


def main():
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(one, SURV):
            print(r)


if __name__ == "__main__":
    main()
