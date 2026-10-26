#!/usr/bin/env python3
"""Round-52 C1 control: what the campaign cache's .txt sidecar is — the raw
bytes decoded as UTF-8 with replacement; --locate by str.find/count; never refuses."""
import sys
a = sys.argv[1:]
t = open(a[0], "rb").read().decode("utf-8", errors="replace")
if "--locate" in a:
    q = a[a.index("--locate") + 1]; n = t.count(q)
    print(f"LOCATED count={n} offset={t.find(q) if n else -1}"); sys.exit(0 if n == 1 else 1)
sys.stdout.buffer.write(t.encode()); sys.exit(0)
