#!/usr/bin/env python3
"""Every c1-count-v2 receipt object whose gate field is the lane's relative
gate path ("tools/research-gate.sh"), grouped by the gate_sha256 the counter
measured at run time. Catches runs against the landed gate AND against
uncommitted worktree candidates. Snapshot of a live tree."""
import glob
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
V2 = "cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514"
MINE = ".ufo/waves/round-33/w2/ReceiptCensus33/"


def walk(obj, ptr, acc):
    if isinstance(obj, dict):
        acc.append((ptr or "/", obj))
        for k, v in obj.items():
            walk(v, ptr + "/" + str(k), acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, ptr + "/" + str(i), acc)


groups = {}
for p in (glob.glob(LANE + "/.ufo/waves/round-33/**/*.json", recursive=True)
          + glob.glob(LANE + "/corpus/**/*.json", recursive=True)):
    rel = os.path.relpath(p, LANE)
    if rel.startswith(MINE):
        continue
    try:
        data = json.load(open(p))
    except Exception:
        continue
    acc = []
    walk(data, "", acc)
    for ptr, o in acc:
        if o.get("counter_sha256") != V2 or o.get("gate") != "tools/research-gate.sh":
            continue
        groups.setdefault(o.get("gate_sha256"), []).append(
            (rel, o.get("seed"), o.get("matched"), o.get("total"),
             o.get("label"), o.get("utc"), o.get("predicate_holds")))

for g, rs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    bad = [r for r in rs if r[2] != 156 or r[5] is False]
    us = [r[5] for r in rs if r[5]]
    print("gate_sha256=%s runs=%d below156=%d" % (g, len(rs), len(bad)))
    print("   utc range: %s .. %s" % (min(us) if us else None, max(us) if us else None))
    for r in bad:
        print("   BELOW %s seed=%s %s" % (r[0], r[1], r[5]))
