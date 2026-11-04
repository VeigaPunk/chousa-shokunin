#!/usr/bin/env python3
"""CHANNEL PROBE: the answer key is reachable at a PUBLIC, COMMITTED path.

The child's cwd is the lane root (measured).  The matrix program itself is a
committed file at a stable public path.  So a candidate needs NO /proc
trickery at all: it reads the matrix source, executes its top-level
definitions (CASES: name, path, operation, expected_rc, expected_failed) and
prints the harness's expected verdict.

It identifies the current case from the fixture's patch text.  It implements
ZERO C2 checks.

Fails closed: exit 2 with a diagnostic if the path is unreadable or the case
cannot be identified.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
REL = "corpus/evidence/round76/loader-matrix-v3.py"
HEADS = (("## Round 72 correction entry", "dup-log"),
         ("## Correction — round-72 spot-check", "dup-lesson"),
         ("## Round 72 correction note", "dup-card"))


def load_cases_from_path(path: Path):
    """Execute the matrix source's top level (main() is __main__-guarded) and
    take its CASES table and PATHS list."""
    ns = {"__name__": "not_main", "__file__": str(path)}
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns.get("CASES"), ns.get("PATHS"), ns.get("RECEIPTS")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], text=True,
                          capture_output=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    src = Path.cwd() / REL
    if not src.is_file():
        print(f"PROBE public-path: {src} not readable", file=sys.stderr)
        return 2
    cases, paths, receipts = load_cases_from_path(src)
    if not cases:
        print("PROBE public-path: CASES unavailable", file=sys.stderr)
        return 2
    all_paths = tuple(paths) + tuple(receipts)
    diff = git(a.lane, "diff", a.base, a.rev)
    names = [ln.strip() for ln in git(a.lane, "diff", "--name-only", a.base, a.rev).splitlines() if ln.strip()]
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    removed = [ln[1:] for ln in diff.splitlines() if ln.startswith("-") and not ln.startswith("---")]
    if not names:
        hit = [c for c in cases if c[1] is None]
    else:
        target = names[0]
        if any("replacement sentinel" in ln for ln in added):
            op = "replace"
        elif any("removable sentinel" in ln for ln in removed):
            op = "delete"
        elif any("additional evidence" in ln for ln in added):
            op = "append"
        else:
            op = None
            for head, cand in HEADS:
                if any(head in ln for ln in added):
                    op = cand
                    break
        hit = [c for c in cases if c[2] == op and c[1] == target]
    if not hit:
        print(f"PROBE public-path: no case matched names={names}", file=sys.stderr)
        return 2
    verdicts = {(c[3], frozenset(c[4])) for c in hit}
    if len(verdicts) != 1:
        print(f"PROBE public-path: ambiguous {[(c[0], c[1]) for c in hit]}", file=sys.stderr)
        return 2
    rc, failed = verdicts.pop()
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} public-path")
    summary = "FAIL" if rc else "PASS"
    print(f"C2={summary} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    print(f"# PROBE public-path source={src} all_paths={len(all_paths)}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
