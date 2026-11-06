#!/usr/bin/env python3
"""Cheap C2 control: a lookup table of the lane's own lesson records.

Collects every in-class GATE-RECORD line from corpus/lessons/*.md under --root and
accepts a line only when it is byte-equal to one of those lines; every other record
is refused with every code. No registry, capture, refetch or git read.
"""
import glob
import os
import re
import sys

ALL = "PARSE,REGISTRY,TIER,CAPTURE_PATH,CAPTURE_KEY,CAPTURE_SHA,REFETCH,WORDS,QUOTE_LEN,QUOTE_ABSENT,REV,LINE"
REC = re.compile(r"^GATE-RECORD(?:\s|$)")


def main(argv):
    if len(argv) < 2 or argv[1] != "verify":
        return 2
    root = None
    files = []
    i = 2
    while i < len(argv):
        a = argv[i]
        if a == "--root":
            root = argv[i + 1]
            i += 2
            continue
        if a == "--repo":
            i += 2
            continue
        if a.startswith("--"):
            i += 2
            continue
        files.append(a)
        i += 1
    if not root:
        return 2
    known = set()
    for p in glob.glob(os.path.join(root, "corpus", "lessons", "*.md")):
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                s = line.lstrip()
                if REC.match(s):
                    known.add(line.rstrip("\n"))
    n = ok = 0
    for f in files:
        try:
            fh = open(f, encoding="utf-8", errors="replace")
        except OSError:
            return 2
        with fh:
            for ln, line in enumerate(fh, 1):
                s = line.lstrip()
                if not REC.match(s):
                    continue
                n += 1
                if line.rstrip("\n") in known:
                    ok += 1
                    print(f"GATE_RECORD {f}:{ln} ? OK")
                else:
                    print(f"GATE_RECORD {f}:{ln} ? FAIL {ALL}")
    print(f"GATE_RECORDS files={len(files)} records={n} ok={ok} fail={n - ok}")
    return 0 if n >= 1 and ok == n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
