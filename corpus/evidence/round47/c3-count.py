#!/usr/bin/env python3
"""c3-count — frozen counter for round 47 claim C3 (depth, sourced).

Predicate R47-C3, the same sentence as corpus/evidence/round47/claims.md:
the two adopted entries `corpus/knowledge/claim-support-test-r37.md` and
`corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md` exist; their
six `source:` lines bind, BY DOCUMENT, S085 (FEVER dataset page, held), S090
(PEOPLEPROFILES, Findings of ACL 2026), S091 (CFEVER, AAAI) to the base entry
and S092 (FEVER arXiv v3 with the annotation guidelines), S093 (climate-fever
arXiv v2), S094 (CorFEVER, COLING 2025) to the amendment, each such Registry
row carrying that URL, status `mined` and the citing entry in `used-by`;
`corpus/evidence/round47/spans.tsv` holds at least 12 rows, at least two per
bound id, each quote in its committed span file and in the citing entry, each
span file the exact slice of the capture sha256(url)[:24].txt at the recorded
offset whose sha256 is the recorded one, and longer than its quote (context);
every `S###` token in either entry is one of S079–S094; every `char N` in the
`anchor` cell of rows S085 and S090–S094 is the character offset of a quote of
that id in the round-46 or round-47 span manifest (span offset + the quote's
position inside the span file) — the round-46 named limit "the counter never
checks a row's anchor cell"; both entries exit 0 under
`tools/inference-ground.py` with this round's spans and the registry; and
`corpus/lessons/round-47.md` carries a quarantine verdict line for each of the
four absent-defect-register rows on this theme's URLs (register ids S093,
S094, S108, S110) with no adopted row whose verdict is `absent`.

`--lane-only` reads lane bytes only: `CAPTURE_BOUND` prints `skipped`.

Cheapest gate that would score full marks without the work (QUALITY 60):
entries plus a self-consistent span manifest with invented quotes and digests
pass `--lane-only`; the default mode refuses them (`CAPTURE_BOUND`). Copying
the staged entries unchanged fails `REF_ID_UNBOUND` (staged ids S097–S115) and
`CITES_BOUND`. The verdict lines' truth is the closure's spot-check.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
BASE = "corpus/knowledge/claim-support-test-r37.md"
AMEND = "corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md"
BINDINGS = [
    (BASE, "S085", "https://fever.ai/dataset/fever.html"),
    (BASE, "S090", "https://aclanthology.org/2026.findings-acl.19.pdf"),
    (BASE, "S091", "https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432"),
    (AMEND, "S092", "https://arxiv.org/html/1803.05355"),
    (AMEND, "S093", "https://arxiv.org/html/2012.00614v2"),
    (AMEND, "S094", "https://aclanthology.org/2025.coling-main.108.pdf"),
]
MIN_ROWS = 12
MIN_PER_ID = 2
ALLOWED_IDS = {f"S{n:03d}" for n in range(79, 95)}
ANCHOR_IDS = ("S085", "S090", "S091", "S092", "S093", "S094")
# register id (campaign numbering) -> the lane id bound to the same URL
QUARANTINE = {"S093": "S090", "S094": "S091", "S108": "S092", "S110": "S094"}
ID_RE = re.compile(r"\bS\d{3,}\b")
CHAR_RE = re.compile(r"\bchar\s+(\d+)")
VERDICT_RE = re.compile(r"register\s+`?(S\d{3,})`?.*?verdict[:=]?\s*`?(present|absent|unverifiable)`?")


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


def manifest(ev: pathlib.Path) -> list[tuple[pathlib.Path, list[str]]]:
    m = ev / "spans.tsv"
    if not m.is_file():
        return []
    return [(ev, l.split("\t")) for l in m.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]


def safe_span(ev: pathlib.Path, raw: str) -> pathlib.Path | None:
    raw = raw.strip()
    if not raw or raw.startswith("/") or ".." in pathlib.PurePath(raw).parts:
        return None
    return ev / raw


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--cache", default=str(CACHE))
    ap.add_argument("--lane-only", action="store_true")
    a = ap.parse_args()
    root, cache = pathlib.Path(a.root), pathlib.Path(a.cache)
    ev47 = root / "corpus" / "evidence" / "round47"
    ev46 = root / "corpus" / "evidence" / "round46"
    sources = root / "corpus" / "SOURCES.md"

    texts = {p: (root / p).read_text(encoding="utf-8")
             for p in (BASE, AMEND) if (root / p).is_file()}

    bound_ids: set[str] = set()
    for path, sid, url in BINDINGS:
        t = texts.get(path, "")
        cites = re.search(r"^source:\s*" + sid + r"\s+—\s+" + re.escape(url) + r"(\s|$)", t, re.M)
        row = row_for(sources, sid)
        ok_row = len(row) == 11 and url in row[1] and row[7] == "mined" and path in row[10]
        if cites and ok_row:
            bound_ids.add(sid)
    bound = len(bound_ids)

    rows = manifest(ev47)
    in_span = in_entry = cap_bound = ctx = 0
    per_id: dict[str, int] = {}
    quote_offsets: dict[str, set[int]] = {}
    for ev, r in rows + manifest(ev46):
        if len(r) != 7:
            continue
        sid, _url, _sha, offset, span_file, quote, _entry = r
        p = safe_span(ev, span_file)
        span = p.read_text(encoding="utf-8") if p and p.is_file() else ""
        if offset.strip().isdigit() and quote and quote in span:
            quote_offsets.setdefault(sid.strip(), set()).add(int(offset) + span.find(quote))
    for ev, r in rows:
        if len(r) != 7:
            continue
        sid, url, cap_sha, offset, span_file, quote, entry = r
        p = safe_span(ev, span_file)
        span = p.read_text(encoding="utf-8") if p and p.is_file() else ""
        per_id[sid.strip()] = per_id.get(sid.strip(), 0) + 1
        in_span += bool(quote and quote in span)
        in_entry += bool(quote and quote in texts.get(entry.strip(), ""))
        ctx += bool(offset.strip().isdigit() and len(span) > len(quote))
        if not a.lane_only and offset.strip().isdigit():
            cap = cache / f"{key(url)}.txt"
            if cap.is_file() and sha(cap) == cap_sha and span:
                ct = cap.read_text(encoding="utf-8", errors="replace")
                o = int(offset)
                cap_bound += ct[o:o + len(span)] == span
    n = len(rows)
    ids_ok = sum(per_id.get(sid, 0) >= MIN_PER_ID for _p, sid, _u in BINDINGS)

    unb = sum(1 for t in texts.values() for i in ID_RE.findall(t) if i not in ALLOWED_IDS)

    anchors = 0
    for sid in ANCHOR_IDS:
        row = row_for(sources, sid)
        if len(row) != 11:
            continue
        chars = [int(c) for c in CHAR_RE.findall(row[5])]
        anchors += bool(chars) and all(c in quote_offsets.get(sid, set()) for c in chars)

    grounded = 0
    tool = root / "tools" / "inference-ground.py"
    for path in (BASE, AMEND):
        if path not in texts or not tool.is_file():
            continue
        p = subprocess.run([sys.executable, str(tool), "--entry", str(root / path),
                            "--spans", str(ev47 / "spans.tsv"), "--counts", "/dev/null",
                            "--registry", str(sources), "--root", str(root), "--quiet"],
                           capture_output=True, text=True)
        grounded += p.returncode == 0

    lesson = root / "corpus" / "lessons" / "round-47.md"
    verdicts: dict[str, str] = {}
    if lesson.is_file():
        for line in lesson.read_text(encoding="utf-8").splitlines():
            m = VERDICT_RE.search(line)
            if m and m.group(1) in QUARANTINE:
                verdicts[m.group(1)] = m.group(2)
    q_ok = len(verdicts)
    q_absent_adopted = sum(1 for rid, v in verdicts.items()
                           if v == "absent" and QUARANTINE[rid] in bound_ids)

    print(f"ENTRIES={len(texts)}/2")
    print(f"CITES_BOUND={bound}/{len(BINDINGS)}")
    print(f"QUOTE_ROWS={n} (min {MIN_ROWS})")
    print(f"SPAN_IDS={ids_ok}/{len(BINDINGS)}")
    print(f"QUOTES_IN_SPAN={in_span}/{n}")
    print(f"QUOTES_IN_ENTRY={in_entry}/{n}")
    print(f"SPAN_CONTEXT={ctx}/{n}")
    print("CAPTURE_BOUND=skipped" if a.lane_only else f"CAPTURE_BOUND={cap_bound}/{n}")
    print(f"REF_ID_UNBOUND={unb}")
    print(f"ANCHOR_BOUND={anchors}/{len(ANCHOR_IDS)}")
    print(f"INFERENCE_GROUNDED={grounded}/2")
    print(f"QUARANTINE_VERDICTS={q_ok}/{len(QUARANTINE)}")
    print(f"QUARANTINE_ABSENT_ADOPTED={q_absent_adopted}")
    ok = (len(texts) == 2 and bound == len(BINDINGS) and n >= MIN_ROWS
          and ids_ok == len(BINDINGS) and in_span == n and in_entry == n and ctx == n
          and (a.lane_only or cap_bound == n) and unb == 0
          and anchors == len(ANCHOR_IDS) and grounded == 2
          and q_ok == len(QUARANTINE) and not q_absent_adopted)
    print("C3=PASS" if ok else "C3=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
