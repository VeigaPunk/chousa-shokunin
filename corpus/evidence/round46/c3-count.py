#!/usr/bin/env python3
"""c3-count — frozen counter for round 46 claim C3 (depth, sourced).

Predicate R46-C3, the same sentence as corpus/evidence/round46/claims.md:
the two adopted entries
`corpus/knowledge/evidence-pool-versioning-r39.md` and
`corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md` exist;
their five `source:` lines bind lane ids S085, S086, S087, S088 and S089 to
the FEVER dataset page, the FEVER ACL paper, the FEVER Zenodo record, the
AVeriTeC dataset page and the AVerImaTeC arXiv HTML, each such Registry row
carrying that URL, status `mined` and the citing entry in `used-by`; the
eleven rows of `corpus/evidence/round46/spans.tsv` each have their quote in
their committed span file and in the citing entry, and each span file is the
exact slice of the capture named sha256(url)[:24].txt at the recorded offset
whose sha256 is the recorded one; every `S###` token in either entry is a
source id of that entry or one of the lane's held rows (S079, S080, S081,
S082, S083, S084), and the two cross-references bind by document — the
sentence naming S079 names RFC 7089, the sentence naming S081 names WARP.

`--lane-only` reads lane bytes only (the round-44 closure D1 lesson):
`CAPTURE_BOUND` prints `skipped` and is not required.

Cheapest gate that would score full marks without the work (QUALITY 60):
entries plus a self-consistent span manifest with invented quotes. Lane-only
mode cannot see that forge; the default mode refuses it, because a span file
must be a slice of the capture at its recorded offset.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
BASE = "corpus/knowledge/evidence-pool-versioning-r39.md"
AMEND = "corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md"
FEVER = "https://fever.ai/dataset/fever.html"
ACL = "https://aclanthology.org/N18-1074.pdf"
ZENODO = "https://zenodo.org/api/records/4925954"
AVERITEC = "https://fever.ai/dataset/averitec.html"
AVERIMATEC = "https://arxiv.org/html/2505.17978v2"
BINDINGS = [(BASE, "S085", FEVER), (BASE, "S086", ACL), (BASE, "S087", ZENODO),
            (AMEND, "S088", AVERITEC), (AMEND, "S089", AVERIMATEC)]
N_QUOTES = 11
ALLOWED_IDS = {"S079", "S080", "S081", "S082", "S083", "S084",
               "S085", "S086", "S087", "S088", "S089"}
CROSS_REFS = {"S079": "RFC 7089", "S081": "WARP"}
ID_RE = re.compile(r"\bS\d{3,}\b")


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


def integral_offset(v: str) -> bool:
    """A recorded offset is a non-negative integer index into the capture."""
    try:
        return int(v) >= 0
    except ValueError:
        return False


def sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?])\s+", text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--cache", default=str(CACHE))
    ap.add_argument("--lane-only", action="store_true")
    a = ap.parse_args()
    root, cache = pathlib.Path(a.root), pathlib.Path(a.cache)
    ev = root / "corpus" / "evidence" / "round46"
    sources = root / "corpus" / "SOURCES.md"

    texts = {p: (root / p).read_text(encoding="utf-8")
             for p in (BASE, AMEND) if (root / p).is_file()}
    entries = len(texts)

    bound = 0
    for path, sid, url in BINDINGS:
        t = texts.get(path, "")
        cites = re.search(r"^source:\s*" + sid + r"\s+—\s+" + re.escape(url) + r"(\s|$)", t, re.M)
        row = row_for(sources, sid)
        ok_row = (len(row) == 11 and url in row[1] and row[7] == "mined" and path in row[10])
        bound += bool(cites and ok_row)

    rows: list[list[str]] = []
    manifest = ev / "spans.tsv"
    if manifest.is_file():
        rows = [l.split("\t") for l in manifest.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    in_span = in_entry = cap_bound = span_ctx = 0
    row_ids: set[str] = set()
    for r in rows:
        if len(r) != 7:
            continue
        sid, url, cap_sha, offset, span_file, quote, entry = r
        raw = span_file.strip()
        if not raw or raw.startswith("/") or ".." in pathlib.PurePath(raw).parts:
            continue
        span_path = ev / raw
        span = span_path.read_text(encoding="utf-8") if span_path.is_file() else ""
        row_ids.add(sid.strip())
        in_span += bool(quote and quote in span)
        span_ctx += bool(integral_offset(offset) and len(span) > len(quote))
        in_entry += bool(quote and quote in texts.get(entry, ""))
        if not a.lane_only:
            cap = cache / f"{key(url)}.txt"
            if cap.is_file() and sha(cap) == cap_sha and span:
                ct = cap.read_text(encoding="utf-8", errors="replace")
                if not integral_offset(offset):
                    continue
                o = int(offset)
                cap_bound += ct[o:o + len(span)] == span

    unb = 0
    for t in texts.values():
        unb += sum(1 for i in ID_RE.findall(t) if i not in ALLOWED_IDS)
    ref_ok = 0
    for sid, token in CROSS_REFS.items():
        hit = False
        for t in texts.values():
            for s in sentences(t):
                if sid in s and token in s:
                    hit = True
        ref_ok += hit

    print(f"ENTRIES={entries}/2")
    print(f"CITES_BOUND={bound}/{len(BINDINGS)}")
    print(f"QUOTE_ROWS={len(rows)}/{N_QUOTES}")
    print(f"QUOTES_IN_SPAN={in_span}/{N_QUOTES}")
    print(f"QUOTES_IN_ENTRY={in_entry}/{N_QUOTES}")
    if a.lane_only:
        print("CAPTURE_BOUND=skipped")
        ok = (entries == 2 and bound == len(BINDINGS) and len(rows) == N_QUOTES
              and in_span == N_QUOTES and in_entry == N_QUOTES
              and unb == 0 and ref_ok == len(CROSS_REFS))
    else:
        print(f"CAPTURE_BOUND={cap_bound}/{N_QUOTES}")
        ok = (entries == 2 and bound == len(BINDINGS) and len(rows) == N_QUOTES
              and in_span == N_QUOTES and in_entry == N_QUOTES and cap_bound == N_QUOTES
              and unb == 0 and ref_ok == len(CROSS_REFS))
    span_ids = len(row_ids & {sid for _e, sid, _u in BINDINGS})
    print(f"SPAN_IDS={span_ids}/{len(BINDINGS)}")
    print(f"SPAN_CONTEXT={span_ctx}/{N_QUOTES}")
    print(f"REF_ID_UNBOUND={unb}")
    ok = ok and span_ids == len(BINDINGS) and span_ctx == N_QUOTES
    print(f"REF_BOUND={ref_ok}/{len(CROSS_REFS)}")
    print("C3=PASS" if ok else "C3=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
