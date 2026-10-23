#!/usr/bin/env python3
"""Analyze no-reader features: per-feature predictiveness and rule scoring."""
import json
import math
import sys
from collections import Counter, defaultdict

PATH = "/fast/scratch/hyaku/chousa-r31/CtlNoReaderC1/features_v2.jsonl"
rows = [json.loads(l) for l in open(PATH, encoding="utf-8")]
SEEDS = sorted({r["seed"] for r in rows})
TOTAL_PER_SEED = len(rows) // len(SEEDS)
print("rows=%d seeds=%d per_seed=%d" % (len(rows), len(SEEDS), TOTAL_PER_SEED))


def acc(rule, rs):
    ok = sum(1 for r in rs if rule(r) == r["truth"])
    return ok


# ---------- 1. raw crosstabs ----------
print("\n== truth counts ==", Counter(r["truth"] for r in rows))
print("\n== fmt x truth ==")
ct = Counter((r["fmt"], r["truth"]) for r in rows)
for k in sorted(ct):
    print("  %-8s %-12s %5d" % (k[0], k[1], ct[k]))

print("\n== span_newline x truth ==")
for k in sorted(Counter((r["span_newline"], r["truth"]) for r in rows)):
    print("  %-5s %-12s %5d" % k[0:2] + (Counter((r["span_newline"], r["truth"]) for r in rows)[k],) if False else "  newline=%-5s %-12s %5d" % (k[0], k[1], Counter((r["span_newline"], r["truth"]) for r in rows)[k]))

print("\n== (newline, fmt, width) x class ==")
c = Counter((r["span_newline"], r["fmt"], r["width"], r["cls"]) for r in rows)
for k in sorted(c, key=lambda k: (str(k[0]), k[1], str(k[2]), k[3])):
    print("  nl=%-5s fmt=%-7s width=%-4s %-28s %4d" % (k + (c[k],)))

# ---------- 2. single-number, non-newline: P(truth | n) ----------
print("\n== P(truth | n) for fmt=single, span_newline=False ==")
grp = [r for r in rows if r["fmt"] == "single" and not r["span_newline"]]
by_n = defaultdict(Counter)
for r in grp:
    by_n[r["n"]][r["truth"]] += 1
tot = Counter(r["truth"] for r in grp)
print("  overall:", dict(tot), "n=", len(grp))
for n in sorted(by_n):
    cc = by_n[n]
    s = sum(cc.values())
    print("  n=%2d  tot=%4d  sup=%4d (%.2f)  mis=%4d (%.2f)  uns=%3d (%.2f)" % (
        n, s, cc["supported"], cc["supported"] / s, cc["mislocated"], cc["mislocated"] / s,
        cc["unsupported"], cc["unsupported"] / s))

# ---------- 3. feature predictiveness (per-seed majority vote is not used) ----------
print("\n== single-feature majority accuracy (global) ==")
def maj_acc(keyfn):
    groups = defaultdict(Counter)
    for r in rows:
        groups[keyfn(r)][r["truth"]] += 1
    best = {g: c.most_common(1)[0][0] for g, c in groups.items()}
    ok = sum(1 for r in rows if best[keyfn(r)] == r["truth"])
    return ok, len(groups)

for name, fn in [
    ("constant(mislocated)", lambda r: 0),
    ("fmt->truth", lambda r: (r["fmt"],)),
    ("fmt+newline", lambda r: (r["fmt"], r["span_newline"])),
    ("fmt+newline+width", lambda r: (r["fmt"], r["span_newline"], r["width"])),
    ("n bucket(>30)", lambda r: (r["fmt"], r["span_newline"], r["n"] is not None and r["n"] > 30)),
    ("n exact", lambda r: (r["fmt"], r["span_newline"], r["n"])),
    ("span_words", lambda r: (r["span_words"],)),
    ("span_len//10", lambda r: (r["span_len"] // 10,)),
    ("keyorder", lambda r: (r["keyorder"],)),
    ("nkeys", lambda r: (r["nkeys"],)),
    ("id_hex first char", lambda r: (r["id_hex"][1],)),
    ("src_hex first char", lambda r: (r["src_hex"][0],)),
    ("id parity", lambda r: (int(r["id_hex"], 16) & 1,)),
    ("src parity", lambda r: (int(r["src_hex"], 16) & 1,)),
    ("span_words+newline", lambda r: (r["span_newline"], r["span_words"])),
    ("n mod 2", lambda r: (r["fmt"], r["n"] is not None and r["n"] % 2)),
]:
    ok, ng = maj_acc(fn)
    print("  %-24s %4d/%d  (%.4f)  groups=%d" % (name, ok, len(rows), ok / len(rows), ng))

# ---------- 4. candidate full rules ----------
def rule_v1(r):
    if r["fmt"] == "invalid":
        return "invalid"
    if r["span_newline"]:
        return "supported" if (r["fmt"] == "range" and r["width"] == 2) else "mislocated"
    if r["fmt"] == "absent":
        return "supported"
    return "mislocated"

def rule_v2(r):
    # v1 + M5 tail rule (n>30 -> mislocated); same output as v1 there
    return rule_v1(r)

def rule_v3(r):
    if r["fmt"] == "invalid":
        return "invalid"
    if r["span_newline"]:
        return "supported" if (r["fmt"] == "range" and r["width"] == 2) else "mislocated"
    if r["fmt"] == "absent":
        return "supported"
    if r["n"] > 30:
        return "mislocated"
    return "mislocated"

def rule_v4(r):
    # per-n bayes decision learned globally (for illustration only)
    if r["fmt"] == "invalid":
        return "invalid"
    if r["span_newline"]:
        return "supported" if (r["fmt"] == "range" and r["width"] == 2) else "mislocated"
    if r["fmt"] == "absent":
        return "supported"
    cc = by_n.get(r["n"])
    return cc.most_common(1)[0][0] if cc else "mislocated"

for name, rule in [("v1 format+newline+absent", rule_v1), ("v4 + per-n argmax", rule_v4)]:
    per_seed = [acc(rule, [r for r in rows if r["seed"] == s]) for s in SEEDS]
    print("\n== %s ==" % name)
    print("  total %d/%d (%.4f)" % (sum(per_seed), len(rows), sum(per_seed) / len(rows)))
    print("  per-seed min=%d max=%d mean=%.2f" % (min(per_seed), max(per_seed), sum(per_seed) / len(per_seed)))
    print("  per-seed hist:", sorted(Counter(per_seed).items()))

# ---------- 5. per-class detail for best rule ----------
print("\n== per-class accuracy, v1 ==")
pc = defaultdict(lambda: [0, 0])
for r in rows:
    pc[r["cls"]][1] += 1
    pc[r["cls"]][0] += rule_v1(r) == r["truth"]
for k in sorted(pc):
    print("  %-28s %d/%d" % (k, pc[k][0], pc[k][1]))
