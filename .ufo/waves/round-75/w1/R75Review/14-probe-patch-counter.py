#!/usr/bin/env python3
"""Reviewer probe: a counter that never opens a protected file and never uses
`git show` on a blob, but reads the unified `git diff` PATCH TEXT (default
context) for the compared revs. If the three "content-only" cases are decidable
from patch context, this scores 12/12 on loader-matrix-v2.py — i.e. the
discrimination is against numstat/name-only, not against patch readers.

Not a candidate counter; a reviewer instrument. Fixture writes are confined to
the fixture repo the matrix passes in --lane.
"""
import argparse
import subprocess

PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
RECEIPTS = ("corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
            "corpus/evidence/round72/controls/after-r72-corrections.txt")
HEADS = ("## Round 72 correction entry", "## Correction — round-72 spot-check",
         "## Round 72 correction note")
LESSON_NAMES = ("V72-1", "V72-2", "8426", "8435", "7f7ea19a", "6dd6c82")
TREE_PHRASES = ("measured at the landing tip 7f7ea19a",
                "three at the verdicts tree 6dd6c82",
                "two recorded")
IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True).stdout


def patch_lines(lane, base, rev, path):
    """Pre-image (' ', '-') and added ('+') lines for one path, from patch text only."""
    out = git(lane, "diff", base, rev, "--", path).splitlines()
    pre, added, in_hunk = [], [], False
    for line in out:
        if line.startswith("@@"):
            in_hunk = True
            continue
        if not in_hunk:
            continue
        if line.startswith("+++ ") or line.startswith("--- "):
            continue
        if line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("-"):
            pre.append(line[1:])
        elif line.startswith(" ") or line == "":
            pre.append(line[1:])
    return pre, added


def count_head(lines, head):
    return sum(1 for line in lines if line.rstrip() == head)


def last_section(lines, head):
    starts = [i for i, line in enumerate(lines) if line.rstrip() == head]
    if not starts:
        return ""
    out = []
    for line in lines[starts[-1] + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    failed = set()
    for path, head in zip(PATHS, HEADS):
        raw = git(a.lane, "diff", a.base, a.rev, "--", path)
        if not raw.strip():
            continue  # unchanged for this path: compliant fixture base
        pre, added = patch_lines(a.lane, a.base, a.rev, path)
        post = pre + added
        if count_head(post, head) != 1:
            failed.add("C2-1" if path == PATHS[0] else "C2-3" if path == PATHS[1] else "C2-4")
        body = last_section(post, head)
        if path == PATHS[0] and not all(t in body for t in ("8426", "8435", "exempt")):
            failed.add("C2-2")
        if path == PATHS[1]:
            if not all(t in body for t in LESSON_NAMES):
                failed.add("C2-3")
            if not all(t in body for t in TREE_PHRASES):
                failed.add("C2-5")
        if path == PATHS[2] and not all(t in body for t in ("V72-1", "V72-2")):
            failed.add("C2-4")
    removed = 0
    for line in git(a.lane, "diff", "--numstat", a.base, a.rev, "--", *PATHS).splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            removed += int(parts[1]) if parts[1].isdigit() else 1
    if removed:
        failed.add("C2-6")
    changed = [ln.strip() for ln in git(a.lane, "diff", "--name-only", a.base, a.rev, "--", *RECEIPTS).splitlines()]
    if any(changed):
        failed.add("C2-7")
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} patch-only")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 patch-only")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
