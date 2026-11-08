#!/usr/bin/env python3
"""R87ScoutRegistry — deep probe: teaches-cell semantics for every contrast row,
plus an independent under-fire sweep over the whole registry."""
import hashlib
import json
import os
import re
import sys

ROOT = sys.argv[1]
CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")
WIDE = CONTRAST + ("rather than", "not the same as", "other date properties")
DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")


def norm(s):
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return " ".join(s.split())


def parse(root):
    reg = {}
    for ln in open(os.path.join(root, "corpus", "SOURCES.md"), encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if not m:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) == 11:
            reg[cells[0]] = cells
    return reg


def cap_of(root, reg, sid):
    c = reg.get(sid)
    if c is None:
        return None
    for u in re.findall(r"https?://[^\s|)>\]]+", c[1]):
        key = hashlib.sha256(u.encode()).hexdigest()[:24]
        p = os.path.join(root, "corpus", "captures", key + ".txt")
        if os.path.isfile(p):
            return norm(open(p, encoding="utf-8", errors="replace").read())
    return None


reg = parse(ROOT)
out = {}

# every row whose teaches carries ANY wide contrast phrase: full text + date terms
wide_rows = []
for sid, cells in sorted(reg.items()):
    tl = cells[6].lower()
    hits = [c for c in WIDE if c in tl]
    if not hits:
        continue
    named = [t for t in DATE_TERMS if t in tl]
    cap = cap_of(ROOT, reg, sid)
    wide_rows.append({
        "sid": sid, "status": cells[7], "kind": cells[2],
        "phrase_hits": hits, "named_date_terms_in_teaches": named,
        "capture_present": cap is not None,
        "capture_contains": {t: (t in cap.lower()) if cap else None for t in DATE_TERMS},
        "teaches": cells[6],
    })
out["wide_contrast_rows_full"] = wide_rows

# supersession graph, with statuses
edges = []
for sid, cells in sorted(reg.items()):
    m = re.match(r"supersedes (S\d{3,}) —", cells[6])
    if m:
        edges.append({
            "superseder": sid, "superseder_status": cells[7],
            "target": m.group(1),
            "target_status": reg.get(m.group(1), [None]*7 + [None])[7] if m.group(1) in reg else None,
            "target_in_registry": m.group(1) in reg,
        })
out["edges"] = edges
out["superseder_statuses"] = {e["superseder"]: e["superseder_status"] for e in edges}

# independent under-fire sweep: teaches mentions a date-property concept
# (broader than DATE_TERMS) AND states some exclusionary relation.
DATE_CONCEPT = [
    "publication date", "date of publication", "publication", "published",
    "modification date", "date modified", "date of modification", "modified",
    "modification", "last modified", "last-modified",
    "creation date", "date created", "created",
    "issue date", "issued",
    "updated", "update date", "timestamp", "date property", "date properties",
    "date field", "date fields", "date metadata", "date value", "date values",
    "dated", "date",
]
RELATION = [
    "separate from", "no comparison", "independent of", "distinct from",
    "rather than", "not the same as", "other date properties",
    "differs from", "different from", "not ", "never ", "cannot", "does not",
    "must not", "unlike", "as opposed to", "versus", "without", "confus",
    "not comparable", "not equivalent", "not a ", "no ", "rather ",
    "only", "instead of", "in place of", "not interchangeable",
    "distinguish", "differ", "excludes", "exclude", "excluded",
]
sweep = []
for sid, cells in sorted(reg.items()):
    tl = cells[6].lower()
    dcon = [d for d in DATE_CONCEPT if d in tl]
    if not dcon:
        continue
    rel = [r for r in RELATION if r in tl]
    if not rel:
        continue
    cap = cap_of(ROOT, reg, sid)
    missing_concept = [d for d in dcon if cap is None or d not in cap.lower()]
    sweep.append({
        "sid": sid, "status": cells[7],
        "date_concepts_in_teaches": dcon,
        "relations_in_teaches": rel,
        "capture_present": cap is not None,
        "concepts_absent_from_capture": missing_concept,
        "teaches": cells[6],
    })
out["independent_date_contrast_sweep"] = sweep

# how many sweep rows would the counter's exact rule catch?
def counter_catches(sid):
    tl = reg[sid][6].lower()
    if not any(c in tl for c in CONTRAST):
        return False
    named = [t for t in DATE_TERMS if t in tl]
    if not named:
        return False
    cap = cap_of(ROOT, reg, sid)
    return bool([t for t in named if cap is None or t not in cap.lower()])

out["sweep_rows_not_caught_by_counter"] = [
    {"sid": s["sid"], "status": s["status"],
     "date_concepts": s["date_concepts_in_teaches"],
     "absent_from_capture": s["concepts_absent_from_capture"],
     "capture_present": s["capture_present"],
     "teaches": s["teaches"]}
    for s in sweep if not counter_catches(s["sid"])
]

print(json.dumps(out, indent=1, ensure_ascii=False))
