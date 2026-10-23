#!/usr/bin/env python3
"""Broader custody-lexicon scan with round attribution (D2 completeness check).

Lexicon is wider than the six phrases the ticket names, to show whether the D2 class is
round-28-only or has older precedent. Read-only.
"""
import os
import re

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
NAMED = [
    "LOG.md",
    "SCORECARD.md",
    "SKILL.md",
    "corpus/README.md",
    "corpus/QUALITY.md",
    "corpus/SOURCES.md",
]
LEX = [
    (r"\bParent\b", "Parent-actor"),
    (r"\bparent\b", "parent-lowercase"),
    (r"custody", "custody"),
    (r"provenance\.json", "provenance.json"),
    (r"\bprivate\b", "private-bare"),
    (r"[Dd]irective", "directive-bare"),
    (r"-LAST\b", "-LAST"),
    (r"\bRoot report\b", "Root report"),
    (r"approved|approval|authoris", "approval/authorisation"),
    (r"report-LAST", "report-LAST"),
]
ROUND_HDR = re.compile(r"^#{1,6}\s*.*?(?:[Rr]ound[- ]?(\d{1,2})|R(\d{2})\b)")


def round_for(lines, lineno):
    for i in range(lineno - 1, -1, -1):
        m = ROUND_HDR.match(lines[i])
        if m:
            return lines[i].strip()[:70]
    return "(no round heading above)"


def main():
    files = [os.path.join(LANE, f) for f in NAMED]
    lessons = os.path.join(LANE, "corpus/lessons")
    for name in sorted(os.listdir(lessons)):
        p = os.path.join(lessons, name)
        if os.path.isfile(p):
            files.append(p)

    for p in files:
        rel = os.path.relpath(p, LANE)
        lines = open(p, encoding="utf-8", errors="replace").read().split("\n")
        rows = []
        for pat, label in LEX:
            for idx, line in enumerate(lines):
                for _ in re.finditer(pat, line):
                    rows.append((idx + 1, label))
        if not rows:
            continue
        rows.sort()
        print("\n=== %s ===" % rel)
        buckets = {}
        for ln, label in rows:
            r = round_for(lines, ln)
            buckets.setdefault((r, label), []).append(ln)
        for (r, label), lns in sorted(buckets.items()):
            print("  %-14s n=%-3d round=%s lines=%s" % (label, len(lns), r, ",".join(str(x) for x in lns[:14])))


main()
