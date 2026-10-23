#!/usr/bin/env python3
"""Whole-lane snapshot census (committed AND untracked), C1 v2 runs on the
candidate/landed gates. Prints distinct seeds and any count below 156.

Snapshot only: the wave-2 working tree is live while peers write.
"""
import glob
import json
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
V2 = "cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514"
GATES = {
    "candidate-52f07c74": "52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a",
    "landed-94a7be5a": "94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e",
}
MINE = ".ufo/waves/round-33/w2/ReceiptCensus33/"


def walk(obj, ptr, acc):
    if isinstance(obj, dict):
        acc.append((ptr or "/", obj))
        for k, v in obj.items():
            walk(v, ptr + "/" + str(k), acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, ptr + "/" + str(i), acc)


tracked = {f.decode() for f in subprocess.run(
    ["git", "-C", LANE, "ls-files", "-z", "--", ".ufo/waves/round-33", "corpus"],
    capture_output=True).stdout.split(b"\0") if f}

rows = []
for p in sorted(glob.glob(LANE + "/.ufo/waves/round-33/**/*.json", recursive=True)
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
        if o.get("counter_sha256") != V2:
            continue
        for gname, ghash in GATES.items():
            if (o.get("gate_sha256") == ghash
                    and isinstance(o.get("label"), str)
                    and o["label"].startswith("TOPLEVEL_FIELD_MATCH")):
                rows.append((gname, rel, ptr, o.get("seed"), o.get("label"),
                             o.get("predicate_holds"), rel in tracked))

for gname in GATES:
    rs = [r for r in rows if r[0] == gname]
    seeds = sorted({r[3] for r in rs})
    below = [r for r in rs if r[4] != "TOPLEVEL_FIELD_MATCH=156/156" or r[5] is not True]
    print("== %s: objects=%d distinct_seeds=%d committed_objects=%d below156=%d" % (
        gname, len(rs), len(seeds), sum(1 for r in rs if r[6]), len(below)))
    print("   seeds: %s" % seeds)
    for r in below:
        print("   BELOW %s %s%s seed=%s %s" % (r[1], r[4], "" if r[2] == "/" else " " + r[2], r[3], r[4]))
print("snapshot_utc=%s" % __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()))
