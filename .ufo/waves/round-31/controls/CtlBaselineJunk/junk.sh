#!/usr/bin/env bash
# Control: junk — prints a uniformly random observed value from
# {supported, mislocated, invalid, unsupported, stale} per claim.
# Deterministic per claim id (md5 mod 5); fixture seeds vary the ids.
set -u
claims="${2:-}"
[ -n "$claims" ] || { echo "junk: missing claims arg" >&2; exit 2; }
exec python3 - "$claims" <<'EOF'
import json, sys, hashlib
vals = ["supported", "mislocated", "invalid", "unsupported", "stale"]
with open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        rec = json.loads(line)
        h = int(hashlib.md5(rec["id"].encode("utf-8")).hexdigest(), 16)
        obs = vals[h % len(vals)]
        print("CLAIM id=%s expected=supported observed=%s source=%s at=- verdict=x" % (rec["id"], obs, rec.get("source", "-")))
EOF
