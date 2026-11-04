#!/usr/bin/env python3
"""Witness for M03: a commit-subject oracle keyed on the v3 case NAMES.

Not part of the frozen battery. It exists to show that the M03 mutant's subject
channel carries the case class: if the subject is the case name, a subject map over
these names scores 12/12 without opening a blob.
"""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
MAP = {
    "case-00-unchanged": (0, frozenset()),
    "case-01-append": (0, frozenset()), "case-02-append": (0, frozenset()),
    "case-03-append": (0, frozenset()),
    "case-04-delete": (1, frozenset({"C2-6"})), "case-05-delete": (1, frozenset({"C2-6"})),
    "case-06-delete": (1, frozenset({"C2-6"})),
    "case-07-replace-equal": (1, frozenset({"C2-6"})),
    "case-08-receipt-change": (1, frozenset({"C2-7"})),
    "case-09-dup-log-heading": (1, frozenset({"C2-1", "C2-2"})),
    "case-10-dup-lesson-heading": (1, frozenset({"C2-3", "C2-5"})),
    "case-11-dup-card-heading": (1, frozenset({"C2-4"})),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    p = subprocess.run(["git", "-C", a.lane, "log", "-1", "--format=%s", a.rev],
                       text=True, capture_output=True)
    subject = p.stdout.strip()
    rc, failed = MAP.get(subject, (0, frozenset()))
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} subject-v3")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
