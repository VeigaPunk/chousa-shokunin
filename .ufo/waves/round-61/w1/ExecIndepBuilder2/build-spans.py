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

Output safety (round 61):
  - a capture is read only when it resolves to a regular file inside the cache, of at most
    64 MiB (`.txt`, `.raw`), and its text form has at most 64 Mi characters; otherwise the row is
    refused (exit 1, nothing written). An unreadable file, a FIFO or a link out of the cache is
    a refused row, never a traceback;
  - nothing is written unless every row builds and every output path passed these checks:
      * `DIR` must be (or become) a directory, `DIR/spans` must not be a symlink or a
        non-directory, and no span or manifest path may be a directory: exit 2;
      * an existing `DIR/spans.tsv` (regular file) that differs from the new manifest, or
        span files in `DIR/spans` that the run does not write beside no manifest, are
        refused (exit 2) unless `--replace` is given; `--replace` rewrites the manifest and
        deletes the unlisted `S###-n.txt` files and nothing else;
      * a symlink at `DIR/spans.tsv` or at a span file path is REPLACED by a regular file (the
        link itself is swapped by rename; its target is never written);
  - files are written to a temporary name in their own directory and renamed into place; the
    manifest goes last. The module writes no bytecode.
Check mode reads a link or a non-regular file at an output path as STALE and follows nothing.

Usage:
  python3 tools/build-spans.py --quotes Q.tsv --out DIR [--cache DIR] [--check] [--replace]
Exit codes: 0 built / no stale row · 1 a row refused or STALE>0 · 2 usage/env/unsafe output.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import importlib.util
import os
import pathlib
import re
import stat

TOOLS = pathlib.Path(__file__).resolve().parent
DEFAULT_CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
CONTEXT = 80
CAP_BYTES = 64 * 1024 * 1024
CAP_CHARS = 64 * 1024 * 1024
IN_HEADER = ["id", "url", "quote", "entry"]
OUT_HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
ID_RE = re.compile(r"^S\d{3}$")
SPAN_RE = re.compile(r"^S\d{3}-\d+\.txt$")
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
ZIP = b"PK\x03\x04"


class Unsafe(Exception):
    """An output path or the output directory is unsafe to write: exit 2."""


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def _capture_text():
    spec = importlib.util.spec_from_file_location("capture_text", TOOLS / "capture-text.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def open_capture(path: pathlib.Path, root: pathlib.Path):
    """(real path, fd) of a regular file inside `root`; None when `path` is not a regular
    file (absent, FIFO, directory); ValueError(reason) when it must be refused."""
    try:
        real = pathlib.Path(os.path.realpath(path))
    except OSError as e:
        raise ValueError(f"cannot resolve {path.name}: {e.strerror}")
    if not os.path.lexists(path):
        return None
    if not (real == root or root in real.parents):
        raise ValueError(f"{path.name} resolves outside the capture cache")
    try:
        # O_NONBLOCK: never hang on a FIFO; checked with fstat below, not by name.
        fd = os.open(real, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    except FileNotFoundError:
        return None
    except OSError as e:
        raise ValueError(f"cannot read {path.name}: {e.strerror}")
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            os.close(fd)
            return None
    except OSError:
        os.close(fd)
        raise
    return real, fd


class Forms:
    def __init__(self, cache: pathlib.Path):
        self.cache, self.ct, self.memo = cache, None, {}
        self.root = pathlib.Path(os.path.realpath(cache))

    def _read(self, fd: int, name: str) -> bytes:
        try:
            if os.fstat(fd).st_size > CAP_BYTES:
                raise ValueError(f"{name} is larger than {CAP_BYTES} bytes")
            with os.fdopen(fd, "rb", closefd=True) as f:
                fd = -1
                b = f.read(CAP_BYTES + 1)
        except OSError as e:
            raise ValueError(f"cannot read {name}: {e.strerror}")
        finally:
            if fd >= 0:
                os.close(fd)
        if len(b) > CAP_BYTES:
            raise ValueError(f"{name} is larger than {CAP_BYTES} bytes")
        return b

    def _get(self, url: str) -> tuple[str | None, str, str]:
        raw, txt = self.cache / f"{key(url)}.raw", self.cache / f"{key(url)}.txt"
        head = b""
        got = open_capture(raw, self.root)
        if got is not None:
            real, fd = got
            try:
                head = os.read(fd, 8)
            except OSError as e:
                os.close(fd)
                raise ValueError(f"cannot read {raw.name}: {e.strerror}")
            if head[:8] == OLE or head[:4] == ZIP:
                os.lseek(fd, 0, os.SEEK_SET)
                b = self._read(fd, raw.name)
                if self.ct is None:
                    self.ct = _capture_text()
                try:
                    form = self.ct.text_form(str(real))
                except Exception as e:  # capture-text's own refusal or a defect, incl. MemoryError
                    return (None, "", f"capture-text refused {raw.name}: {str(e)[:120]}")
                if len(form) > CAP_CHARS:
                    return (None, "", f"text form of {raw.name} has more than {CAP_CHARS} characters")
                return (form, hashlib.sha256(b).hexdigest(), raw.name)
            os.close(fd)
        got = open_capture(txt, self.root)
        if got is not None:
            _, fd = got
            b = self._read(fd, txt.name)
            form = b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
            return (form, hashlib.sha256(b).hexdigest(), txt.name)
        return (None, "", f"no defined text form for {key(url)} (raw neither OLE nor zip, no .txt)")

    def get(self, url: str) -> tuple[str | None, str, str]:
        """(form or None, file digest, reason/name)."""
        if url not in self.memo:
            try:
                self.memo[url] = self._get(url)
            except ValueError as e:
                self.memo[url] = (None, "", str(e))
        return self.memo[url]


def read_quotes(path: pathlib.Path) -> list[tuple[str, str, str, str]]:
    if not path.is_file():
        print(f"build-spans: no input {path}", file=sys.stderr)
        sys.exit(2)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as e:
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


def regular_bytes(p: pathlib.Path) -> bytes | None:
    """The bytes of `p` iff it is itself (not through a link) a regular file of at most
    CAP_BYTES; None otherwise."""
    try:
        st = os.lstat(p)
    except OSError:
        return None
    if not stat.S_ISREG(st.st_mode) or st.st_size > CAP_BYTES:
        return None
    try:
        fd = os.open(p, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0))
    except OSError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        with os.fdopen(fd, "rb", closefd=False) as f:
            return f.read(CAP_BYTES + 1)
    except OSError:
        return None
    finally:
        os.close(fd)


def span_names(sd: pathlib.Path) -> list[str]:
    """Names in `sd` that look like span files; [] when `sd` is not a real directory."""
    try:
        if stat.S_ISLNK(os.lstat(sd).st_mode) or not sd.is_dir():
            return []
        return sorted(n for n in os.listdir(sd) if SPAN_RE.match(n))
    except OSError:
        return []


def check(out: pathlib.Path, lines: list[str], files: dict[str, str]) -> int:
    mb = regular_bytes(out / "spans.tsv")
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
        elif regular_bytes(out / name) != files[name].encode("utf-8"):
            print(f"SPANS_FILE_STALE {name}")
            stale += 1
    for extra in cur[len(lines):]:
        cells = extra.split("\t")
        print(f"SPANS_ROW_EXTRA {cells[4] if len(cells) > 4 else extra[:40]}")
        stale += 1
    for n in span_names(out / "spans"):
        if f"spans/{n}" not in files:
            print(f"SPANS_FILE_ORPHAN spans/{n}")
            stale += 1
    print(f"SPANS_ROWS={len(lines) - 1} STALE={stale}")
    return 0 if stale == 0 else 1


def preflight(out: pathlib.Path, manifest: bytes, files: dict[str, str], replace: bool) -> list[str]:
    """Refuse (Unsafe) before any write; return the orphan span names to delete."""
    if os.path.lexists(out) and not out.is_dir():
        raise Unsafe(f"--out {out} exists and is not a directory")
    sd = out / "spans"
    try:
        sst = os.lstat(sd)
    except FileNotFoundError:
        sst = None
    except OSError as e:
        raise Unsafe(f"cannot inspect {sd}: {e.strerror}")
    if sst is not None and stat.S_ISLNK(sst.st_mode):
        raise Unsafe(f"{sd} is a symlink; refusing to write through it")
    if sst is not None and not stat.S_ISDIR(sst.st_mode):
        raise Unsafe(f"{sd} exists and is not a directory")
    for name in ["spans.tsv", *files]:
        try:
            st = os.lstat(out / name)
        except FileNotFoundError:
            continue
        except OSError as e:
            raise Unsafe(f"cannot inspect {out / name}: {e.strerror}")
        if stat.S_ISDIR(st.st_mode):
            raise Unsafe(f"{out / name} is a directory")
    orphans = [n for n in span_names(sd) if f"spans/{n}" not in files]
    for n in orphans:
        if stat.S_ISDIR(os.lstat(sd / n).st_mode):
            raise Unsafe(f"{sd / n} is a directory")
    if not replace:
        try:
            mst = os.lstat(out / "spans.tsv")
        except FileNotFoundError:
            mst = None
        if mst is not None and stat.S_ISREG(mst.st_mode):
            if regular_bytes(out / "spans.tsv") != manifest:
                raise Unsafe(f"{out / 'spans.tsv'} holds a different manifest; refusing (use --replace)")
        elif orphans:
            raise Unsafe(f"{sd} holds span files this run does not write ({orphans[0]}...) beside no manifest; "
                         "refusing (use --replace)")
    return orphans


def put(dest: pathlib.Path, data: bytes) -> None:
    """Write `data` to a fresh temporary file beside `dest`, then rename it over `dest`
    (a link at `dest` is replaced, never followed)."""
    tmp = dest.with_name(f".{dest.name}.tmp{os.getpid()}")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o666)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, dest)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
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
    if os.path.lexists(out) and not out.is_dir():
        print(f"build-spans: --out {out} exists and is not a directory", file=sys.stderr)
        return 2
    rows = read_quotes(pathlib.Path(a.quotes))
    lines, files, chars = build(rows, Forms(cache))
    if a.check:
        return check(out, lines, files)
    manifest = ("\n".join(lines) + "\n").encode("utf-8")
    try:
        orphans = preflight(out, manifest, files, a.replace)
        sd = out / "spans"
        sd.mkdir(parents=True, exist_ok=True)
        for n in orphans:
            os.unlink(sd / n)
        for name, body in files.items():
            put(out / name, body.encode("utf-8"))
        put(out / "spans.tsv", manifest)
    except Unsafe as e:
        print(f"build-spans: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"build-spans: cannot write output: {e}", file=sys.stderr)
        return 2
    for line, c in zip(lines[1:], chars):
        cells = line.split("\t")
        print(f"QUOTE {cells[0]} char {c} {cells[4]}")
    print(f"SPANS_ROWS={len(files)} WRITTEN={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
