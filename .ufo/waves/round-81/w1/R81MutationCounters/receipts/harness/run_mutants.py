#!/usr/bin/env python3
"""Mutation harness for round-81 C1/C2 counters.

For each mutant: mutate one counter in a private worktree of the candidate
landing rev, run the committed control driver (run-controls.sh) against that
worktree, compare every control's rc with the pristine baseline, then restore
the exact pristine bytes and verify their sha256.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r81/R81MutationCounters"
TREE = os.path.join(S, "tree")
BASE = "378fda82dc2cbcc555a0565052cc408121813cef"
REV = "7e2da96a0541946e796384d42fea18e09ede9e9f"
ALLOW_MULTI = {"c15"}
LINE_RE = re.compile(r"^(\S+) expect_rc=(\d+) got_rc=(\d+)")
sys.path.insert(0, S)
from spec import DEPTH, CHECKLIST  # noqa: E402


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def battery(wt, out, scratch):
    env = dict(os.environ, HYAKU_SCRATCH=scratch)
    p = subprocess.run(["bash", os.path.join(wt, "corpus/evidence/round81/run-controls.sh"), BASE, out],
                       cwd=S, env=env, capture_output=True, text=True, timeout=1200)
    res, crash = {}, []
    for line in p.stdout.splitlines():
        m = LINE_RE.match(line)
        if m:
            res[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    for f in os.listdir(out):
        if f.endswith(".txt"):
            try:
                if "Traceback (most recent call last)" in open(os.path.join(out, f), encoding="utf-8", errors="replace").read():
                    crash.append(f)
            except OSError:
                pass
    return res, sorted(crash), p.returncode, p.stdout


def worker(wi, jobs, results):
    wt = os.path.join(S, "wt%d" % wi)
    if os.path.isdir(wt):
        subprocess.run(["git", "-C", TREE, "worktree", "remove", "--force", wt], capture_output=True)
    subprocess.run(["git", "-C", TREE, "worktree", "add", "-q", "--detach", wt, REV], check=True)
    top = subprocess.run(["git", "-C", wt, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top == wt, (top, wt)
    for mid, fname, edits, desc in jobs:
        path = os.path.join(wt, fname)
        pristine = open(path, encoding="utf-8").read()
        psha = sha(path)
        text = pristine
        for old, new in edits:
            n = text.count(old)
            if n == 0:
                results[mid] = {"error": "target not found: %r" % old[:60]}
                break
            if n > 1 and mid not in ALLOW_MULTI:
                results[mid] = {"error": "%d occurrences of %r" % (n, old[:60])}
                break
            text = text.replace(old, new)
        else:
            assert text != pristine
            open(path, "w", encoding="utf-8").write(text)
            msha = sha(path)
            out = os.path.join(S, "results", mid)
            shutil.rmtree(out, ignore_errors=True)
            try:
                res, crash, drc, stdout = battery(wt, out, os.path.join(S, "drv", "w%d" % wi))
                open(os.path.join(S, "results", mid + ".out"), "w", encoding="utf-8").write(stdout)
            finally:
                subprocess.run(["git", "-C", wt, "checkout", "--", fname], check=True)
            rsha = sha(path)
            results[mid] = {"desc": desc, "file": fname, "mutant_sha": msha, "pristine_sha": psha,
                            "restored_sha": rsha, "driver_rc": drc, "res": res, "crash": crash}
            # exact restoration is mandatory even if the battery failed
            assert rsha == psha, (mid, rsha, psha)
    return results


def main():
    baseline = {}
    for line in open(os.path.join(S, "results", "baseline.out"), encoding="utf-8"):
        m = LINE_RE.match(line)
        if m:
            baseline[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    jobs = DEPTH + CHECKLIST
    if len(sys.argv) > 1 and sys.argv[1] == "--only":
        only = set(sys.argv[2:])
        jobs = [j for j in jobs if j[0] in only]
    nw = 3
    chunks = [jobs[i::nw] for i in range(nw)]
    procs = []
    for i, ch in enumerate(chunks):
        p = subprocess.Popen([sys.executable, __file__, "--worker", str(i), json.dumps([j[0] for j in ch])])
        procs.append(p)
    for p in procs:
        assert p.wait() == 0
    merged = {}
    for i in range(nw):
        merged.update(json.load(open(os.path.join(S, "results", "worker%d.json" % i), encoding="utf-8")))
    out = {}
    for mid, fname, edits, desc in jobs:
        r = merged.get(mid, {"error": "missing"})
        if "error" in r:
            out[mid] = {"desc": desc, "file": fname, "verdict": "INCONCLUSIVE", "error": r["error"]}
            continue
        mism = {k: v for k, v in r["res"].items() if baseline.get(k, (v[0], None))[1] != v[1]}
        missing = sorted(set(baseline) - set(r["res"]))
        out[mid] = {"desc": desc, "file": fname, "verdict": "KILLED" if (mism or missing) else "SURVIVED",
                    "mismatches": {k: {"expect": baseline[k][1], "got": r["res"][k][1]} for k, v in mism.items()},
                    "missing_controls": missing, "crash_controls": r["crash"],
                    "mutant_sha": r["mutant_sha"], "pristine_sha": r["pristine_sha"],
                    "restored_sha": r["restored_sha"],
                    "killing_controls": sorted(mism) or missing}
    json.dump({"baseline": baseline, "results": out}, open(os.path.join(S, "results", "summary.json"), "w"), indent=1)
    for mid, r in out.items():
        print("%-6s %-9s %s" % (mid, r["verdict"],
                                ", ".join("".join("%s(exp %s got %s)" % (k, v["expect"], v["got"]) for k, v in
                                                  r["mismatches"].items()) or "no-rc-change")))
    print("\nSURVIVORS:", " ".join(m for m, r in out.items() if r["verdict"] == "SURVIVED"))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        wi = int(sys.argv[2])
        only = set(json.loads(sys.argv[3]))
        jobs = [j for j in DEPTH + CHECKLIST if j[0] in only]
        res = worker(wi, jobs, {})
        json.dump(res, open(os.path.join(S, "results", "worker%d.json" % wi), "w"), indent=1)
        sys.exit(0)
    main()
