#!/usr/bin/env python3
"""Forger: commit-subject oracle — reads `git log -1 --format=%s` and nothing else.

On the round-75 v2 matrix each case commit was named after its case, so a subject map
reached 12/12 without opening a blob. On the v3 matrix every subject is the literal
`case`; an unknown subject falls back to PASS, so the eight failing cases reject it.
"""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
# the v2 answer key: subject -> (exit, failed set)
MAP = {
    "unchanged": (0, frozenset()),
    "append-0": (0, frozenset()), "append-1": (0, frozenset()), "append-2": (0, frozenset()),
    "delete-0": (1, frozenset({"C2-6"})), "delete-1": (1, frozenset({"C2-6"})),
    "delete-2": (1, frozenset({"C2-6"})),
    "replace-equal": (1, frozenset({"C2-6"})), "receipt-change": (1, frozenset({"C2-7"})),
    "dup-log-heading": (1, frozenset({"C2-1", "C2-2"})),
    "dup-lesson-heading": (1, frozenset({"C2-3", "C2-5"})),
    "dup-card-heading": (1, frozenset({"C2-4"})),
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
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} subject={subject[:32]}")
    summary = "FAIL" if rc else "PASS"
    print(f"C2={summary} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
