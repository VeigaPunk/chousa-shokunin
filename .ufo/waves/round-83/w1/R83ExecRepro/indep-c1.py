#!/usr/bin/env python3
"""Independent re-check of the C1 depth predicate numbers, written from the claims text only.

Reads the archived tree; does not import or execute depth-r83.py.
"""
import hashlib
import os
import re
import sys

ROUND_START = "2026-11-06T20:53:00Z"
root = os.path.abspath(sys.argv[1])
entry = os.path.join(root, "corpus/knowledge/appraisal-judgment-records-r83.md")
text = open(entry, encoding="utf-8").read()
lines = text.splitlines()


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def sec(name):
    out, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            on = ln[3:].strip().lower() == name
            continue
        if on:
            out.append(ln)
    return out


# --- source line
src = [ln for ln in lines if ln.startswith("source:")][0]
sids = re.findall(r"S\d{3,}", src)
print("source_line:", src.strip())
print("source_sids:", ",".join(sids), "count=", len(sids))

# --- located quotes table
tbl = [ln for ln in sec("located quotes") if ln.strip().startswith("|")]
hdr = [c.strip() for c in tbl[0].strip().strip("|").split("|")]
quotes = []
for r in tbl[2:]:
    cells = [c.strip() for c in r.strip().strip("|").split("|")]
    if len(cells) != 3:
        print("BAD_ROW", r)
        continue
    quotes.append((cells[0], cells[1], cells[2]))
print("declared_quotes:", len(quotes), "header:", hdr)

# --- decision table body rows
dt = [ln for ln in sec("decision table") if ln.strip().startswith("|")]
dtd = [c.strip() for c in dt[0].strip().strip("|").split("|")]
print("decision_header:", dtd)
body = []
for r in dt[2:]:
    cells = [c.strip() for c in r.strip().strip("|").split("|")]
    body.append(cells)
print("decision_body_rows:", len(body), "all_4_cells:", all(len(c) == 4 for c in body))
warrant_idx = [i for i, h in enumerate(dtd) if h.lower() == "warrant"]
print("warrant_column:", warrant_idx)
wi = warrant_idx[0] if warrant_idx else -1
named = set()
for c in body:
    named |= set(re.findall(r"\bQ\d+\b", c[wi]))
declared_q = {q[0] for q in quotes}
print("warrant_named_qids:", len(named), "declared:", len(declared_q),
      "unnamed_declared:", sorted(declared_q - named), "undefined_named:", sorted(named - declared_q))
row_min_words = min((len(c[i].split()) for c in body for i in range(4) if i != wi), default=0)
print("min_non_warrant_cell_words:", row_min_words)

# --- registry + refetch + captures
reg = {}
for ln in open(os.path.join(root, "corpus/SOURCES.md"), encoding="utf-8"):
    m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", ln)
    if not m:
        continue
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    if len(cells) != 11:
        continue
    reg.setdefault(cells[0], cells)

fetch = []
for ln in open(os.path.join(root, "corpus/evidence/round57/refetch.tsv"), encoding="utf-8"):
    f = ln.rstrip("\n").split("\t")
    if len(f) == 9:
        fetch.append(f)

capsha = {}
fresh_ok = 0
for sid in sids:
    row = reg.get(sid)
    if row is None:
        print(f"FRESH {sid} NO_REGISTRY_ROW")
        continue
    m = re.search(r"https?://[^\s|)>\]]+", row[1])
    url = m.group(0) if m else ""
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    cap = os.path.join(root, "corpus/captures", key + ".txt")
    exists = os.path.isfile(cap)
    csha = hashlib.sha256(open(cap, "rb").read()).hexdigest() if exists else None
    capsha[sid] = csha
    rows = [r for r in fetch if r[0] == sid and r[1] == url and r[2] == key]
    fresh_rows = [r for r in rows if r[5] == "0" and re.fullmatch(r"2\d\d", r[6]) and r[4] >= ROUND_START]
    match = [r for r in fresh_rows if csha is not None and r[8] == csha]
    status, usedby = row[7], row[10]
    fresh = bool(match) and status == "mined" and "corpus/knowledge/appraisal-judgment-records-r83.md" in usedby
    fresh_ok += 1 if fresh else 0
    print(f"FRESH {sid} tier={row[3]} status={status} key={key} capture_exists={exists} "
          f"refetch_rows={len(rows)} fresh_rows={len(fresh_rows)} sha_match={len(match)} fresh={fresh}")
print("fresh_sources:", fresh_ok)

# --- quote location, independent normalization
located = 0
for qid, sid, q in quotes:
    if len(q) >= 2 and q.startswith('"') and q.endswith('"'):
        q = q[1:-1]
    n = len(q.split())
    csha = capsha.get(sid)
    cap = None
    if csha is not None:
        row = reg[sid]
        key = hashlib.sha256(re.search(r"https?://[^\s|)>\]]+", row[1]).group(0).encode()).hexdigest()[:24]
        cap = os.path.join(root, "corpus/captures", key + ".txt")
    ok = cap is not None and os.path.isfile(cap) and norm(q) in norm(open(cap, encoding="utf-8", errors="replace").read())
    ok = ok and 8 <= n <= 25
    located += 1 if ok else 0
    if not ok:
        print(f"QUOTE_NOT_LOCATED {qid} {sid} words={n}")
print("declared_quotes_in_range_and_located:", located, "/", len(quotes))
print("distinct_quote_texts:", len({norm(q[2].strip('"')) for q in quotes}))
