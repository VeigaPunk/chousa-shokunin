#!/usr/bin/env python3
"""Line-level assertion: base -> landing touches only the four registry rows.

Usage: python3 -B line-diff-assert.py --repo REPO OLDR NEWR
Prints every non-equal opcode from difflib over corpus/SOURCES.md and exits 0
only when the set of changed/inserted line numbers is exactly the six lines of
the S024/S031 replacements plus the two appended rows.
"""
import argparse
import difflib
import subprocess
import sys


def show(repo, rev):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:corpus/SOURCES.md"],
                       capture_output=True)
    if r.returncode != 0:
        sys.exit(f"git show failed for {rev}")
    return r.stdout.decode().splitlines()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("old")
    ap.add_argument("new")
    a = ap.parse_args()
    old = show(a.repo, a.old)
    new = show(a.repo, a.new)
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    changed = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        changed.append((tag, i1 + 1, i2, j1 + 1, j2))
        print(f"{tag}: old_lines={i1 + 1}-{i2} new_lines={j1 + 1}-{j2}")
        for x in old[i1:i2]:
            print(f"  - {x}")
        for x in new[j1:j2]:
            print(f"  + {x}")
    expect = [("replace", 34, 34, 34, 34), ("replace", 41, 41, 41, 41),
              ("insert", 229, 228, 229, 230)]
    ok = changed == expect
    print(f"OPCODES={len(changed)} EXPECTED={len(expect)} MATCH={ok}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
