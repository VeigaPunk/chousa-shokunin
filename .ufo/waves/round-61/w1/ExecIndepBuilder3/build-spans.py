#!/usr/bin/env python3
"""build-spans — derive a span manifest and span files from a quote table, reading every
capture through its DEFINED text form (round 55; supersedes the per-round builders
`corpus/evidence/round5x/build-spans.py`, whose non-zip `.raw` fallback decoded an OLE `.doc`
as UTF-16LE — an undefined form, round-54 lesson `## Mistakes` row 2).

Text form of the capture of URL u (key = first 24 hex of sha256(u)):
  - `<key>.raw` is an OLE compound file (D0CF11E0A1B11AE1) or a zip (`PK\\x03\\x04`): the
    form is the stdout of `tools/capture-text.py <key>.raw` (imported, not spawned); the
    `.txt` sidecar is never used for such a capture, and a raw capture-text refuses is a
    refused row (`capture-text refused`);
  - otherwise `<key>.txt`, read as UTF-8 (errors replaced) with universal newlines;
  - neither: a refused row (`no defined text form`).
`capture_sha256` is the digest of the FILE read (`.raw` or `.txt`). The quote must occur
exactly once in the form, else the row is refused. The span is
`form[max(0, off-80) : off+len(quote)+80]`, the `offset` column its start; the span file is
`spans/<id>-<n>.txt` (n counts that id's rows in input order).

Input: TSV header `id url quote entry`, one quote per row. Output (DIR): `spans.tsv`, header
`id url capture_sha256 offset span_file quote entry` (the 7 columns `tools/inference-ground.py`
reads), and the span files. A refused row prints `build-spans: refused <id>: <reason>` on
stderr; any refusal writes nothing and exits 1. Each written row prints
`QUOTE <id> char <N> <span_file>`, N = offset + the quote's position in its span (the value a
Registry `anchor` cell's `char N` must equal). `--check` re-derives every row and compares it
with the manifest and span files already in DIR, writing nothing, and prints
`SPANS_ROWS=n STALE=k`.

Usage:
  python3 tools/build-spans.py --quotes Q.tsv --out DIR [--cache DIR] [--check] [--replace]
Safety: no write before every check passes; DIR holding a different `spans.tsv` or span files this run
does not write is refused (exit 2) unless `--replace`; links and non-files at an output path, and `--out`
that is not a directory, are refused; captures must resolve inside the cache, be regular files and be at
most 64 MiB (text form 64 Mi chars); files are written by temp file + rename.
Exit codes: 0 built / no stale row · 1 a row refused or STALE>0 · 2 usage/env/refused output.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import pathlib
import re
import stat
import sys
import tempfile

sys.dont_write_bytecode = True

TOOLS = pathlib.Path(__file__).resolve().parent
DEFAULT_CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
CONTEXT = 80
MAX_BYTES = 64 * 1024 * 1024
IN_HEADER = ["id", "url", "quote", "entry"]
OUT_HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
ID_RE = re.compile(r"^S\d{3}$")
SPAN_RE = re.compile(r"^S\d{3}-\d+\.txt$")
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
ZIP = b"PK\x03\x04"


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def _capture_text():
    spec = importlib.util.spec_from_file_location("capture_text", TOOLS / "capture-text.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Forms:
    def __init__(self, cache: pathlib.Path):
        self.cache, self.ct, self.memo = cache, None, {}

    def get(self, url: str) -> tuple[str | None, str, str]:
        """(form or None, file digest, reason/name)."""
        if url in self.memo:
            return self.memo[url]
        raw, txt = self.cache / f"{key(url)}.raw", self.cache / f"{key(url)}.txt"
        res: tuple[str | None, str, str]
        try:
            head = self.slurp(raw, 8, True) if raw.is_file() else b""
            if head[:8] == OLE or head[:4] == ZIP:
                if self.ct is None:
                    self.ct = _capture_text()
                b = self.slurp(raw, MAX_BYTES)
                try:
                    form = self.ct.text_form(str(raw))
                except Exception as e:  # capture-text's own refusal (ValueError) or a defect
                    raise ValueError(f"capture-text refused {raw.name}: {str(e)[:120]}")
                if len(form) > MAX_BYTES:
                    raise ValueError(f"{raw.name} text form is over {MAX_BYTES} chars")
                res = (form, hashlib.sha256(b).hexdigest(), raw.name)
            elif txt.is_file():
                b = self.slurp(txt, MAX_BYTES)
                res = (b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n"),
                       hashlib.sha256(b).hexdigest(), txt.name)
            else:
                res = (None, "", f"no defined text form for {key(url)} (raw neither OLE nor zip, no .txt)")
        except (OSError, ValueError) as e:
            res = (None, "", f"unreadable capture for {key(url)}: {str(e)[:120]}")
        self.memo[url] = res
        return res

    def slurp(self, p: pathlib.Path, cap: int, head: bool = False) -> bytes:
        """Bytes of a regular file that resolves inside the cache; over `cap` is an error unless `head`."""
        rp = p.resolve(strict=True)
        if not rp.is_relative_to(self.cache.resolve()):
            raise ValueError(f"{p.name} resolves outside the cache")
        fd = os.open(rp, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
        with os.fdopen(fd, "rb") as f:
            st = os.fstat(f.fileno())
            if not stat.S_ISREG(st.st_mode):
                raise ValueError(f"{p.name} is not a regular file")
            if st.st_size > cap and not head:
                raise ValueError(f"{p.name} is {st.st_size} bytes, over the {cap} cap")
            return f.read(cap)


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


def build(rows, forms: Forms) -> tuple[list[str], dict[str, str], list[int]]:
    lines, files, chars, refused = [OUT_HEADER], {}, [], []
    seen: dict[str, int] = {}
    for sid, url, quote, entry in rows:
        text, digest, why = forms.get(url)
        if text is None:
            refused.append(f"{sid}: {why}")
            continue
        n = text.count(quote)
        if n != 1:
            refused.append(f"{sid}: quote occurs {n}x in {why}: {quote[:60]!r}")
            continue
        off = text.find(quote)
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        start = max(0, off - CONTEXT)
        span = text[start:off + len(quote) + CONTEXT]
        if span == quote:
            refused.append(f"{sid}: {why} holds no context around {quote[:60]!r}")
            continue
        files[name] = span
        chars.append(off)
        lines.append("\t".join([sid, url, digest, str(start), name, quote, entry]))
    if refused:
        for r in refused:
            print(f"build-spans: refused {r}", file=sys.stderr)
        sys.exit(1)
    return lines, files, chars


def check(out: pathlib.Path, lines: list[str], files: dict[str, str]) -> int:
    m = out / "spans.tsv"
    cur = m.read_text(encoding="utf-8").splitlines() if m.is_file() else []
    stale = 0
    if not cur or cur[0] != OUT_HEADER:
        print("SPANS_HEADER_STALE")
        stale += 1
    for i, want in enumerate(lines[1:], start=1):
        name = want.split("\t")[4]
        p = out / name
        if i >= len(cur) or cur[i] != want:
            print(f"SPANS_ROW_STALE {name}")
            stale += 1
        elif not p.is_file() or p.read_bytes() != files[name].encode("utf-8"):
            print(f"SPANS_FILE_STALE {name}")
            stale += 1
    for extra in cur[len(lines):]:
        cells = extra.split("\t")
        print(f"SPANS_ROW_EXTRA {cells[4] if len(cells) > 4 else extra[:40]}")
        stale += 1
    sd = out / "spans"
    for p in sorted(sd.iterdir()) if sd.is_dir() else []:
        if SPAN_RE.match(p.name) and f"spans/{p.name}" not in files:
            print(f"SPANS_FILE_ORPHAN spans/{p.name}")
            stale += 1
    print(f"SPANS_ROWS={len(lines) - 1} STALE={stale}")
    return 0 if stale == 0 else 1


def preflight(out: pathlib.Path, lines, files, replace: bool) -> str | None:
    """Refusal reason, or None. Reads only; runs before anything is written."""
    if out.exists() and not out.is_dir():
        return f"--out {out} exists and is not a directory"
    sd, m = out / "spans", out / "spans.tsv"
    if sd.is_symlink() or (sd.exists() and not sd.is_dir()):
        return f"{sd} is a link or not a directory"
    for p in [m] + [out / n for n in files]:
        if p.is_symlink() or (p.exists() and not p.is_file()):
            return f"{p} is a link or not a regular file"
    if replace:
        return None
    new = ("\n".join(lines) + "\n").encode("utf-8")
    if m.is_file() and (m.stat().st_size > MAX_BYTES or m.read_bytes() != new):
        return f"{m} holds a different manifest (use --replace)"
    for p in sorted(sd.iterdir()) if sd.is_dir() else []:
        if SPAN_RE.match(p.name) and f"spans/{p.name}" not in files:
            return f"{p} is a span file this run does not write (use --replace)"
    return None


def put(path: pathlib.Path, data: bytes) -> None:
    """Atomic write: a temp file beside the target, renamed over it (a link at the target is replaced)."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".bs-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        pathlib.Path(tmp).unlink(missing_ok=True)
        raise


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quotes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache", default=str(DEFAULT_CACHE))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()
    cache, out = pathlib.Path(a.cache), pathlib.Path(a.out)
    if not cache.is_dir():
        print(f"build-spans: no capture cache {cache}", file=sys.stderr)
        return 2
    if out.exists() and not out.is_dir():
        print(f"build-spans: --out {out} is not a directory", file=sys.stderr)
        return 2
    rows = read_quotes(pathlib.Path(a.quotes))
    lines, files, chars = build(rows, Forms(cache))
    if a.check:
        return check(out, lines, files)
    why = preflight(out, lines, files, a.replace)
    if why:
        print(f"build-spans: refused {why}", file=sys.stderr)
        return 2
    sd = out / "spans"
    sd.mkdir(parents=True, exist_ok=True)
    for p in sd.iterdir():
        if SPAN_RE.match(p.name) and f"spans/{p.name}" not in files:
            p.unlink()
    put(out / "spans.tsv", ("\n".join(lines) + "\n").encode("utf-8"))
    for name, body in files.items():
        put(out / name, body.encode("utf-8"))
    for line, c in zip(lines[1:], chars):
        cells = line.split("\t")
        print(f"QUOTE {cells[0]} char {c} {cells[4]}")
    print(f"SPANS_ROWS={len(files)} WRITTEN={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
