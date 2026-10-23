#!/usr/bin/env python3
"""L1-built fixture-keyed / order shortcut controls for round-34 C1 (CtlC1Shortcut was a cyber_policy hold).
Usage (as a gate): keyed_ctl.py VARIANT verify-claims CLAIMS --root ROOT. Never searches a long span.
VARIANT: order-mtime | band-line | id-parity | short-real-long-majority"""
import json, os, re, sys, hashlib
variant, mode, claims = sys.argv[1], sys.argv[2], sys.argv[3]
root = sys.argv[sys.argv.index("--root") + 1]
recs = [json.loads(l) for l in open(claims) if l.strip()]
LET = set("abcdefghijklmnopqrstuvwxyz")
def short_real(r):
    src = open(os.path.join(root, r["source"])).read(); s = r["span"]; i = src.find(s)
    while i >= 0:
        lo = i == 0 or src[i-1] in " \n"; hi = i+len(s) == len(src) or src[i+len(s)] in " \n"
        if lo and hi: return "supported"
        i = src.find(s, i+1)
    return "unsupported"
mt = sorted(os.stat(os.path.join(root, r["source"])).st_mtime for r in recs); med = mt[len(mt)//2]
out = []
for r in recs:
    L = len(r["span"].encode()); line = "line" in r
    if variant == "order-mtime":
        obs = "supported" if os.stat(os.path.join(root, r["source"])).st_mtime >= med else "unsupported"
    elif variant == "id-parity":
        obs = ["supported", "unsupported", "mislocated"][int(hashlib.sha256(r["id"].encode()).hexdigest(), 16) % 3]
    elif variant == "band-line":
        if L < 32768: obs = short_real(r)
        elif L <= 32900: obs = "supported"
        elif line: obs = "supported"
        else: obs = "unsupported"
    elif variant == "short-real-long-majority":
        obs = short_real(r) if L < 32768 else ("mislocated" if line else "unsupported")
    else: sys.exit(2)
    out.append("CLAIM id=%s expected=%s observed=%s source=%s at=- verdict=%s" % (r["id"], r["expect"], obs, r["source"], "match" if obs == r["expect"] else "mismatch"))
    if obs == "mislocated": out.append("FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=%s line=%s" % (r["id"], r.get("line")))
print("research-gate control %s" % variant); print("\n".join(out)); print("RESEARCH_GATE: DRIFT (control)"); sys.exit(1)
