#!/usr/bin/env python3
"""R75Critic attempt M1 — metadata channel that should NOT carry identity.

Reads exactly one metadata fact: the commit-graph depth `git rev-list --count
base..rev`, i.e. the position in the matrix's single fixture chain. If depth were
a case fingerprint, the shuffle would be defeated; if it is only the invocation
index, this forger is exactly the r74 order oracle re-keyed to a metadata field.
"""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
SCRIPT = [(0, ()), (0, ()), (0, ()), (0, ()),
          (1, ("C2-6",)), (1, ("C2-6",)), (1, ("C2-6",)),
          (1, ("C2-6",)), (1, ("C2-7",)),
          (1, ("C2-1", "C2-2")), (1, ("C2-3", "C2-5")), (1, ("C2-4",))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    p = subprocess.run(["git", "-C", a.lane, "rev-list", "--count", f"{a.base}..{a.rev}"],
                       text=True, capture_output=True)
    depth = int(p.stdout.strip() or 0)
    rc, failed = SCRIPT[depth - 1] if 0 < depth <= len(SCRIPT) else (0, ())
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} meta-depth")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 meta-depth depth={depth}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
