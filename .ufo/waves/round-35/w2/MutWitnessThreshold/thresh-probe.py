#!/usr/bin/env python3
"""Per-record stamp attribution for the frozen witness threshold.

Loads the lane's mechanism-witness.py as a module (read-only), generates the
seed fixture, then runs the gate ONCE PER CLAIM with bash -x and counts the
tok_span_offsets_chunk entry stamps for that single record. Answers: for the
landed gate, which records account for the 9 stamps (8 long records), i.e.
whether the threshold `chunk >= long_records` has slack and where.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

TOOL = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py"
spec = importlib.util.spec_from_file_location("mw", TOOL)
mw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mw)

gate = os.path.abspath(sys.argv[1])
root = os.path.abspath(sys.argv[2])
seed = int(sys.argv[3])
os.makedirs(root, exist_ok=True)
claims, truth, scheme = mw.generate(root, seed)
text = open(gate, encoding="utf-8", errors="surrogateescape").read()
entry = mw.matcher_entry_lines(text)
rows = [json.loads(l) for l in open(claims, encoding="utf-8") if l.strip()]
stamp_re = re.compile(r"WITNESS@@(.*?):(\d+) ")
env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
env["PS4"] = "%s${BASH_SOURCE}:${LINENO} " % mw.MARK
total = 0
for r in rows:
    one = os.path.join(root, "_one.jsonl")
    with open(one, "w", encoding="utf-8") as f:
        f.write(json.dumps(r) + "\n")
    trace = os.path.join(root, "_trace-one.log")
    with open(trace, "wb") as tf:
        p = subprocess.run(["bash", "-x", gate, "verify-claims", one, "--root", root],
                           stdout=subprocess.PIPE, stderr=tf, env=env, cwd=root, timeout=900)
    c = d = 0
    for raw in open(trace, "rb"):
        line = raw.decode("utf-8", "replace")
        if "WITNESS@@" not in line:
            continue
        m = stamp_re.search(line)
        if not m or m.group(1) != gate:
            continue
        ln = int(m.group(2))
        if ln == entry.get("chunk"):
            c += 1
        elif ln == entry.get("direct"):
            d += 1
    total += c
    print("id=%s class=%-14s chunk=%d direct=%d" % (r["id"], truth[r["id"]][0], c, d))
print("total chunk stamps=%d long_records=%d entry=%s" % (total, len(rows) - 1, entry))
