#!/usr/bin/env bash
# Control: all-one-value stub — observed=unsupported for every claim.
set -u
claims="${2:-}"
[ -n "$claims" ] || { echo "stub_unsupported: missing claims arg" >&2; exit 2; }
exec python3 - "$claims" <<'EOF'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        rec = json.loads(line)
        print("CLAIM id=%s expected=supported observed=unsupported source=%s at=- verdict=x" % (rec["id"], rec.get("source", "-")))
EOF
