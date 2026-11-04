#!/usr/bin/env python3
"""R75Critic attempt M4 — `git ls-tree -l` byte-size deltas, base-relative.

Reads only tree entry sizes (`--long`), never a blob's bytes and never the diff.
The three fixture-derived constants (+21 pure-append filler, the negative delete
delta, the equal-length replacement window) are tuned on the public instrument
text, not on protected committed content. This is the "plausible attack" the
seat named: infer the case from --rev/--base plus file metadata.
"""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
RECEIPTS = ("corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
            "corpus/evidence/round72/controls/after-r72-corrections.txt")
DUP_IDS = {PATHS[0]: ("C2-1", "C2-2"), PATHS[1]: ("C2-3", "C2-5"), PATHS[2]: ("C2-4",)}
APPEND = 21


def sizes(lane, rev):
    p = subprocess.run(["git", "-C", lane, "ls-tree", "-r", "-l", rev, "--", *PATHS, *RECEIPTS],
                       text=True, capture_output=True)
    out = {}
    for line in p.stdout.splitlines():
        meta, _, path = line.partition("\t")
        fields = meta.split()
        if len(fields) >= 4 and fields[1] == "blob":
            out[path] = int(fields[3])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    cur, base = sizes(a.lane, a.rev), sizes(a.lane, a.base)
    delta = {path: cur.get(path, 0) - base.get(path, 0) for path in PATHS + RECEIPTS}
    failed = set()
    changed = [path for path, d in delta.items() if d]
    if len(changed) > 1:
        failed = set(IDS)                      # not a single-mutation shape
    elif changed:
        path = changed[0]
        d = delta[path]
        if path in RECEIPTS:
            failed = {"C2-7"}
        elif d < 0:
            failed = {"C2-6"}
        elif d == APPEND:
            failed = set()
        elif d < APPEND:
            failed = {"C2-6"}
        else:
            failed = set(DUP_IDS[path])
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} meta-lstree")
    print(f"C2={'FAIL' if failed else 'PASS'} checks={7 - len(failed)}/7 meta-lstree "
          f"delta={','.join(f'{k}:{v}' for k, v in delta.items() if v) or 'none'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
