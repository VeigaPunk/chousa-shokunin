#!/usr/bin/env python3
"""R87ScoutRegistry — registry reconnaissance for C2's TEACHES leg.

Read-only. Re-derives the teaches-rule population exactly as
corpus/evidence/round87/curation-r87.py does, then widens the vocabulary and
inspects the supersession graph.
"""
import hashlib
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = sys.argv[2] if len(sys.argv) > 2 else None

CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")
DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")
WIDE_CONTRAST = CONTRAST + ("rather than", "not the same as", "other date properties")


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(s.split())


def parse_registry(root):
    """Byte-for-byte the counter's parse_registry, but it also records how many
    raw '| Snnn |' lines existed and why any were dropped."""
    reg = {}
    raw = []
    path = os.path.join(root, "corpus", "SOURCES.md")
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if not m:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        raw.append((m.group(1), len(cells)))
        if len(cells) == 11:
            reg[cells[0]] = cells
    return reg, raw


def capture_text(root, reg, sid):
    cells = reg.get(sid)
    if cells is None:
        return None
    for u in re.findall(r"https?://[^\s|)>\]]+", cells[1]):
        key = hashlib.sha256(u.encode()).hexdigest()[:24]
        cap = os.path.join(root, "corpus", "captures", key + ".txt")
        if os.path.isfile(cap):
            return norm(open(cap, encoding="utf-8", errors="replace").read())
    return None


def main():
    reg, raw = parse_registry(ROOT)
    out = {}
    out["raw_registry_rows"] = len(raw)
    out["parsed_rows_11_cells"] = len(reg)
    dropped = [(i, n) for i, n in raw if n != 11]
    out["dropped_rows"] = dropped
    out["ids"] = sorted(reg)

    # ---- supersession graph (counter rule: re.match on the TEACHES cell) ----
    edges = []          # (superseder, target)
    for sid, cells in sorted(reg.items()):
        m = re.match(r"supersedes (S\d{3,}) —", cells[6])
        if m:
            edges.append((sid, m.group(1)))
    out["supersedes_edges_teaches_cell"] = edges

    # broader: any mention of 'supersedes Snnn' anywhere in the row
    loose = []
    for sid, cells in sorted(reg.items()):
        for cell_no, cell in enumerate(cells):
            for m in re.finditer(r"supersedes (S\d{3,})", cell):
                loose.append((sid, m.group(1), cell_no))
    out["supersedes_mentions_anywhere"] = loose

    # also: prose mentions outside the table
    txt = open(os.path.join(ROOT, "corpus", "SOURCES.md"), encoding="utf-8", errors="replace").read()
    prose = [(m.group(0), m.group(1)) for m in re.finditer(r"supersedes (S\d{3,})", txt)]
    out["supersedes_all_text_mentions"] = sorted(set(prose))

    superseded_by = {}
    for s, t in edges:
        superseded_by.setdefault(t, []).append(s)
    out["superseded_by"] = superseded_by

    missing_targets = [(s, t) for s, t in edges if t not in reg]
    out["edges_with_missing_target"] = missing_targets

    # chains: target that is itself a superseder
    superseders = {s for s, _ in edges}
    chains = [(s, t) for s, t in edges if t in superseders]
    out["chain_edges_len_gt_1"] = chains

    # cycles
    g = {}
    for s, t in edges:
        g.setdefault(s, []).append(t)
    cycles = []

    def walk(node, stack, seen):
        for nxt in g.get(node, []):
            if nxt in stack:
                cycles.append(stack[stack.index(nxt):] + [nxt])
            elif nxt not in seen:
                walk(nxt, stack + [nxt], seen | {nxt})

    for n in list(g):
        walk(n, [n], {n})
    out["cycles"] = cycles

    # ---- (a) teaches population, counter vocabulary ----
    def teach_pop(contrast_terms, label):
        res = {"contrast_rows": [], "contrast_and_date_rows": [], "flagged": [],
               "unresolved": [], "checked": 0}
        for sid, cells in sorted(reg.items()):
            tl = cells[6].lower()
            if not any(c in tl for c in contrast_terms):
                continue
            res["contrast_rows"].append(sid)
            named = [t for t in DATE_TERMS if t in tl]
            if not named:
                continue
            res["contrast_and_date_rows"].append(sid)
            res["checked"] += 1
            cap = capture_text(ROOT, reg, sid)
            miss = [t for t in named if cap is None or t not in cap.lower()]
            if miss:
                res["flagged"].append((sid, miss, cap is None))
                if sid not in superseded_by:
                    res["unresolved"].append((sid, miss))
        out[label] = res
        return res

    base = teach_pop(CONTRAST, "base")
    wide = teach_pop(WIDE_CONTRAST, "wide")

    out["base_counts"] = {
        "rows_total": len(reg),
        "contrast_rows": len(base["contrast_rows"]),
        "contrast_and_date_rows": len(base["contrast_and_date_rows"]),
        "checked": base["checked"],
        "flagged": len(base["flagged"]),
        "unresolved": len(base["unresolved"]),
    }
    out["wide_counts"] = {
        "contrast_rows": len(wide["contrast_rows"]),
        "contrast_and_date_rows": len(wide["contrast_and_date_rows"]),
        "checked": wide["checked"],
        "flagged": len(wide["flagged"]),
        "unresolved": len(wide["unresolved"]),
    }
    newly_flagged = [x for x in wide["flagged"] if x[0] not in {y[0] for y in base["flagged"]}]
    out["newly_flagged_wide"] = newly_flagged
    newly_checked = [s for s in wide["contrast_and_date_rows"] if s not in base["contrast_and_date_rows"]]
    out["newly_checked_wide"] = newly_checked

    # per-newly-flagged capture evidence
    ev = []
    for sid, miss, nocap in newly_flagged:
        cells = reg[sid]
        tl = cells[6].lower()
        cap = capture_text(ROOT, reg, sid)
        terms = {t: (t in cap.lower()) if cap else None for t in DATE_TERMS}
        phrase_hits = [c for c in WIDE_CONTRAST if c in tl]
        ev.append({"sid": sid, "miss": miss, "capture_missing": nocap,
                   "status": cells[7], "superseded_by": superseded_by.get(sid, []),
                   "wide_phrase_hits": phrase_hits,
                   "teaches": cells[6],
                   "capture_terms": terms,
                   "capture_chars": len(cap) if cap else 0})
    out["newly_flagged_evidence"] = ev

    # capture-presence census for every newly-checked row
    ev2 = []
    for sid in newly_checked:
        cells = reg[sid]
        tl = cells[6].lower()
        cap = capture_text(ROOT, reg, sid)
        named = [t for t in DATE_TERMS if t in tl]
        miss = [t for t in named if cap is None or t not in cap.lower()]
        ev2.append({"sid": sid, "named": named, "miss": miss, "capture_missing": cap is None,
                    "status": cells[7], "superseded_by": superseded_by.get(sid, []),
                    "teaches": cells[6]})
    out["newly_checked_evidence"] = ev2

    # ---- (b) over/under fire measurement across a wider vocabulary ----
    # Under-fire probe: rows whose teaches states a contrast against a date term
    # using any phrase outside CONTRAST, that the counter never checks.
    under = []
    for sid, cells in sorted(reg.items()):
        tl = cells[6].lower()
        named = [t for t in DATE_TERMS if t in tl]
        if not named:
            continue
        if any(c in tl for c in CONTRAST):
            continue
        # crude contrast probe outside the counter's list
        probe = [p for p in ("rather than", "not the same as", "other date properties",
                             "differs from", "different from", "not ", "never ", "cannot",
                             "does not", "must not", "unlike", "as opposed to", "versus",
                             "no ", "without", "confus", "not comparable", "not equivalent")
                 if p in tl]
        if probe:
            cap = capture_text(ROOT, reg, sid)
            miss = [t for t in named if cap is None or t not in cap.lower()]
            under.append({"sid": sid, "probe": probe, "named": named, "miss": miss,
                          "capture_missing": cap is None, "status": cells[7],
                          "superseded_by": superseded_by.get(sid, []), "teaches": cells[6]})
    out["under_fire_candidates"] = under

    # Over-fire probe: rows the counter FLAGS whose capture does contain a
    # morphological variant of the missing term.
    over = []
    for sid, miss, nocap in base["flagged"]:
        cap = capture_text(ROOT, reg, sid)
        variants = {}
        if cap:
            cl = cap.lower()
            for t in miss:
                stem = t[:-1] if t.endswith("d") else t
                variants[t] = [w for w in set(re.findall(r"[a-z]{5,}", cl))
                                if w.startswith(stem[:6])]
        over.append({"sid": sid, "miss": miss, "capture_missing": nocap,
                     "capture_stem_variants": variants,
                     "status": reg[sid][7], "superseded_by": superseded_by.get(sid, []),
                     "teaches": reg[sid][6]})
    out["base_flagged_detail"] = over

    # ---- (c) disposition rule vs chains ----
    disp = []
    for sid, cells in sorted(reg.items()):
        tl = cells[6].lower()
        if not any(c in tl for c in CONTRAST):
            continue
        named = [t for t in DATE_TERMS if t in tl]
        if not named:
            continue
        cap = capture_text(ROOT, reg, sid)
        miss = [t for t in named if cap is None or t not in cap.lower()]
        if not miss:
            continue
        sup = superseded_by.get(sid, [])
        # is the superseder itself superseded?
        sup_meta = []
        for x in sup:
            xcells = reg.get(x)
            sup_meta.append({"superseder": x, "status": xcells[7] if xcells else None,
                             "itself_superseded_by": superseded_by.get(x, []),
                             "teaches_head": xcells[6][:120] if xcells else None})
        disp.append({"sid": sid, "miss": miss, "status": cells[7],
                     "superseded_by": sup, "superseders": sup_meta,
                     "counter_disposition": "superseded" if sid in superseded_by else "UNRESOLVED"})
    out["flagged_dispositions"] = disp

    # ---- (d) id sets ----
    def ids_of(path):
        s = set()
        for ln in open(path, encoding="utf-8", errors="replace"):
            m = re.match(r"^ {0,3}\| (S\d{3,}) \|", ln.rstrip("\n"))
            if m:
                s.add(m.group(1))
        return s

    lane_ids = ids_of(os.path.join(ROOT, "corpus", "SOURCES.md"))
    out["lane_id_count"] = len(lane_ids)
    append_path = "/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md"
    if os.path.isfile(append_path):
        app_ids = ids_of(append_path)
        out["append_exists"] = True
        out["append_id_count"] = len(app_ids)
        out["append_ids"] = sorted(app_ids)
        out["id_collision"] = sorted(lane_ids & app_ids)
        out["collision_count"] = len(lane_ids & app_ids)
        out["append_only"] = sorted(app_ids - lane_ids)
        out["lane_only_count"] = len(lane_ids - app_ids)
    else:
        out["append_exists"] = False

    blob = json.dumps(out, indent=1, ensure_ascii=False)
    if OUT:
        open(OUT, "w", encoding="utf-8").write(blob)
    print(blob)


if __name__ == "__main__":
    main()
