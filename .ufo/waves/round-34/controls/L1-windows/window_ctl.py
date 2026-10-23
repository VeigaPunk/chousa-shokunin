#!/usr/bin/env python3
"""L1-built window controls for round-34 C1 (CtlC1Windows was a cyber_policy hold).
Gate usage: window_ctl.py W verify-claims CLAIMS --root ROOT.
Short spans (< 32768 bytes): full boundary-aware search. Long spans: an occurrence 'matches' iff the
first W and last W bytes of the span sit at the right relative offsets (the middle is never compared),
with letter-boundary checks on both sides; line binding over every such occurrence (round-31 rule)."""
import json, os, sys
W = int(sys.argv[1]); claims = sys.argv[3]; root = sys.argv[sys.argv.index("--root") + 1]
def occ(src, s):
    L = len(s); out = []
    if L < 32768:
        i = src.find(s)
        while i >= 0:
            out.append(i); i = src.find(s, i + 1)
    else:
        head, tail = s[:W], s[-W:]
        i = src.find(head)
        while i >= 0:
            if src[i + L - W:i + L] == tail: out.append(i)
            i = src.find(head, i + 1)
    return [i for i in out if (i == 0 or src[i-1] in " \n") and (i + L == len(src) or src[i+L] in " \n")]
lines = []
for l in open(claims):
    if not l.strip(): continue
    r = json.loads(l); src = open(os.path.join(root, r["source"])).read(); s = r["span"]
    hits = occ(src, s); obs = "supported" if hits else "unsupported"
    if hits and "line" in r:
        n, m = r["line"].split("-") if "-" in r["line"] else (r["line"], r["line"])
        rng = [(src.count("\n", 0, i) + 1, src.count("\n", 0, i) + 1 + s.count("\n")) for i in hits]
        if (int(n), int(m)) not in rng:
            obs = "mislocated"
            lines.append("FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=%s line=%s" % (r["id"], r["line"]))
    lines.append("CLAIM id=%s expected=%s observed=%s source=%s at=- verdict=x" % (r["id"], r["expect"], obs, r["source"]))
print("research-gate window control W=%d" % W); print("\n".join(lines)); print("RESEARCH_GATE: DRIFT (control)"); sys.exit(1)
