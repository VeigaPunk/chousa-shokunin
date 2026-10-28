#!/usr/bin/env python3
"""build-spans — derive a span manifest and span files from a quote table, reading every
capture through its DEFINED text form (round 55; supersedes the per-round builders
`corpus/evidence/round5x/build-spans.py`, whose non-zip `.raw` fallback decoded an OLE `.doc`
as UTF-16LE — an undefined form, round-54 lesson `## Mistakes` row 2). Output safety added in
round 61 (hazard review `.ufo/waves/round-56/w1/R55W2SentBuilder.md`; round-61 wave `w1` reviews).

Text form of the capture of URL u (key = first 24 hex of sha256(u)):
  - `<key>.raw` is an OLE compound file (D0CF11E0A1B11AE1) or a zip (`PK\\x03\\x04`): the
    form is the stdout of `tools/capture-text.py <key>.raw` (imported, not spawned, and
    without writing bytecode into this tool's directory); the `.txt` sidecar is never used
    for such a capture, and a raw capture-text refuses is a refused row
    (`capture-text refused`);
  - `<key>.raw` exists but is not a usable file (a symlink out of the cache, a FIFO or device,
    a file with more than one hard link, unreadable): a refused row — the `.txt` sidecar is not
    a fallback for it;
  - otherwise `<key>.txt`, read as UTF-8 (errors replaced) with universal newlines;
  - neither: a refused row (`no defined text form`).
A capture file is read only when it is a regular file with one hard link whose real path lies
inside the cache and whose size is at most 64 MiB (checked on the opened descriptor, before any
content is read); a derived form over 64 MiB chars is refused after it is built (capture-text
bounds the inflated part at 256 MiB, so peak memory is not bounded by the 64 MiB form cap).
`capture_sha256` is the digest of the FILE read (`.raw` or `.txt`). The quote must occur
exactly once in the form (overlapping occurrences count), else the row is refused. The span is
`form[max(0, off-80) : off+len(quote)+80]`, the `offset` column its start; the span file is
`spans/<id>-<n>.txt` (n counts that id's rows in input order).

Input: UTF-8 TSV (a BOM is accepted; lines split on LF, CRLF or CR only) with header `id url quote entry`, one quote per row, no NUL byte, ids `S` + 3 ASCII digits, an `entry` that is lane-relative (no leading `/`, no backslash, no drive letter, no `..`). Output (DIR): `spans.tsv`, header
`id url capture_sha256 offset span_file quote entry` (the 7 columns `tools/inference-ground.py`
reads), and the span files. A refused row prints `build-spans: refused <id>: <reason>` on
stderr; any refusal writes nothing and exits 1. Each written row prints
`QUOTE <id> char <N> <span_file>`, N = offset + the quote's position in its span (the value a
Registry `anchor` cell's `char N` must equal). `--check` re-derives every row and compares it
with the manifest and span files already in DIR, writing nothing, and prints
`SPANS_ROWS=n STALE=k`; it exits 2 on a symlinked or unreadable output.

Output safety (round 61). DIR, DIR/spans and the files inside are opened through directory
descriptors (`O_NOFOLLOW`, `dir_fd`), so a path swapped for a link after the checks is not
followed. A build refuses, exit 2 and nothing written or removed, when: DIR is a symlink or not a
directory; `DIR/spans` is a symlink or not a directory; `DIR/spans.tsv` is a symlink or not a
regular file; any `DIR/spans/S###-N.txt` is not a regular file; or DIR already holds a
`spans.tsv` that differs from this run's, a span file this run does not write, or a leftover
`.tmp` file of an interrupted run, unless `--replace` is given (an identical rebuild with none of
those present is always allowed; `--replace` removes the orphans and leftovers last). Files are
written by temp file + `os.replace` (span files first, then `spans.tsv`), so a run that fails
after the span files leaves the OLD manifest beside new spans — `--check` reports it and a rerun
with `--replace` recovers; a manifest is never written before its span files. Linux/POSIX only.

Usage:
  python3 tools/build-spans.py --quotes Q.tsv --out DIR [--cache DIR] [--check] [--replace]
Exit codes: 0 built / no stale row · 1 a row refused or STALE>0 · 2 usage/env, an unreadable
quotes file, or an output refusal above.
"""
from __future__ import annotations

import argparse
import errno
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
ID_RE = re.compile(r"S[0-9]{3}")
SPAN_RE = re.compile(r"S[0-9]{3}-[0-9]+\.txt")
TMP_RE = re.compile(r"\.(?:S[0-9]{3}-[0-9]+\.txt|spans\.tsv)\.[0-9a-f]{12}\.tmp")
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
ZIP = b"PK\x03\x04"
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC


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

    def _open(self, p: pathlib.Path):
        """('absent',) | ('bad', reason) | ('ok', real path, bytes read whole) — head only for .raw."""
        if not os.path.lexists(p):
            return ("absent",)
        real = os.path.realpath(p)
        if os.path.commonpath([real, self.root]) != self.root:
            return ("bad", f"{p.name} resolves outside the cache")
        try:
            fd = os.open(real, os.O_RDONLY | os.O_NONBLOCK | os.O_CLOEXEC)
        except OSError as e:
            return ("bad", f"{p.name} unreadable ({e.strerror})")
        try:
            st = os.fstat(fd)
            if not stat.S_ISREG(st.st_mode):
                return ("bad", f"{p.name} is not a regular file")
            if st.st_nlink != 1:
                return ("bad", f"{p.name} has {st.st_nlink} hard links")
            return ("ok", real, st.st_size, fd)
        except BaseException:
            os.close(fd)
            raise

    def get(self, url: str) -> tuple[str | None, str, str]:
        """(form or None, file digest, reason/name)."""
        if url in self.memo:
            return self.memo[url]
        raw, txt = self.cache / f"{key(url)}.raw", self.cache / f"{key(url)}.txt"
        r, t = self._open(raw), self._open(txt)
        try:
            self.memo[url] = res = self._decide(url, raw, txt, r, t)
        finally:
            for o in (r, t):
                if o[0] == "ok":
                    os.close(o[3])
        return res

    def _decide(self, url, raw, txt, r, t) -> tuple[str | None, str, str]:
        if r[0] == "bad":
            return None, "", r[1]
        if r[0] == "ok":
            try:
                head = os.pread(r[3], 8, 0)
            except OSError as e:
                return None, "", f"{raw.name} unreadable ({e.strerror})"
            if head[:8] == OLE or head[:4] == ZIP:
                return self._read(r, raw.name, lambda b: self._ct_form(r[1]))
        if t[0] == "ok":
            return self._read(t, txt.name,
                              lambda b: b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n"))
        if t[0] == "bad":
            return None, "", t[1]
        return None, "", f"no defined text form for {key(url)} (raw neither OLE nor zip, no .txt)"

    def _ct_form(self, real: str) -> str:
        if self.ct is None:
            try:
                self.ct = _capture_text()
            except Exception as e:
                print(f"build-spans: cannot load tools/capture-text.py: {e}", file=sys.stderr)
                sys.exit(2)
        return self.ct.text_form(real)

    def _read(self, o, name, to_form) -> tuple[str | None, str, str]:
        _, real, size, fd = o
        if size > MAX_CAPTURE:
            return None, "", f"{name} is {size} bytes, over the {MAX_CAPTURE}-byte capture cap"
        try:
            b = os.pread(fd, MAX_CAPTURE + 1, 0)
        except OSError as e:
            return None, "", f"unreadable capture {name} ({e.strerror})"
        if len(b) > MAX_CAPTURE:
            return None, "", f"{name} grew past the {MAX_CAPTURE}-byte capture cap while read"
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
    try:
        text = path.read_text(encoding="utf-8-sig")
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    except (OSError, UnicodeDecodeError) as e:
        print(f"build-spans: cannot read {path}: {e}", file=sys.stderr)
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
        if any("\x00" in c for c in (sid, url, quote, entry)):
            bad.append(f"line {n}: a cell holds a NUL byte")
        elif not ID_RE.fullmatch(sid):
            bad.append(f"line {n}: id {sid!r} is not S###")
        elif url_of.setdefault(sid, url) != url:
            bad.append(f"line {n}: {sid} names {url}, earlier rows name {url_of[sid]}")
        elif entry.startswith("/") or "\\" in entry or re.match(r"[A-Za-z]:", entry) or ".." in pathlib.PurePath(entry).parts:
            bad.append(f"line {n}: entry {entry!r} must be lane-relative")
        else:
            rows.append((sid, url, quote, entry))
    if bad:
        for b in bad:
            print(f"build-spans: {path} {b}", file=sys.stderr)
        sys.exit(2)
    return rows


def occurrences(text: str, quote: str) -> tuple[int, int]:
    """(count capped at 2, first offset), overlapping occurrences counted."""
    first = text.find(quote)
    if first < 0:
        return 0, -1
    return (2 if text.find(quote, first + 1) >= 0 else 1), first


def build(rows, forms: Forms) -> tuple[list[str], dict[str, str], list[int]]:
    lines, files, chars, refused = [OUT_HEADER], {}, [], []
    seen: dict[str, int] = {}
    for sid, url, quote, entry in rows:
        text, digest, why = forms.get(url)
        if text is None:
            refused.append(f"{sid}: {why}")
            continue
        n, off = occurrences(text, quote)
        if n != 1:
            refused.append(f"{sid}: quote occurs {'0' if n == 0 else '2+'}x in {why}: {quote[:60]!r}")
            continue
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


class Refusal(Exception):
    """An output refusal: exit 2, nothing written or removed."""


def _lstat(name: str, dfd: int):
    try:
        return os.stat(name, dir_fd=dfd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def _open_dir(name: str, dfd: int):
    """The directory `name` under dfd (no link followed), or None when absent; Refusal otherwise."""
    try:
        return os.open(name, DIR_FLAGS, dir_fd=dfd)
    except FileNotFoundError:
        return None
    except OSError as e:
        if e.errno in (errno.ELOOP, errno.ENOTDIR):
            raise Refusal(f"{name} is a symlink or not a directory")
        raise Refusal(f"{name} cannot be opened ({e.strerror})")


def _read_file(name: str, dfd: int) -> bytes:
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=dfd)
    except OSError as e:
        raise Refusal(f"{name} cannot be read ({e.strerror})")
    with os.fdopen(fd, "rb") as f:
        return f.read()


def _open_out(out: pathlib.Path) -> int:
    try:
        st = os.lstat(out)
    except FileNotFoundError:
        try:
            out.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise Refusal(f"{out} cannot be created ({e.strerror})")
    else:
        if stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode):
            raise Refusal(f"{out} is a symlink or not a directory")
    try:
        return os.open(out, DIR_FLAGS)
    except OSError as e:
        raise Refusal(f"{out} cannot be opened ({e.strerror})")


def _scan(dfd: int, what: str):
    try:
        return sorted(os.listdir(dfd))
    except OSError as e:
        raise Refusal(f"{what} cannot be listed ({e.strerror})")


def guard(ofd: int, sfd, manifest: bytes, files: dict[str, str], replace: bool):
    """Inspect without changing: the (dir fd, name) pairs to remove last, or raise Refusal."""
    mst = _lstat("spans.tsv", ofd)
    differs = False
    if mst is not None:
        if not stat.S_ISREG(mst.st_mode):
            raise Refusal("spans.tsv is a symlink or not a regular file")
        differs = _read_file("spans.tsv", ofd) != manifest
    stale = []
    for name in _scan(ofd, "output directory"):
        if TMP_RE.fullmatch(name):
            stale.append((ofd, name))
    if sfd is not None:
        for name in _scan(sfd, "spans directory"):
            if SPAN_RE.fullmatch(name) or TMP_RE.fullmatch(name):
                st = _lstat(name, sfd)
                if st is None or not stat.S_ISREG(st.st_mode):
                    raise Refusal(f"spans/{name} is not a regular file")
                if TMP_RE.fullmatch(name) or f"spans/{name}" not in files:
                    stale.append((sfd, name))
    if (differs or stale) and not replace:
        what = "a different spans.tsv" if differs else f"{len(stale)} span or temp file(s) this run does not write"
        raise Refusal(f"output already holds {what}; pass --replace to overwrite it")
    return stale


def _atomic_write(dfd: int, name: str, data: bytes) -> None:
    tmp = f".{name}.{secrets.token_hex(6)}.tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o644, dir_fd=dfd)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, name, src_dir_fd=dfd, dst_dir_fd=dfd)
    except BaseException:
        try:
            os.unlink(tmp, dir_fd=dfd)
        except OSError:
            pass
        raise


def write_out(out: pathlib.Path, lines: list[str], files: dict[str, str], replace: bool) -> int:
    manifest = ("\n".join(lines) + "\n").encode("utf-8")
    ofd = sfd = None
    try:
        ofd = _open_out(out)
        sfd = _open_dir("spans", ofd)
        stale = guard(ofd, sfd, manifest, files, replace)
        if sfd is None:
            try:
                os.mkdir("spans", 0o755, dir_fd=ofd)
            except FileExistsError:
                raise Refusal("spans appeared during the run")
            sfd = _open_dir("spans", ofd)
            if sfd is None:
                raise Refusal("spans vanished during the run")
        for name, body in files.items():
            _atomic_write(sfd, name.split("/", 1)[1], body.encode("utf-8"))
        _atomic_write(ofd, "spans.tsv", manifest)
        for dfd, name in stale:
            os.unlink(name, dir_fd=dfd)
    except Refusal as e:
        print(f"build-spans: refused output: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"build-spans: write failed under {out}: {e}", file=sys.stderr)
        return 2
    finally:
        for fd in (sfd, ofd):
            if fd is not None:
                os.close(fd)
    return 0


def check(out: pathlib.Path, lines: list[str], files: dict[str, str]) -> int:
    ofd = sfd = None
    try:
        try:
            ofd = _open_out(out) if os.path.lexists(out) else None
            sfd = _open_dir("spans", ofd) if ofd is not None else None
        except Refusal as e:
            print(f"build-spans: cannot check {out}: {e}", file=sys.stderr)
            return 2
        cur: list[str] = []
        if ofd is not None:
            mst = _lstat("spans.tsv", ofd)
            if mst is not None:
                if not stat.S_ISREG(mst.st_mode):
                    print(f"build-spans: cannot check {out}: spans.tsv is a symlink or not a regular file", file=sys.stderr)
                    return 2
                try:
                    cur = _read_file("spans.tsv", ofd).decode("utf-8").splitlines()
                except (Refusal, UnicodeDecodeError) as e:
                    print(f"build-spans: cannot read {out}/spans.tsv: {e}", file=sys.stderr)
                    return 2
        stale = 0
        if not cur or cur[0] != OUT_HEADER:
            print("SPANS_HEADER_STALE")
            stale += 1
        for i, want in enumerate(lines[1:], start=1):
            name = want.split("\t")[4]
            if i >= len(cur) or cur[i] != want:
                print(f"SPANS_ROW_STALE {name}")
                stale += 1
                continue
            try:
                got = _read_file(name.split("/", 1)[1], sfd) if sfd is not None else None
            except Refusal:
                got = None
            if got != files[name].encode("utf-8"):
                print(f"SPANS_FILE_STALE {name}")
                stale += 1
        for extra in cur[len(lines):]:
            cells = extra.split("\t")
            print(f"SPANS_ROW_EXTRA {cells[4] if len(cells) > 4 else extra[:40]}")
            stale += 1
        if sfd is not None:
            try:
                names = _scan(sfd, "spans directory")
            except Refusal as e:
                print(f"build-spans: cannot check {out}: {e}", file=sys.stderr)
                return 2
            for n in names:
                if SPAN_RE.fullmatch(n) and f"spans/{n}" not in files:
                    print(f"SPANS_FILE_ORPHAN spans/{n}")
                    stale += 1
        print(f"SPANS_ROWS={len(lines) - 1} STALE={stale}")
        return 0 if stale == 0 else 1
    finally:
        for fd in (sfd, ofd):
            if fd is not None:
                os.close(fd)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quotes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache", default=str(DEFAULT_CACHE))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()
    if not a.out.strip():
        print("build-spans: --out must name a directory", file=sys.stderr)
        return 2
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
