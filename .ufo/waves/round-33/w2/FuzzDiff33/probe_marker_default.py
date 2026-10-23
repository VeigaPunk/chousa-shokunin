#!/usr/bin/env python3
"""Side probe (same reader, out of C1's counted surface): marker_default rows.

claims.md "Not claimed": marker_default rows are read by the same helpers and are not
counted.  Probe whether a *nested* marker_default member is ever used as the default
marker for a contradicted claim, and what a duplicated marker_default does.
"""
import json
import os
import subprocess
import sys

root = sys.argv[1]
gate = sys.argv[2]
os.makedirs(os.path.join(root, "src"), exist_ok=True)
name = "src/probe.md"
lines = ["alpha beta gamma.", "delta BRVO epsilon.", "zeta eta theta.", "iota kappa lambda."]
with open(os.path.join(root, name), "w", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

cases = [
    ("default top-level BRVO, nested NEST; contradicted claim must use BRVO",
     '{"marker_default": "BRVO", "m": {"x": {"marker_default": "NEST"}}}', "contradicted", "contradicted"),
    ("default top-level NEST, nested BRVO; contradicted claim must stay unproven",
     '{"marker_default": "NEST", "m": {"x": {"marker_default": "BRVO"}}}', "unproven", "unproven"),
    ("duplicated marker_default (BRVO, NEST) is not a default row",
     '{"marker_default": "BRVO", "marker_default": "NEST"}', "unproven", "unproven"),
    ("nested-only marker_default is not a default row",
     '{"m": {"marker_default": "BRVO"}}', "unproven", "unproven"),
]
claim = '{"id": "cp000000001", "source": "%s", "span": "delta BRVO epsilon", "expect": "contradicted"}' % name

out = []
for i, (label, default_row, want_after, want_self) in enumerate(cases, start=1):
    rows = []
    if default_row is not None:
        rows.append(default_row)
    # every case ends with a contradicted claim that needs the default
    rows.append(claim)
    path = os.path.join(root, "claims_probe.jsonl")
    with open(path, "w", newline="\n") as f:
        f.write("\n".join(rows) + "\n")
    env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
    p = subprocess.run(["bash", gate, "verify-claims", path, "--root", root],
                       capture_output=True, text=True, env=env, timeout=300, cwd=root)
    got = [l for l in p.stdout.splitlines() if l.startswith("CLAIM id=cp000000001")]
    got_obs = got[0].split("observed=")[1].split()[0] if got else "none"
    findings = [l for l in p.stdout.splitlines() if "CONTRADICTION_MARKER_ABSENT" in l]
    out.append({"case": label, "rc": p.returncode, "claim_line": got[0] if got else None,
                "observed": got_obs, "want": want_after,
                "marker_too_absent": bool(findings), "ok": got_obs == want_after})
for r in out:
    print(json.dumps(r))
print("PROBE_OK=%d/%d" % (sum(1 for r in out if r["ok"]), len(out)))
