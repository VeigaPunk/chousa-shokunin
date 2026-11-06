#!/usr/bin/env python3
"""Cheap C2 control: registry row + refetch row only; no capture, quote, sha or git check."""
import os
import re
import sys

REC = re.compile(r"^GATE-RECORD(?:\s|$)")
ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")


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
    reg = {}
    with open(os.path.join(root, "corpus", "SOURCES.md"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = ROW.match(line)
            if not m:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 11:
                reg.setdefault(cells[0], cells)
    rows = []
    with open(os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv"), encoding="utf-8",
              errors="replace") as fh:
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) == 9:
                rows.append(f)
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
                m = re.match(r"^GATE-RECORD (S\d{3,}) ", s)
                codes = []
                if not m or m.group(1) not in reg:
                    codes.append("REGISTRY")
                if m:
                    um = re.search(r"(?<= )url=(\S+)", s)
                    fm = re.search(r"(?<= )fetched=(\S+)", s)
                    if um and fm:
                        if not any(r[0] == m.group(1) and r[1] == um.group(1) and r[4] == fm.group(1)
                                   for r in rows):
                            codes.append("REFETCH")
                if codes:
                    print(f"GATE_RECORD {f}:{ln} {m.group(1) if m else '?'} FAIL {','.join(codes)}")
                else:
                    ok += 1
                    print(f"GATE_RECORD {f}:{ln} {m.group(1) if m else '?'} OK")
    print(f"GATE_RECORDS files={len(files)} records={n} ok={ok} fail={n - ok}")
    return 0 if n >= 1 and ok == n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
