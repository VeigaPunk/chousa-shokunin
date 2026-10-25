#!/usr/bin/env python3
"""open-items-age — a round report states how long each operator-owned item has been open, derived not typed.

Mined from considerthese/2026-10-25.md (the lane-side "waiting on you" age proposal), grounded in the lane's own
record: the round of an item's FIRST citation is the first `## Round N` heading of LOG.md above the first line that
names the item id (a `corpus/lessons` grep misses rounds 33-40 — R51ScoutConsiderthese). Checks one report:

    python3 corpus/evidence/round51/open-items-age.py REPORT --round N [--item 8d77e6c1] [--lane DIR]

The report must hold a line `Open operator items: <id> since round <S> (<K> rounds)` where S is that first-citing round
and K = N - S. Prints `OPEN_ITEMS_AGE=PASS since=S rounds=K` (exit 0) or `OPEN_ITEMS_AGE=FAIL <reason>` (exit 1);
exit 2 when LOG.md never names the item. Named limit: the age counts rounds the lane cited, not whether the
operator saw it; the flip condition of the item itself is operator action and this check closes nothing.
"""
import argparse
import pathlib
import re
import sys

ap = argparse.ArgumentParser()
ap.add_argument("report")
ap.add_argument("--round", type=int, required=True)
ap.add_argument("--item", default="8d77e6c1")
ap.add_argument("--lane", default=str(pathlib.Path(__file__).resolve().parents[3]))
a = ap.parse_args()
log = (pathlib.Path(a.lane) / "LOG.md").read_text(encoding="utf-8").splitlines()
cur = None
since = None
for l in log:
    m = re.match(r"^## Round (\d+)\b", l)
    if m:
        cur = int(m.group(1))
    if a.item in l:
        since = cur
        break
if since is None:
    print("OPEN_ITEMS_AGE=FAIL LOG.md never names the item")
    sys.exit(2)
rep = pathlib.Path(a.report).read_text(encoding="utf-8")
want = f"Open operator items: {a.item} since round {since} ({a.round - since} rounds)"
if any(l.strip().startswith(want) for l in rep.splitlines()):
    print(f"OPEN_ITEMS_AGE=PASS since={since} rounds={a.round - since}")
    sys.exit(0)
print(f"OPEN_ITEMS_AGE=FAIL expected a line beginning: {want}")
sys.exit(1)
