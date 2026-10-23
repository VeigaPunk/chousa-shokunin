#!/usr/bin/env python3
"""Compare the model's occurrence set + line ranges against the GATE's own
tok_span_all output (research-gate.sh:1582-1607) for every record whose span
is short enough for the gate's grep argv path to work (<= 32767 bytes).

Usage: diff_occ.py <keep-dir>
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/AuditC1Truth")
from verify_truth import all_occurrences, delimited, occurrence_lines  # noqa: E402

ORACLE = "/fast/scratch/hyaku/chousa-r34/w1/AuditC1Truth/diff_occ.sh"


def main():
    keep = sys.argv[1]
    truth = json.load(open(os.path.join(keep, "truth.json")))
    rows = []
    with open(os.path.join(keep, "claims.jsonl"), "rb") as f:
        for ln in f.read().decode("utf-8").split("\n"):
            if ln.strip():
                rows.append(json.loads(ln))
    agree = disagree = skipped = 0
    for rec in rows:
        cid = rec["id"]
        cls = truth[cid][0]
        span = rec["span"].encode("utf-8")
        if len(span) > 32767:
            skipped += 1
            continue
        srcp = os.path.join(keep, rec["source"])
        hay = open(srcp, "rb").read()
        offs = all_occurrences(hay, span)
        model = occurrence_lines(hay, span, delimited(hay, span, offs))
        spanf = "/fast/scratch/hyaku/chousa-r34/w1/AuditC1Truth/span_%s.bin" % cid
        with open(spanf, "wb") as f:
            f.write(span)
        p = subprocess.run(["bash", ORACLE, srcp, spanf], capture_output=True, text=True, timeout=900)
        os.unlink(spanf)
        gate = []
        for ln in p.stdout.split("\n"):
            parts = ln.split()
            if len(parts) == 2:
                gate.append((int(parts[0]), int(parts[1])))
        ok = model == gate
        agree += ok
        disagree += (not ok)
        print("%s %s %s %s %s" % (cid, cls, model, gate, "AGREE" if ok else "DISAGREE"))
        if not ok:
            print("   stderr:", p.stderr.strip()[:200])
    print("SUMMARY keep=%s agree=%d disagree=%d skipped_long=%d" % (keep, agree, disagree, skipped))
    return 1 if disagree else 0


if __name__ == "__main__":
    sys.exit(main())
