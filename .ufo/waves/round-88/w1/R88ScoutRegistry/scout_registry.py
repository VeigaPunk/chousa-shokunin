#!/usr/bin/env python3
"""R88ScoutRegistry — independent re-derivation of C2's supersession graph, teaches leg,
qid-set pin and token floor, from the committed tree at 4ea9d008. Read-only."""
import hashlib
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")
CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")
STOPWORDS = set(
    "state record recording report describe present specify using used resource content date dates which when where "
    "that this with without from into their them they there these those than then only also have been were will would "
    "must should never always".split()
)
QID_SETS = {
    "corpus/knowledge/search-transparency-reporting-r84.md": ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13"),
    "corpus/knowledge/provenance-recording-r85.md": ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"),
}
MIN_TOKENS = 7


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


reg = parse_registry(ROOT)
print("REGISTRY_ROWS=%d" % len(reg))

# ---------- (a) supersession graph ----------
print("\n=== (a) SUPERSESSION GRAPH: every 'supersedes S0NN —' edge with both statuses ===")
edges = []
for sid in sorted(reg):
    cells = reg[sid]
    m = re.match(r"supersedes (S\d{3,}) —", cells[6])
    if m:
        target = m.group(1)
        tc = reg.get(target)
        edges.append((sid, target, cells[7], (tc[7] if tc else "MISSING-ROW")))
for sid, target, sstat, tstat in edges:
    mined = "MINED" if sstat == "mined" else "NON-MINED"
    print("EDGE %s -> %s | superseder_status=%s (%s) | target_status=%s" % (sid, target, sstat, mined, tstat))
print("EDGES_TOTAL=%d" % len(edges))
nonmined = [(s, t) for s, t, ss, ts in edges if ss != "mined"]
print("EDGES_WITH_NON_MINED_SUPERSEDER=%d -> %s" % (len(nonmined), nonmined))

# superseded-live check (same shape as the counter's SUPERSEDED leg)
sup_live = []
for sid, target, sstat, tstat in edges:
    if tstat == "mined" and sstat != "mined":
        sup_live.append((sid, target, sstat))
print("SUPERSEDED_LIVE=%d %s" % (len(sup_live), sup_live))

# mined superseder map
mined_sup = {}
for sid, target, sstat, _ts in edges:
    if sstat == "mined":
        mined_sup.setdefault(target, []).append(sid)
print("MINED_SUPERSEDER_MAP=%s" % mined_sup)

# ---------- (b) teaches detector, all rows ----------
print("\n=== (b) TEACHES DETECTOR: rows whose teaches carries a contrast phrase AND a date term ===")
flagged = []
checked = 0
for sid in sorted(reg):
    tl = reg[sid][6].lower()
    if not any(c in tl for c in CONTRAST):
        continue
    named = [t for t in DATE_TERMS if t in tl]
    if not named:
        continue
    checked += 1
    cap = capture_text(ROOT, reg, sid)
    miss = [t for t in named if cap is None or t not in cap.lower()]
    if miss:
        flagged.append((sid, named, miss))
print("TEACHES_CHECKED=%d" % checked)
for sid, named, miss in flagged:
    disp = mined_sup.get(sid)
    print("FLAGGED %s named_terms=%s missing_in_own_capture=%s | mined_superseder=%s"
          % (sid, named, miss, disp if disp else "NONE"))
print("FLAGGED_COUNT=%d" % len(flagged))
print("FLAGGED_WITH_MINED_SUPERSEDER=%d"
      % sum(1 for sid, _n, _m in flagged if sid in mined_sup))

# superseder's own read: rows that both supersede and carry contrast+date term
print("\n--- superseding rows that themselves carry a contrast phrase + date term ---")
sup_unres = []
for sid in sorted(reg):
    tl = reg[sid][6].lower()
    if not re.match(r"supersedes (S\d{3,}) —", tl):
        continue
    contrast = [c for c in CONTRAST if c in tl]
    named = [t for t in DATE_TERMS if t in tl]
    if not contrast or not named:
        continue
    cap = capture_text(ROOT, reg, sid)
    miss = [t for t in named if cap is None or t not in cap.lower()]
    reads = {t: (cap is not None and t in cap.lower()) for t in named}
    print("SUPERSEDER %s status=%s contrast=%s terms=%s reads_own_capture=%s missing=%s"
          % (sid, reg[sid][7], contrast, named, reads, miss))
    if miss:
        sup_unres.append((sid, miss))
print("SUPERSEDERS_WITH_CONTRAST_AND_DATE_TERM=%d SUP_UNRESOLVED=%d %s"
      % (len([s for s in reg if re.match(r"supersedes (S\d{3,}) —", reg[s][6].lower())
              and any(c in reg[s][6].lower() for c in CONTRAST)
              and any(t in reg[s][6].lower() for t in DATE_TERMS)]),
         len(sup_unres), sup_unres))

# also: every superseding row, its own teaches terms read status (no contrast filter)
print("\n--- ALL superseding rows: own teaches terms read in own capture ---")
for sid in sorted(reg):
    tl = reg[sid][6].lower()
    m = re.match(r"supersedes (S\d{3,}) —", tl)
    if not m:
        continue
    named = [t for t in DATE_TERMS if t in tl]
    cap = capture_text(ROOT, reg, sid)
    reads = {t: (cap is not None and t in cap.lower()) for t in named}
    print("ALLSUP %s status=%s target=%s terms=%s reads=%s capture_present=%s"
          % (sid, reg[sid][7], m.group(1), named, reads, cap is not None))

# ---------- (c) qid-set pin and token floor ----------
print("\n=== (c) QID-SET PIN + TOKEN FLOOR ===")
ENTRIES = list(QID_SETS)
total_loc = 0
for rel in ENTRIES:
    path = os.path.join(ROOT, rel)
    text = open(path, encoding="utf-8", errors="replace").read()
    qrows = [c for c in table_rows(section_lines(text, "Located quotes"), 3)
             if re.match(r"Q\d+$", c[0])]
    carried = [c[0] for c in qrows]
    pinned = list(QID_SETS[rel])
    located = {}
    for cells in qrows:
        sid, raw = cells[1], cells[2]
        quote = raw.strip().strip('"')
        if not quote:
            continue
        cap = capture_text(ROOT, reg, sid)
        if cap is not None and norm(quote) in cap:
            located[cells[0]] = norm(quote)
    total_loc += len(located)
    tok = {q: len(t.split()) for q, t in located.items()}
    short = {q: n for q, n in tok.items() if n < MIN_TOKENS}
    print("ENTRY %s carried_qids=%d located=%d pinned=%d" % (rel, len(carried), len(located), len(pinned)))
    print("  carried_set=%s" % sorted(set(carried), key=lambda x: int(x[1:])))
    print("  pinned_set =%s" % sorted(set(pinned), key=lambda x: int(x[1:])))
    print("  set_equal=%s missing_from_entry=%s extra_in_entry=%s"
          % (set(carried) == set(pinned),
             sorted(set(pinned) - set(carried)), sorted(set(carried) - set(pinned))))
    print("  token_counts=%s" % tok)
    print("  min_tokens=%d below_floor=%s" % (min(tok.values()) if tok else -1, short))
print("TOTAL_LOCATED=%d" % total_loc)
ALL_LOC = []
for rel in ENTRIES:
    text = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
    for cells in table_rows(section_lines(text, "Located quotes"), 3):
        if not re.match(r"Q\d+$", cells[0]):
            continue
        quote = cells[2].strip().strip('"')
        if not quote:
            continue
        cap = capture_text(ROOT, reg, cells[1])
        if cap is not None and norm(quote) in cap:
            ALL_LOC.append((rel.split("/")[-1], cells[0], len(norm(quote).split()), norm(quote)))
print("LOCATED_QUOTES=%d" % len(ALL_LOC))
mins = sorted(ALL_LOC, key=lambda t: t[2])
print("MIN_TOKEN_QUOTES:")
for r, q, n, t in mins[:5]:
    print("  %s %s tokens=%d %r" % (r, q, n, t))
print("BELOW_FLOOR_ANY=%s" % [(r, q, n) for r, q, n, _ in ALL_LOC if n < MIN_TOKENS])

# ---------- warrant leg independence: per-row qid resolution + term sharing ----------
print("\n--- warrant leg: per-row qid resolution and term sharing (independent re-derivation) ---")
for rel in ENTRIES:
    text = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
    quotes = {}
    for cells in table_rows(section_lines(text, "Located quotes"), 3):
        if not re.match(r"Q\d+$", cells[0]):
            continue
        quote = cells[2].strip().strip('"')
        if not quote:
            continue
        cap = capture_text(ROOT, reg, cells[1])
        if cap is not None and norm(quote) in cap:
            quotes[cells[0]] = norm(quote)
    for cells in table_rows(section_lines(text, "Decision table"), 4):
        qids = re.findall(r"Q\d+", cells[3])
        resolved = [q for q in qids if q in quotes]
        terms = set()
        for c in (cells[1], cells[2]):
            for w in re.findall(r"[a-z]{5,}", c.lower()):
                if w not in STOPWORDS:
                    terms.add(w)
        shared = {q: sorted(terms & set(re.findall(r"[a-z]{5,}", quotes[q].lower()))) for q in resolved}
        ok = bool(qids) and len(resolved) == len(qids) and all(shared[q] for q in resolved)
        print("ROW %s %s warrant=%s resolved=%d/%d ok=%s shared=%s"
              % (rel.split("/")[-1], cells[0], cells[3], len(resolved), len(qids), ok, shared))
