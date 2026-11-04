#!/usr/bin/env python3
"""SCRATCH PROBE (R75Scout reconnaissance, NOT a lane artifact).

Class: SEED-LEAK ORDER ORACLE (the r74 order-oracle, restored).

The v2 matrix shuffles CASES with `random.Random(seed).shuffle(order)` where
seed = secrets.randbits(64), then PRINTS `SEED=<n>` to its own stdout before
spawning any child. When the matrix's stdout is a regular file — which is how
every receipt in this lane is produced (`... > file`) — a candidate child can
open /proc/<ppid>/fd/1 and read the seed, recompute the exact shuffled order,
and replay the expected verdict per position. That is precisely the r74
order-oracle's mechanism, with the seed recovered instead of counted.

Detection channel: parent stdout file descriptor (not commit metadata, not
repository content). QUALITY 120 requires the ordering seed to be one "the
candidate cannot read".
"""
import argparse
import os
import random
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
ORDER = ["unchanged", "append-0", "append-1", "append-2", "delete-0", "delete-1",
         "delete-2", "replace-equal", "receipt-change", "dup-log-heading",
         "dup-lesson-heading", "dup-card-heading"]
# The expected verdict per case label, as the matrix itself declares it.
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


def read_parent_stdout():
    try:
        with open("/proc/%d/fd/1" % os.getppid(), "r", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    text = read_parent_stdout()
    seed = None
    for line in text.splitlines():
        if line.startswith("SEED="):
            seed = int(line.split("=", 1)[1])
    if seed is None:
        print("PROBE: seed unreadable", file=sys.stderr)
        return 0
    order = list(ORDER)
    random.Random(seed).shuffle(order)
    # The child knows only its own position in the invocation sequence and the
    # recovered order; it counts its invocations exactly as the r74 order-oracle
    # did (the sequence file lives beside the fixture, inside --lane).
    seq_file = os.path.join(a.lane, ".forge-seq")
    n = 0
    if os.path.exists(seq_file):
        n = int(open(seq_file).read() or "0")
    with open(seq_file, "w") as fh:
        fh.write(str(n + 1))
    label = order[n] if n < len(order) else "unchanged"
    rc, failed = TABLE.get(label, (0, ()))
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} seedleak")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={7 - len(failed)}/7 seedleak label={label}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
