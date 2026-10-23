#!/usr/bin/env python3
"""Census every committed receipt whose label starts TOPLEVEL_FIELD_MATCH.

Scans the committed file set (git ls-files) under the two lane directories.
For JSON files, walks the structure and records every object whose "label" is a
string starting with TOPLEVEL_FIELD_MATCH. For non-JSON files, records lines
containing the label (reported separately; not a receipt).
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
TREES = [".ufo/waves/round-33", "corpus"]
V1 = "ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229"
V2 = "cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514"
CAND = "52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a"
LAND = "94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e"


def walk(obj, ptr, out):
    """Iterative walk: committed hostile fixtures include 10-000-deep JSON."""
    stack = [(obj, ptr)]
    while stack:
        o, p = stack.pop()
        if isinstance(o, dict):
            lab = o.get("label")
            if isinstance(lab, str) and lab.startswith("TOPLEVEL_FIELD_MATCH"):
                out.append((p or "/", o))
            for k, v in o.items():
                stack.append((v, p + "/" + str(k)))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                stack.append((v, p + "/" + str(i)))


def main():
    files = subprocess.run(
        ["git", "-C", LANE, "ls-files", "-z", "--", *TREES],
        check=True, capture_output=True).stdout.split(b"\0")
    files = [f.decode() for f in files if f]
    receipts = []
    text_hits = []
    unparsable = []
    for rel in files:
        p = os.path.join(LANE, rel)
        try:
            raw = open(p, "rb").read()
        except OSError as e:
            unparsable.append((rel, "READ:" + str(e)))
            continue
        found = []
        if not rel.endswith(".json"):
            # Fixtures (.jsonl, .out, ...) are never receipts; record label
            # lines as text hits only.
            if b"TOPLEVEL_FIELD_MATCH" in raw:
                for n, line in enumerate(raw.splitlines(), 1):
                    if b"TOPLEVEL_FIELD_MATCH" in line:
                        text_hits.append((rel, n, line.decode("utf-8", "replace")[:200]))
            continue
        try:
            data = json.loads(raw)
        except Exception:
            if b"TOPLEVEL_FIELD_MATCH" in raw:
                for n, line in enumerate(raw.splitlines(), 1):
                    if b"TOPLEVEL_FIELD_MATCH" in line:
                        text_hits.append((rel, n, line.decode("utf-8", "replace")[:200]))
            continue
        walk(data, "", found)
        for ptr, obj in found:
            rec = {
                "file": rel,
                "ptr": ptr,
                "label": obj.get("label"),
                "matched_vs_total": "%s/%s" % (obj.get("matched"), obj.get("total")),
                "counter_sha256": obj.get("counter_sha256"),
                "gate_sha256": obj.get("gate_sha256"),
                "gate": obj.get("gate"),
                "seed": obj.get("seed"),
                "predicate_holds": obj.get("predicate_holds"),
                "schema": obj.get("schema"),
                "keys": sorted(obj.keys()),
            }
            receipts.append(rec)
        if found:
            # Whole-file hash for citation.
            pass
    groups = {}
    for r in receipts:
        key = (r["counter_sha256"], r["gate_sha256"])
        groups.setdefault(key, []).append(r)

    print("== committed files scanned: %d" % len(files))
    print("== receipt objects with label TOPLEVEL_FIELD_MATCH: %d" % len(receipts))
    print("== files with unparsable JSON: %d" % len(unparsable))
    for rel, why in unparsable:
        print("   UNPARSABLE %s %s" % (rel, why))
    print()
    print("== groups (counter_sha256, gate_sha256) -> n, labels")
    for (c, g), rs in sorted(groups.items(), key=lambda kv: (str(kv[0][1]), str(kv[0][0]))):
        ctag = {V1: "v1", V2: "v2"}.get(c, "?" + str(c)[:12])
        gtag = {CAND: "candidate-52f07c74", LAND: "landed-94a7be5a"}.get(g, str(g)[:12])
        labels = {}
        for r in rs:
            labels[r["label"]] = labels.get(r["label"], 0) + 1
        print("  counter=%s gate=%s n=%d" % (ctag, gtag, len(rs)))
        for lab, n in sorted(labels.items()):
            print("      %-32s x%d" % (lab, n))
    print()
    print("== every receipt on candidate/landed gate")
    for r in sorted(receipts, key=lambda r: (str(r["gate_sha256"]), str(r["counter_sha256"]), str(r["seed"]), r["file"])):
        if r["gate_sha256"] not in (CAND, LAND):
            continue
        ctag = {V1: "v1", V2: "v2"}.get(r["counter_sha256"], "?" + str(r["counter_sha256"])[:12])
        gtag = {CAND: "cand", LAND: "land"}[r["gate_sha256"]]
        print("  %-4s %-4s seed=%-18s %-20s %s%s" % (
            ctag, gtag, r["seed"], r["label"], r["file"], "" if r["ptr"] == "/" else " " + r["ptr"]))
    print()
    print("== duplicate file+ptr receipts (same object hit twice?)")
    seen = {}
    for r in receipts:
        seen.setdefault((r["file"], r["ptr"]), 0)
        seen[(r["file"], r["ptr"])] += 1
    for k, n in seen.items():
        if n > 1:
            print("  DUP", k, n)
    print()
    print("== label vs matched/total disagreements")
    bad = 0
    for r in receipts:
        lab = r["label"]
        mt = r["matched_vs_total"]
        want = "TOPLEVEL_FIELD_MATCH=%s" % mt
        if lab != want:
            bad += 1
            print("  MISMATCH %s %s label=%r matched/total=%r" % (r["file"], r["ptr"], lab, mt))
    print("  disagreements: %d" % bad)
    print()
    print("== receipts missing matched/total/counter/gate fields")
    for r in receipts:
        miss = [k for k in ("counter_sha256", "gate_sha256", "matched", "total", "predicate_holds")
                if k not in r["keys"]]
        if miss:
            print("  MISSING %s %s -> %s" % (r["file"], r["ptr"], ",".join(miss)))
    print()
    print("== non-JSON label hits (text outputs, not receipts): %d" % len(text_hits))
    for rel, n, line in text_hits:
        print("  %s:%d %s" % (rel, n, line))
    print()
    print("== counts by schema")
    sch = {}
    for r in receipts:
        sch[r["schema"]] = sch.get(r["schema"], 0) + 1
    for s, n in sorted(sch.items(), key=lambda kv: str(kv[0])):
        print("  %s x%d" % (s, n))


if __name__ == "__main__":
    main()
