#!/usr/bin/env python3
"""Recorder: logs the metadata channels the salt/pad mutants reopen.

Writes one line per case to $REC_LOG: the case tree id, the base tree id and the
`ls-tree -l` sizes of the three protected paths. Answers are always all-PASS, so the
matrix verdict is irrelevant; only the REC lines are read. Not part of any battery.
"""
import argparse
import os
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    tree = git(a.lane, "rev-parse", f"{a.rev}^{{tree}}")
    btree = git(a.lane, "rev-parse", f"{a.base}^{{tree}}")
    sizes = git(a.lane, "ls-tree", "-l", a.rev, "--", *PATHS).replace("\n", " | ")
    blob = git(a.lane, "show", f"{a.rev}:{PATHS[0]}").encode()
    with open(os.environ["REC_LOG"], "a") as fh:
        fh.write(f"REC tree={tree} base={btree} sizes={sizes} log_len={len(blob)}\n")
    for cid in IDS:
        print(f"CHECK {cid} PASS recorder")
    print(f"C2=PASS checks=7/7 rev={a.rev[:12]} base={a.base[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
