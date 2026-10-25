#!/usr/bin/env python3
"""build-spans — derive round 47's span manifest and span files from quotes.tsv.

Input `corpus/evidence/round47/quotes.tsv`, header `id url quote entry`, one
quote per row. Every row of `spans.tsv` is derived, never hand-written: the
span file `spans/<id>-<n>.txt` (n counts that id's rows in input order) is the
exact slice `capture[offset:offset+len(span)]`, holding the quote and 80 chars
of captured context either side, `offset` is the span's start, and
`capture_sha256` is the sha256 of the capture `sha256(url)[:24].txt`. Run from
anywhere:

    python3 corpus/evidence/round47/build-spans.py [--root LANE] [--cache DIR] [--check]

A quote absent from its capture, or occurring in it more than once, is refused
by name and nothing is written. Each written row prints `QUOTE <id> char <N>`,
N = offset + the quote's position in its span, the value a Registry `anchor`
cell's `char N` must equal. `--check` re-derives every row and compares it with
the committed manifest and span files, writing nothing, and prints
`SPANS_ROWS=n STALE=k` (a stale row, a missing or extra committed row, an
orphan span file each count one).

Exit codes: 0 built / no stale row · 1 a quote refused, a capture missing, or
STALE>0 · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
DEFAULT_CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
CONTEXT = 80
IN_HEADER = ["id", "url", "quote", "entry"]
OUT_HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
ID_RE = re.compile(r"^S\d{3}$")
SPAN_RE = re.compile(r"^S\d{3}-\d+\.txt$")


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def read_quotes(path: pathlib.Path) -> list[tuple[str, str, str, str]]:
    if not path.is_file():
        print(f"build-spans: no input {path}", file=sys.stderr)
        sys.exit(2)
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].split("\t") != IN_HEADER:
        print(f"build-spans: {path} header must be {' '.join(IN_HEADER)} (tab-separated)", file=sys.stderr)
        sys.exit(2)
    rows, bad, url_of = [], [], {}
    for n, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        cells = line.split("\t")
        if len(cells) != 4 or not all(c.strip() for c in cells):
            bad.append(f"line {n}: need 4 non-empty tab cells, got {len(cells)}")
            continue
        sid, url, quote, entry = (c.strip() for c in cells)
        if not ID_RE.match(sid):
            bad.append(f"line {n}: id {sid!r} is not S###")
        elif url_of.setdefault(sid, url) != url:
            bad.append(f"line {n}: {sid} names {url}, earlier rows name {url_of[sid]}")
        elif entry.startswith("/") or ".." in pathlib.PurePath(entry).parts:
            bad.append(f"line {n}: entry {entry!r} must be lane-relative")
        else:
            rows.append((sid, url, quote, entry))
    if bad:
        for b in bad:
            print(f"build-spans: {path} {b}", file=sys.stderr)
        sys.exit(2)
    return rows


def build(rows, cache: pathlib.Path) -> tuple[list[str], dict[str, str], list[int]]:
    lines, files, chars, refused = [OUT_HEADER], {}, [], []
    seen: dict[str, int] = {}
    caps: dict[str, tuple[str, str]] = {}
    for sid, url, quote, entry in rows:
        cap = cache / f"{key(url)}.txt"
        if url not in caps:
            if not cap.is_file():
                refused.append(f"{sid}: no capture {cap} for {url}")
                continue
            caps[url] = (cap.read_text(encoding="utf-8", errors="replace"),
                         hashlib.sha256(cap.read_bytes()).hexdigest())
        text, digest = caps[url]
        hits = text.count(quote)
        if hits != 1:
            refused.append(f"{sid}: quote {'absent from' if hits == 0 else f'occurs {hits}x in'} {cap.name}: {quote!r}")
            continue
        off = text.find(quote)
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        start = max(0, off - CONTEXT)
        span = text[start:off + len(quote) + CONTEXT]
        if span == quote:
            refused.append(f"{sid}: capture {cap.name} holds no context around {quote!r}")
            continue
        files[name] = span
        chars.append(off)
        lines.append("\t".join([sid, url, digest, str(start), name, quote, entry]))
    if refused:
        for r in refused:
            print(f"build-spans: refused {r}", file=sys.stderr)
        sys.exit(1)
    return lines, files, chars


def check(ev: pathlib.Path, lines: list[str], files: dict[str, str]) -> int:
    m = ev / "spans.tsv"
    cur = m.read_text(encoding="utf-8").splitlines() if m.is_file() else []
    stale = 0
    if not cur or cur[0] != OUT_HEADER:
        print("SPANS_HEADER_STALE")
        stale += 1
    for i, want in enumerate(lines[1:], start=1):
        name = want.split("\t")[4]
        p = ev / name
        if i >= len(cur) or cur[i] != want:
            print(f"SPANS_ROW_STALE {name}")
            stale += 1
        elif not p.is_file() or p.read_text(encoding="utf-8") != files[name]:
            print(f"SPANS_FILE_STALE {name}")
            stale += 1
    for extra in cur[len(lines):]:
        cells = extra.split("\t")
        print(f"SPANS_ROW_EXTRA {cells[4] if len(cells) > 4 else extra[:40]}")
        stale += 1
    sd = ev / "spans"
    for p in sorted(sd.iterdir()) if sd.is_dir() else []:
        if SPAN_RE.match(p.name) and f"spans/{p.name}" not in files:
            print(f"SPANS_FILE_ORPHAN spans/{p.name}")
            stale += 1
    print(f"SPANS_ROWS={len(lines) - 1} STALE={stale}")
    return 0 if stale == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--cache", default=str(DEFAULT_CACHE))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    ev = pathlib.Path(a.root) / "corpus" / "evidence" / "round47"
    cache = pathlib.Path(a.cache)
    if not cache.is_dir():
        print(f"build-spans: no capture cache {cache}", file=sys.stderr)
        return 2
    rows = read_quotes(ev / "quotes.tsv")
    lines, files, chars = build(rows, cache)
    if a.check:
        return check(ev, lines, files)
    sd = ev / "spans"
    sd.mkdir(parents=True, exist_ok=True)
    for p in sd.iterdir():
        if SPAN_RE.match(p.name) and f"spans/{p.name}" not in files:
            p.unlink()
    (ev / "spans.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for name, body in files.items():
        (ev / name).write_text(body, encoding="utf-8")
    for line, c in zip(lines[1:], chars):
        cells = line.split("\t")
        print(f"QUOTE {cells[0]} char {c} {cells[4]}")
    print(f"SPANS_ROWS={len(files)} WRITTEN={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
