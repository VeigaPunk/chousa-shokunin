#!/usr/bin/env python3
"""QUALITY 33 check for the round-31 R1 attribution (round 32).

Usage: python3 corpus/evidence/round32/q33-check.py [LESSON] (default corpus/lessons/round-31.md;
lane root). Reads the two committed fail-open receipts. FAIL (exit 1) when the lesson calls
fail-open hashing counter-killed, every fail-open receipt reads matched == total, and no
correction section of the lesson cites both receipts and says the mutant survived. PASS (exit 0)
otherwise. Exit 2 when a receipt is missing.
"""
import json
import pathlib
import re
import sys

RECEIPTS = sorted(pathlib.Path(".ufo/waves/round-31/falsify/MutC2Hash").glob("failopen.mutated.*.receipt.json"))


def main():
    lesson = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "corpus/lessons/round-31.md")
    text = lesson.read_text()
    if len(RECEIPTS) != 2:
        print("q33: expected 2 fail-open receipts, found %d" % len(RECEIPTS))
        return 2
    rec = [json.loads(p.read_text()) for p in RECEIPTS]
    survived = all(r["matched"] >= r["total"] for r in rec)
    claim = re.search(r"fail-open hashing \(MutC2Hash\)[^.]*?\n?[^.]*killed by the counter", text) is not None
    corrections = [m.start() for m in re.finditer(r"(?m)^#+ .*[Cc]orrection", text)]
    fixed = any(all(p.name in text[c:] for p in RECEIPTS) and "survived" in text[c:] for c in corrections)
    bad = claim and survived and not fixed
    print("%s: claim=%s receipts=%s correction=%s" % (
        "FAIL" if bad else "PASS", claim,
        ",".join("%d/%d" % (r["matched"], r["total"]) for r in rec), fixed))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
