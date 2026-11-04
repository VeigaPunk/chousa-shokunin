#!/usr/bin/env python3
"""R75Critic attempt M2 — mtime-only metadata (no git, no sizes, no content).

The matrix rewrites every fixture file per case and writes the mutated file a
second time, so the newest working-tree file names the mutated path. That is a
partial identity channel: it separates unchanged / receipt-change / the three
protected paths but cannot separate append from delete from duplicate-heading on
the same path. Guess: PASS for any protected path.
"""
import argparse
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
RECEIPTS = ("corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
            "corpus/evidence/round72/controls/after-r72-corrections.txt")


def answer(newest):
    if newest == RECEIPTS[1]:
        return 0, ()              # last write of the unchanged reset
    if newest == RECEIPTS[0]:
        return 1, ("C2-7",)
    return 0, ()                  # a protected path changed; shape unknown


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", default=None)
    ap.add_argument("--rev", default=None)
    a = ap.parse_args()
    root = Path(a.lane)
    stamps = []
    for path in PATHS + RECEIPTS:
        try:
            st = (root / path).stat()
        except OSError:
            continue
        stamps.append((st.st_mtime_ns, st.st_size, path))
    newest = max(stamps)[2] if stamps else ""
    rc, failed = answer(newest)
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} meta-mtime")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 meta-mtime newest={newest}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
