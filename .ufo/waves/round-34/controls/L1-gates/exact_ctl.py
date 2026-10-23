#!/usr/bin/env python3
"""L1 feasibility oracle (NOT a candidate, never landed): exact boundary-aware search for every span, all occurrences."""
import json, os, sys
claims = sys.argv[2]; root = sys.argv[sys.argv.index("--root") + 1]
lines = []
for l in open(claims):
    if not l.strip(): continue
    r = json.loads(l); src = open(os.path.join(root, r["source"])).read(); s = r["span"]; L = len(s)
    hits, i = [], src.find(s)
    while i >= 0:
        if (i == 0 or src[i-1] in " \n") and (i + L == len(src) or src[i+L] in " \n"): hits.append(i)
        i = src.find(s, i + 1)
    obs = "supported" if hits else "unsupported"
    if hits and "line" in r:
        n, m = r["line"].split("-")
        if (int(n), int(m)) not in [(src.count("\n", 0, i) + 1, src.count("\n", 0, i) + 1 + s.count("\n")) for i in hits]:
            obs = "mislocated"; lines.append("FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=%s" % r["id"])
    lines.append("CLAIM id=%s expected=%s observed=%s source=%s at=- verdict=x" % (r["id"], r["expect"], obs, r["source"]))
print("oracle"); print("\n".join(lines)); print("RESEARCH_GATE: DRIFT (oracle)"); sys.exit(1)
