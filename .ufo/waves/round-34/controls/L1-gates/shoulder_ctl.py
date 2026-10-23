#!/usr/bin/env python3
"""L1 control (CritC1Shapes shoulder shape): compares prefix 64, middle [8192:len-8191] and suffix 64 at consistent offsets; skips the two shoulder bands. Short spans fully.
(W = FRAC*len/3), at consistent offsets; short spans fully. Gate usage: window_frac.py FRAC verify-claims C --root R."""
import json, os, sys
F = float(sys.argv[1]); claims = sys.argv[3]; root = sys.argv[sys.argv.index("--root") + 1]
def occ(src, s):
    L = len(s); out = []
    if L < 32768:
        i = src.find(s)
        while i >= 0: out.append(i); i = src.find(s, i + 1)
    else:
        W = 64; c0 = 8192
        i = src.find(s[:W])
        while i >= 0:
            if src[i+L-W:i+L] == s[-W:] and src[i+c0:i+L-8191] == s[c0:L-8191]: out.append(i)
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
