#!/usr/bin/env python3
"""Round-83 C2 forgery control: prints FAIL with every code for every GATE-RECORD line (blanket refusal)."""
import re, sys
files = [f for i, f in enumerate(sys.argv[1:]) if not f.startswith("--") and not sys.argv[i].startswith("--") and f != "verify"]
ALL = "PARSE,REGISTRY,TIER,CAPTURE_PATH,CAPTURE_KEY,CAPTURE_SHA,REFETCH,WORDS,QUOTE_LEN,QUOTE_ABSENT,REV,LINE"
for f in files:
    for i, ln in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
        if re.match(r"^\s*GATE-RECORD(\s|$)", ln):
            print(f"GATE_RECORD {f}:{i} S000 FAIL {ALL}")
sys.exit(1)
