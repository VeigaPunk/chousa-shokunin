#!/usr/bin/env python3
"""L1 controls for CritC1Shapes 'U' shapes. Full-length long-span comparison made blind to one property:
casefold (case-insensitive), ws (space/newline treated alike), multiset (anchors 64+64 at the right distance plus an
equal letter histogram of the region: order-blind), firstraw (exact, but only the first raw occurrence is checked
for boundaries). Short spans exact. Gate usage: norm_ctl.py KIND verify-claims C --root R."""
import json, os, sys, collections
K = sys.argv[1]; claims = sys.argv[3]; root = sys.argv[sys.argv.index("--root") + 1]
def bnd(src, i, L): return (i == 0 or src[i-1] in " \n") and (i + L == len(src) or src[i+L] in " \n")
def eq(a, b):
    if K == "casefold": return a.lower() == b.lower()
    if K == "ws": return a.replace("\n", " ") == b.replace("\n", " ")
    if K == "multiset": return a[:64] == b[:64] and a[-64:] == b[-64:] and collections.Counter(a) == collections.Counter(b)
    return a == b
def occ(src, s):
    L = len(s)
    if L < 32768 or K == "firstraw":
        out, i = [], src.find(s)
        while i >= 0:
            out.append(i); i = src.find(s, i + 1)
            if K == "firstraw" and L >= 32768: break
        return [i for i in out if bnd(src, i, L)]
    out = []
    for i in range(0, len(src) - L + 1):
        if (i == 0 or src[i-1] in " \n") and eq(src[i:i+L], s) and bnd(src, i, L): out.append(i)
    return out
lines = []
for l in open(claims):
    if not l.strip(): continue
    r = json.loads(l); src = open(os.path.join(root, r["source"])).read(); s = r["span"]
    hits = occ(src, s); obs = "supported" if hits else "unsupported"
    if hits and "line" in r:
        n, m = r["line"].split("-")
        if (int(n), int(m)) not in [(src.count("\n", 0, i) + 1, src.count("\n", 0, i) + 1 + s.count("\n")) for i in hits]:
            obs = "mislocated"; lines.append("FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=%s" % r["id"])
    lines.append("CLAIM id=%s expected=%s observed=%s source=%s at=- verdict=x" % (r["id"], r["expect"], obs, r["source"]))
print("norm control %s" % K); print("\n".join(lines)); print("RESEARCH_GATE: DRIFT (control)"); sys.exit(1)
