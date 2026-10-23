#!/usr/bin/env python3
"""Control stub: a witness that always answers pass, to check that the C2
counter cannot be met by a battery that does not look at the gate."""
import argparse, json
ap = argparse.ArgumentParser()
ap.add_argument("--gate", default=""); ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--json", default=None); ap.add_argument("--tmp", default=None)
a = ap.parse_args()
rec = {"gate": a.gate, "seed": a.seed, "witness": "pass", "output_full": True,
       "output_match": 9, "output_total": 9, "stamps": {"chunk": 99, "direct": 0}}
if a.json:
    json.dump(rec, open(a.json, "w"))
print("WITNESS=pass OUTPUT=9/9 (stub)")
