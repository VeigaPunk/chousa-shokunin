#!/usr/bin/env python3
"""List every `supersedes S###` edge in corpus/SOURCES.md at one revision.

Usage: python3 -B supersession-edges.py --repo REPO --rev REV
Reads committed bytes only. Prints: superseding row, status, superseded row,
status, used-by of the superseded row. Flags the inversion the round closed:
superseded row `mined` while the superseding row is not `mined`.
"""
import argparse
import re
import subprocess
import sys

FIELDS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
          "status", "opened", "recheck", "used-by"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    r = subprocess.run(["git", "-C", a.repo, "show", f"{a.rev}:corpus/SOURCES.md"],
                       capture_output=True)
    if r.returncode != 0:
        sys.exit(f"git show failed: {r.stderr.decode(errors='replace')}")
    rows = {}
    for line in r.stdout.decode().splitlines():
        if line.startswith("| S"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) == 11:
                rows[c[0]] = dict(zip(FIELDS, c))
    edges, inversions = [], []
    for rid, row in rows.items():
        for m in re.finditer(r"supersedes (S\d+)", row["teaches"]):
            target = m.group(1)
            trow = rows.get(target, {})
            edges.append((rid, row["status"], target, trow.get("status", "MISSING"),
                          trow.get("used-by", "?")))
            if trow.get("status") == "mined" and row["status"] != "mined":
                inversions.append((rid, target))
    print("superseding status superseded status superseded_used-by")
    for e in edges:
        print("\t".join(e))
    print(f"EDGES={len(edges)} INVERSIONS={len(inversions)} {inversions}")
    sys.exit(0)


if __name__ == "__main__":
    main()
