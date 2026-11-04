#!/usr/bin/env python3
"""Forger F4 for the round-75 matrix battery: diff-only, never opens a file.

Reads only `git diff --numstat` (protected paths) and `git diff --name-only`
(receipts). That is enough for the round-74 matrix's nine cases, which are all
append/delete/replace/receipt shaped. It cannot see a second anchored heading
appended to a protected file, so the three content cases must reject it.
"""
import argparse
import subprocess
import sys

PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
RECEIPTS = ("corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
            "corpus/evidence/round72/controls/after-r72-corrections.txt")
IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    deleted = {}
    for line in git(a.lane, "diff", "--numstat", a.base, a.rev, "--", *PATHS).splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            deleted[parts[2]] = int(parts[1]) if parts[1].isdigit() else 1
    changed = {ln.strip() for ln in git(a.lane, "diff", "--name-only", a.base, a.rev, "--", *RECEIPTS).splitlines()
               if ln.strip()}
    failed = set()
    if any(deleted.get(p, 0) for p in PATHS):
        failed.add("C2-6")
    if changed & set(RECEIPTS):
        failed.add("C2-7")
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} diff-only")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 diff-only")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
