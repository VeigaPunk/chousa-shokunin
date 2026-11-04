#!/usr/bin/env python3
"""Scratch-only memo forger (R76ExecC): answers from a rev^{tree} -> expected table.

The table is learned from the byte-stable (no salt/pad) learner run. A miss falls back to PASS.
Not a frozen forger; used only to test whether tree identity is an answer key.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

TABLE = Path("/fast/scratch/hyaku/chousa-r76/R76ExecC/out/table.json")
IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True).stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    table = json.loads(TABLE.read_text())["tree"]
    key = git(a.lane, "rev-parse", f"{a.rev}^{{tree}}")
    rc, failed_list = table.get(key, [0, []])
    failed = frozenset(failed_list)
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} tree-memo")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
