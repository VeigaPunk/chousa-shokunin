#!/usr/bin/env python3
"""build-spans — rebuild round 46's committed spans and manifest from the captures.

Every row of `spans.tsv` is derived, never hand-written: the span file is the
exact slice `capture[offset:offset+len(span)]`, holding the quote and 80 chars
of captured context either side, and `capture_sha256` is the sha256 of the
capture file named `sha256(url)[:24].txt`. Run from anywhere:

    python3 corpus/evidence/round46/build-spans.py [--cache DIR] [--check]

`--check` re-derives the manifest from the captures and exits 1 if the
committed bytes differ (nothing is written). A missing capture or a quote
absent from its capture also exits 1, with the reason on stderr.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
BASE = "corpus/knowledge/evidence-pool-versioning-r39.md"
AMEND = "corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md"
U = {
    "S085": "https://fever.ai/dataset/fever.html",
    "S086": "https://aclanthology.org/N18-1074.pdf",
    "S087": "https://zenodo.org/api/records/4925954",
    "S088": "https://fever.ai/dataset/averitec.html",
    "S089": "https://arxiv.org/html/2505.17978v2",
}
OWNER = {"S085": BASE, "S086": BASE, "S087": BASE, "S088": AMEND, "S089": AMEND}
CONTEXT = 80
QUOTES = [
    ("S085", "A list of evidence sets"),
    ("S085", "Pre-processed Wikipedia Pages (June 2017 dump)"),
    ("S086", "used the June 2017 Wikipedia dump, processed"),
    ("S086", "recall of 72.36%"),
    ("S086", "We found that 91.2%"),
    ("S087", '"conceptdoi": "10.5281/zenodo.4925953"'),
    ("S087", '"key": "wiki-pages.zip"'),
    ("S088", "An archive.org link for the source url"),
    ("S088", "Our best estimate for the date the claim first appeared"),
    ("S089", "temporally constrained evidence annotation"),
    ("S089", "published before the claim’s date"),
]


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def build(cache: pathlib.Path) -> tuple[str, dict[str, str]]:
    lines = ["id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"]
    files: dict[str, str] = {}
    seen: dict[str, int] = {}
    for sid, quote in QUOTES:
        url = U[sid]
        cap = cache / f"{key(url)}.txt"
        if not cap.is_file():
            raise SystemExit(f"build-spans: no capture {cap}")
        text = cap.read_text(encoding="utf-8", errors="replace")
        off = text.find(quote)
        if off < 0:
            raise SystemExit(f"build-spans: quote absent from {cap}: {quote!r}")
        if text.count(quote) > 1:
            raise SystemExit(f"build-spans: quote not unique in {cap}: {quote!r}")
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        # The span carries CONTEXT around the quote (round-46 `ReviewOpenS086`
        # M1: a span byte-identical to its quote makes QUOTES_IN_SPAN entailed
        # by CAPTURE_BOUND and shows nothing of the captured page). `offset` is
        # the span's start; the quote must sit inside the slice.
        start = max(0, off - CONTEXT)
        span = text[start:off + len(quote) + CONTEXT]
        files[name] = span
        lines.append("\t".join([sid, url, hashlib.sha256(cap.read_bytes()).hexdigest(),
                                str(start), name, quote, OWNER[sid]]))
    return "\n".join(lines) + "\n", files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cache", default=str(DEFAULT_CACHE))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    manifest, files = build(pathlib.Path(a.cache))
    diffs = 0
    if a.check:
        cur = (HERE / "spans.tsv")
        if not cur.is_file() or cur.read_text(encoding="utf-8") != manifest:
            print("SPANS_MANIFEST_STALE")
            diffs += 1
        for name, body in files.items():
            p = HERE / name
            if not p.is_file() or p.read_text(encoding="utf-8") != body:
                print(f"SPANS_FILE_STALE {name}")
                diffs += 1
        print(f"SPANS_ROWS={len(QUOTES)} STALE={diffs}")
        return 0 if diffs == 0 else 1
    (HERE / "spans").mkdir(parents=True, exist_ok=True)
    (HERE / "spans.tsv").write_text(manifest, encoding="utf-8")
    for name, body in files.items():
        (HERE / name).write_text(body, encoding="utf-8")
    print(f"SPANS_ROWS={len(QUOTES)} WRITTEN={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
