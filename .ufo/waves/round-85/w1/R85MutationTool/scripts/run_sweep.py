#!/usr/bin/env python3
"""Run the frozen round-85 counter against every generated mutant; record predicate lines."""
import json
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r85/R85MutationTool"
TREE = os.path.join(S, "tree")
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
COUNTER = os.path.join(TREE, "corpus/evidence/round85/gate-records-r85.py")
REC = os.path.join(S, "receipts")
WORKROOT = os.path.join(S, "work")
PRED = re.compile(r"^TOOL=\S+ POSITIVE=\S+ FRESH_POSITIVE=\S+ FORGED_REFUSED=\S+ EXPECTED_CODE=\S+ "
                  r"EMPTY_REFUSED=\S+ RC=\S+ SETUP=\S+")
RES = re.compile(r"^GATE_RECORDS_R85=(PASS|FAIL)$")


def main():
    with open(os.path.join(S, "mutants/manifest.json"), encoding="utf-8") as fh:
        manifest = json.load(fh)
    os.makedirs(REC, exist_ok=True)
    rows = []
    for m in manifest:
        name = m["name"]
        work = os.path.join(WORKROOT, name)
        os.makedirs(work, exist_ok=True)
        p = subprocess.run([sys.executable, "-B", COUNTER, "--root", TREE, "--repo", LANE,
                            "--tool", m["path"], "--work", work],
                           capture_output=True, text=True, timeout=300)
        log = p.stdout + (("\n[STDERR]\n" + p.stderr) if p.stderr else "")
        with open(os.path.join(REC, name + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(f"# command: python3 -B {COUNTER} --root {TREE} --repo {LANE} --tool {m['path']} --work {work}\n")
            fh.write(f"# mutant sha256: {m['sha256']}\n# rc: {p.returncode}\n\n")
            fh.write(log)
        pred = next((ln for ln in p.stdout.splitlines() if PRED.match(ln)), "")
        verdict = next((ln.split("=", 1)[1] for ln in p.stdout.splitlines() if RES.match(ln)), "?")
        not_refused = [ln for ln in p.stdout.splitlines() if ln.startswith("NOT_REFUSED ")]
        wrong_code = [ln for ln in p.stdout.splitlines() if ln.startswith("WRONG_CODE ")]
        rows.append({
            "name": name,
            "why": m["why"],
            "sha256": m["sha256"],
            "rc": p.returncode,
            "predicate": pred,
            "verdict": verdict,
            "not_refused": len(not_refused),
            "wrong_code": len(wrong_code),
            "not_refused_classes": sorted({ln.split()[2] for ln in not_refused}),
            "wrong_code_classes": sorted({ln.split()[2] for ln in wrong_code}),
            "receipt": os.path.join(REC, name + ".txt"),
        })
    with open(os.path.join(REC, "sweep.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
    print(f"{'mutant':46s} rc  verdict  nref  wrong  classes")
    for r in rows:
        print(f"{r['name']:46s} {r['rc']:<3} {r['verdict']:8s} {r['not_refused']:<5} {r['wrong_code']:<6} "
              f"{','.join(r['not_refused_classes'] + r['wrong_code_classes'])[:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
