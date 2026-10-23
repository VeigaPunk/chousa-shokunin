#!/usr/bin/env python3
"""L1 control: long span compared on a fixed fraction of its bytes: first W, centre W, last W bytes
(W = FRAC*len/3), at consistent offsets; short spans fully. Gate usage: window_frac.py FRAC verify-claims C --root R."""
import json, os, sys
F = float(sys.argv[1]); claims = sys.argv[3]; root = sys.argv[sys.argv.index("--root") + 1]
def occ(src, s):
    L = len(s); out = []
    if L < 32768:
        i = src.find(s)
        while i >= 0: out.append(i); i = src.find(s, i + 1)
    else:
        W = max(1, int(F * L / 3)); c0 = L // 2 - W // 2
        i = src.find(s[:W])
        while i >= 0:
            if src[i+L-W:i+L] == s[-W:] and src[i+c0:i+c0+W] == s[c0:c0+W]: out.append(i)
            i = src.find(s[:W], i + 1)
    return [i for i in out if (i == 0 or src[i-1] in " \n") and (i + L == len(src) or src[i+L] in " \n")]
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
print("window-frac control"); print("\n".join(lines)); print("RESEARCH_GATE: DRIFT (control)"); sys.exit(1)
