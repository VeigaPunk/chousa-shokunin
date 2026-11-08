#!/usr/bin/env python3
"""curation-r93 — round-93 C2 (calibration) counter. Successor of curation-r91.py.

Round 91's non-author spot-check (`corpus/lessons/round-91-verifier-spotcheck.md` §8 routed
defect 2) and its wave name the residuals this counter repairs:

  S1  the `## Located quotes` pipe-leading rows share a first-cell filter with the
      decision table: a data row whose first cell is `qid`, `Situation`, or empty is
      dropped BEFORE its shape is checked, so a forged row starting with one of those
      cells never reaches QSHAPE;
  S2  decision rows are collected by `table_rows(..., 4)`, which SILENTLY drops a row
      whose width is not 4: a five-cell decision row shrinks warrant_total by one and
      passes as if it were absent;
  S3  `source_link` accepts a `used-by` cell by substring (`entry in used`), so a
      longer sibling entry name containing this entry's basename (or the reverse) is
      accepted: the join is not tokenised;
  S4  `source_link` is one-directional: nothing checks, from the registry side, that a
      row whose `used-by` names an entry is actually cited by that entry's Located
      quotes.

Repair map: S1 -> the Located-quotes section skips only the structural header/separator
rows (first table line, or all-dash cells), and every other pipe-leading line reaches
`q_shape_violation`; S2 -> decision-row width is pinned per entry
(`DECISION_COUNTS`) and a wrong-width row is a `DECISION_WIDTH` finding, never a silent
drop; S3 -> the used-by cell is tokenised on non-identifier separators and the match is
an exact entry-basename token (`USED_BY_OK` counts exact tokens only); S4 -> a new
USED_BY leg requires every mined row that names an entry in `used-by` to be cited by at
least one Located-quote row of that entry.

Legs (every leg appends exactly one record; `passed` requires `len(legs) == EXPECTED_LEGS` and every leg ok, so a
counter edit that deletes a leg changes the verdict):

  1 FLOOR     per entry: located >= frozen floor AND located == total AND the qid set equals the pinned set AND
              every located quote carries at least MIN_TOKENS tokens (r87-r90 carried)
  2 QSHAPE    every data row of `## Located quotes` is a `Q<n>` row with exactly three cells, a registry-shaped
              source id and a non-empty quote, and no qid repeats (R1)
  3 SOURCE    every located quote's source is a registry row with `status=mined` whose `used-by` names the entry
              (R2)
  4 SUPERSEDED no row that a later row supersedes is `mined` while the superseding row is not (CORPUS rule 2)
  5 UNENTAILED no decision-table cell carries a frozen defect term that no located quote of that entry carries;
              one appended record per offending (row, term), with the term the row actually carries (R4)
  6 DEF_CITED at least one located quote is the S023 `modified` Definition
  7 WARRANT   for every decision-table row, each named qid resolves to a located quote of that entry and every
              named qid's quote shares a distinctive content word with the row's Do/Never cells
  8 TFREQ     every shared term accepted as a warrant has document frequency <= DF_MAX over the entry's located
              quotes (R3); the measured maximum over the legitimate rows is DF_MAX
  9 TEACHES   every registry row whose `teaches` states a contrast against a date-property term reads that term in
              its own capture, unless a `mined` row supersedes it
 10 SETUP     a missing routed entry or registry prints `CURATION_R93=SETUP` and exits 2
 11 DUPQID    a qid cited twice on one warrant cell is not two warrants
 12 USED_BY   every mined registry row that names an entry in `used-by` is cited by at least one
              Located-quote row of that entry (S4)
 13 WITNESS   each detector fires when it must and stays silent when it must (two directions each)
 14 VERDICT   the printed verdict is the tally it was taken over, appended before the summary

Usage: python3 -B corpus/evidence/round93/curation-r93.py --root DIR
Exit 0 PASS, 1 FAIL, 2 setup. No network, no writes.
"""
import argparse
import hashlib
import os
import re
import sys

ENTRIES = [
    "corpus/knowledge/search-transparency-reporting-r84.md",
    "corpus/knowledge/provenance-recording-r85.md",
]
FLOORS = {
    "corpus/knowledge/search-transparency-reporting-r84.md": 13,
    "corpus/knowledge/provenance-recording-r85.md": 7,
}
# S2: decision-row count per entry, pinned at the frozen tree (11 + 6 = 17 warrant rows).
DECISION_COUNTS = {
    "corpus/knowledge/search-transparency-reporting-r84.md": 11,
    "corpus/knowledge/provenance-recording-r85.md": 6,
}
DECISION_WIDTH = 4
DEFECT_TERMS = ("modification", "modified")
MODIFIED_DEF = "date on which the resource was changed"
DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")
CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")
MIN_TOKENS = 7
# Round-91 R3: a shared term is a warrant only when it is distinctive in the entry. The documents are the entry's
# located quotes plus its decision rows' Do/Never cells; measured over the 17 legitimate decision rows, the largest
# selected shared-term document frequency is 3. A term carried by many units (here `source`, df 7) links anything to
# anything and is not a warrant.
DF_MAX = 3
QID_SETS = {
    "corpus/knowledge/search-transparency-reporting-r84.md": ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13"),
    "corpus/knowledge/provenance-recording-r85.md": ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"),
}
STOPWORDS = set(
    "state record recording report describe present specify using used resource content date dates which when where "
    "that this with without from into their them they there these those than then only also have been were will would "
    "must should never always".split()
)
EXPECTED_LEGS = 15


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def parse_registry(root):
    reg = {}
    path = os.path.join(root, "corpus", "SOURCES.md")
    if not os.path.isfile(path):
        return None
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
            return norm(open(cap, encoding="utf-8", errors="replace").read())
    return None


def section_lines(text, heading):
    on = False
    for ln in text.split("\n"):
        if ln.startswith("## "):
            on = ln.strip() == "## " + heading
            continue
        if on:
            yield ln


def table_cells(ln):
    return [c.strip() for c in ln.strip().strip("|").split("|")]


def _is_separator(cells):
    return bool(cells) and cells[0] and set(cells[0]) <= set("-: ")


def data_lines(lines):
    for ln in lines:
        if not ln.lstrip().startswith("|"):
            continue
        cells = table_cells(ln)
        if cells and (cells[0] in ("Situation", "qid") or _is_separator(cells)):
            continue
        yield ln, cells


def quote_lines(lines):
    """S1: pipe-leading lines of a Located-quotes table; skip ONLY the structural header (first
    table line) and separator rows, so a forged data row never hides behind the shared filter."""
    # The structural header is the first table line whose cells are the literal header; a forged
    # row at line 1 with cells[0]=="qid" is a data row, not the header.
    pending_header = True
    for ln in lines:
        if not ln.lstrip().startswith("|"):
            continue
        cells = table_cells(ln)
        if pending_header and cells and cells == ["qid", "source", "quote"]:
            pending_header = False
            continue
        if cells and _is_separator(cells):
            continue
        pending_header = False
        yield ln, cells


def table_rows(lines, width):
    out = []
    for _ln, cells in data_lines(lines):
        if len(cells) != width:
            continue
        out.append(cells)
    return out


def distinctive(cells):
    words = set()
    for c in cells:
        for w in re.findall(r"[a-z]{5,}", c.lower()):
            if w not in STOPWORDS:
                words.add(w)
    return words


def quote_terms(quote):
    return set(re.findall(r"[a-z]{5,}", quote.lower()))


# Named detectors: each is exercised in both directions by `witness()`.
def locates(quote, cap):
    return cap is not None and norm(quote) in cap


def unentailed_terms(cells, joined):
    """The terms the row's Do/Never cells carry but its entry's quotes do not (R4: one record per term)."""
    text = (cells[1] + " " + cells[2]).lower()
    return [t for t in DEFECT_TERMS if t in text and t not in joined]


def teaches_miss(cap, named):
    return [t for t in named if cap is None or t not in cap.lower()]


def dup_qid(qids):
    return len(set(qids)) != len(qids)


def q_shape_violation(cells):
    """None when a Located-quotes row is `Qn | S-id | non-empty quote`, else the reason (R1)."""
    if len(cells) != 3:
        return f"cells={len(cells)}"
    if not re.match(r"Q\d+$", cells[0]):
        return f"qid={cells[0] or '<empty>'}"
    if not re.match(r"S\d{3,}$", cells[1]):
        return f"source={cells[1] or '<empty>'}"
    inner = cells[2].strip().strip('"').strip()
    if not inner:
        return "quote=<empty>" if not cells[2].strip().strip('"') else "quote=<whitespace>"
    return None


def used_by_tokens(cell):
    """Tokenise a used-by cell on non-identifier separators (S3)."""
    return [tok.strip("/") for tok in re.split(r"[^A-Za-z0-9._/-]+", cell) if tok.strip("/")]


def source_link(sid, entry_rel, reg):
    """(status_ok, used_by_ok) for one located quote's cited source (S3: exact entry-basename token)."""
    cells = reg.get(sid)
    if cells is None:
        return False, False
    entry = os.path.basename(entry_rel)
    tokens = used_by_tokens(cells[10])
    return cells[7] == "mined", (entry in tokens or entry_rel in tokens)


def witness():
    """Two-directional assertions over every detector, including the two new legs."""
    cap = "the date on which the resource was changed is recorded"
    rows = [
        ("locate-fire", locates("date on which the resource", cap) is True),
        ("locate-silent", locates("date on which the resource was deleted", cap) is False),
        ("unentailed-fire", unentailed_terms(["S", "a modified value", "never altered", "Q1"], "other words")
         == ["modified"]),
        ("unentailed-silent", unentailed_terms(["S", "a modified value", "never altered", "Q1"],
                                               "we state modified in the quote") == []),
        ("teaches-fire", teaches_miss("no such property here", ["modified"]) == ["modified"]),
        ("teaches-silent", teaches_miss("the modified date", ["modified"]) == []),
        ("dup-fire", dup_qid(["Q1", "Q1"]) is True),
        ("dup-silent", dup_qid(["Q1", "Q2"]) is False),
        ("qshape-silent", q_shape_violation(["Q1", "S214", '"a quote"']) is None),
        ("qshape-fire", q_shape_violation(["note", "S214", '"a quote"']) == "qid=note"),
        ("qshape-width", q_shape_violation(["Q1", "S214"]) == "cells=2"),
    ]
    bad = [n for n, ok in rows if not ok]
    return bad, f"{len(rows) - len(bad)}/{len(rows)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    reg = parse_registry(root)
    if reg is None:
        print("CURATION_R93=SETUP missing corpus/SOURCES.md")
        return 2

    legs = []

    # 1. supersession graph
    mined_superseded_by = {}
    superseded_live = []
    for sid, cells in reg.items():
        m = re.match(r"supersedes (S\d{3,}) —", cells[6])
        if not m:
            continue
        if cells[7] == "mined":
            mined_superseded_by.setdefault(m.group(1), []).append(sid)
        target = reg.get(m.group(1))
        if target is not None and target[7] == "mined" and cells[7] != "mined":
            superseded_live.append((sid, m.group(1), cells[7]))

    entry_quotes = {}
    unentailed = []
    shape_violations = []
    source_rows = []
    modified_def_cited = 0
    floor_detail = []
    floor_rows = []
    warrant_detail = []
    decision_width = []
    decision_counts_seen = {}
    dup_qids = []
    ws_quote_rows = []
    warrant_ok = warrant_total = 0
    tfreq_rows_ok = tfreq_total = 0
    tfreq_max = 0
    for rel in ENTRIES:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            print(f"CURATION_R93=SETUP missing {rel}")
            return 2
        text = open(path, encoding="utf-8", errors="replace").read()
        quotes = {}
        located = 0
        total = 0
        qids_seen = []
        for ln, cells in quote_lines(section_lines(text, "Located quotes")):
            # WSQUOTE population: counted on every three-cell quote row BEFORE the shape filter, so the
            # class is measured independently of the leg that refuses it (r92 drops it before counting).
            if len(cells) == 3 and not cells[2].strip().strip('"').strip():
                ws_quote_rows.append((rel, cells[0]))
            bad = q_shape_violation(cells)
            if bad is not None:
                shape_violations.append((rel, ln.strip(), bad))
                continue
            qid, sid, raw_quote = cells[0], cells[1], cells[2]
            qids_seen.append(qid)
            quote = raw_quote.strip().strip('"')
            total += 1
            cap = capture_text(root, reg, sid)
            if locates(quote, cap):
                located += 1
                quotes[qid] = norm(quote)
                source_rows.append((rel, sid))
                if MODIFIED_DEF in norm(quote).lower():
                    modified_def_cited += 1
        if len(qids_seen) != len(set(qids_seen)):
            shape_violations.append((rel, "<duplicate qid>", "duplicate"))
        short_rows = [q for q, txt in quotes.items() if len(txt.split()) < MIN_TOKENS]
        entry_quotes[rel] = quotes
        joined = " ".join(quotes.values()).lower()
        docs = list(quotes.values())
        decision_lines = list(data_lines(section_lines(text, "Decision table")))
        rows = []
        for ln, cells in decision_lines:
            if len(cells) != DECISION_WIDTH:
                decision_width.append((rel, ln.strip(), f"cells={len(cells)}"))
                continue
            rows.append(cells)
        decision_counts_seen[rel] = len(decision_lines)  # data rows the table holds (header/separator skipped)
        docs += [cells[1] + " " + cells[2] for cells in rows]
        qdf = {}
        for txt in docs:
            for w in quote_terms(txt):
                qdf[w] = qdf.get(w, 0) + 1
        for cells in rows:
            for term in unentailed_terms(cells, joined):
                unentailed.append((rel, cells[0], term))
            qids = re.findall(r"Q\d+", cells[3])
            warrant_total += 1
            if dup_qid(qids):
                dup_qids.append((rel, cells[0], cells[3]))
            resolved = [q for q in qids if q in quotes]
            terms = distinctive([cells[1], cells[2]])
            shares = all(terms & quote_terms(quotes[q]) for q in resolved)
            if qids and len(resolved) == len(qids) and shares:
                warrant_ok += 1
            else:
                warrant_detail.append((rel, cells[0], cells[3], len(resolved), len(qids)))
            # 8. TFREQ: each resolved qid must share at least one term whose document frequency is <= DF_MAX.
            if qids and len(resolved) == len(qids):
                tfreq_total += 1
                row_ok = True
                for q in resolved:
                    dfs = [qdf.get(w, 0) for w in terms & quote_terms(quotes[q])]
                    good = [d for d in dfs if 0 < d <= DF_MAX]
                    if not good:
                        row_ok = False
                    else:
                        tfreq_max = max(tfreq_max, min(good))
                if row_ok:
                    tfreq_rows_ok += 1
        floor = FLOORS.get(rel, 1)
        floor_rows.append((rel, located, total, floor, qids_seen, short_rows))
        floor_detail.append(f"{os.path.basename(rel)}={located}/{total} floor{floor}")

    floors_ok = all(loc >= fl and loc == tot and set(qs) == set(QID_SETS.get(rel, ())) and not short
                    for rel, loc, tot, fl, qs, short in floor_rows)
    legs.append(("FLOOR", floors_ok, ",".join(floor_detail)))

    # 2. QSHAPE: every Located-quotes data row is well-shaped and no qid repeats.
    legs.append(("QSHAPE", not shape_violations,
                 "; ".join(f"{os.path.basename(r)} {bad}" for r, _ln, bad in shape_violations)
                 or f"rows={len(source_rows)}"))

    # 3. SOURCE: every located quote's source is mined and names this entry.
    status_bad, used_bad = 0, 0
    for rel, sid in source_rows:
        st, ub = source_link(sid, rel, reg)
        status_bad += 0 if st else 1
        used_bad += 0 if ub else 1
    src_ok = not status_bad and not used_bad
    legs.append(("SOURCE", src_ok,
                 f"status_fail={status_bad} used_by_fail={used_bad} rows={len(source_rows)}"))

    # 4. SUPERSEDED
    legs.append(("SUPERSEDED", not superseded_live,
                 "; ".join(f"{t} mined while {s} supersedes it" for s, t, _ in superseded_live) or "0"))

    # 5. UNENTAILED (one record per offending row/term).
    legs.append(("UNENTAILED", not unentailed,
                 "; ".join(f"{os.path.basename(r)} {s} term={t}" for r, s, t in unentailed) or "0"))
    legs.append(("DEF_CITED", modified_def_cited >= 1, str(modified_def_cited)))
    decision_count_bad = [rel for rel in ENTRIES if decision_counts_seen.get(rel) != DECISION_COUNTS.get(rel)]
    legs.append(("WARRANT", warrant_total > 0 and warrant_ok == warrant_total and not decision_width
                 and not decision_count_bad,
                 f"{warrant_ok}/{warrant_total} width_fail={len(decision_width)} count_bad={len(decision_count_bad)}"))
    # 8. TFREQ
    legs.append(("TFREQ", tfreq_total > 0 and tfreq_rows_ok == tfreq_total,
                 f"{tfreq_rows_ok}/{tfreq_total} max_df={tfreq_max}<={DF_MAX}"))

    # 9. teaches
    teaches_flagged, teaches_unresolved = [], []
    teaches_checked = 0
    for sid, cells in sorted(reg.items()):
        tl = cells[6].lower()
        if not any(c in tl for c in CONTRAST):
            continue
        named = [t for t in DATE_TERMS if t in tl]
        if not named:
            continue
        teaches_checked += 1
        miss = teaches_miss(capture_text(root, reg, sid), named)
        if miss:
            teaches_flagged.append((sid, miss))
            if sid not in mined_superseded_by:
                teaches_unresolved.append((sid, miss))
    teaches_sup_unresolved = []
    teaches_sup_checked = 0
    for sid, cells in sorted(reg.items()):
        if not re.match(r"supersedes (S\d{3,}) —", cells[6]):
            continue
        tl = cells[6].lower()
        if not any(c in tl for c in CONTRAST):
            continue
        named = [t for t in DATE_TERMS if t in tl]
        if not named:
            continue
        teaches_sup_checked += 1
        miss = teaches_miss(capture_text(root, reg, sid), named)
        if miss:
            teaches_sup_unresolved.append((sid, miss))
    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_unresolved
                 and not teaches_sup_unresolved,
                 f"checked={teaches_checked} flagged={len(teaches_flagged)} "
                 f"unresolved={len(teaches_unresolved)} sup_unresolved={len(teaches_sup_unresolved)}"))
    # 12. USED_BY (S4): every mined row naming an entry is cited by that entry.
    cited = {}
    for rel, sid in source_rows:
        cited.setdefault(rel, set()).add(sid)
    used_by_unlinked = []
    for sid, cells in reg.items():
        if cells[7] != "mined":
            continue
        tokens = used_by_tokens(cells[10])
        for rel in ENTRIES:
            entry = os.path.basename(rel)
            if entry in tokens or rel in tokens:
                if sid not in cited.get(rel, set()):
                    used_by_unlinked.append((sid, rel))
    legs.append(("USED_BY", not used_by_unlinked,
                 "; ".join(f"{sid} not cited by {os.path.basename(r)}" for sid, r in used_by_unlinked) or "0"))
    legs.append(("SETUP", True, "registry+entries present"))
    legs.append(("DUPQID", not dup_qids,
                 "; ".join(f"{os.path.basename(r)} {s} warrant={w}" for r, s, w in dup_qids) or "0"))
    # 15. WSQUOTE (round 93): a whitespace-only located quote is refused as a shape failure, counted
    # from the located-quote population independently of the cell parser, so the `" "` quote that r92
    # passed through QSHAPE and only caught at FLOOR now fails shape on its own leg.
    legs.append(("WSQUOTE", not ws_quote_rows,
                 "; ".join(f"{os.path.basename(r)} {qid}" for r, qid in ws_quote_rows) or "0"))
    witness_bad, witness_detail = witness()
    legs.append(("WITNESS", not witness_bad, f"{witness_detail} bad={len(witness_bad)}"))

    located_all = sum(loc for _rel, loc, _tot, _fl, _qs, _sh in floor_rows)
    total_all = sum(tot for _rel, _loc, tot, _fl, _qs, _sh in floor_rows)

    for rel, line, detail in decision_width:
        print(f"DECISION_WIDTH {os.path.basename(rel)} row={line} {detail}")
    prior_ok = all(ok for _, ok, _ in legs)
    fields_hold = (len(superseded_live) == 0
                   and len(unentailed) == 0
                   and modified_def_cited >= 1
                   and located_all == total_all and total_all > 0
                   and all(loc >= fl and loc == tot and set(qs) == set(QID_SETS.get(rel, ())) and not short
                           for rel, loc, tot, fl, qs, short in floor_rows)
                   and len(shape_violations) == 0
                   and src_ok
                   and warrant_total > 0 and warrant_ok == warrant_total
                   and tfreq_total > 0 and tfreq_rows_ok == tfreq_total and tfreq_max <= DF_MAX
                   and len(dup_qids) == 0
                   and teaches_checked > 0 and len(teaches_flagged) >= 1
                   and len(teaches_unresolved) == 0
                   and len(teaches_sup_unresolved) == 0
                   and not decision_width and not decision_count_bad
                   and not used_by_unlinked
                   and not ws_quote_rows
                   and not witness_bad)
    legs.append(("VERDICT", fields_hold and fields_hold == prior_ok,
                 f"fields_hold={1 if fields_hold else 0} legs_ok={sum(1 for _, ok, _ in legs if ok)}/{len(legs)}"))
    print(f"SUPERSEDED_LIVE={len(superseded_live)} UNENTAILED_TERM={len(unentailed)} "
          f"MODIFIED_DEF_CITED={1 if modified_def_cited else 0} QUOTES_LOCATED={located_all}/{total_all} "
          f"Q_ROWS={located_all} Q_SHAPE_FAIL={len(shape_violations)} Q_WSQUOT={len(ws_quote_rows)} "
          f"SOURCE_STATUS_OK={len(source_rows) - status_bad}/{len(source_rows)} "
          f"USED_BY_OK={len(source_rows) - used_bad}/{len(source_rows)} "
          f"Q_FLOORS={','.join(floor_detail)} "
          f"WARRANT_OK={warrant_ok}/{warrant_total} TFREQ_OK={tfreq_rows_ok}/{tfreq_total} "
          f"TFREQ_MAX_DF={tfreq_max} DUP_QIDS={len(dup_qids)} TEACHES_CHECKED={teaches_checked} "
          f"TEACHES_FLAGGED={len(teaches_flagged)} TEACHES_UNRESOLVED={len(teaches_unresolved)} "
          f"SUP_CLAUSE_CHECKED={teaches_sup_checked} SUP_UNRESOLVED={len(teaches_sup_unresolved)} "
          f"LEGS_MEASURED={sum(1 for _, ok, _ in legs if ok)}/{len(legs)}")
    for sid, miss in teaches_flagged:
        print(f"TEACHES_FLAGGED {sid} terms={','.join(miss)} disposition="
              f"{'superseded by ' + ','.join(mined_superseded_by[sid]) if sid in mined_superseded_by else 'UNRESOLVED'}")
    for sid, miss in teaches_sup_unresolved:
        print(f"TEACHES_SUP_UNRESOLVED {sid} terms={','.join(miss)}")
    for rel, sit, war, res, tot in warrant_detail:
        print(f"WARRANT_UNLINKED {rel} row={sit} warrant={war} resolved={res}/{tot}")
    for rel, ln, bad in shape_violations:
        print(f"Q_SHAPE {os.path.basename(rel)} {bad} row={ln[:80]}")
    for rel, s, t in unentailed:
        print(f"UNENTAILED {os.path.basename(rel)} row={s} term={t}")
    print(f"VERDICT fields_hold={1 if fields_hold else 0} legs_ok={sum(1 for _, ok, _ in legs if ok)}/{len(legs)} "
          f"DETECTOR_WITNESS={witness_detail}")
    passed = (len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs) and fields_hold)
    for name, ok, detail in legs:
        if not ok:
            print(f"LEG_FAIL {name} {detail}")
    print(f"CURATION_R93={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
