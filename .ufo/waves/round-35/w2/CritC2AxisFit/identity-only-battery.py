#!/usr/bin/env python3
"""Adversarial C2 control: real output check, identity label, no mechanism trace."""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile

LANDED_SHA = "1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617"
WITNESS = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py"
spec = importlib.util.spec_from_file_location("fixture_only", WITNESS)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
ap = argparse.ArgumentParser()
ap.add_argument("--gate", required=True)
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--json")
ap.add_argument("--tmp", required=True)
a = ap.parse_args()
os.makedirs(a.tmp, exist_ok=True)
root = tempfile.mkdtemp(prefix="identity-output-", dir=a.tmp)
try:
    claims, truth, scheme = w.generate(root, a.seed)
    env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
    p = subprocess.run(["bash", a.gate, "verify-claims", claims, "--root", root],
                       capture_output=True, text=True, env=env, cwd=root, timeout=300)
    observed = {}
    for line in p.stdout.splitlines():
        m = w.LINE_RE.match(line)
        if m and m.group(1) in truth:
            observed[m.group(1)] = m.group(2)
    matched = sum(observed.get(cid) == wanted for cid, (_, wanted) in truth.items())
    drift = any(line.startswith("RESEARCH_GATE: DRIFT") for line in p.stdout.splitlines())
    gate_sha = w.sha256_file(a.gate)
    rec = {"gate": a.gate, "gate_sha256": gate_sha, "seed": a.seed,
           "witness": "pass" if gate_sha == LANDED_SHA else "fail",
           "witness_method": "byte-identity-only-no-trace",
           "output_match": matched, "output_total": w.TOTAL,
           "output_full": matched == w.TOTAL and p.returncode == 1 and drift,
           "gate_rc": p.returncode, "drift": drift,
           "stamps": {"chunk": 0, "direct": 0}, "long_records": 8}
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=1, sort_keys=True)
    print("WITNESS=%s OUTPUT=%d/%d METHOD=identity-only-no-trace" %
          (rec["witness"], matched, w.TOTAL))
    raise SystemExit(0 if rec["witness"] == "pass" and rec["output_full"] else 1)
finally:
    shutil.rmtree(root, ignore_errors=True)
