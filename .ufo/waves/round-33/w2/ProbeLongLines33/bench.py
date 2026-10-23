#!/usr/bin/env python3
"""Time `verify-claims` on base (f4731885...) vs landed (94a7be5a...) gates.
Wall + child CPU (user+sys) via getrusage(RUSAGE_CHILDREN); every run under
`timeout 300`; stdout/stderr captured to files (never piped)."""
import hashlib
import json
import os
import resource
import subprocess
import sys
import time

B = os.path.dirname(os.path.abspath(__file__))
GATES = {"base": os.path.join(B, "gate-base.sh"),
         "landed": os.path.join(B, "gate-landed.sh")}
FX = os.path.join(B, "fx")
OUTDIR = os.path.join(B, "out")
CASES = ["span512", "span4096", "span16384", "span65536", "pad65536", "many200"]
LOCALES = ["C", "en_US.UTF-8"]
REPS = {"span512": 3, "span4096": 2, "span16384": 1, "span65536": 1,
        "pad65536": 1, "many200": 1}


def run_one(gate, case, loc, rep):
    d = os.path.join(FX, case)
    claims = os.path.join(d, "claims.jsonl")
    tag = "%s.%s.%s.r%d" % (case, os.path.basename(gate).split('-')[1], loc.replace('.', '_'), rep)
    outf = os.path.join(OUTDIR, tag + ".out")
    errf = os.path.join(OUTDIR, tag + ".err")
    env = dict(os.environ)
    env.update({"LC_ALL": loc, "LANG": loc, "CHOUSA_ROOT": d,
                "C1_TMP": os.path.join(B, "tmp"), "C2_TMP": os.path.join(B, "tmp2"),
                "TMPDIR": os.path.join(B, "tmp")})
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    cmd = ["timeout", "300", "bash", gate, "verify-claims", claims]
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.monotonic()
    with open(outf, "wb") as fo, open(errf, "wb") as fe:
        p = subprocess.run(cmd, cwd=d, env=env, stdout=fo, stderr=fe)
    wall = time.monotonic() - t0
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
    out = open(outf, "rb").read().decode("utf-8", "replace")
    err = open(errf, "rb").read().decode("utf-8", "replace")
    claimline = [l for l in out.splitlines() if l.startswith("CLAIM id=")]
    verdict = [l for l in out.splitlines() if l.startswith("VERDICT_BEARING_CLAIMS=")]
    roll = [l for l in out.splitlines() if l.startswith("RESEARCH_GATE:")]
    return {"gate": os.path.basename(gate), "gate_sha256":
            hashlib.sha256(open(gate, "rb").read()).hexdigest(),
            "case": case, "locale": loc, "rep": rep, "cmd": cmd,
            "exit": p.returncode, "wall_s": round(wall, 4),
            "cpu_s": round(cpu, 4),
            "claims": claimline[:3], "verdict": verdict, "roll": roll,
            "err_head": err.splitlines()[:2]}


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for t in ("tmp", "tmp2"):
        os.makedirs(os.path.join(B, t), exist_ok=True)
    rows = []
    only = sys.argv[1:] or None
    for case in CASES:
        if only and case not in only:
            continue
        for loc in LOCALES:
            for rep in range(1, REPS[case] + 1):
                for gname in ("base", "landed"):
                    r = run_one(GATES[gname], case, loc, rep)
                    rows.append(r)
                    print("%-10s %-7s %-11s r%d rc=%d wall=%8.3fs cpu=%8.3fs %s %s"
                          % (r["case"], r["locale"], gname, rep, r["exit"],
                             r["wall_s"], r["cpu_s"],
                             (r["verdict"] or ["-"])[0],
                             (r["claims"] or ["-"])[0][:60]), flush=True)
    with open(os.path.join(B, "results.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main()
