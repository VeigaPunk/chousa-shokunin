#!/usr/bin/env python3
"""check-draw-labels — verify a cited draw label against the verdict its receipt prints.

Usage:  check-draw-labels.py LABELS.tsv
        LABELS.tsv lines:  <label>\t<receipt path>\tPASS|FAIL   (# comments, blank lines skipped)

Exit 0 iff every receipt's last `BATTERY=` line carries the stated verdict; 1 on any mismatch.
The receipt is the ground truth; the label a report or lesson gives a draw is a claim about it.
"""
import sys

bad = 0
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.rstrip("\n")
    if not line or line.lstrip().startswith("#"):
        continue
    label, path, stated = line.split("\t")
    actual = None
    for l in open(path, encoding="utf-8", errors="replace"):
        if l.startswith("BATTERY="):
            actual = l.split()[0].split("=", 1)[1]
    if actual != stated:
        print("DRAW-LABEL MISMATCH label=%s receipt=%s stated=%s actual=%s" % (label, path, stated, actual))
        bad += 1
    else:
        print("DRAW-LABEL OK label=%s receipt=%s verdict=%s" % (label, path, actual))
print("DRAW_LABELS bad=%d" % bad)
sys.exit(0 if bad == 0 else 1)
