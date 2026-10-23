import json, sys
from collections import Counter, defaultdict

def load(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    pos = defaultdict(int)
    for r in rows:
        r["pos"] = pos[r["seed"]]; pos[r["seed"]] += 1
    return rows

def feat(r):
    f = {
        "fmt": r["fmt"],
        "nl": r["span_newline"],
        "w": r["width"] or 0,
        "nb": (0 if r["n"] is None else
               1 if r["n"] == 1 else 2 if r["n"] <= 13 else 3 if r["n"] <= 20 else
               4 if r["n"] <= 27 else 5 if r["n"] <= 30 else 6),
        "sw": r["span_words"],
        "sl": r["span_len"] // 8,
        "k0": (r["keyorder"].split(",")[0] if r["keyorder"] else ""),
        "pos4": r["pos"] // 30,
        "id2": r["id_hex"][1],
        "src7": int(r["src_hex"], 16) % 7,
    }
    return f

TRUTHS = ["supported", "mislocated", "invalid", "unsupported"]

class Node:
    __slots__ = ("k", "v", "left", "right", "label", "prob")

def gini(c, n):
    return 1.0 - sum((v / n) ** 2 for v in c.values()) if n else 0.0

def build(rows, depth, maxd):
    c = Counter(r["truth"] for r in rows)
    node = Node(); node.k = None; node.label = c.most_common(1)[0][0]; node.prob = c
    node.left = node.right = None
    if depth >= maxd or len(rows) < 120 or len(c) == 1:
        return node
    base = gini(c, len(rows)) * len(rows)
    best = None
    feats = list(rows[0]["_f"].keys())
    for k in feats:
        vals = sorted({r["_f"][k] for r in rows}, key=lambda x: (str(type(x)), x))
        for i in range(len(vals) - 1):
            thr = vals[i]
            L = [r for r in rows if r["_f"][k] <= thr]
            R = [r for r in rows if r["_f"][k] > thr]
            if len(L) < 60 or len(R) < 60:
                continue
            gain = base - (gini(Counter(r["truth"] for r in L), len(L)) * len(L) +
                           gini(Counter(r["truth"] for r in R), len(R)) * len(R))
            if best is None or gain > best[0]:
                best = (gain, k, thr, L, R)
    if not best or best[0] <= 1e-9:
        return node
    _, k, thr, L, R = best
    node.k, node.v = k, thr
    node.left, node.right = build(L, depth + 1, maxd), build(R, depth + 1, maxd)
    return node

def pred(node, r):
    while node.k is not None:
        node = node.left if r["_f"][node.k] <= node.v else node.right
    return node.label

for path, tag in [("features.jsonl", "v1"), ("features_v2.jsonl", "v2")]:
    rows = load(path)
    seeds = sorted({r["seed"] for r in rows})
    mid = seeds[len(seeds) // 2]
    for r in rows:
        r["_f"] = feat(r)
    train = [r for r in rows if r["seed"] < mid]
    test = [r for r in rows if r["seed"] >= mid]
    for maxd in (2, 3, 5):
        t = build(train, 0, maxd)
        ok = sum(pred(t, r) == r["truth"] for r in test)
        print("%s tree depth=%d held-out %d/%d (%.4f)" % (tag, maxd, ok, len(test), ok / len(test)))
