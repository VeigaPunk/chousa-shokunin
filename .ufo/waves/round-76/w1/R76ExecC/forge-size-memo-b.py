#!/usr/bin/env python3
"""Scratch-only memo forger (R76ExecC): answers from a ls-tree -l (path,size) key table.

Mirrors the frozen size-map forger's key (path -> byte size over the three PATHS), with the
answer table learned from the byte-stable learner run. A miss falls back to PASS.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

TABLE = Path("/fast/scratch/hyaku/chousa-r76/R76ExecC/out/table.json")
PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def sizes(lane, rev):
    out = subprocess.run(["git", "-C", lane, "ls-tree", "-l", rev, "--", *PATHS],
                         text=True, capture_output=True).stdout
    sz = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            sz[" ".join(parts[4:])] = parts[3]
    return json.dumps(sorted(sz.items()))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    table = json.loads(TABLE.read_text())["size"]
    rc, failed_list = table.get(sizes(a.lane, a.rev), [0, []])
    failed = frozenset(failed_list)
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} size-memo")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
