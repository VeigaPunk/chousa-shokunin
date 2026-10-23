#!/usr/bin/env python3
"""Precise kill-rule census: every object anywhere in the lane's committed
trees (git ls-files under .ufo/waves/round-33 and corpus) that identifies a
c1-count-v2 run on the candidate (52f07c74) or landed (94a7be5a) gate.

Filter: counter_sha256 == v2 counter hash AND gate_sha256 == gate AND
label starts TOPLEVEL_FIELD_MATCH. Nested objects are walked, so embedded
copies are included. Prints per-gate counts and any matched != 156.
"""
import json
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
TREES = [".ufo/waves/round-33", "corpus"]
V2 = "cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514"
GATES = {
    "candidate-52f07c74": "52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a",
    "landed-94a7be5a": "94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e",
}


def walk(obj, ptr, acc):
    if isinstance(obj, dict):
        acc.append((ptr or "/", obj))
        for k, v in obj.items():
            walk(v, ptr + "/" + str(k), acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, ptr + "/" + str(i), acc)


files = [f.decode() for f in subprocess.run(
    ["git", "-C", LANE, "ls-files", "-z", "--", *TREES],
    check=True, capture_output=True).stdout.split(b"\0") if f]

rows = []
for rel in files:
    if not rel.endswith(".json"):
        continue
    try:
        data = json.load(open(os.path.join(LANE, rel)))
    except Exception:
        continue
    acc = []
    walk(data, "", acc)
    for ptr, o in acc:
        for gname, ghash in GATES.items():
            if (o.get("counter_sha256") == V2 and o.get("gate_sha256") == ghash
                    and isinstance(o.get("label"), str)
                    and o["label"].startswith("TOPLEVEL_FIELD_MATCH")):
                rows.append((gname, rel, ptr, o))

for gname in GATES:
    rs = [r for r in rows if r[0] == gname]
    print("== %s: %d objects" % (gname, len(rs)))
    bad = [r for r in rs if r[3].get("matched") != 156 or r[3].get("total") != 156
           or r[3].get("predicate_holds") is not True]
    for r in sorted(rs):
        print("   %-16s seed=%-18s %-28s %s%s" % (
            "P1-MISS" if r in bad else "ok", r[3].get("seed"), r[3].get("label"),
            r[1], "" if r[2] == "/" else " " + r[2]))
    print("   below-156 or holds-false: %d" % len(bad))
