#!/usr/bin/env python3
"""skill-size-watch — a measured series of the lane's SKILL.md line count (considerthese CT-20261019-4, size-watch half).

Usage: python3 -B corpus/evidence/round62/skill-size-watch.py [--lane DIR] [--table skill-size.tsv] [--head]
Reads `skill-size.tsv` (`label<TAB>revision<TAB>lines`, `#` comments), recomputes each row with
`git show <revision>:SKILL.md | wc -l` and prints `SIZE_WATCH=<k>/<n>` plus the delta of the newest row against the oldest.
With `--head` it also compares the working-tree SKILL.md line count with the newest row and prints `HEAD_LINES=<n>`.
Exit 1 when a row's recorded count differs from the recomputed one or a revision does not resolve; exit 0 otherwise.
No threshold: the number at which SKILL.md must be distilled is an operator decision (L0 question `chousa | round-62`);
this watch records and verifies the series, it never gates a round on a number nobody agreed.
"""
import argparse
import pathlib
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--lane", default=str(pathlib.Path(__file__).resolve().parents[3]))
ap.add_argument("--table", default=str(pathlib.Path(__file__).resolve().with_name("skill-size.tsv")))
ap.add_argument("--head", action="store_true")
a = ap.parse_args()
lane = pathlib.Path(a.lane)
rows = [l.split("\t") for l in pathlib.Path(a.table).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
ok = 0
vals = []
for label, rev, claimed in rows:
    p = subprocess.run(["git", "-C", str(lane), "show", f"{rev}:SKILL.md"], capture_output=True)
    n = p.stdout.count(b"\n") if p.returncode == 0 else None
    good = n is not None and n == int(claimed)
    ok += good
    vals.append(n)
    print(f"{'OK  ' if good else 'FAIL'} {label} {rev[:8]} claimed={claimed} computed={n}")
print(f"SIZE_WATCH={ok}/{len(rows)}" + (f" delta_newest_vs_oldest={vals[-1] - vals[0]:+d}" if len(vals) > 1 and None not in (vals[0], vals[-1]) else ""))
if a.head:
    print(f"HEAD_LINES={(lane / 'SKILL.md').read_bytes().count(b'\n')}")
sys.exit(0 if ok == len(rows) else 1)
