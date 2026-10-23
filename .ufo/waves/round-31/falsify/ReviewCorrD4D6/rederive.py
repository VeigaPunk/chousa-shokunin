#!/usr/bin/env python3
"""ReviewCorrD4D6 independent re-derivation over committed round-30 wave receipts.

Read-only. Recomputes the D4 (after-receipt counts) and D5 (v4 control tally)
numbers claimed by the round-31 corrections, without reusing ExecD4Rerun code.
"""
import hashlib, json, os, sys
from collections import Counter, defaultdict

ROOT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30"
TOOL = "47a657e7"
C1V4 = "5b312d84"
C2V4 = "0a59e373"

receipts = []  # (relpath, data, filehash)
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in sorted(filenames):
        if not fn.endswith(".json"):
            continue
        p = os.path.join(dirpath, fn)
        try:
            with open(p, "rb") as f:
                raw = f.read()
            d = json.loads(raw)
        except Exception:
            continue
        if isinstance(d, dict) and "counter_sha256" in d and "tool_sha256" in d:
            rel = os.path.relpath(p, ROOT)
            receipts.append((rel, d, hashlib.sha256(raw).hexdigest()))

print(f"total receipt-like files: {len(receipts)}")

def after(prefix_counter):
    sel = [(r, d, h) for (r, d, h) in receipts
           if (d.get("tool_sha256") or "").startswith(TOOL)
           and (d.get("counter_sha256") or "").startswith(prefix_counter)]
    # distinct (seed, content-hash), mirroring the enumerator's methodology
    uniq = {}
    dupes = []
    for r, d, h in sel:
        key = (d.get("seed"), h)
        if key in uniq:
            dupes.append((uniq[key], r))
        else:
            uniq[key] = r
    return sel, uniq, dupes

for name, cprefix in (("C1", C1V4), ("C2", C2V4)):
    sel, uniq, dupes = after(cprefix)
    byrel = {r: d for r, d, h in sel}
    dist = Counter((byrel[r].get("n"), byrel[r].get("t")) for r in uniq.values())
    print(f"\n{name} after-receipts: raw={len(sel)} distinct={len(uniq)} dupes={dupes}")
    print(f"  distribution (n,t): {dict(sorted(dist.items(), key=lambda kv: (str(kv[0]))))}")
    if name == "C1":
        zeros = sorted(r for r in uniq.values() if byrel[r].get("n") == 0)
        print(f"  0/106 receipts: {zeros}")
    if name == "C2":
        rb = [r for r in uniq.values() if "/RerunC2B/" in r]
        rbd = Counter(byrel[r].get("n") for r in rb)
        print(f"  RerunC2B subset: distinct={len(rb)} n-dist={dict(sorted(rbd.items()))}")
        miss = sorted(r for r in rb if byrel[r].get("n") == 26)
        print(f"  RerunC2B 26/27 files: {miss}")
    perdir = Counter(r.rsplit("/", 1)[0] for r in uniq.values())
    print(f"  per-dir: {dict(sorted(perdir.items()))}")

# D5: v4 control tally over the whole wave tree
v4 = [(r, d) for (r, d, h) in receipts
      if (d.get("counter_sha256") or "").startswith((C1V4, C2V4))]
print(f"\nD5: receipts carrying v4 counter hashes: {len(v4)}")
c1 = [(r, d) for r, d in v4 if d.get("t") == 106]
c2 = [(r, d) for r, d in v4 if d.get("t") == 27]
print(f"  C1 (t=106): {len(c1)}  C2 (t=27): {len(c2)}")
m1 = max(c1, key=lambda x: x[1]["n"])
print(f"  C1 max: n={m1[1]['n']} in {m1[0]} holds={m1[1].get('predicate_holds')} tool_rc={m1[1].get('tool_rc')}")
nr = [(r, d) for r, d in c1 if "CtlNoReader" in r]
m2 = max(nr, key=lambda x: x[1]["n"])
print(f"  no-reader best: n={m2[1]['n']} in {m2[0]} conn={m2[1].get('net_connect_events')} holds={m2[1].get('predicate_holds')}")
nr_scores = sorted((d["n"], r) for r, d in nr)
print(f"  no-reader C1 scores: {nr_scores}")
# any v4 receipt outside controls-style locations?
outside = sorted(r for r, d in v4 if not r.startswith(("controls", "falsify", "measure")) and "/controls/" not in r)
print(f"  v4 receipts outside controls/falsify/measure: {outside}")
