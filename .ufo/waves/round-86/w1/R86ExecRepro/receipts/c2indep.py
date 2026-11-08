#!/usr/bin/env python3
"""Independent C2 leg: quotes located in the capture of the row's own URL; supersession statuses; defect terms."""
import hashlib
import os
import re
import sys

tree = os.path.join(sys.argv[1], "tree")


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


reg = {}
for ln in open(os.path.join(tree, "corpus", "SOURCES.md"), encoding="utf-8", errors="replace"):
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    if len(cells) == 11 and re.match(r"^S\d{3,}$", cells[0]):
        reg[cells[0]] = cells

def cap(sid):
    urls = re.findall(r"https?://[^\s|)>\]]+", reg[sid][1])
    if not urls:
        return None, None
    key = hashlib.sha256(urls[-1].encode()).hexdigest()[:24]
    p = os.path.join(tree, "corpus", "captures", key + ".txt")
    if not os.path.isfile(p):
        return None, urls[-1]
    return norm(open(p, encoding="utf-8", errors="replace").read()), urls[-1]

entries = ["corpus/knowledge/search-transparency-reporting-r84.md",
           "corpus/knowledge/provenance-recording-r85.md"]
total = located = 0
for rel in entries:
    text = open(os.path.join(tree, rel), encoding="utf-8").read()
    sec = None
    print(f"ENTRY {rel}")
    for ln in text.split("\n"):
        if ln.startswith("## "):
            sec = "located" if ln[3:].strip().lower().startswith("located quotes") else (
                "decision" if ln[3:].strip().lower().startswith("decision table") else None)
            continue
        if sec == "located" and ln.lstrip().startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) != 3 or not re.match(r"Q\d+$", cells[0]):
                continue
            q = cells[2].strip().strip('"')
            if not q:
                continue
            total += 1
            cap_text, url = cap(cells[1])
            ok = cap_text is not None and norm(q) in cap_text
            located += ok
            print(f"  {cells[0]} {cells[1]} located={int(ok)} quote={norm(q)[:80]!r}")
        if sec == "decision" and ln.lstrip().startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) != 4 or cells[0] in ("Situation", "") or set(cells[0]) <= set("-: "):
                continue
            for term in ("modification", "modified"):
                if term in (cells[1] + " " + cells[2]).lower():
                    print(f"  DECISION-TERM {term} row={cells[0]!r} do={cells[1][:70]!r} never={cells[2][:70]!r}")
print(f"INDEP_QUOTES_LOCATED={located}/{total}")

for sid in ("S024", "S031", "S023"):
    print(f"ROW {sid}: status={reg[sid][7]} teaches={reg[sid][6][:110]!r}")
print(f"S023_CAPTURE_HAS_DEF={('date on which the resource was changed' in (cap('S023')[0] or ''))}")

for rel in entries:
    text = open(os.path.join(tree, rel), encoding="utf-8").read()
    sids = sorted(set(re.findall(r"\bS\d{3,}\b", text)))
    print(f"ENTRY_SIDS {rel}: S024={'S024' in sids} S031={'S031' in sids} count={len(sids)}")
