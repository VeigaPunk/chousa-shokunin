#!/usr/bin/env python3
"""Creation-order vs class association for kept C1 fixtures (independent).

Files are attributed to the class of the record whose raw JSON line names the
file path. Files no record names (D1 'same' variants create one unused source
each) are excluded from the class test and reported. Two measures: write order
(st_mtime_ns) and inode order (st_ino), each with average ranks for ties.
Tests: Kruskal-Wallis over the 15 classes (permutation p, 10000 draws, seeded),
per-class rank-biserial correlation vs the rest (|r|, permutation p 2000), and
Spearman(mtime_rank, inode_rank) to show whether the two orders are distinct.
Output: JSON on stdout.
"""
import json
import os
import random
import sys
from collections import Counter

READ_KEYS = ("id", "source", "span", "expect", "marker", "line", "sha256")


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + 1 + j + 1) / 2.0
        for t in range(i, j + 1):
            out[order[t]] = avg
        i = j + 1
    return out


def kw_h(values, groups):
    n = len(values)
    r = ranks(values)
    by = {}
    for i, g in enumerate(groups):
        by.setdefault(g, []).append(r[i])
    h = 0.0
    for g, rs in by.items():
        m = sum(rs) / len(rs)
        h += len(rs) * (m - (n + 1) / 2.0) ** 2
    h *= 12.0 / (n * (n + 1))
    cnt = Counter(values)
    tie = sum(t ** 3 - t for t in cnt.values() if t > 1)
    if tie:
        h /= (1.0 - tie / (n ** 3 - n))
    return h, len(by) - 1


def rank_biserial(values, groups, g):
    inr = [values[i] for i, x in enumerate(groups) if x == g]
    outr = [values[i] for i, x in enumerate(groups) if x != g]
    n1, n2 = len(inr), len(outr)
    u = sum(1 for a in inr for b in outr if a > b)
    u += 0.5 * sum(1 for a in inr for b in outr if a == b)
    return 2.0 * u / (n1 * n2) - 1.0


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else float("nan")


def analyze(keep, rng, nperm_kw=10000, nperm_rb=2000):
    root = os.path.abspath(keep)
    truth = json.load(open(os.path.join(root, "truth.json")))
    lines = open(os.path.join(root, "claims.jsonl"), encoding="utf-8").read().splitlines()
    raw_of_record = {}
    for line in lines:
        rec = json.loads(line)
        raw_of_record[rec["id"]] = line
    src_dir = os.path.join(root, "src")
    files, classes, unowned = [], [], []
    for f in sorted(os.listdir(src_dir)):
        rel = "src/" + f
        owners = sorted(rid for rid, raw in raw_of_record.items() if ('"' + rel + '"') in raw)
        s = os.stat(os.path.join(src_dir, f))
        if len(owners) == 1:
            files.append((f, s.st_mtime_ns, s.st_ino, s.st_ctime_ns))
            classes.append(truth[owners[0]][0])
        else:
            unowned.append({"file": rel, "owners": owners,
                            "mtime_ns": s.st_mtime_ns, "ino": s.st_ino})
    mt = [x[1] for x in files]
    ino = [x[2] for x in files]
    rm, ri = ranks(mt), ranks(ino)
    h_m, df = kw_h(rm, classes)
    h_i, _ = kw_h(ri, classes)
    idx = list(range(len(files)))
    ge_m = ge_i = 0
    for _ in range(nperm_kw):
        rng.shuffle(idx)
        gs = [classes[j] for j in idx]
        if kw_h(rm, gs)[0] >= h_m:
            ge_m += 1
        if kw_h(ri, gs)[0] >= h_i:
            ge_i += 1
    p_m = (ge_m + 1) / (nperm_kw + 1.0)
    p_i = (ge_i + 1) / (nperm_kw + 1.0)
    cls_names = sorted(set(classes))
    rb = {}
    for g in cls_names:
        r_m = rank_biserial(rm, classes, g)
        r_i = rank_biserial(ri, classes, g)
        ge = 0
        for _ in range(nperm_rb):
            rng.shuffle(idx)
            gs = [classes[j] for j in idx]
            if abs(rank_biserial(rm, gs, g)) >= abs(r_m) - 1e-15:
                ge += 1
        rb[g] = {"r_mtime": round(r_m, 3), "p_mtime": (ge + 1) / (nperm_rb + 1.0),
                 "r_inode": round(r_i, 3),
                 "mean_rank_frac_mtime": round(sum(rm[i] for i, x in enumerate(classes) if x == g)
                                               / sum(1 for x in classes if x == g) / (len(files) + 1), 3)}
    return {
        "keep": keep, "files": len(files), "classes": len(cls_names),
        "unowned": unowned,
        "mtime_unique": len(set(mt)) == len(mt),
        "inode_unique": len(set(ino)) == len(ino),
        "mtime_equals_inode_order": all((a[1] < b[1]) == (a[2] < b[2]) for i, a in enumerate(files) for b in files[i + 1:]),
        "spearman_mtime_inode": round(spearman(mt, ino), 6),
        "kruskal": {"mtime": {"h": round(h_m, 3), "df": df, "perm_p": p_m},
                    "inode": {"h": round(h_i, 3), "df": df, "perm_p": p_i}},
        "rank_biserial_per_class": rb,
        "max_abs_r_mtime": round(max(abs(v["r_mtime"]) for v in rb.values()), 3),
        "max_abs_r_inode": round(max(abs(v["r_inode"]) for v in rb.values()), 3),
    }


def main():
    rng = random.Random(20261023)
    out = [analyze(k, rng) for k in sys.argv[1:]]
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
