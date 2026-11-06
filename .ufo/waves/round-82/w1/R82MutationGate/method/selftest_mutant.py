#!/usr/bin/env python3
"""Apply one gate mutant to a tree, run the gate --selftest, restore bytes."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/chousa-r82/R82MutationGate"
spec = importlib.util.spec_from_file_location("gm", os.path.join(ROOT, "gate_mutants.py"))
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)


def main():
    mid, idx = sys.argv[1], int(sys.argv[2])
    tree = os.path.join(ROOT, "mut-trees", f"mu{idx:02d}")
    path = os.path.join(tree, "tools/research-gate.sh")
    mut = next(m for m in gm.MUTANTS if m[0] == mid)
    pristine = open(os.path.join(ROOT, "tools/research-gate.sh"), "rb").read()
    text = pristine.decode()
    assert text.count(mut[2]) == 1
    mutated = text.replace(mut[2], mut[3], 1).encode()
    tmp = path + ".new"
    open(tmp, "wb").write(mutated)
    os.replace(tmp, path)
    try:
        p = subprocess.run(["bash", "tools/research-gate.sh", "--selftest"], cwd=tree,
                           capture_output=True, text=True, timeout=1200)
        out = p.stdout + p.stderr
        fails = [ln for ln in out.splitlines() if "FAIL" in ln.upper() or "SKIP" in ln.upper()]
        verdict = [ln for ln in out.splitlines() if "RESEARCH_GATE_SELFTEST" in ln]
        print(json.dumps({"id": mid, "tree": tree, "mut_sha256": hashlib.sha256(mutated).hexdigest(),
                          "selftest_rc": p.returncode, "verdict": verdict[-3:],
                          "fail_lines": fails[:20], "n_fail_lines": len(fails),
                          "tail": out.splitlines()[-4:]}))
        open(os.path.join(ROOT, f"selftest-{mid}.log"), "w").write(out)
    finally:
        tmp = path + ".orig"
        open(tmp, "wb").write(pristine)
        os.replace(tmp, path)
        now = hashlib.sha256(open(path, "rb").read()).hexdigest()
        print(json.dumps({"id": mid, "restored_sha256": now,
                          "restored_ok": now == hashlib.sha256(pristine).hexdigest()}))


if __name__ == "__main__":
    main()
