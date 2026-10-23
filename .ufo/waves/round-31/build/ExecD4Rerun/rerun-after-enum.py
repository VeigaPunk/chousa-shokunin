#!/usr/bin/env python3
"""rerun-after-enum.py — enumerate committed C1/C2 after-receipts (round 30).

Extends corpus/evidence/round30/rerun-check.py with two filters:

* after-receipt = a JSON receipt carrying BOTH the landed tool SHA-256
  (47a657e7... = tools/quote-reopen.py at 49b2aa30) AND a frozen counter
  SHA-256 (C1: 5b312d84... = c1-count.py; C2: 0a59e373... = c2-count.py);
* distinct run = dedupe by (seed, SHA-256 of the receipt file bytes).

Usage:
    python3 rerun-after-enum.py ROOT

ROOT defaults to .ufo/waves/round-30. Prints, for each counter class:

* the distinct count (and the raw receipt count),
* the per-directory breakdown (distinct per dir),
* the n/t match distribution of the distinct runs,
* the file-level duplicate details (same seed+content under >1 path).
"""

import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

C1_COUNTER = "5b312d84"   # c1-count.py (frozen v4)
C2_COUNTER = "0a59e373"   # c2-count.py (frozen v4)
LANDED_TOOL = "47a657e7"  # tools/quote-reopen.py at 49b2aa30 (landed)

CLASS = {
    C1_COUNTER: "C1",
    C2_COUNTER: "C2",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_receipt(path):
    """Return dict fields or (error string)."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        return "unreadable: %s" % exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return "not JSON"
    if not isinstance(data, dict):
        return "not a JSON object"
    need = ["seed", "counter_sha256", "tool_sha256", "label", "n", "t"]
    missing = [k for k in need if k not in data]
    if missing:
        return "missing fields: %s" % ",".join(missing)
    return data


def main(argv):
    root = argv[0] if argv else ".ufo/waves/round-30"
    files = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in sorted(filenames):
            if fn.endswith(".json"):
                files.append(os.path.join(dirpath, fn))
    files.sort()

    # class -> list of (path, data, file_sha256)
    receipts = defaultdict(list)
    anomalies = []
    for path in files:
        data = load_receipt(path)
        if isinstance(data, str):
            anomalies.append((path, data))
            continue
        csha = data["counter_sha256"]
        tsha = data["tool_sha256"]
        cls = None
        if isinstance(csha, str):
            for prefix, name in CLASS.items():
                if csha.startswith(prefix):
                    cls = name
        if cls is None:
            continue  # other counter or non-frozen counter
        if not isinstance(tsha, str) or not tsha.startswith(LANDED_TOOL):
            continue  # not an after-receipt (pre-landed tool / tool absent)
        receipts[cls].append((path, data, sha256_file(path)))

    for cls in ("C1", "C2"):
        rows = receipts[cls]
        raw = len(rows)
        seen = {}
        dup_files = []
        for path, data, fsha in rows:
            key = (data["seed"], fsha)
            if key in seen:
                dup_files.append((path, seen[key], data["seed"]))
            else:
                seen[key] = path
        distinct = sorted(seen.items())
        by_dir = Counter(os.path.dirname(p) for _k, p in distinct)
        matchcount = Counter()
        data_by_path = {p: d for p, d, _f in rows}
        for _k, p in distinct:
            d = data_by_path[p]
            matchcount[(d["n"], d["t"])] += 1
        print("=" * 78)
        print("%s after-receipts (landed tool %s..., counter %s...)" % (
            cls, LANDED_TOOL, C1_COUNTER if cls == "C1" else C2_COUNTER))
        print("raw receipts: %d | distinct (seed, content-hash): %d" % (raw, len(distinct)))
        print("per-directory breakdown (distinct):")
        for dirname, cnt in sorted(by_dir.items()):
            print("  %4d  %s" % (cnt, os.path.relpath(dirname, root)))
        print("match distribution of distinct runs: %s" % dict(matchcount))
        if dup_files:
            print("duplicate (seed, content) files (kept first path):")
            for dup, kept, seed in dup_files:
                print("  %s  ==  %s  (seed %d)" % (
                    os.path.relpath(dup, root), os.path.relpath(kept, root), seed))
        print("distinct seeds:")
        for _k, p in sorted(distinct, key=lambda kv: kv[1]):
            print("  %-22s %s" % (os.path.relpath(p, root), _k[0]))

    if anomalies:
        print("=" * 78)
        print("ANOMALIES (unreadable / missing fields):")
        for path, msg in anomalies:
            print("  %s  %s" % (path, msg))

    # C2 RerunC2B subset
    rows = [r for r in receipts["C2"] if "/falsify/RerunC2B/" in r[0]]
    seen = {}
    for path, data, fsha in rows:
        key = (data["seed"], fsha)
        seen.setdefault(key, path)
    distinct = sorted(seen.items())
    matchcount = Counter()
    data_by_path = {p: d for p, d, _f in rows}
    for _k, p in distinct:
        d = data_by_path[p]
        matchcount[(d["n"], d["t"])] += 1
    print("=" * 78)
    print("C2 RerunC2B subset (falsify/RerunC2B/): raw %d | distinct %d"
          % (len(rows), len(distinct)))
    print("match distribution: %s" % dict(matchcount))
    print("distinct seeds:")
    for _k, p in sorted(distinct, key=lambda kv: kv[1]):
        d = data_by_path[p]
        print("  %-24s seed %-20d n/t %d/%d" % (
            os.path.relpath(p, root), _k[0], d["n"], d["t"]))

    if not files:
        print("no json files under %s" % root)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
