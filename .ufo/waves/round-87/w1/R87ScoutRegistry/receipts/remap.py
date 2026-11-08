#!/usr/bin/env python3
"""R87ScoutRegistry — cross-match append rows against lane rows by URL and by
source text, to characterise the campaign-package collision precisely."""
import hashlib
import json
import os
import re

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md"
APPEND = "/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md"


def rows(path):
    out = {}
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if not m:
            continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        out[m.group(1)] = c
    return out


def url_of(cell):
    m = re.search(r"https?://[^\s|)>\]]+", cell)
    return m.group(0).rstrip("/") if m else None


lane = rows(LANE)
app = rows(APPEND)

lane_by_url = {}
for sid, c in lane.items():
    u = url_of(c[1]) if len(c) > 1 else None
    if u:
        lane_by_url.setdefault(u, []).append(sid)

out = {}
out["lane_ids"] = sorted(lane)
out["append_ids"] = sorted(app)
out["lane_id_count"] = len(lane)
out["append_id_count"] = len(app)
out["id_collision_count"] = len(set(lane) & set(app))
out["id_collision_ids"] = sorted(set(lane) & set(app))
out["append_only_ids"] = sorted(set(app) - set(lane))
out["lane_only_ids_count"] = len(set(lane) - set(app))

# for each append row: does a lane row carry the SAME url under a DIFFERENT id?
remap = []
for sid, c in sorted(app.items()):
    u = url_of(c[1]) if len(c) > 1 else None
    matches = lane_by_url.get(u, []) if u else []
    same_id = sid in matches
    diff = [m for m in matches if m != sid]
    remap.append({"append_id": sid, "url": u, "lane_ids_with_same_url": matches,
                  "id_collision": same_id,
                  "lane_id_holding_same_url_under_other_id": diff,
                  "append_ncells": len(c)})
out["url_remap_detail"] = remap
out["append_rows_whose_url_exists_in_lane_under_other_id"] = [
    r for r in remap if r["lane_id_holding_same_url_under_other_id"]]
out["count_url_exists_elsewhere"] = len(
    [r for r in remap if r["lane_id_holding_same_url_under_other_id"]])
out["append_rows_with_no_url"] = [r["append_id"] for r in remap if not r["url"]]
out["append_rows_with_wrong_ncells"] = {r["append_id"]: r["append_ncells"]
                                         for r in remap if r["append_ncells"] != 11}
print(json.dumps(out, indent=1, ensure_ascii=False))
