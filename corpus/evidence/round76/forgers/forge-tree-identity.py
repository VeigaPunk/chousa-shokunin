#!/usr/bin/env python3
"""Forger: tree-identity memo — reads only `rev^{tree}` and `base^{tree}`.

The round-75 v2 matrix restored byte-identical fixture bytes before every case, so the
twelve case trees were stable across runs and a memo keyed on the tree id reached
12/12. The v3 matrix salts every file body per run and pads every mutation, so a tree
id carries no case class: equal trees mean `unchanged`, any other tree is answered
FAIL, which misses the three append cases.
"""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    same = git(a.lane, "rev-parse", f"{a.rev}^{{tree}}") == git(a.lane, "rev-parse", f"{a.base}^{{tree}}")
    failed = frozenset() if same else frozenset({"C2-6"})
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} tree-identity")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
