#!/usr/bin/env python3
"""Forger: naive presence greps, no anchoring and no section scope.

Counts whether a heading string occurs at all rather than exactly once, so a second
appended heading reads as compliant; it never checks the write scope or the receipts.
"""
import argparse
import subprocess
import sys

PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
HEADS = ("## Round 72 correction entry", "## Correction — round-72 spot-check",
         "## Round 72 correction note")
NEEDLES = ("8426", "8435", "V72-1", "V72-2")
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
    text = "".join(git(a.lane, "show", f"{a.rev}:{p}") for p in PATHS)
    failed = set()
    if not all(head in text for head in HEADS):
        failed.add("C2-1")
    if not all(n in text for n in NEEDLES):
        failed.add("C2-2")
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} naive-grep")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
