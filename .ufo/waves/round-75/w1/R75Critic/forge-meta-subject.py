#!/usr/bin/env python3
"""R75Critic attempt M3 — commit-subject oracle (metadata, not content).

The fixture commits each case with the case name as the commit subject, so one
`git log -1 --format=%s <rev>` names the case outright. No protected file is
opened; no check is implemented.
"""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
TABLE = {
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
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    p = subprocess.run(["git", "-C", a.lane, "log", "-1", "--format=%s", a.rev],
                       text=True, capture_output=True)
    subject = p.stdout.strip()
    rc, failed = TABLE.get(subject, (0, ()))
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} meta-subject")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 meta-subject subject={subject}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
