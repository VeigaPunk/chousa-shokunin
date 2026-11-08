#!/usr/bin/env python3
"""curation-r87 — round-87 C2 (calibration) counter. Successor of curation-r86.py.

Closes the two round-86 routed curation defects (`corpus/lessons/round-86-verifier-spotcheck.md` §Routed defects 4-5):

  4. `QUOTES_LOCATED` had no denominator floor and no warrant linkage: deleting the failing quote row scored `19/19`,
     keeping two of twenty scored `2/2`, and re-pointing the repaired row's warrant at a quote that does not carry the
     row's distinction still scored `MODIFIED_DEF_CITED=1` (`R86ReviewerEntry` §2.3 E5b/E5c2, §2.4 E6).
  5. A registry `teaches` cell was never read against its own capture, so a frozen cell could assert a contrast its
     source refuses (QUALITY 178; the `S024` cell vs the `S031` capture).

Legs (every leg appends exactly one record; `passed` requires `len(legs) == EXPECTED_LEGS` and every leg ok, so a
counter edit that deletes a leg changes the verdict — the round-86 M5 shape):

  1 SUPERSEDED  no row that a later row supersedes is `mined` while the superseding row is not (CORPUS rule 2)
  2 UNENTAILED  no decision-table cell of the routed entries carries a frozen defect term that no located quote of
                that entry carries
  3 DEF_CITED   at least one located quote of the routed entries is the S023 `modified` Definition
  4 FLOOR       per entry, the located-quote denominator is at least its frozen floor AND located == total
                (a round-sum floor would pass the `2/2` forgery; per-entry floors do not)
  5 WARRANT     for every decision-table row, each named qid resolves to a located quote of that entry, and at least
                one named qid's quote shares a distinctive content word with the row's Do/Never cells
  6 TEACHES     every registry row whose `teaches` states a contrast against a date-property term reads that term in
                its own capture, unless another row supersedes it (a superseded row's frozen `teaches` is not
                evidence, QUALITY 178). The leg requires the detector to fire at least once (it has a live instance)
                and zero unresolved rows.
  7 SETUP       a missing routed entry or registry prints `CURATION_R87=SETUP` and exits 2

Usage: python3 -B corpus/evidence/round87/curation-r87.py --root DIR
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
STOPWORDS = set(
    "state record recording report describe present specify using used resource content date dates which when where "
    "that this with without from into their them they there these those than then only also have been were will would "
    "must should never always".split()
)
EXPECTED_LEGS = 7


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
        print("CURATION_R87=SETUP missing corpus/SOURCES.md")
        return 2

    legs = []

    # 1. supersession graph: a superseded row must not be the live citation while its superseder is unadopted
    superseded_by = {}
    superseded_live = []
    for sid, cells in reg.items():
        m = re.match(r"supersedes (S\d{3,}) —", cells[6])
        if not m:
            continue
        superseded_by.setdefault(m.group(1), []).append(sid)
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
    warrant_ok = warrant_total = 0
    for rel in ENTRIES:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            print(f"CURATION_R87=SETUP missing {rel}")
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
        entry_quotes[rel] = quotes
        joined = " ".join(quotes.values()).lower()
        for cells in table_rows(section_lines(text, "Decision table"), 4):
            for term in DEFECT_TERMS:
                if term in (cells[1] + " " + cells[2]).lower() and term not in joined:
                    unentailed.append((rel, cells[0], term))
            # warrant linkage
            qids = re.findall(r"Q\d+", cells[3])
            warrant_total += 1
            resolved = [q for q in qids if q in quotes]
            terms = distinctive([cells[1], cells[2]])
            shares = any(terms & set(re.findall(r"[a-z]{5,}", quotes[q].lower())) for q in resolved)
            if qids and len(resolved) == len(qids) and shares:
                warrant_ok += 1
            else:
                warrant_detail.append((rel, cells[0], cells[3], len(resolved), len(qids)))
        floor = FLOORS.get(rel, 1)
        floor_rows.append((rel, located, total, floor))
        floor_detail.append(f"{os.path.basename(rel)}={located}/{total} floor{floor}")

    # 4. one aggregated floor leg: per entry, located >= its frozen floor AND located == total
    floors_ok = all(loc >= fl and loc == tot for _rel, loc, tot, fl in floor_rows)
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
            if sid not in superseded_by:
                teaches_unresolved.append((sid, miss))

    # 6. legs
    legs.append(("SUPERSEDED", not superseded_live,
                 "; ".join(f"{t} mined while {s} supersedes it" for s, t, _ in superseded_live) or "0"))
    legs.append(("UNENTAILED", not unentailed,
                 "; ".join(f"{os.path.basename(r)} {s} term={t}" for r, s, t in unentailed) or "0"))
    legs.append(("DEF_CITED", modified_def_cited >= 1, str(modified_def_cited)))
    legs.append(("WARRANT", warrant_total > 0 and warrant_ok == warrant_total,
                 f"{warrant_ok}/{warrant_total}"))
    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_unresolved,
                 f"checked={teaches_checked} flagged={len(teaches_flagged)} unresolved={len(teaches_unresolved)}"))
    legs.append(("SETUP", True, "registry+entries present"))

    located_all = sum(loc for _rel, loc, _tot, _fl in floor_rows)
    total_all = sum(tot for _rel, _loc, tot, _fl in floor_rows)

    print(f"SUPERSEDED_LIVE={len(superseded_live)} UNENTAILED_TERM={len(unentailed)} "
          f"MODIFIED_DEF_CITED={1 if modified_def_cited else 0} QUOTES_LOCATED={located_all}/{total_all} "
          f"Q_FLOORS={','.join(floor_detail)} "
          f"WARRANT_OK={warrant_ok}/{warrant_total} TEACHES_CHECKED={teaches_checked} "
          f"TEACHES_FLAGGED={len(teaches_flagged)} TEACHES_UNRESOLVED={len(teaches_unresolved)} "
          f"LEGS={sum(1 for _, ok, _ in legs if ok)}/{EXPECTED_LEGS}")
    for sid, miss in teaches_flagged:
        print(f"TEACHES_FLAGGED {sid} terms={','.join(miss)} disposition="
              f"{'superseded by ' + ','.join(superseded_by[sid]) if sid in superseded_by else 'UNRESOLVED'}")
    for rel, sit, war, res, tot in warrant_detail:
        print(f"WARRANT_UNLINKED {rel} row={sit} warrant={war} resolved={res}/{tot}")
    passed = len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs)
    for name, ok, detail in legs:
        if not ok:
            print(f"LEG_FAIL {name} {detail}")
    print(f"CURATION_R87={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
