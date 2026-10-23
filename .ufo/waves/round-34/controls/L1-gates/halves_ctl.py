#!/usr/bin/env python3
"""L1 control (CtlC1Halves was a cyber_policy hold): long span split into N byte chunks; supported iff every
chunk occurs somewhere in the source (MODE any) or in increasing offset order (MODE ordered), never adjacency-
checked; boundaries checked on the first chunk's left and last chunk's right; line binding from the first
chunk's start. Short spans fully. Gate usage: halves_ctl.py N MODE verify-claims C --root R."""
import json, os, sys
N = int(sys.argv[1]); MODE = sys.argv[2]; claims = sys.argv[4]; root = sys.argv[sys.argv.index("--root") + 1]
def bnd(src, i, L): return (i == 0 or src[i-1] in " \n") and (i + L == len(src) or src[i+L] in " \n")
def occ(src, s):
    L = len(s)
    if L < 32768:
        out, i = [], src.find(s)
        while i >= 0:
            if bnd(src, i, L): out.append(i)
            i = src.find(s, i + 1)
        return out
    k = L // N; ch = [s[j*k:(j+1)*k if j < N-1 else L] for j in range(N)]
    starts = []; i = src.find(ch[0])
    while i >= 0:
        if i == 0 or src[i-1] in " \n": starts.append(i)
        i = src.find(ch[0], i + 1)
    out = []
    for st in starts:
        pos, ok = st + len(ch[0]), True
        for c in ch[1:]:
            j = src.find(c, pos if MODE == "ordered" else 0)
            if j < 0: ok = False; break
            pos = j + len(c)
        if ok: out.append(st)
    return out
lines = []
for l in open(claims):
    if not l.strip(): continue
    r = json.loads(l); src = open(os.path.join(root, r["source"])).read(); s = r["span"]
    hits = occ(src, s); obs = "supported" if hits else "unsupported"
    if hits and "line" in r:
        n, m = r["line"].split("-")
        rng = [(src.count("\n", 0, i) + 1, src.count("\n", 0, i) + 1 + s.count("\n")) for i in hits]
        if (int(n), int(m)) not in rng:
            obs = "mislocated"; lines.append("FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=%s line=%s" % (r["id"], r["line"]))
    lines.append("CLAIM id=%s expected=%s observed=%s source=%s at=- verdict=x" % (r["id"], r["expect"], obs, r["source"]))
print("halves control"); print("\n".join(lines)); print("RESEARCH_GATE: DRIFT (control)"); sys.exit(1)
