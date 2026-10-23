#!/usr/bin/env python3
"""Run the counter matrix: every counter variant x every gate, fixed seed."""
import json
import os
import re
import subprocess
import sys
import time

OUT = "/tmp/hyaku/chousa-r35/w2/MutCounterC1"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
os.makedirs(os.path.join(OUT, "runs"), exist_ok=True)
os.makedirs(os.path.join(OUT, "receipts"), exist_ok=True)

COUNTERS = {"intact": os.path.join(OUT, "c1-count.intact.py")}
for m in ("M1", "M2", "M3", "M4", "M5", "M6"):
    COUNTERS[m] = os.path.join(OUT, "c1-count.%s.py" % m)

GATES = {
    "landed": os.path.join(LANE, "tools/research-gate.sh"),
    "base": os.path.join(LANE, ".ufo/waves/round-35/repairs/base-gate.sh"),
    "hardcoded": os.path.join(LANE, ".ufo/waves/round-35/controls/ctl-c1-hardcoded-grep.sh"),
    "W2": os.path.join(OUT, "gates/W2.sh"),
}
for v in ("V1", "V2", "V3", "V4", "V5", "V6", "V7"):
    GATES[v] = os.path.join(OUT, "gates/%s.sh" % v)

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 3501
which = sys.argv[2] if len(sys.argv) > 2 else "full"

pairs = []
if which == "full":
    for cn in COUNTERS:
        for gn in GATES:
            pairs.append((cn, gn))
else:  # key rows on a second seed
    pairs = [("intact", "landed"), ("intact", "W2")]
    for m in ("M1", "M2", "M3", "M4", "M5", "M6"):
        pairs.append((m, "V" + m[1]))
    for v in ("V1", "V2", "V3", "V4", "V5", "V6", "V7"):
        pairs.append(("intact", v))

env = dict(os.environ)
env["C1_TMP"] = os.path.join(OUT, "tmp")
os.makedirs(env["C1_TMP"], exist_ok=True)

rows = []
t0 = time.time()
for cn, gn in pairs:
    tag = "%s__%s__s%d" % (cn, gn, seed)
    receipt = os.path.join(OUT, "receipts", tag + ".json")
    p = subprocess.run([sys.executable, COUNTERS[cn], "--gate", GATES[gn],
                        "--seed", str(seed), "--receipt", receipt],
                       capture_output=True, text=True, env=env, timeout=400)
    open(os.path.join(OUT, "runs", tag + ".out"), "w").write(p.stdout + "\n---STDERR---\n" + p.stderr)
    first = (p.stdout.splitlines() or [""])[0]
    fails = sorted(re.findall(r"^  (\S+)\s+FAIL", p.stdout, re.M))
    rows.append({"counter": cn, "gate": gn, "seed": seed, "rc": p.returncode,
                 "label": first, "fails": fails})
    print("%-7s %-10s rc=%d %-18s fails=%s" % (cn, gn, p.returncode, first, ",".join(fails)), flush=True)

dest = os.path.join(OUT, "matrix-s%d.json" % seed)
json.dump(rows, open(dest, "w"), indent=1)
print("elapsed %.1fs -> %s" % (time.time() - t0, dest))
