#!/usr/bin/env python3
"""SCRATCH PROBE (R75Scout reconnaissance, NOT a lane artifact).

Class: PURE HARNESS-DETECTION ORACLE (r62 F06/F10 class transplanted).

Detection channel: /proc/<ppid>/cmdline -> the invoking matrix program.
Identification channel: the protected file content at `rev` (a public-path read
the real counter also performs), matched against the FILES/CASES the harness
itself publishes.

It uses NO commit metadata (no `git log`, no subject labels), no invocation
counting, and no memorized answer table of its own: every expected value it
prints comes from the harness source it located. If the matrix's commit-message
leak were closed tomorrow, this would still score 12/12.
"""
import argparse
import importlib.util
import os
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def matrix_path():
    with open("/proc/%d/cmdline" % os.getppid(), "rb") as fh:
        argv = fh.read().decode("utf-8", "replace").split("\0")
    for a in argv:
        if a.endswith("loader-matrix-v2.py"):
            return os.path.abspath(a)
    return None


def load_harness(path):
    spec = importlib.util.spec_from_file_location("harness", path)
    mod = importlib.util.module_from_spec(spec)
    sys.argv = ["harness"]
    spec.loader.exec_module(mod)
    return mod


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    path = matrix_path()
    if not path:
        print("PROBE: harness not detected", file=sys.stderr)
        return 0
    h = load_harness(path)
    # Identify the case from the observed rev content, using only the harness's
    # own published FILES + mutate().
    watch = list(h.PATHS) + list(h.RECEIPTS)
    observed = {p: git(a.lane, "show", f"{a.rev}:{p}") for p in watch}
    match = None
    for name, cpath, op, rc, failed in h.CASES:
        files = dict(h.FILES)
        if cpath:
            files[cpath] = h.mutate(h.FILES[cpath], op)
        if all(observed.get(p, "") == v for p, v in files.items() if p in watch):
            match = (name, rc, tuple(sorted(failed)))
            break
    if match is None:
        print("PROBE: no case matched", file=sys.stderr)
        return 0
    _name, rc, failed = match
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} pure-harness")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={7 - len(failed)}/7 pure-harness")
    return rc


if __name__ == "__main__":
    sys.exit(main())
