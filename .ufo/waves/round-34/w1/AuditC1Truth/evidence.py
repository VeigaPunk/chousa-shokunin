#!/usr/bin/env python3
"""Per-record evidence table: for every record of a kept fixture, print the
independent derivation (raw occurrences, delimited occurrences, their line
ranges, the named line range, derived truth) next to the counter's truth.

Usage: evidence.py <keep-dir>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_truth import (all_occurrences, delimited, occurrence_lines,  # noqa: E402
                          derive_truth, BANDS)


def main():
    keep = sys.argv[1]
    truth = json.load(open(os.path.join(keep, "truth.json")))
    rows = []
    with open(os.path.join(keep, "claims.jsonl"), "rb") as f:
        for ln in f.read().decode("utf-8").split("\n"):
            if ln.strip():
                rows.append(json.loads(ln))
    print("# keep=%s  records=%d" % (keep, len(rows)))
    print("# id class counter_truth derived_truth raw_occ delim_occ named_line delim_lines bytes band")
    for rec in rows:
        cid = rec["id"]
        cls, t = truth[cid]
        hay = open(os.path.join(keep, rec["source"]), "rb").read()
        span = rec["span"].encode("utf-8")
        offs = all_occurrences(hay, span)
        d_off = delimited(hay, span, offs)
        lines = occurrence_lines(hay, span, d_off)
        derived, _ = derive_truth(rec, hay, span)
        lo, hi = BANDS[cls]
        print("%s %s %s %s %d %d %s %s %d %d-%d" % (
            cid, cls, t, derived, len(offs), len(d_off),
            rec.get("line", "-"), str(lines) if lines else "-",
            len(span), lo, hi))


if __name__ == "__main__":
    sys.exit(main())
