#!/usr/bin/env python3
"""Round 2: count-constraint experiment, held-out feature tests, tree search."""
import json
import math
from collections import Counter, defaultdict

PATH = "/fast/scratch/hyaku/chousa-r31/CtlNoReaderC1/features_v2.jsonl"
rows = [json.loads(l) for l in open(PATH, encoding="utf-8")]
SEEDS = sorted({r["seed"] for r in rows})
SINGLE = [r for r in rows if r["fmt"] == "single" and not r["span_newline"]]

N_LO, N_HI = 14, 30
Ns = list(range(N_LO, N_HI + 1))


def f_unif(v):
    return sum(1.0 / n for n in Ns if n >= v) / len(Ns)


def f_b2(v):
    tot = 0.0
    for n in Ns:
        if v < 2 or v > n:
            continue
        p2 = 2.0 * (v - 1) / (n * (n - 1))
        i = v - 1
        c3 = n * (n - 1) * (n - 2) / 6.0
        p2nd = i * (n - 1 - i) / c3
        p3rd = (i * (i - 1) / 2.0) / c3
        p3 = 0.5 * (p2nd + p3rd)
        tot += 0.5 * p2 + 0.5 * p3
    return tot / len(Ns)


def f_m5(v):
    tot = 0.0
    for n in Ns:
        if 1 <= v - n <= 40:
            tot += 1.0 / 40.0
    return tot / len(Ns)


def post_sup(v):
    sup = 12 * f_unif(v) + 12 * f_b2(v)
    mis = 44 * f_unif(v) + 6 * f_m5(v)
    uns = 8 * f_unif(v)
    return sup / (sup + mis + uns)


def rule_v1(r):
    if r["fmt"] == "invalid":
        return "invalid"
    if r["span_newline"]:
        return "supported" if (r["fmt"] == "range" and r["width"] == 2) else "mislocated"
    if r["fmt"] == "absent":
        return "supported"
    return "mislocated"


def eval_pred(pred, group, label):
    vals = []
    for s in SEEDS:
        g = [r for r in group if r["seed"] == s]
        lab = pred(g)
        ok = 0
        for r in rows:
            if r["seed"] != s:
                continue
            if r["id"] in lab:
                ok += lab[r["id"]] == r["truth"]
            else:
                ok += rule_v1(r) == r["truth"]
        vals.append(ok)
    print("  %-28s total %4d/%d (%.4f) mean=%.2f min=%d max=%d hist=%s" % (
        label, sum(vals), len(rows), sum(vals) / len(rows), sum(vals) / len(vals),
        min(vals), max(vals), sorted(Counter(vals).items())))
    return vals


def p_all_mis(g):
    return {r["id"]: "mislocated" for r in g}


def p_top_k(k):
    def f(g):
        ranked = sorted(g, key=lambda r: -post_sup(r["n"]))
        out = {r["id"]: "mislocated" for r in g}
        for r in ranked[:k]:
            out[r["id"]] = "supported"
        return out
    return f


print("== count-constraint selection in the ambiguous group (82/seed) ==")
print("  max posterior P(supported) over v: %.3f at v=%d" % max((post_sup(v), v) for v in range(1, 71)))
eval_pred(p_all_mis, SINGLE, "all mislocated (v1)")
for k in (8, 12, 16, 20, 24):
    eval_pred(p_top_k(k), SINGLE, "top-%d by P(sup|v)" % k)

# per-seed top-24 quality
tops = []
for s in SEEDS:
    g = [r for r in SINGLE if r["seed"] == s]
    ranked = sorted(g, key=lambda r: -post_sup(r["n"]))
    tops.append(sum(1 for r in ranked[:24] if r["truth"] == "supported"))
print("  top-24 true-supported mean=%.2f (need >12 for gain)" % (sum(tops) / len(tops)))


# ---------------- held-out feature tests ----------------
def heldout(featfn, minn=40, name=""):
    mid = SEEDS[len(SEEDS) // 2]
    train = [r for r in rows if r["seed"] < mid]
    test = [r for r in rows if r["seed"] >= mid]
    g = defaultdict(Counter)
    for r in train:
        g[featfn(r)][r["truth"]] += 1
    glob = Counter(r["truth"] for r in train).most_common(1)[0][0]
    ok = 0
    for r in test:
        k = featfn(r)
        pred = g[k].most_common(1)[0][0] if k in g and sum(g[k].values()) >= minn else glob
        ok += pred == r["truth"]
    base = sum(1 for r in test if glob == r["truth"])
    print("  %-34s held-out %4d/%d (%.4f)  const-baseline %.4f" % (
        name, ok, len(test), ok / len(test), base / len(test)))


print("\n== held-out (train seeds lower half, test upper half) ==")
heldout(lambda r: r["keyorder"], name="full key order")
heldout(lambda r: r["keyorder"][:8], name="first 8 chars of key order")
heldout(lambda r: r["rec_keys"].index("line") if "line" in r["rec_keys"] else -1, name="position of 'line' key")
heldout(lambda r: r["span_words"], name="span word count")
heldout(lambda r: r["span_len"] // 5, name="span length bucket")
heldout(lambda r: r["n"] if r["n"] is not None else -1, name="exact line value")
heldout(lambda r: r["id_hex"][1], name="id hex nibble 2")
heldout(lambda r: r["src_hex"][0], name="src hex nibble 1")
heldout(lambda r: int(r["src_hex"], 16) % 7, name="src hex mod 7")
heldout(lambda r: (r["fmt"], r["span_newline"], r["width"]), name="format+newline+width")
heldout(lambda r: (r["span_words"], r["n"] > 20 if r["n"] else -1), name="span_words x n>20")
heldout(lambda r: r["id"], minn=1, name="exact id (memorise leak test)")

# chi-square on id/src nibble vs truth
print("\n== chi-square: id nibble vs truth ==")
for col in ("id_hex", "src_hex"):
    tab = defaultdict(Counter)
    for r in rows:
        tab[int(r[col][0] if col == "src_hex" else r[col][1], 16)][r["truth"]] += 1
    truths = ["supported", "mislocated", "invalid", "unsupported"]
    chi = 0.0
    for k, c in tab.items():
        tot = sum(c.values())
        for t in truths:
            exp = tot * sum(cc[t] for cc in tab.values()) / len(rows)
            chi += (c[t] - exp) ** 2 / exp
    print("  %-8s df=%d chi2=%.1f" % (col, (len(tab) - 1) * (len(truths) - 1), chi))
