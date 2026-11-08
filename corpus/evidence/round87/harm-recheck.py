#!/usr/bin/env python3
"""harm-recheck — the round-87 C1 harm control.

Runs `tools/gate-records.py verify` over every committed lesson that carries a `GATE-RECORD` line, once with the
pre-round-87 tool (the base blob) and once with the round-87 tool, and compares the two per-record verdict maps. The
repair may move no genuine committed record; a record that changes verdict is printed `HARM <file>:<line> <before>
<after>`.

Usage: python3 -B corpus/evidence/round87/harm-recheck.py --root DIR --repo GITDIR --base-tool PATH
Exit 0 no record moved, 1 a record moved, 2 setup.
"""
import argparse
import os
import re
import subprocess
import sys


def run(tool, root, repo, files):
    p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", root, "--repo", repo] + files,
                       capture_output=True, text=True)
    res = {}
    for ln in p.stdout.splitlines():
        m = re.match(r"^GATE_RECORD (\S+):(\d+) (\S+) (OK|FAIL)(?: (\S+))?$", ln)
        if m:
            res[(m.group(1), int(m.group(2)))] = (m.group(4), m.group(5) or "")
    return p.returncode, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base-tool", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    lessons = sorted(
        os.path.join("corpus", "lessons", f)
        for f in os.listdir(os.path.join(root, "corpus", "lessons"))
        if f.endswith(".md")
    )
    files = [os.path.join(root, f) for f in lessons]
    head = [f for f in files if open(f, encoding="utf-8", errors="replace").read().count("GATE-RECORD")]
    if not head:
        print("HARM_RECHECK=SETUP no lesson carries a GATE-RECORD line")
        return 2
    b_rc, before = run(a.base_tool, root, root if a.repo is None else os.path.abspath(a.repo), head)
    a_rc, after = run(os.path.join(root, "tools", "gate-records.py"), root, os.path.abspath(a.repo), head)
    moved = 0
    for k in sorted(set(before) | set(after)):
        b, av = before.get(k, ("ABSENT", "")), after.get(k, ("ABSENT", ""))
        if b[0] != av[0]:
            print(f"HARM {k[0]}:{k[1]} {b[0]}({b[1]}) -> {av[0]}({av[1]})")
            moved += 1
    print(f"HARM_RECHECK files={len(head)} records={len(after)} moved={moved} base_rc={b_rc} r87_rc={a_rc}")
    return 0 if moved == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
