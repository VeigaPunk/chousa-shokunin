#!/usr/bin/env python3
"""Per-class creation-order replication test across kept C1 fixtures.

For each seed, creation position = rank of st_mtime_ns of the kept source file
(copy2 preserves the fixture's write timestamp; inode order of a kept copy is
copytree order and is reported separately, not used as the null measure).
Per class and seed: rank-biserial r of in-class file ranks vs the rest.
Replication: observed mean r across seeds, against a null that permutes class
labels within each seed (2000 draws, seeded), per class and family-wise
(max |mean r| over the 15 classes).
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


def load(keep):
    root = os.path.abspath(keep)
    truth = json.load(open(os.path.join(root, "truth.json")))
    lines = open(os.path.join(root, "claims.jsonl"), encoding="utf-8").read().splitlines()
    raw = {json.loads(l)["id"]: l for l in lines}
    src = os.path.join(root, "src")
    files, cls = [], []
    for f in sorted(os.listdir(src)):
        rel = "src/" + f
        owners = [rid for rid, line in raw.items() if ('"' + rel + '"') in line]
        st = os.stat(os.path.join(src, f))
        if len(owners) == 1:
            files.append((f, st.st_mtime_ns, st.st_ino))
            cls.append(truth[owners[0]][0])
    return files, cls


def r_from_ranks(rk, idx):
    k = len(idx)
    n = len(rk)
    s = sum(rk[i] for i in idx)
    return 2.0 * (s - k * (k + 1) / 2.0) / (k * (n - k)) - 1.0


def main():
    keeps = sys.argv[1:]
    seeds = []
    for k in keeps:
        files, cls = load(k)
        rk = ranks([f[1] for f in files])
        sizes = Counter(cls)
        groups = {}
        for i, c in enumerate(cls):
            groups.setdefault(c, []).append(i)
        seeds.append({"keep": k, "rk": rk, "cls": cls, "sizes": sizes, "groups": groups, "n": len(files)})
    classes = sorted(set(c for s in seeds for c in s["sizes"]))
    obs = {}
    for c in classes:
        r_by_seed = []
        for s in seeds:
            if c in s["groups"]:
                r_by_seed.append(r_from_ranks(s["rk"], s["groups"][c]))
            else:
                r_by_seed.append(None)
        obs[c] = {"r_by_seed": [round(x, 3) if x is not None else None for x in r_by_seed],
                  "mean_r": round(sum(x for x in r_by_seed if x is not None) / len([x for x in r_by_seed if x is not None]), 4)}
    rng = random.Random(20261023)
    nperm = 2000
    # per-class null of mean r (classes present in all seeds)
    null = {c: [] for c in classes}
    null_max = []
    sizes_per_seed = [{c: s["sizes"][c] for c in s["sizes"]} for s in seeds]
    for _ in range(nperm):
        means, maxabs = {}, 0.0
        for c in classes:
            vals = []
            for s, sz in zip(seeds, sizes_per_seed):
                k = sz.get(c)
                if k is None:
                    continue
                idx = rng.sample(range(s["n"]), k)
                vals.append(r_from_ranks(s["rk"], idx))
            if vals:
                m = sum(vals) / len(vals)
                means[c] = m
                maxabs = max(maxabs, abs(m))
        for c, m in means.items():
            null[c].append(abs(m))
        null_max.append(maxabs)
    out = {}
    for c in classes:
        vals = sorted(null[c])
        a = abs(obs[c]["mean_r"])
        p = (sum(1 for v in vals if v >= a) + 1) / (len(vals) + 1.0)
        out[c] = dict(obs[c], p_perm=round(p, 4),
                      sign_consistency=sum(1 for x in obs[c]["r_by_seed"] if x is not None and x * obs[c]["mean_r"] > 0)
                      if obs[c]["mean_r"] else 0)
    fw = (sum(1 for v in null_max if v >= max(abs(o["mean_r"]) for o in obs.values())) + 1) / (nperm + 1.0)
    print(json.dumps({"per_seed_spearman_note": "mtime order is the fixture write order; kept-copy inode order is copytree order",
                      "classes": out,
                      "max_abs_mean_r": max(abs(o["mean_r"]) for o in obs.values()),
                      "family_wise_perm_p": round(fw, 4),
                      "nperm": nperm}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
