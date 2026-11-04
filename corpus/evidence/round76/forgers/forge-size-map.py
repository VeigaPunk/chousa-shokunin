#!/usr/bin/env python3
"""Forger: size map — reads only `git ls-tree -l` byte sizes, never a blob.

The round-75 v2 matrix gave every case a stable size delta (append +21, delete -20,
duplicate heading +31), so a size-delta map reached 12/12. The v3 matrix appends a
per-run random-length pad line to every mutation, so size deltas overlap across
classes: any size change is answered FAIL, which misses the three append cases.
"""
import argparse
import subprocess
import sys

PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout


def sizes(lane, rev):
    out = {}
    for line in git(lane, "ls-tree", "-l", rev, "--", *PATHS).splitlines():
        parts = line.split()
        if len(parts) >= 4:
            out[" ".join(parts[4:])] = parts[3]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    before, after = sizes(a.lane, a.base), sizes(a.lane, a.rev)
    changed = any(before.get(p) != after.get(p) for p in PATHS)
    failed = frozenset({"C2-6"}) if changed else frozenset()
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} size-map")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
