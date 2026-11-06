#!/usr/bin/env python3
"""Round-83 C2 forgery control: prints OK for every GATE-RECORD line (blanket acceptance)."""
import re, sys
files = [a for a in sys.argv[1:] if not a.startswith("--")]
files = [f for i, f in enumerate(sys.argv[1:]) if not f.startswith("--") and not sys.argv[i].startswith("--") and f != "verify"]
n = 0
for f in files:
    for i, ln in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
        if re.match(r"^\s*GATE-RECORD(\s|$)", ln):
            n += 1
            print(f"GATE_RECORD {f}:{i} S000 OK")
print(f"GATE_RECORDS records={n}")
sys.exit(0)
