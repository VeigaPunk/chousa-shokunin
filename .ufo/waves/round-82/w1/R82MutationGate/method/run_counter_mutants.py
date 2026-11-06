#!/usr/bin/env python3
"""Score frozen-counter mutants against the committed round-82 control battery."""
import concurrent.futures as cf
import json
import os
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/chousa-r82/R82MutationGate"
REPO = os.path.join(ROOT, "repo38")
DRIVER = "corpus/evidence/round82/run-controls-r82.sh"
EXPECTED = os.path.join(REPO, "corpus/evidence/round82/controls/summary.tsv")
WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 10
ONLY = sys.argv[2:]


def expected_map():
    exp = {}
    with open(EXPECTED) as fh:
        for ln in fh:
            cid, e, _o = ln.rstrip("\n").split("\t")
            exp[cid] = e
    return exp


def score(m):
    mid = m["id"]
    out = os.path.join(ROOT, "out-counter38", mid)
    scr = os.path.join(ROOT, "drvtmp", mid)
    os.makedirs(scr, exist_ok=True)
    env = dict(os.environ, HYAKU_SCRATCH=scr)
    p = subprocess.run(["bash", os.path.join(REPO, DRIVER), m["commit"], out],
                       cwd=REPO, env=env, capture_output=True, text=True, timeout=1800)
    exp = expected_map()
    obs = {}
    sp = os.path.join(out, "summary.tsv")
    if os.path.isfile(sp):
        with open(sp) as fh:
            for ln in fh:
                parts = ln.rstrip("\n").split("\t")
                if len(parts) == 3:
                    obs[parts[0]] = parts[2]
    mism = {k: (exp[k], obs.get(k, "MISSING")) for k in exp if obs.get(k) != exp[k]}
    # which control receipts exist and their rc
    rcs = {}
    if os.path.isdir(out):
        for f in os.listdir(out):
            if f.endswith(".txt"):
                txt = open(os.path.join(out, f), encoding="utf-8", errors="replace").read()
                r = [ln for ln in txt.splitlines() if ln.startswith("rc=")]
                rcs[f[:-4]] = r[-1] if r else "NO-RC"
    return {"id": mid, "desc": m["desc"], "commit": m["commit"],
            "driver_rc": p.returncode, "killed": bool(mism), "mismatches": mism,
            "controles": rcs, "stdout_tail": p.stdout.strip().splitlines()[-2:],
            "stderr_tail": p.stderr.strip().splitlines()[-2:]}


def main():
    with open(os.path.join(ROOT, "counter-mutants38.json")) as fh:
        muts = json.load(fh)
    todo = [m for m in muts if "commit" in m and (not ONLY or m["id"] in ONLY)]
    res = []
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(score, m): m["id"] for m in todo}
        for f in cf.as_completed(futs):
            r = f.result()
            res.append(r)
            print(json.dumps({k: r[k] for k in ("id", "killed", "mismatches")}))
    res.sort(key=lambda r: r["id"])
    with open(os.path.join(ROOT, "counter-mutant-results38.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    kills = sum(1 for r in res if r["killed"])
    print(f"COUNTER_MUTANTS killed={kills}/{len(res)}")


if __name__ == "__main__":
    main()
