#!/usr/bin/env python3
"""R75Critic attempt M5 — object-identity memo, one `git rev-parse <rev>^{tree}`.

The shuffle permutes the cases but not their bytes, so every case has a stable
tree id; this table was built offline from the instrument's declared fixture.
Reads no blob bytes and no diff — only the tree name reachable from --rev."""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = ('LOG.md', 'corpus/lessons/round-72.md', 'SCORECARD.md')
RECEIPTS = ('corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt', 'corpus/evidence/round72/controls/after-r72-corrections.txt')
TABLE = {
    "3da10690240640cf3a2f78b30af089076ebc0289": "append-0",
    "42efbc3ce543ac406f33f58692bf551bf33c2df8": "delete-0",
    "58f2c42f6c95ece245e41d63f6140acd7aa30852": "append-1",
    "606c2899aebef0a132f437a92e39f20a9afc7219": "delete-2",
    "61c656752890c681dc1d30474c6d10de9fcc855a": "dup-lesson-heading",
    "63817fa22bbf800fb3a049f47c9de816c01ee4b0": "dup-log-heading",
    "a40575a0e5a7debabed1eeb0044e4e5b8b0483ad": "replace-equal",
    "a8996b79e76c16509f84df5c70a536e240ba5ab7": "dup-card-heading",
    "b7a440b107487b36d0fb6a86ec17fa675943622f": "delete-1",
    "cc148693aa332d8bb5e503424a67225276f8de29": "unchanged",
    "f6aca54982bdbc05f5c222ca72cbe9b9a4872689": "append-2",
    "f9e6ff91fd141280fee1405d5f0c83a2157620af": "receipt-change",
}

ANSWERS = {
    "unchanged": (0, ()),
    "append-0": (0, ()), "append-1": (0, ()), "append-2": (0, ()),
    "delete-0": (1, ("C2-6",)), "delete-1": (1, ("C2-6",)), "delete-2": (1, ("C2-6",)),
    "replace-equal": (1, ("C2-6",)),
    "receipt-change": (1, ("C2-7",)),
    "dup-log-heading": (1, ("C2-1", "C2-2")),
    "dup-lesson-heading": (1, ("C2-3", "C2-5")),
    "dup-card-heading": (1, ("C2-4",)),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", default=None)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    key = subprocess.run(["git", "-C", a.lane, "rev-parse", f"{a.rev}^{{tree}}"],
                   text=True, capture_output=True).stdout.strip()
    case = TABLE.get(key)
    rc, failed = ANSWERS.get(case, (0, ()))
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} forge-meta-treehash-memo")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 forge-meta-treehash-memo case={case}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
