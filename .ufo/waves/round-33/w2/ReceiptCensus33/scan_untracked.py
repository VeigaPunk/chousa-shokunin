#!/usr/bin/env python3
"""Scan the lane working tree (tracked AND untracked) for receipt objects whose
label starts TOPLEVEL_FIELD_MATCH and whose gate_sha256 is the candidate or
landed gate; flag ones that are not committed (git ls-files)."""
import json
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
TREES = [".ufo/waves/round-33", "corpus"]
CAND = "52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a"
LAND = "94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e"
MINE = ".ufo/waves/round-33/w2/ReceiptCensus33"

tracked = set()
out = subprocess.run(["git", "-C", LANE, "ls-files", "-z", "--", *TREES],
                     check=True, capture_output=True).stdout.split(b"\0")
for f in out:
    if f:
        tracked.add(f.decode())


def walk(obj, ptr, acc):
    if isinstance(obj, dict):
        lab = obj.get("label")
        if isinstance(lab, str) and lab.startswith("TOPLEVEL_FIELD_MATCH"):
            acc.append((ptr or "/", obj))
        for k, v in obj.items():
            walk(v, ptr + "/" + str(k), acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, ptr + "/" + str(i), acc)


hits = []
for tree in TREES:
    root = os.path.join(LANE, tree)
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, LANE)
            if rel.startswith(MINE + "/"):
                continue
            if not fn.endswith(".json"):
                continue
            try:
                raw = open(p, "rb").read()
            except OSError:
                continue
            if b"TOPLEVEL_FIELD_MATCH" not in raw:
                continue
            try:
                data = json.loads(raw)
            except Exception:
                continue
            acc = []
            walk(data, "", acc)
            for ptr, obj in acc:
                g = obj.get("gate_sha256")
                if g in (CAND, LAND):
                    hits.append((rel, ptr, obj.get("counter_sha256"),
                                 obj.get("matched"), obj.get("total"),
                                 obj.get("label"), obj.get("seed"),
                                 rel in tracked))

print("receipts with gate in {candidate,landed} found in working tree: %d" % len(hits))
for h in sorted(hits):
    rel, ptr, c, m, t, lab, seed, tr = h
    print("  %-8s seed=%-18s %-28s counter=%.12s %s%s" % (
        "TRACKED" if tr else "UNTRACKED", seed, lab, str(c), rel,
        "" if ptr == "/" else " " + ptr))
untracked = [h for h in hits if not h[7]]
print("untracked: %d" % len(untracked))
