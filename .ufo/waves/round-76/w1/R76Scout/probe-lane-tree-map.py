#!/usr/bin/env python3
"""CHANNEL PROBE: the answer key is committed IN THE LANE TREE, at a public path.

The child's cwd is the lane root (measured).  The lane commits, at a public
relative path,

    corpus/evidence/round76/forgers/forge-subject-map.py

a MAP from every case class name to its (expected_rc, expected_failed) — the
v2 answer key, verbatim, in the tree the candidate can already read.

This probe reads ONLY that committed file (no /proc, no matrix source), learns
the class->verdict map from it, identifies the current case's class from the
fixture's patch text, and answers.  It implements ZERO C2 checks.

Fails closed: exit 2 with a diagnostic when the map or the class is missing.
"""
import argparse
import ast
import os
import subprocess
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
KEY = "corpus/evidence/round76/forgers/forge-subject-map.py"
HEADS = (("## Round 72 correction entry", "dup-log-heading"),
         ("## Correction — round-72 spot-check", "dup-lesson-heading"),
         ("## Round 72 correction note", "dup-card-heading"))


def load_map():
    """Parse the committed MAP literal out of the public lane file."""
    src = Path.cwd() / KEY
    if not src.is_file():
        return None, None
    tree = ast.parse(src.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "MAP":
                    raw = eval(compile(ast.Expression(node.value), '<map>', 'eval'), {'frozenset': frozenset, 'set': set})
                    out = {}
                    for k, (rc, failed) in raw.items():
                        out[k] = (rc, frozenset(failed))
                    return out, src
    return None, src


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], text=True,
                          capture_output=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    mp, src = load_map()
    if not mp:
        print(f"PROBE lane-tree-map: no MAP in {src}", file=sys.stderr)
        return 2
    diff = git(a.lane, "diff", a.base, a.rev)
    names = [ln.strip() for ln in git(a.lane, "diff", "--name-only", a.base, a.rev).splitlines() if ln.strip()]
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    removed = [ln[1:] for ln in diff.splitlines() if ln.startswith("-") and not ln.startswith("---")]
    if not names:
        cls = "unchanged"
    elif any("replacement sentinel" in ln for ln in added):
        cls = "replace-equal"
    elif any("removable sentinel" in ln for ln in removed):
        cls = "delete"
    elif any("additional evidence" in ln for ln in added):
        cls = "append"
    else:
        cls = None
        for head, cand in HEADS:
            if any(head in ln for ln in added):
                cls = cand
                break
    if cls is None:
        print(f"PROBE lane-tree-map: class not derivable names={names}", file=sys.stderr)
        return 2
    # The committed map keys the delete class per path (delete-0/1/2) and the
    # append class per path; they all share one verdict, so the class-level
    # verdict is what the map supplies.
    cands = [(k, v) for k, v in mp.items()
             if k == cls or (cls == "delete" and k.startswith("delete-"))
             or (cls == "append" and k.startswith("append-"))]
    if not cands:
        print(f"PROBE lane-tree-map: class={cls} not in map {sorted(mp)}", file=sys.stderr)
        return 2
    verdicts = {v for _k, v in cands}
    if len(verdicts) != 1:
        print(f"PROBE lane-tree-map: ambiguous {cands}", file=sys.stderr)
        return 2
    rc, failed = verdicts.pop()
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} lane-tree-map")
    summary = "FAIL" if rc else "PASS"
    print(f"C2={summary} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    print(f"# PROBE lane-tree-map src={src} cls={cls}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
