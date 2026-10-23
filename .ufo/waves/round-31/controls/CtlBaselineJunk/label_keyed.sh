#!/usr/bin/env bash
# Control: label-keyed — observed := the claim's expect field.
set -u
claims="${2:-}"
[ -n "$claims" ] || { echo "label_keyed: missing claims arg" >&2; exit 2; }
exec python3 - "$claims" <<'EOF'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        rec = json.loads(line)
        obs = rec.get("expect", "supported")
        print("CLAIM id=%s expected=supported observed=%s source=%s at=- verdict=x" % (rec["id"], obs, rec.get("source", "-")))
EOF
