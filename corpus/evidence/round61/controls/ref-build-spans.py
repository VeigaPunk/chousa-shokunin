#!/usr/bin/env python3
"""build-spans — derive a span manifest and span files from a quote table, reading every
capture through its DEFINED text form (round 55; supersedes the per-round builders
`corpus/evidence/round5x/build-spans.py`, whose non-zip `.raw` fallback decoded an OLE `.doc`
as UTF-16LE — an undefined form, round-54 lesson `## Mistakes` row 2). Output safety added in
round 61 (hazard review `.ufo/waves/round-56/w1/R55W2SentBuilder.md`).

Text form of the capture of URL u (key = first 24 hex of sha256(u)):
  - `<key>.raw` is an OLE compound file (D0CF11E0A1B11AE1) or a zip (`PK\\x03\\x04`): the
    form is the stdout of `tools/capture-text.py <key>.raw` (imported, not spawned, and
    without writing bytecode into this tool's directory); the `.txt` sidecar is never used
    for such a capture, and a raw capture-text refuses is a refused row
    (`capture-text refused`);
  - otherwise `<key>.txt`, read as UTF-8 (errors replaced) with universal newlines;
  - neither: a refused row (`no defined text form`).
A capture file is read only when it is a regular file whose real path lies inside the cache
and whose size is at most 64 MiB (a symlink out of the cache, a FIFO or device, an oversize or
unreadable file is a refused row, decided before any byte is read); a derived form over 64 MiB
chars is refused likewise.
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

Output safety (round 61). A build refuses, exit 2 and nothing written or removed, when: DIR is
not a directory; `DIR/spans` or `DIR/spans.tsv` is a symlink or not the expected kind, or any
`DIR/spans/S###-N.txt` is a symlink; or DIR already holds a `spans.tsv` that differs from this
run's, or a span file this run does not write, unless `--replace` is given (an identical
rebuild is always allowed). Files are written by temp file + `os.replace` (span files first,
then `spans.tsv`) and orphan span files are removed last, so a failed run never leaves a
manifest without its spans.

Usage:
  python3 tools/build-spans.py --quotes Q.tsv --out DIR [--cache DIR] [--check] [--replace]
Exit codes: 0 built / no stale row · 1 a row refused or STALE>0 · 2 usage/env or an output
refusal above.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import pathlib
import re
import secrets
import stat
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
DEFAULT_CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
CONTEXT = 80
MAX_CAPTURE = 64 << 20
MAX_FORM = 64 << 20
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
    old, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = old
    return mod


class Forms:
    def __init__(self, cache: pathlib.Path):
        self.cache, self.ct, self.memo = cache, None, {}
        self.root = os.path.realpath(cache)

    def _probe(self, p: pathlib.Path) -> tuple[str, object]:
        """('absent', '') | ('bad', reason) | ('ok', size) — decided from metadata only."""
        if not os.path.lexists(p):
            return "absent", ""
        real = os.path.realpath(p)
        if os.path.commonpath([real, self.root]) != self.root:
            return "bad", f"{p.name} resolves outside the cache"
        try:
            st = os.stat(real)
        except OSError as e:
            return "bad", f"{p.name} unreadable ({e.strerror})"
        if not stat.S_ISREG(st.st_mode):
            return "bad", f"{p.name} is not a regular file"
        return "ok", st.st_size

    def get(self, url: str) -> tuple[str | None, str, str]:
        """(form or None, file digest, reason/name)."""
        if url in self.memo:
            return self.memo[url]
        raw, txt = self.cache / f"{key(url)}.raw", self.cache / f"{key(url)}.txt"
        rk, rv = self._probe(raw)
        tk, tv = self._probe(txt)
        head = b""
        if rk == "ok":
            try:
                with raw.open("rb") as f:
                    head = f.read(8)
            except OSError as e:
                rk, rv = "bad", f"{raw.name} unreadable ({e.strerror})"
        res: tuple[str | None, str, str]
        if rk == "ok" and (head[:8] == OLE or head[:4] == ZIP):
            res = self._read(raw, rv, raw.name, lambda b: self._ct_form(raw))
        elif tk == "ok":
            res = self._read(txt, tv, txt.name,
                             lambda b: b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n"))
        elif tk == "bad":
            res = (None, "", str(tv))
        else:
            res = (None, "", f"no defined text form for {key(url)} (raw neither OLE nor zip, no .txt)")
        self.memo[url] = res
        return res

    def _ct_form(self, raw: pathlib.Path) -> str:
        if self.ct is None:
            self.ct = _capture_text()
        return self.ct.text_form(str(raw))

    def _read(self, path, size, name, to_form) -> tuple[str | None, str, str]:
        if size > MAX_CAPTURE:
            return None, "", f"{name} is {size} bytes, over the {MAX_CAPTURE}-byte capture cap"
        try:
            b = path.read_bytes()
        except OSError as e:
            return None, "", f"unreadable capture {name} ({e.strerror})"
        try:
            form = to_form(b)
        except Exception as e:  # capture-text's own refusal (ValueError) or a defect
            return None, "", f"capture-text refused {name}: {str(e)[:120]}"
        if len(form) > MAX_FORM:
            return None, "", f"{name} text form is {len(form)} chars, over the {MAX_FORM}-char cap"
        return form, hashlib.sha256(b).hexdigest(), name


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
    try:
        cur = m.read_text(encoding="utf-8").splitlines() if m.is_file() else []
    except (OSError, UnicodeDecodeError) as e:
        print(f"build-spans: cannot read {m}: {e}", file=sys.stderr)
        return 2
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


def _refuse(why: str) -> int:
    print(f"build-spans: refused output: {why}", file=sys.stderr)
    return 2


def guard_out(out: pathlib.Path, manifest: bytes, files: dict[str, str], replace: bool):
    """Inspect DIR without changing it: (exit code, None) to refuse, or (0, orphan paths)."""
    if os.path.lexists(out) and not out.is_dir():
        return _refuse(f"{out} is not a directory"), None
    sd, m = out / "spans", out / "spans.tsv"
    if os.path.lexists(sd) and (sd.is_symlink() or not sd.is_dir()):
        return _refuse(f"{sd} is a symlink or not a directory"), None
    if os.path.lexists(m) and (m.is_symlink() or not m.is_file()):
        return _refuse(f"{m} is a symlink or not a regular file"), None
    orphans = []
    if sd.is_dir():
        for p in sorted(sd.iterdir()):
            if not SPAN_RE.match(p.name):
                continue
            if p.is_symlink():
                return _refuse(f"{p} is a symlink"), None
            if f"spans/{p.name}" not in files:
                orphans.append(p)
    differs = m.is_file() and m.read_bytes() != manifest
    if (differs or orphans) and not replace:
        what = "a different spans.tsv" if differs else f"{len(orphans)} span file(s) this run does not write"
        return _refuse(f"{out} already holds {what}; pass --replace to overwrite it"), None
    return 0, orphans


def _atomic_write(path: pathlib.Path, data: bytes) -> None:
    tmp = path.with_name(f".{path.name}.{secrets.token_hex(6)}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def write_out(out: pathlib.Path, lines: list[str], files: dict[str, str], replace: bool) -> int:
    manifest = ("\n".join(lines) + "\n").encode("utf-8")
    rc, orphans = guard_out(out, manifest, files, replace)
    if rc:
        return rc
    try:
        (out / "spans").mkdir(parents=True, exist_ok=True)
        for name, body in files.items():
            _atomic_write(out / name, body.encode("utf-8"))
        _atomic_write(out / "spans.tsv", manifest)
        for p in orphans:
            p.unlink()
    except OSError as e:
        print(f"build-spans: write failed under {out}: {e}", file=sys.stderr)
        return 2
    return 0


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
    rows = read_quotes(pathlib.Path(a.quotes))
    lines, files, chars = build(rows, Forms(cache))
    if a.check:
        return check(out, lines, files)
    rc = write_out(out, lines, files, a.replace)
    if rc:
        return rc
    for line, c in zip(lines[1:], chars):
        cells = line.split("\t")
        print(f"QUOTE {cells[0]} char {c} {cells[4]}")
    print(f"SPANS_ROWS={len(files)} WRITTEN={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
