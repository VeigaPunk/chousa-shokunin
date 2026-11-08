#!/usr/bin/env python3
"""curation-r89 — round-89 C2 (calibration) counter. Successor of curation-r87.py.

Closes the four round-87 routed curation defects (`corpus/lessons/round-87-verifier-spotcheck.md` §Amendments 1, 2, 3, 6
and `plans/round-87.md` routed-to-round-88 items):

  A1. Warrant sharing was per row (`any`): a padding qid whose quote shares nothing with the row passed beside a good
      one (`R87ReviewerC2` F1; B1b). The leg now requires every named qid to share a term with the row's cells.
  A2. Floors counted rows only: a substituted table whose count is restored by a verbatim one-word quote passed
      (A1c), and so did a truncated quote (A1d). The FLOOR leg now also requires a per-row token floor (measured
      minimum over the located base quotes) and per-entry qid-set pinning (caseG).
  A3. The TEACHES disposition was structural: a `rejected` superseder disposed a flagged row (`R87ReviewerC2` F2).
      A superseder now disposes only when its `status` is `mined`.
  A6. An uncited quote row was invisible to the warrant leg, so deleting `Q10` and re-labelling a duplicate of `Q13`
      as `Q14` restored the floor with no new evidence (caseG). The FLOOR leg now pins the per-entry qid set.

Legs (every leg appends exactly one record; `passed` requires `len(legs) == EXPECTED_LEGS` and every leg ok, so a
counter edit that deletes a leg changes the verdict — the round-86 M5 shape):

  1 SUPERSEDED  no row that a later row supersedes is `mined` while the superseding row is not (CORPUS rule 2)
  2 UNENTAILED  no decision-table cell of the routed entries carries a frozen defect term that no located quote of
                that entry carries
  3 DEF_CITED   at least one located quote of the routed entries is the S023 `modified` Definition
  4 FLOOR       per entry: the located-quote count is at least its frozen floor AND located == total AND equals the
                pinned qid set AND every located quote row carries at least MIN_TOKENS tokens (a round-sum floor
                would pass the `2/2` forgery; per-entry floors do not)
  5 WARRANT     for every decision-table row, each named qid resolves to a located quote of that entry, and every
                named qid's quote shares a distinctive content word with the row's Do/Never cells
  6 TEACHES     every registry row whose `teaches` states a contrast against a date-property term reads that term in
                its own capture, unless a `mined` row supersedes it (a superseded row's frozen `teaches` is not
                evidence, QUALITY 178; a non-mined superseder does not dispose). The leg requires the detector to fire
                at least once (it has a live instance) and zero unresolved rows.
  7 SETUP       a missing routed entry or registry prints `CURATION_R89=SETUP` and exits 2

Usage: python3 -B corpus/evidence/round88/curation-r89.py --root DIR
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
DEFECT_TERMS = ("modification", "modified")
MODIFIED_DEF = "date on which the resource was changed"
DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")
CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")
# Amendment 2 remedy: a per-row token floor. Measured base minimum over the 20 located quotes is 7
# (`Q13` "Date on which the resource was changed." in search-transparency-reporting-r84.md), so 7 is the measured
# minimum, not a round-number choice. A 1-word A1c/A1d substitution fails it.
MIN_TOKENS = 7
# Amendment 6 remedy: the per-entry qid set is pinned. caseG deleted the uncited `Q10` and re-labelled a duplicate
# of `Q13` as `Q14`; the count was restored without adding evidence because the floor counted rows. The set must
# equal this committed list, so a relabelled duplicate changes it. Measured on the landing tree.
QID_SETS = {
    "corpus/knowledge/search-transparency-reporting-r84.md": ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13"),
    "corpus/knowledge/provenance-recording-r85.md": ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"),
}
STOPWORDS = set(
    "state record recording report describe present specify using used resource content date dates which when where "
    "that this with without from into their them they there these those than then only also have been were will would "
    "must should never always".split()
)
EXPECTED_LEGS = 9


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


def table_rows(lines, width):
    out = []
    for ln in lines:
        if not ln.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != width:
            continue
        if cells[0] in ("Situation", "") or set(cells[0]) <= set("-: "):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    reg = parse_registry(root)
    if reg is None:
        print("CURATION_R89=SETUP missing corpus/SOURCES.md")
        return 2

    legs = []

    # 1. supersession graph: a superseded row must not be the live citation while its superseder is unadopted
    #    (CORPUS rule 2). Amendment 3: a superseding row disposes a flagged row only when its `status` is `mined`.
    superseded_by = {}          # target -> [superseding sids]
    mined_superseded_by = {}    # target -> [mined sup. sids] (the disposal set)
    superseded_live = []
    for sid, cells in reg.items():
        m = re.match(r"supersedes (S\d{3,}) —", cells[6])
        if not m:
            continue
        superseded_by.setdefault(m.group(1), []).append(sid)
        if cells[7] == "mined":
            mined_superseded_by.setdefault(m.group(1), []).append(sid)
        target = reg.get(m.group(1))
        if target is not None and target[7] == "mined" and cells[7] != "mined":
            superseded_live.append((sid, m.group(1), cells[7]))

    # per-entry quote tables and decision rows
    entry_quotes = {}
    unentailed = []
    modified_def_cited = 0
    floor_detail = []
    floor_rows = []
    warrant_detail = []
    dup_qids = []
    warrant_ok = warrant_total = 0
    for rel in ENTRIES:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            print(f"CURATION_R89=SETUP missing {rel}")
            return 2
        text = open(path, encoding="utf-8", errors="replace").read()
        quotes = {}
        located = 0
        total = 0
        for cells in table_rows(section_lines(text, "Located quotes"), 3):
            if not re.match(r"Q\d+$", cells[0]):
                continue
            sid, raw_quote = cells[1], cells[2]
            quote = raw_quote.strip().strip('"')
            if not quote:
                continue
            total += 1
            cap = capture_text(root, reg, sid)
            if cap is not None and norm(quote) in cap:
                located += 1
                quotes[cells[0]] = norm(quote)
                if MODIFIED_DEF in norm(quote).lower():
                    modified_def_cited += 1
        short_rows = [q for q, txt in quotes.items() if len(txt.split()) < MIN_TOKENS]
        qids_seen = [cells[0] for cells in table_rows(section_lines(text, "Located quotes"), 3) if re.match(r"Q\d+$", cells[0])]
        entry_quotes[rel] = quotes
        joined = " ".join(quotes.values()).lower()
        for cells in table_rows(section_lines(text, "Decision table"), 4):
            for term in DEFECT_TERMS:
                if term in (cells[1] + " " + cells[2]).lower() and term not in joined:
                    unentailed.append((rel, cells[0], term))
            # warrant linkage
            qids = re.findall(r"Q\d+", cells[3])
            warrant_total += 1
            # Round-89 repair: a warrant cell that cites the same qid twice is a duplicate citation, not a
            # second warrant. The round-88 counter accepted `Q1, Q1 (S215)` (R88ExecC2Forge finding 3).
            if len(set(qids)) != len(qids):
                dup_qids.append((rel, cells[0], cells[3]))
            resolved = [q for q in qids if q in quotes]
            terms = distinctive([cells[1], cells[2]])
            shares = all(terms & set(re.findall(r"[a-z]{5,}", quotes[q].lower())) for q in resolved)
            if qids and len(resolved) == len(qids) and shares:
                warrant_ok += 1
            else:
                warrant_detail.append((rel, cells[0], cells[3], len(resolved), len(qids)))
        floor = FLOORS.get(rel, 1)
        floor_rows.append((rel, located, total, floor, qids_seen, short_rows))
        floor_detail.append(f"{os.path.basename(rel)}={located}/{total} floor{floor}")

    # 4. one aggregated floor leg: per entry, located >= its frozen floor AND located == total AND the qid set
    #    equals the pinned set AND every located quote row carries at least MIN_TOKENS tokens (Amendments 2 and 6).
    floors_ok = all(loc >= fl and loc == tot and set(qs) == set(QID_SETS.get(rel, ())) and not short
                    for rel, loc, tot, fl, qs, short in floor_rows)

    legs.append(("FLOOR", floors_ok, ",".join(floor_detail)))

    # 5. teaches: contrast against a date term must be readable in the row's own capture unless superseded
    teaches_flagged = []
    teaches_unresolved = []
    teaches_checked = 0
    for sid, cells in sorted(reg.items()):
        tl = cells[6].lower()
        if not any(c in tl for c in CONTRAST):
            continue
        named = [t for t in DATE_TERMS if t in tl]
        if not named:
            continue
        teaches_checked += 1
        cap = capture_text(root, reg, sid)
        miss = [t for t in named if cap is None or t not in cap.lower()]
        if miss:
            teaches_flagged.append((sid, miss))
            if sid not in mined_superseded_by:
                teaches_unresolved.append((sid, miss))
    # Amendment 3: the superseding row's own teaches must read in its own capture (same contrast+term rule).
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
        cap = capture_text(root, reg, sid)
        miss = [t for t in named if cap is None or t not in cap.lower()]
        if miss:
            teaches_sup_unresolved.append((sid, miss))

    # 6. legs
    legs.append(("SUPERSEDED", not superseded_live,
                 "; ".join(f"{t} mined while {s} supersedes it" for s, t, _ in superseded_live) or "0"))
    legs.append(("UNENTAILED", not unentailed,
                 "; ".join(f"{os.path.basename(r)} {s} term={t}" for r, s, t in unentailed) or "0"))
    legs.append(("DEF_CITED", modified_def_cited >= 1, str(modified_def_cited)))
    legs.append(("WARRANT", warrant_total > 0 and warrant_ok == warrant_total,
                 f"{warrant_ok}/{warrant_total}"))
    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_unresolved and not teaches_sup_unresolved,
                 f"checked={teaches_checked} flagged={len(teaches_flagged)} unresolved={len(teaches_unresolved)} sup_unresolved={len(teaches_sup_unresolved)}"))
    legs.append(("SETUP", True, "registry+entries present"))
    # Round-89 repair (R88ExecC2Forge finding 3): a qid cited twice on one warrant cell is not two warrants.
    legs.append(("DUPQID", not dup_qids,
                 "; ".join(f"{os.path.basename(r)} {s} warrant={w}" for r, s, w in dup_qids) or "0"))

    located_all = sum(loc for _rel, loc, _tot, _fl, _qs, _sh in floor_rows)
    total_all = sum(tot for _rel, _loc, tot, _fl, _qs, _sh in floor_rows)

    print(f"SUPERSEDED_LIVE={len(superseded_live)} UNENTAILED_TERM={len(unentailed)} "
          f"MODIFIED_DEF_CITED={1 if modified_def_cited else 0} QUOTES_LOCATED={located_all}/{total_all} "
          f"Q_FLOORS={','.join(floor_detail)} "
          f"WARRANT_OK={warrant_ok}/{warrant_total} DUP_QIDS={len(dup_qids)} TEACHES_CHECKED={teaches_checked} "
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
    # Round-89 repair (R88CriticClaims C2 firing): the verdict is derived from the printed fields, not from a
    # separate `all(ok)`. A dead detector prints TEACHES_FLAGGED=0 and a detached leg prints
    # TEACHES_UNRESOLVED=1; either way the fields refuse PASS even if a leg's `ok` was detached from its
    # measurement. `fields_hold` is computed from the same values the summary line printed.
    fields_hold = (len(superseded_live) == 0
                   and len(unentailed) == 0
                   and modified_def_cited >= 1
                   and located_all == total_all and total_all > 0
                   and all(loc >= fl and loc == tot and set(qs) == set(QID_SETS.get(rel, ())) and not short
                           for rel, loc, tot, fl, qs, short in floor_rows)
                   and warrant_total > 0 and warrant_ok == warrant_total
                   and len(dup_qids) == 0
                   and teaches_checked > 0 and len(teaches_flagged) >= 1
                   and len(teaches_unresolved) == 0
                   and len(teaches_sup_unresolved) == 0)
    legs.append(("VERDICT", fields_hold == all(ok for _, ok, _ in legs) and fields_hold,
                 f"fields_hold={1 if fields_hold else 0} legs_ok={sum(1 for _, ok, _ in legs if ok)}/{len(legs)}"))
    passed = (len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs) and fields_hold)
    for name, ok, detail in legs:
        if not ok:
            print(f"LEG_FAIL {name} {detail}")
    print(f"CURATION_R89={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
