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

Output safety (strict policy):
  - no symlink is followed or accepted: a link as DIR, `DIR/spans`, `DIR/spans.tsv`, a span
    file, or any entry of DIR or DIR/spans, and a link as a cache capture (`.raw` / `.txt`),
    is refused (output link: exit 2; cache link: a refused row, exit 1);
  - existing output must equal what this run derives: a differing `spans.tsv`, a differing span
    file, or a span file (`S###-n.txt`) this run does not write is refused with exit 2 and
    nothing is touched. Identical existing output is accepted (a rebuild is a no-op). `--replace`
    lets a differing manifest/span file be overwritten and orphan span files be deleted; it
    never lifts the link refusal, and files that are not output (not `spans.tsv`, not
    `S###-n.txt` under `spans/`) are never touched;
  - a cache capture or a derived text form above 64 MiB is refused before it is read in full;
    only regular files are read (a FIFO, device or directory is refused without being opened
    for blocking I/O); an unreadable capture is a refused row;
  - every file is written to a fresh temporary name inside its directory and renamed into place,
    so a path is replaced, never written through; no bytecode is written beside the tools.
Limit: checks precede writes; a process that swaps a directory for a link in between is not
stopped.

Usage:
  python3 tools/build-spans.py --quotes Q.tsv --out DIR [--cache DIR] [--check] [--replace]
Exit codes: 0 built / no stale row · 1 a row refused or STALE>0 · 2 usage/env/output refused.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # importing capture-text must not write tools/__pycache__

import argparse
import errno
import hashlib
import importlib.util
import os
import pathlib
import re
import stat

TOOLS = pathlib.Path(__file__).resolve().parent
DEFAULT_CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
CONTEXT = 80
MAX_BYTES = 64 * 1024 * 1024   # largest cache file / quote table read
MAX_FORM = 64 * 1024 * 1024    # largest text form, in characters
IN_HEADER = ["id", "url", "quote", "entry"]
OUT_HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
ID_RE = re.compile(r"^S\d{3}$")
SPAN_RE = re.compile(r"^S\d{3}-\d+\.txt$")
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
ZIP = b"PK\x03\x04"


class Refuse(Exception):
    """Output or environment refused: exit 2, nothing written."""


class Unusable(Exception):
    """A cache file that may not be read: the row is refused."""


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def safe_read(path: pathlib.Path, exc) -> bytes | None:
    """Bytes of a regular, non-link file of at most MAX_BYTES; None when absent.
    Anything else raises `exc`. A FIFO is opened non-blocking and refused after fstat."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
    except FileNotFoundError:
        return None
    except OSError as e:
        if e.errno == errno.ELOOP:
            raise exc(f"{path} is a symbolic link")
        raise exc(f"{path} cannot be opened: {e.strerror}")
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise exc(f"{path} is not a regular file")
        if st.st_size > MAX_BYTES:
            raise exc(f"{path} is {st.st_size} bytes (limit {MAX_BYTES})")
        chunks, n = [], 0
        while True:
            try:
                b = os.read(fd, 1 << 20)
            except OSError as e:
                raise exc(f"{path} cannot be read: {e.strerror}")
            if not b:
                break
            n += len(b)
            if n > MAX_BYTES:
                raise exc(f"{path} grew past {MAX_BYTES} bytes")
            chunks.append(b)
        return b"".join(chunks)
    finally:
        os.close(fd)


def is_link(path: pathlib.Path) -> bool:
    return os.path.islink(path)


def _capture_text():
    spec = importlib.util.spec_from_file_location("capture_text", TOOLS / "capture-text.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Forms:
    def __init__(self, cache: pathlib.Path):
        self.cache, self.ct, self.memo = cache, None, {}

    def _head(self, raw: pathlib.Path) -> bytes:
        """First 8 bytes of a `.raw` ('' if absent); a link/FIFO/oversize raw raises Unusable."""
        if not os.path.lexists(raw):
            return b""
        if is_link(raw):
            raise Unusable(f"{raw.name} is a symbolic link")
        st = os.lstat(raw)
        if not stat.S_ISREG(st.st_mode):
            raise Unusable(f"{raw.name} is not a regular file")
        if st.st_size > MAX_BYTES:
            raise Unusable(f"{raw.name} is {st.st_size} bytes (limit {MAX_BYTES})")
        b = safe_read(raw, Unusable)
        return (b or b"")[:8]

    def get(self, url: str) -> tuple[str | None, str, str]:
        """(form or None, file digest, reason/name)."""
        if url in self.memo:
            return self.memo[url]
        raw, txt = self.cache / f"{key(url)}.raw", self.cache / f"{key(url)}.txt"
        res: tuple[str | None, str, str]
        try:
            head = self._head(raw)
            if head[:8] == OLE or head[:4] == ZIP:
                if self.ct is None:
                    self.ct = _capture_text()
                b = safe_read(raw, Unusable)
                if b is None:
                    raise Unusable(f"{raw.name} vanished")
                try:
                    form = self.ct.text_form(str(raw))
                except Exception as e:  # capture-text's own refusal (ValueError) or a defect
                    res = (None, "", f"capture-text refused {raw.name}: {str(e)[:120]}")
                else:
                    if len(form) > MAX_FORM:
                        raise Unusable(f"text form of {raw.name} is {len(form)} chars (limit {MAX_FORM})")
                    res = (form, hashlib.sha256(b).hexdigest(), raw.name)
            else:
                b = safe_read(txt, Unusable)
                if b is None:
                    res = (None, "", f"no defined text form for {key(url)} (raw neither OLE nor zip, no .txt)")
                else:
                    res = (b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n"),
                           hashlib.sha256(b).hexdigest(), txt.name)
        except Unusable as e:
            res = (None, "", f"{e}")
        except MemoryError:
            res = (None, "", f"capture for {key(url)} too large to render in memory")
        self.memo[url] = res
        return res


def read_quotes(path: pathlib.Path) -> list[tuple[str, str, str, str]]:
    if not path.is_file():
        print(f"build-spans: no input {path}", file=sys.stderr)
        sys.exit(2)
    try:
        raw = safe_read(path, Refuse)
        lines = raw.decode("utf-8").splitlines()
    except (Refuse, UnicodeDecodeError) as e:
        print(f"build-spans: cannot read input {path}: {e}", file=sys.stderr)
        sys.exit(2)
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


def scan_out(out: pathlib.Path) -> list[str]:
    """Structural safety of an existing OUT: raise Refuse on any link, or on a path that must be
    a directory/regular file and is not. Returns the names of the span files present in spans/."""
    if not os.path.lexists(out):
        return []
    if is_link(out):
        raise Refuse(f"{out} is a symbolic link")
    if not out.is_dir():
        raise Refuse(f"{out} exists and is not a directory")
    for p in sorted(out.iterdir()):
        if is_link(p):
            raise Refuse(f"{p} is a symbolic link")
    tsv = out / "spans.tsv"
    if os.path.lexists(tsv) and not stat.S_ISREG(os.lstat(tsv).st_mode):
        raise Refuse(f"{tsv} exists and is not a regular file")
    sd = out / "spans"
    present: list[str] = []
    if os.path.lexists(sd):
        if is_link(sd):
            raise Refuse(f"{sd} is a symbolic link")
        if not sd.is_dir():
            raise Refuse(f"{sd} exists and is not a directory")
        for p in sorted(sd.iterdir()):
            if is_link(p):
                raise Refuse(f"{p} is a symbolic link")
            if SPAN_RE.match(p.name):
                if not stat.S_ISREG(os.lstat(p).st_mode):
                    raise Refuse(f"{p} exists and is not a regular file")
                present.append(p.name)
    return present


def existing(path: pathlib.Path) -> bytes | None:
    return safe_read(path, Refuse)


def check(out: pathlib.Path, lines: list[str], files: dict[str, str]) -> int:
    scan_out(out)
    m = out / "spans.tsv"
    mb = existing(m)
    cur = mb.decode("utf-8", errors="replace").splitlines() if mb is not None else []
    stale = 0
    if not cur or cur[0] != OUT_HEADER:
        print("SPANS_HEADER_STALE")
        stale += 1
    for i, want in enumerate(lines[1:], start=1):
        name = want.split("\t")[4]
        if i >= len(cur) or cur[i] != want:
            print(f"SPANS_ROW_STALE {name}")
            stale += 1
        elif existing(out / name) != files[name].encode("utf-8"):
            print(f"SPANS_FILE_STALE {name}")
            stale += 1
    for extra in cur[len(lines):]:
        cells = extra.split("\t")
        print(f"SPANS_ROW_EXTRA {cells[4] if len(cells) > 4 else extra[:40]}")
        stale += 1
    sd = out / "spans"
    for name in sorted(p.name for p in sd.iterdir()) if sd.is_dir() else []:
        if SPAN_RE.match(name) and f"spans/{name}" not in files:
            print(f"SPANS_FILE_ORPHAN spans/{name}")
            stale += 1
    print(f"SPANS_ROWS={len(lines) - 1} STALE={stale}")
    return 0 if stale == 0 else 1


def put(path: pathlib.Path, data: bytes) -> None:
    """Replace `path` with `data` through a fresh temporary file in the same directory."""
    tmp = path.with_name(f".{path.name}.tmp{os.getpid()}")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o644)
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


def write_out(out: pathlib.Path, lines: list[str], files: dict[str, str], replace: bool) -> None:
    present = scan_out(out)
    tsv = ("\n".join(lines) + "\n").encode("utf-8")
    want: dict[str, bytes] = {"spans.tsv": tsv}
    want.update({n: b.encode("utf-8") for n, b in files.items()})
    orphans = [n for n in present if f"spans/{n}" not in files]
    todo: list[str] = []
    for name, data in want.items():
        cur = existing(out / name)
        if cur is None:
            todo.append(name)
        elif cur != data:
            if not replace:
                raise Refuse(f"{out / name} exists and differs from this build (use --replace)")
            todo.append(name)
    if orphans and not replace:
        raise Refuse(f"{out / 'spans'} holds {orphans[0]} which this build does not write (use --replace)")
    out.mkdir(parents=True, exist_ok=True)
    (out / "spans").mkdir(exist_ok=True)
    if is_link(out) or is_link(out / "spans"):
        raise Refuse(f"{out} or {out / 'spans'} became a symbolic link")
    for n in orphans:
        os.unlink(out / "spans" / n)
    for name in todo:
        put(out / name, want[name])


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
    try:
        scan_out(out)
        rows = read_quotes(pathlib.Path(a.quotes))
        lines, files, chars = build(rows, Forms(cache))
        if a.check:
            return check(out, lines, files)
        write_out(out, lines, files, a.replace)
    except Refuse as e:
        print(f"build-spans: refused output: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"build-spans: {e.strerror}: {e.filename}", file=sys.stderr)
        return 2
    for line, c in zip(lines[1:], chars):
        cells = line.split("\t")
        print(f"QUOTE {cells[0]} char {c} {cells[4]}")
    print(f"SPANS_ROWS={len(files)} WRITTEN={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
