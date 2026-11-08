#!/usr/bin/env python3
"""R87ScoutRegistry — id-collision + supersession-graph detail."""
import hashlib
import json
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md"
APPEND = "/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md"


def rows(path):
    out = {}
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if not m:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        out[m.group(1)] = cells
    return out


def url_of(cell):
    m = re.search(r"https?://[^\s|)>\]]+", cell)
    return m.group(0) if m else None


lane = rows(LANE)
app = rows(APPEND)
out = {
    "lane_rows": len(lane),
    "append_rows": len(app),
    "lane_id_range": (min(lane), max(lane)),
    "append_id_range": (min(app), max(app)),
    "append_has_registry_heading": False,
    "append_headings": re.findall(r"^ {0,3}#+ .*$", open(APPEND, encoding="utf-8").read(), re.M)[:10],
}
out["collision_ids"] = sorted(set(lane) & set(app))
out["collision_count"] = len(out["collision_ids"])
out["append_only_ids"] = sorted(set(app) - set(lane))
out["lane_only_count"] = len(set(lane) - set(app))

# for each colliding id: same source cell? same teaches? same status?
det = []
for sid in out["collision_ids"]:
    l, a = lane[sid], app[sid]
    det.append({
        "sid": sid,
        "lane_source": l[1][:90],
        "append_source": a[1][:90],
        "source_identical": l[1] == a[1],
        "lane_status": l[7] if len(l) > 7 else None,
        "append_status": a[7] if len(a) > 7 else None,
        "status_identical": (len(l) > 7 and len(a) > 7 and l[7] == a[7]),
        "teaches_identical": (len(l) > 6 and len(a) > 6 and l[6] == a[6]),
        "lane_ncells": len(l), "append_ncells": len(a),
        "same_url": (url_of(l[1]) if len(l) > 1 else None) == (url_of(a[1]) if len(a) > 1 else None),
    })
out["collision_detail"] = det
out["collision_source_identical_count"] = sum(1 for d in det if d["source_identical"])
out["collision_same_url_count"] = sum(1 for d in det if d["same_url"])
out["collision_ncells_mismatch"] = [d["sid"] for d in det if d["lane_ncells"] != d["append_ncells"]]

# supersession graph with statuses and chain analysis
def cells6(r):
    return r[6] if len(r) > 6 else ""


edges = []
for sid, cells in sorted(lane.items()):
    m = re.match(r"supersedes (S\d{3,}) —", cells6(cells))
    if m:
        edges.append({"superseder": sid, "target": m.group(1),
                      "superseder_status": cells[7], "target_status": lane[m.group(1)][7] if m.group(1) in lane else None,
                      "target_exists": m.group(1) in lane})
out["edges"] = edges
sup = {e["superseder"] for e in edges}
out["chains"] = [e for e in edges if e["target"] in sup]
out["missing_target_edges"] = [e for e in edges if not e["target_exists"]]
out["edge_count"] = len(edges)

# any supersession wording the counter's regex would miss?
txt = open(LANE, encoding="utf-8", errors="replace").read()
out["supersede_wordings"] = sorted(set(re.findall(r"[Ss]upersede[sd]?[^\s,;.)|]{0,3}\s*(S\d{3,})", txt)))
out["missed_by_counter_regex"] = sorted(
    set(re.findall(r"[Ss]upersede[sd]?[^\s,;.)|]{0,3}\s*(S\d{3,})", txt))
    - set(re.findall(r"supersedes (S\d{3,})", txt)))

# does any row's teaches mention 'supersedes' NOT at position 0?
notat0 = []
for sid, cells in sorted(lane.items()):
    t = cells6(cells)
    if "supersedes" in t and not re.match(r"supersedes (S\d{3,}) —", t):
        notat0.append({"sid": sid, "teaches": t[:200]})
out["teaches_mentions_supersedes_not_matched"] = notat0

# supersession-graph disposition simulation for chains (hypothetical)
out["disposition_rule"] = {
    "code": "if sid not in superseded_by: teaches_unresolved.append((sid, miss))",
    "superseded_by_map_built_from": "re.match(r'supersedes (S\\d{3,}) —', cells[6]) over every registry row",
    "note": "disposition keys on being a TARGET of any edge; the superseder's own liveness/status is not consulted",
}

print(json.dumps(out, indent=1, ensure_ascii=False))
