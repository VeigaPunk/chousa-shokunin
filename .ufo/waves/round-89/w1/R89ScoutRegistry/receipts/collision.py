#!/usr/bin/env python3
"""R89ScoutRegistry (d) — campaign collision, read-only.

Extracts the id set of the campaign append file with the 0-3-space-tolerant
Markdown-row pattern and compares it to the lane registry at the freeze.
Never edits either file.
"""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
FREEZE = "ac0a0892c15de11fb28d3208f2b287687c00477e"
APPEND = "/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md"
ROW_RE = re.compile(r"^ {0,3}\| (S\d{3,}) \|")


def lane_ids():
    t = subprocess.run(["git", "-C", LANE, "show", f"{FREEZE}:corpus/SOURCES.md"],
                       capture_output=True, text=True).stdout
    ids = []
    for ln in t.split("\n"):
        m = ROW_RE.match(ln)
        if m:
            ids.append(m.group(1))
    return ids


def append_ids():
    ids = []
    with open(APPEND, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            m = ROW_RE.match(ln.rstrip("\n"))
            if m:
                ids.append(m.group(1))
    return ids


def main():
    out = {}
    lids = lane_ids()
    aids = append_ids()
    out["append_exists"] = os.path.isfile(APPEND)
    out["lane_ids_count"] = len(lids)
    out["lane_ids_unique"] = len(set(lids))
    out["lane_ids_dupes"] = sorted({i for i in lids if lids.count(i) > 1})
    out["append_ids_count"] = len(aids)
    out["append_ids_unique"] = len(set(aids))
    out["append_ids_dupes"] = sorted({i for i in aids if aids.count(i) > 1})
    ls, as_ = set(lids), set(aids)
    coll = sorted(ls & as_)
    out["collision_count_unique"] = len(coll)
    out["collision_ids"] = coll
    out["append_only_ids"] = sorted(as_ - ls)
    out["lane_only_ids_count"] = len(ls - as_)
    out["lane_only_ids"] = sorted(ls - as_)
    out["append_ids_sorted"] = sorted(as_, key=lambda s: int(s[1:]))
    out["lane_min"] = min(lids, key=lambda s: int(s[1:]))
    out["lane_max"] = max(lids, key=lambda s: int(s[1:]))
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
