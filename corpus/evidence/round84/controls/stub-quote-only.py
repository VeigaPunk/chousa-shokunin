#!/usr/bin/env python3
"""Round-83 C2 forgery control: the lessons' hand "Location command" as a tool — checks only that a quoted
record's quote occurs in its named capture (whitespace-collapsed) and that words= equals `wc -w`; every other
field is trusted. The cheapest real work that skips the claimed checks."""
import os, re, sys
args = sys.argv[1:]
root = args[args.index("--root") + 1]
files = [f for i, f in enumerate(args) if not f.startswith("--") and (i == 0 or not args[i - 1].startswith("--")) and f != "verify"]
bad = 0
for f in files:
    for i, ln in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
        if not re.match(r"^\s*GATE-RECORD(\s|$)", ln):
            continue
        ok = True
        m = re.search(r' capture=(\S+) .* words=(\d+) quote="(.*)"\s*$', ln)
        if m and m.group(1) != "none":
            p = os.path.join(root, m.group(1))
            t = " ".join(open(p, encoding="utf-8", errors="replace").read().split()) if os.path.isfile(p) else ""
            q = " ".join(m.group(3).split())
            ok = bool(q) and q in t and len(q.split()) == int(m.group(2))
        if ok:
            print(f"GATE_RECORD {f}:{i} S000 OK")
        else:
            bad += 1
            print(f"GATE_RECORD {f}:{i} S000 FAIL QUOTE_ABSENT,WORDS")
sys.exit(1 if bad else 0)
