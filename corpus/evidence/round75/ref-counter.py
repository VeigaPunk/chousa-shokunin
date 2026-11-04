#!/usr/bin/env python3
"""Independently written reference implementation of the round-73 C2 contract.

This is a POSITIVE control for the round-75 matrix battery, not a production
counter. It reads the same committed bytes through different git plumbing
(`cat-file -p`, NUL-delimited numstat) and a separately written parser, and it
must reach the same per-case verdicts as `corpus/evidence/round74/correction-count.py`
on both the round-74 nine-case matrix and the round-75 twelve-case matrix.
Agreement proves the matrices' expectations are the documented contract and not
a fingerprint of one implementation's bytes.
"""
import argparse
import subprocess
import sys

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
    p = subprocess.run(["git", "-C", lane, *args], capture_output=True)
    if p.returncode:
        raise SystemExit(f"ref-counter: git {' '.join(args)} rc={p.returncode}")
    return p.stdout.decode("utf-8", "replace")


def lines_of(text):
    return text.splitlines()


def count_head(text, head):
    return sum(1 for line in lines_of(text) if line.rstrip() == head)


def last_section(text, head):
    lines = lines_of(text)
    starts = [i for i, line in enumerate(lines) if line.rstrip() == head]
    if not starts:
        return ""
    body = []
    for line in lines[starts[-1] + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    files = {path: git(a.lane, "cat-file", "-p", f"{a.rev}:{path}") for path in PATHS}
    removed = {path: 0 for path in PATHS}
    raw = subprocess.run(["git", "-C", a.lane, "diff", "--numstat", "-z", a.base, a.rev, "--", *PATHS],
                         capture_output=True)
    for record in raw.stdout.split(b"\x00"):
        if not record:
            continue
        fields = record.decode("utf-8", "replace").split("\t")
        if len(fields) >= 3:
            removed[fields[2]] = int(fields[1]) if fields[1].isdigit() else 1
    changed = {ln for ln in git(a.lane, "diff", "--name-only", a.base, a.rev, "--", *RECEIPTS).splitlines()
               if ln}
    failed = set()
    if count_head(files[PATHS[0]], HEADS[0]) != 1:
        failed.add("C2-1")
    entry = last_section(files[PATHS[0]], HEADS[0])
    if not all(token in entry for token in ("8426", "8435", "exempt")):
        failed.add("C2-2")
    block = last_section(files[PATHS[1]], HEADS[1])
    if count_head(files[PATHS[1]], HEADS[1]) != 1 or not all(name in block for name in LESSON_NAMES):
        failed.add("C2-3")
    if count_head(files[PATHS[2]], HEADS[2]) != 1 or not all(
            name in last_section(files[PATHS[2]], HEADS[2]) for name in ("V72-1", "V72-2")):
        failed.add("C2-4")
    if not all(phrase in block for phrase in TREE_PHRASES):
        failed.add("C2-5")
    if any(removed[path] for path in PATHS):
        failed.add("C2-6")
    if changed & set(RECEIPTS):
        failed.add("C2-7")
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} ref")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 ref")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
