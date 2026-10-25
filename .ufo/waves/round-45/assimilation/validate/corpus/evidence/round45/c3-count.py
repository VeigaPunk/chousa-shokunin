#!/usr/bin/env python3
"""c3-count — frozen counter for round 45 claim C3 (depth, sourced).

Predicate R45-C3, the same sentence as corpus/evidence/round45/claims.md:
the two adopted entries corpus/knowledge/evidence-archive-field-policy-r41.md
and corpus/knowledge/evidence-snapshot-coverage-r40.md exist; their three
`source:` lines bind lane ids S082, S083 and S084 to the AVeriTeC README,
the AVeriTeC v3 HTML paper and the AVeriTeC train.json URLs, each such
Registry row carrying that URL, status `mined` and the citing entry in
used-by; the four located quotes in corpus/evidence/round45/spans.tsv each
sit in their lane-committed span file and in the citing entry, and each span
sits at its recorded offset in the capture named sha256(url)[:24].txt whose
sha256 is the recorded one; the seven counts in
corpus/evidence/round45/counts.json each appear in the snapshot entry and are
re-derived from the train.json capture with the recorded sha256.

`--lane-only` reads lane bytes only (round-44 closure D1): the capture-bound
counts print `skipped` and are not required.

Cheapest gate that would score full marks without the work (QUALITY 60):
entries plus a self-consistent span manifest with invented quotes. Lane-only
mode cannot see that forge; the default mode refuses it, because a span must
sit at its offset inside the capture the row URL names. Committed control:
controls/c3-control-forged-span.txt.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
FIELD = "corpus/knowledge/evidence-archive-field-policy-r41.md"
SNAP = "corpus/knowledge/evidence-snapshot-coverage-r40.md"
README = "https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md"
PAPER = "https://arxiv.org/html/2305.13117v3"
TRAIN = "https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json"
BINDINGS = [(FIELD, "S082", README), (FIELD, "S083", PAPER), (SNAP, "S084", TRAIN)]
N_QUOTES = 4
COUNT_KEYS = ["records", "evidence_with_field", "evidence_nonempty", "evidence_empty",
              "claims_with_field", "claims_nonempty", "claims_empty"]


def row_for(sources: pathlib.Path, sid: str) -> list[str]:
    if not sources.is_file():
        return []
    inside = False
    for line in sources.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Registry"
            continue
        if inside and re.match(r"^ {0,3}\|\s*" + sid + r"\s*\|", line):
            return [c.strip() for c in line.strip().strip("|").split("|")]
    return []


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fmt_variants(n: int) -> list[str]:
    return [f"{n:,}", str(n)]


def rederive(train: pathlib.Path) -> dict:
    d = json.loads(train.read_text(encoding="utf-8"))
    ev = [a for r in d for q in r.get("questions", []) for a in q.get("answers", [])
          if "cached_source_url" in a]
    cl = [r for r in d if "cached_original_claim_url" in r]
    return {
        "records": len(d),
        "evidence_with_field": len(ev),
        "evidence_nonempty": sum(1 for a in ev if a["cached_source_url"]),
        "evidence_empty": sum(1 for a in ev if not a["cached_source_url"]),
        "claims_with_field": len(cl),
        "claims_nonempty": sum(1 for r in cl if r["cached_original_claim_url"]),
        "claims_empty": sum(1 for r in cl if not r["cached_original_claim_url"]),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--cache", default=str(CACHE))
    ap.add_argument("--lane-only", action="store_true")
    a = ap.parse_args()
    root, cache = pathlib.Path(a.root), pathlib.Path(a.cache)
    ev = root / "corpus" / "evidence" / "round45"
    sources = root / "corpus" / "SOURCES.md"

    texts = {p: (root / p).read_text(encoding="utf-8") for p in (FIELD, SNAP) if (root / p).is_file()}
    entries = len(texts)

    bound = 0
    for path, sid, url in BINDINGS:
        t = texts.get(path, "")
        cites = re.search(r"^source:\s*" + sid + r"\s+—\s+" + re.escape(url) + r"(\s|$)", t, re.M)
        row = row_for(sources, sid)
        ok_row = (len(row) == 11 and url in row[1] and row[7] == "mined" and path in row[10])
        bound += bool(cites and ok_row)

    in_span = in_entry = cap_bound = 0
    rows = []
    manifest = ev / "spans.tsv"
    if manifest.is_file():
        lines = manifest.read_text(encoding="utf-8").splitlines()
        rows = [l.split("\t") for l in lines[1:] if l.strip()]
    for r in rows:
        if len(r) != 7:
            continue
        sid, url, cap_sha, offset, span_file, quote, entry = r
        span_path = ev / span_file
        span = span_path.read_text(encoding="utf-8") if span_path.is_file() else ""
        in_span += bool(quote and quote in span)
        in_entry += bool(quote and quote in texts.get(entry, ""))
        if not a.lane_only:
            cap = cache / f"{key(url)}.txt"
            if cap.is_file() and sha(cap) == cap_sha and span:
                ct = cap.read_text(encoding="utf-8")
                o = int(offset)
                cap_bound += ct[o:o + len(span)] == span

    counts_in = counts_re = 0
    cj = ev / "counts.json"
    counts = json.loads(cj.read_text(encoding="utf-8")) if cj.is_file() else {}
    vals = counts.get("counts", {})
    snap = texts.get(SNAP, "")
    for k in COUNT_KEYS:
        if k in vals and any(re.search(r"(?<![\d,])" + re.escape(v) + r"(?![\d,])", snap)
                             for v in fmt_variants(int(vals[k]))):
            counts_in += 1
    if not a.lane_only and vals:
        train = cache / f"{key(TRAIN)}.txt"
        if train.is_file() and counts.get("url") == TRAIN and sha(train) == counts.get("capture_sha256"):
            got = rederive(train)
            counts_re = sum(1 for k in COUNT_KEYS if k in vals and got.get(k) == int(vals[k]))

    nq = len(rows)
    print(f"ENTRIES={entries}/2")
    print(f"CITES_BOUND={bound}/{len(BINDINGS)}")
    print(f"QUOTES_IN_SPAN={in_span}/{N_QUOTES}")
    print(f"QUOTES_IN_ENTRY={in_entry}/{N_QUOTES}")
    print(f"COUNTS_IN_ENTRY={counts_in}/{len(COUNT_KEYS)}")
    if a.lane_only:
        print("CAPTURE_BOUND=skipped")
        print("COUNTS_REDERIVED=skipped")
        ok = (entries == 2 and bound == len(BINDINGS) and nq == N_QUOTES and in_span == N_QUOTES
              and in_entry == N_QUOTES and counts_in == len(COUNT_KEYS))
    else:
        print(f"CAPTURE_BOUND={cap_bound}/{N_QUOTES}")
        print(f"COUNTS_REDERIVED={counts_re}/{len(COUNT_KEYS)}")
        ok = (entries == 2 and bound == len(BINDINGS) and nq == N_QUOTES and in_span == N_QUOTES
              and in_entry == N_QUOTES and cap_bound == N_QUOTES and counts_in == len(COUNT_KEYS)
              and counts_re == len(COUNT_KEYS))
    print("C3=PASS" if ok else "C3=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
