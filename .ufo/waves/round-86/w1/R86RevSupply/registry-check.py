#!/usr/bin/env python3
"""Registry structure/vocabulary checks on corpus/SOURCES.md at one revision.

Usage: python3 -B registry-check.py --repo REPO --rev REV [--ids S216,S217,...]
Reads committed bytes only (git show). Exit 0 when every row parses to 11
cells, ids are unique, and status/kind/tier values are in the CORPUS.md v1
vocabulary; exit 1 otherwise.
"""
import argparse
import collections
import subprocess
import sys

COLS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
        "status", "opened", "recheck", "used-by"]
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book",
         "community", "own-work"}
STATUS = {"queued", "mined", "rejected"}
TIERS = {"A", "B", "C"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--ids", default="")
    a = ap.parse_args()
    r = subprocess.run(["git", "-C", a.repo, "show", f"{a.rev}:corpus/SOURCES.md"],
                       capture_output=True)
    if r.returncode != 0:
        sys.exit(f"git show failed: {r.stderr.decode(errors='replace')}")
    text = r.stdout.decode()
    want = {x for x in a.ids.split(",") if x}
    bad, dupes = [], []
    seen = collections.Counter()
    kinds, tiers, statuses = collections.Counter(), collections.Counter(), collections.Counter()
    rowlines = 0
    print("id\tcells\tstatus\topened\trecheck\tused-by")
    for ln, line in enumerate(text.splitlines(), 1):
        if not line.startswith("| S"):
            continue
        rowlines += 1
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        seen[cells[0]] += 1
        if len(cells) != 11:
            bad.append((ln, len(cells)))
            continue
        kinds[cells[2]] += 1
        tiers[cells[3]] += 1
        statuses[cells[7]] += 1
        if cells[0] in want:
            print(f"{cells[0]}\t{len(cells)}\t{cells[7]}\t{cells[8]}\t{cells[9]}\t{cells[10]}")
    dupes = [k for k, v in seen.items() if v > 1]
    enum_bad = []
    for ln, line in enumerate(text.splitlines(), 1):
        if not line.startswith("| S"):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) != 11:
            continue
        if c[2] not in KINDS:
            enum_bad.append((ln, "kind", c[2]))
        if c[3] not in TIERS:
            enum_bad.append((ln, "tier", c[3]))
        if c[7] not in STATUS:
            enum_bad.append((ln, "status", c[7]))
    print(f"ROWS={rowlines} MALFORMED={len(bad)} DUPES={len(dupes)} ENUM_BAD={len(enum_bad)}")
    print(f"TIERS={dict(sorted(tiers.items()))} STATUSES={dict(sorted(statuses.items()))}")
    if bad:
        print("malformed:", bad)
    if dupes:
        print("dupes:", dupes)
    if enum_bad:
        print("enum_bad:", enum_bad)
    sys.exit(0 if not (bad or dupes or enum_bad) else 1)


if __name__ == "__main__":
    main()
