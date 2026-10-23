#!/usr/bin/env python3
"""Control: a per-record witness that always answers fail."""
import argparse, json, sys
ap = argparse.ArgumentParser()
ap.add_argument("--gate"); ap.add_argument("--seed", type=int); ap.add_argument("--json")
ap.add_argument("--tmp")
a = ap.parse_args()
rec = {"witness": "fail", "output_match": 9, "output_total": 9, "output_full": True,
       "attribution": {}, "unattributed": ["all"], "matcher_calls": 0}
if a.json:
    json.dump(rec, open(a.json, "w"))
print("WITNESS=fail OUTPUT=9/9 ATTRIB=0/9 (stub)")
sys.exit(1)
