#!/usr/bin/env python3
"""curation-r86 — round-86 C2 (calibration) counter, frozen before any scored run.

Checks the lane's registry supersession graph and the warrant cells the round-85 non-author check routed for repair,
over committed bytes only (no network, no writes).

Fields:
  SUPERSEDED_LIVE    rows whose `teaches` opens `supersedes S0NN —` whose target row is still `mined`
                     while the superseding row is not (CORPUS.md rule 2: a correction is a new row, and the
                     correction — not the superseded row — is the live citation)
  UNENTAILED_TERM    decision-table cells in the two routed entries that carry the frozen defect terms
                     ("modification", "modified") while no located quote of that entry carries the term
                     (round-85 routed defect 1: an imported distinction the cited source refuses)
  MODIFIED_DEF_CITED 1 when the round-84 entry carries a located quote of the S023 `modified` Definition
                     ("Date on which the resource was changed."), the definition its row 9 needs and did not cite
  QUOTES_LOCATED     located/total over every qid of the two routed entries, matched verbatim (normalized) in the
                     committed capture of the row's URL

Usage: python3 -B corpus/evidence/round86/curation-r86.py --root DIR
Exit 0 PASS, 1 FAIL, 2 setup (a routed entry or the registry is missing).
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
DEFECT_TERMS = ("modification", "modified")
MODIFIED_DEF = "date on which the resource was changed"


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def parse_registry(root):
    reg = {}
    path = os.path.join(root, "corpus", "SOURCES.md")
    if not os.path.isfile(path):
        raise SystemExit("CURATION_R86=SETUP missing corpus/SOURCES.md")
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
    urls = re.findall(r"https?://[^\s|)>\]]+", cells[1])
    if not urls:
        return None
    url = urls[-1]
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    cap = os.path.join(root, "corpus", "captures", key + ".txt")
    if not os.path.isfile(cap):
        return None
    return norm(open(cap, encoding="utf-8", errors="replace").read())


def section_lines(text, heading):
    """Yield the body lines of the first `## <heading>` section, stopping at the next `## `."""
    inside = False
    for ln in text.split("\n"):
        if ln.startswith("## "):
            if inside:
                break
            inside = ln[3:].strip().lower().startswith(heading.lower())
            continue
        if inside:
            yield ln


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    reg = parse_registry(root)

    # 1. supersession graph: a row a later row supersedes must not be the live citation while the superseding
    #    row is unadopted (queued/rejected) — the round-85 inversion (S024 mined, S031 queued)
    superseded_live = []
    for sid, cells in reg.items():
        teaches = cells[6]
        m = re.match(r"supersedes (S\d{3,}) —", teaches)
        if not m:
            continue
        target = reg.get(m.group(1))
        if target is not None and target[7] == "mined" and cells[7] != "mined":
            superseded_live.append((sid, m.group(1), cells[7]))

    # 2. routed entries: located quotes and wartant terms
    unentailed = []
    quotes_located = quotes_total = 0
    modified_def_cited = 0
    for rel in ENTRIES:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            print(f"CURATION_R86=SETUP missing {rel}")
            return 2
        text = open(path, encoding="utf-8", errors="replace").read()
        entry_located = []
        for ln in section_lines(text, "Located quotes"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")] if ln.lstrip().startswith("|") else []
            if len(cells) != 3 or not re.match(r"Q\d+$", cells[0]):
                continue
            sid, raw_quote = cells[1], cells[2]
            quote = raw_quote.strip().strip('"')
            if not quote:
                continue
            quotes_total += 1
            cap = capture_text(root, reg, sid)
            if cap is not None and norm(quote) in cap:
                quotes_located += 1
                entry_located.append((cells[0], sid, norm(quote)))
        joined = " ".join(q for _, _, q in entry_located).lower()
        for qid, sid, q in entry_located:
            if MODIFIED_DEF in q.lower():
                modified_def_cited += 1
        for ln in section_lines(text, "Decision table"):
            if not ln.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) != 4 or cells[0] in ("Situation", "") or set(cells[0]) <= set("-: "):
                continue
            for term in DEFECT_TERMS:
                if term in (cells[1] + " " + cells[2]).lower() and term not in joined:
                    unentailed.append((rel, cells[0], term))

    pred = (not superseded_live and not unentailed and modified_def_cited >= 1
            and quotes_total > 0 and quotes_located == quotes_total)
    print(f"SUPERSEDED_LIVE={len(superseded_live)} UNENTAILED_TERM={len(unentailed)} "
          f"MODIFIED_DEF_CITED={1 if modified_def_cited else 0} QUOTES_LOCATED={quotes_located}/{quotes_total}")
    for sid, target, status in superseded_live:
        print(f"SUPERSEDED_STILL_LIVE {target} is mined while {sid} supersedes it and is {status}")
    for rel, situation, term in unentailed:
        print(f"UNENTAILED {rel} row={situation} term={term}")
    print(f"CURATION_R86={'PASS' if pred else 'FAIL'}")
    return 0 if pred else 1


if __name__ == "__main__":
    sys.exit(main())
