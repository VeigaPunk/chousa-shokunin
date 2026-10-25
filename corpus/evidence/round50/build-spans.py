#!/usr/bin/env python3
"""build-spans — derive round 50's span manifest and span files from quotes.tsv.

The round-47 builder (corpus/evidence/round47/build-spans.py) with one change:
a capture's TEXT FORM. The form is `sha256(url)[:24].txt` when the quote
occurs there exactly once; otherwise the UTF-16LE decoding (errors replaced)
of the raw capture `sha256(url)[:24].raw` when the quote occurs there exactly
once — the round-48 finding that an OLE `.doc` capture's `.txt` sidecar is a
lossy binary decode while its text runs are UTF-16LE (S095/S096 register
rows). `capture_sha256` is the digest of the FILE the form was read from (the
`.txt` or the `.raw`), so a reader re-derives the form from the digest; the
manifest keeps the 7 columns `tools/inference-ground.py` reads.

Input `corpus/evidence/round50/quotes.tsv`, header `id url quote entry`, one
quote per row. Every row of `spans.tsv` is derived, never hand-written: the
span file `spans/<id>-<n>.txt` (n counts that id's rows in input order) is the
exact slice `form[offset:offset+len(span)]`, holding the quote and 80 chars
of captured context either side, `offset` is the span's start. Run from
anywhere:

    python3 corpus/evidence/round50/build-spans.py [--root LANE] [--cache DIR] [--check]

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


def form_texts(cache: pathlib.Path, url: str) -> list[tuple[str, str, str]]:
    """(text, sha256 of the file read, file name) per text form, in order:
    the `.txt` capture, then the UTF-16LE decoding of the `.raw` capture."""
    out = []
    txt, raw = cache / f"{key(url)}.txt", cache / f"{key(url)}.raw"
    if txt.is_file():
        out.append((txt.read_text(encoding="utf-8", errors="replace"),
                    hashlib.sha256(txt.read_bytes()).hexdigest(), txt.name))
    if raw.is_file():
        b = raw.read_bytes()
        out.append((b.decode("utf-16le", errors="replace"), hashlib.sha256(b).hexdigest(), raw.name))
    return out


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
    for sid, url, quote, entry in rows:
        forms = form_texts(cache, url)
        if not forms:
            refused.append(f"{sid}: no capture {key(url)}.txt/.raw for {url}")
            continue
        pick = [(t, d, n) for t, d, n in forms if t.count(quote) == 1]
        if not pick:
            hits = [f"{n}:{t.count(quote)}x" for t, d, n in forms]
            refused.append(f"{sid}: quote not exactly once in any form ({', '.join(hits)}): {quote!r}")
            continue
        text, digest, fname = pick[0]
        cap = cache / fname
        off = text.find(quote)
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        start = max(0, off - CONTEXT)
        end = off + len(quote) + CONTEXT
        if fname.endswith(".raw"):
            # Round-49 post-freeze repair (disclosed in claims-erratum.md): the
            # frozen counter reads span FILES with universal newlines, so a bare
            # CR (Word's paragraph mark in the UTF-16LE text) reads back as LF
            # and the exact-slice check fails on true bytes. Raw-form context is
            # clipped at the nearest CR on each side; the span stays an exact
            # slice of the form. `.txt` forms are read with universal newlines
            # on both sides already.
            cr = text.rfind("\r", start, off)
            start = cr + 1 if cr >= 0 else start
            cr = text.find("\r", off + len(quote), end)
            end = cr if cr >= 0 else end
        span = text[start:end]
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
    ev = pathlib.Path(a.root) / "corpus" / "evidence" / "round50"
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
