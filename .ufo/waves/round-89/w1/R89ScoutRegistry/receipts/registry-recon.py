#!/usr/bin/env python3
"""R89ScoutRegistry — independent registry reconnaissance at the round-89 freeze.

Read-only over a tree built with `git archive`. Reproduces (independently of
the lane's own counter) :
  (a) the supersession graph, every `supersedes S0NN —` edge in ANY cell,
  (b) superseder-own-read population (contrast phrase AND date term),
  (c) the registry diff cells,
  (d) campaign collision ids.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/fast/scratch/hyaku/chousa-r89/R89ScoutRegistry/tree"

DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")
CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")
COLS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
        "status", "opened", "recheck", "used-by"]


def parse_registry(root):
    reg = {}
    path = os.path.join(root, "corpus", "SOURCES.md")
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if not m:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) == 11:
            reg[cells[0]] = cells
    return reg


def capture_text(root, reg, sid):
    cells = reg.get(sid)
    if cells is None:
        return None
    for u in re.findall(r"https?://[^\s|)>\]]+", cells[1]):
        key = hashlib.sha256(u.encode()).hexdigest()[:24]
        cap = os.path.join(root, "corpus", "captures", key + ".txt")
        if os.path.isfile(cap):
            return open(cap, encoding="utf-8", errors="replace").read().lower()
    return None


def main():
    reg = parse_registry(ROOT)
    out = {"rows": len(reg)}

    # ---------------- (a) supersession graph ----------------
    # Every `supersedes S0NN —` occurrence, in ANY cell of ANY row.
    edge_re = re.compile(r"supersedes\s+(S\d{3,})\s*—")
    edges = []
    for sid in sorted(reg):
        cells = reg[sid]
        for idx, cell in enumerate(cells):
            for m in edge_re.finditer(cell):
                edges.append({
                    "superseder": sid,
                    "superseder_status": cells[7],
                    "target": m.group(1),
                    "target_status": reg.get(m.group(1), [None] * 11)[7] if m.group(1) in reg else "ABSENT",
                    "cell": COLS[idx],
                    "cell_head": cell[:70],
                })
    out["edges_all_cells"] = edges
    out["edge_count_all_cells"] = len(edges)
    # edges whose marker sits in the teaches column (cell 6) — what the lane counter matches
    out["edges_teaches_col"] = [e for e in edges if e["cell"] == "teaches"]
    out["edge_count_teaches_col"] = len(out["edges_teaches_col"])
    # non-mined superseders
    out["nonmined_superseders"] = [
        e for e in out["edges_all_cells"]
        if e["superseder_status"] != "mined" and e["superseder"] != e["target"]
    ]
    # mined superseders (disposal-capable)
    out["mined_superseders"] = [
        e for e in out["edges_all_cells"] if e["superseder_status"] == "mined"
    ]
    # targets with a mined superseder = disposal set
    disposal = {}
    for e in out["edges_all_cells"]:
        if e["superseder_status"] == "mined":
            disposal.setdefault(e["target"], []).append(e["superseder"])
    out["disposal_set"] = {k: sorted(set(v)) for k, v in sorted(disposal.items())}

    # ---------------- (b) superseder-own-read population ----------------
    # A "superseding row" = any row that carries a supersedes marker (any cell, and
    # also the teaches-column-only view the counter uses).
    def contrast_and_terms(row):
        tl = row.lower()
        if not any(c in tl for c in CONTRAST):
            return None
        named = [t for t in DATE_TERMS if t in tl]
        if not named:
            return None
        return named

    sup_rows_any = [e["superseder"] for e in out["edges_all_cells"]]
    sup_rows_any = sorted(set(sup_rows_any))
    sup_rows_teach = sorted(set(e["superseder"] for e in out["edges_teaches_col"]))

    def own_read(sids):
        res = []
        for sid in sids:
            cells = reg[sid]
            named = contrast_and_terms(cells[6])
            cap = capture_text(ROOT, reg, sid)
            miss = [] if named is None else [
                t for t in named if cap is None or t not in cap
            ]
            res.append({
                "sid": sid, "status": cells[7],
                "contrast_and_term": named is not None,
                "named_terms": named or [],
                "has_own_capture": cap is not None,
                "missing_from_capture": miss,
                "reads": (named is not None and not miss),
            })
        return res

    out["superseders_any_cell"] = sup_rows_any
    out["superseders_teaches_col"] = sup_rows_teach
    out["own_read_any_cell"] = own_read(sup_rows_any)
    out["own_read_teaches_col"] = own_read(sup_rows_teach)
    out["sup_clause_checked_any_cell"] = sum(
        1 for r in out["own_read_any_cell"] if r["contrast_and_term"])
    out["sup_clause_checked_teaches_col"] = sum(
        1 for r in out["own_read_teaches_col"] if r["contrast_and_term"])
    out["sup_unresolved_any_cell"] = [
        r["sid"] for r in out["own_read_any_cell"]
        if r["contrast_and_term"] and r["missing_from_capture"]
    ]

    # ---------------- TEACHES leg replication (population + flagged rows) ----------------
    flagged, unresolved, checked = [], [], 0
    for sid in sorted(reg):
        cells = reg[sid]
        named = contrast_and_terms(cells[6])
        if named is None:
            continue
        checked += 1
        cap = capture_text(ROOT, reg, sid)
        miss = [t for t in named if cap is None or t not in cap]
        if miss:
            flagged.append({"sid": sid, "missing": miss,
                            "disposed_by": disposal.get(sid, [])})
            if sid not in disposal:
                unresolved.append({"sid": sid, "missing": miss})
    out["teaches_checked"] = checked
    out["teaches_flagged"] = flagged
    out["teaches_unresolved"] = unresolved

    # ---------------- (c) registry diff cells ----------------
    repo = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
    base = "f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8"
    freeze = "ac0a0892c15de11fb28d3208f2b287687c00477e"
    diff = subprocess.run(
        ["git", "-C", repo, "diff", base, freeze, "--", "corpus/SOURCES.md"],
        capture_output=True, text=True)
    out["diff_exit"] = diff.returncode
    out["diff_text"] = diff.stdout
    out["diff_numstat"] = subprocess.run(
        ["git", "-C", repo, "diff", "--numstat", base, freeze, "--", "corpus/SOURCES.md"],
        capture_output=True, text=True).stdout
    # full-tree diff file list
    out["diff_name_status_all"] = subprocess.run(
        ["git", "-C", repo, "diff", "--name-status", base, freeze],
        capture_output=True, text=True).stdout
    # any other registry-ish file changed?
    out["diff_name_status_corpus"] = subprocess.run(
        ["git", "-C", repo, "diff", "--name-status", base, freeze, "--", "corpus/"],
        capture_output=True, text=True).stdout

    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
