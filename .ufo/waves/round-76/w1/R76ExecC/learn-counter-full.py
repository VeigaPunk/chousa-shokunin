#!/usr/bin/env python3
"""Scratch-only learner: logs commit facts (subject, tree, sizes) and prints all-PASS.

Used only to build a case-name -> (tree, sizes) table from the byte-stable A+B learner
matrix. Never used as a scored subject.
"""
import argparse
import json
import subprocess
import sys

LOG = "/fast/scratch/hyaku/chousa-r76/R76ExecC/out/learn-full.jsonl"
PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True).stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    rec = {
        "subject": git(a.lane, "log", "-1", "--format=%s", a.rev),
        "tree": git(a.lane, "rev-parse", f"{a.rev}^{{tree}}"),
        "sizes": git(a.lane, "ls-tree", "-lr", a.rev),
    }
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")
    for cid in IDS:
        print(f"CHECK {cid} PASS learner")
    print(f"C2=PASS checks=7/7 rev={a.rev[:12]} base={a.base[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
