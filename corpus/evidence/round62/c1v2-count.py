#!/usr/bin/env python3
"""R62-C1 frozen counter (v2) — output safety of the lane span builder, hardened against detection.

Counter contract R62-C1K (cited by claims.md; the claim predicate R62-C1 is the one in c1v2-battery.py): run on a builder B
(default `tools/build-spans.py`) copied beside the lane's `tools/capture-text.py` into 20 fresh
fixture directories, each leg run twice — a `plain` profile (the round-61 layout) and a `neutral`
profile (random directory, builder, quotes, cache and output names, random URL host shape, random
extra environment variables, LANG, PATH order and file-size limit, an empty cwd outside the
fixture, a closed-pipe stdin, stdout and stderr as pipes) — inside a fresh unprivileged PID/user namespace (`unshare -Ufp
--kill-child --mount-proc`, so no process of the leg outlives it and the builder cannot see the
counter or its other ancestors) under a 200 MiB address-space limit, B exits and leaves the file tree
as each leg states in BOTH profiles — counted `LEGS=20/20 C1V2=PASS`. A leg's verdict comes from the
child's exit code, its file tree and its peak RSS only; the counter never searches the child's output
for a token (QUALITY 117), and the leg order and fixture contents come from a seed the counter reads
from the environment (`C1V2_SEED`), never from its argv.

  P01 TXT      a `.txt` capture, three rows (two ids, one id twice): exit 0, the output tree equals
               the counter's own golden tree byte for byte (manifest, span files, nothing else).
  P02 DOCX     a minimal `.docx` capture: exit 0 and the golden tree.
  P03 NOPYC    after P02 the builder's `tools/` listing is unchanged (no `__pycache__` written).
  P04 CHECK    `--check` on a golden tree: exit 0; after one span byte is changed: exit 1.
  P05 REFUSEROW a quote absent from the form: exit 1 and no file written.
  P06 REBUILD  the same build twice into one DIR: both exit 0, the golden tree.
  H07 FOREIGN  DIR holds a different `spans.tsv` (alone, then with span files): exit 2 each time,
               tree unchanged.
  H08 REPLACE  the same input with `--replace`: exit 0, golden tree plus the non-span file kept.
  H09 ORPHAN   DIR holds only a span file the run does not write: exit 2, tree unchanged.
  H10 SPANSLINK `DIR/spans` is a symlink to a victim directory: the victim tree is unchanged and
               (exit non-zero, or `DIR/spans` is no longer a symlink and the tree is golden).
  H11 FILELINK a span file path is a symlink to a victim file: the victim bytes are unchanged and
               (exit non-zero, or the path is a regular file and the tree is golden).
  H12 TSVLINK  `DIR/spans.tsv` is a symlink to a victim file: same rule.
  H13 OUTSIDE  the cache `.txt` is a symlink to a file outside the cache: exit non-zero and no
               output file holds that file's marker.
  H14 BIGTXT   a 192 MiB sparse `.txt`: exit non-zero, nothing written, peak RSS under 96 MiB.
  H15 BIGRAW   a 192 MiB sparse OLE-magic `.raw`: same.
  H16 OUTFILE  `--out` is a regular file: exit 2 and the file unchanged.
  H17 UNREADABLE the `.txt` is mode 000: exit 1 or 2 and nothing written.
  H18 FIFO     the `.txt` is a FIFO: exit 1 or 2 inside the timeout, nothing written.
  H19 ENTRYDOT an `entry` cell `../x`: exit 2 and nothing written.
  H20 BIGFORM  a `.docx` of 70 MiB of paragraph text (a few hundred KiB on disk): exit non-zero, nothing
               written, no timeout (the text form is over 64 MiB chars).

Every run has a 60 s timeout (a timeout fails the leg), a file-size limit on the child, a 200 MiB
address-space limit, a fresh PID namespace torn down by the kernel when the builder exits, and a 64 KiB
read of its stderr. The order of the leg groups is a seeded shuffle. The `.txt` text form is the UTF-8
decode with universal newlines; the `.docx` form is each `w:p` paragraph's text plus a newline; the
golden manifest and span files follow the builder docstring's contract (span = form[max(0,off-80) :
off+len(quote)+80], offset = its start, file `spans/<id>-<n>.txt`, digest of the file read).

Usage: [C1V2_SEED=N] python3 corpus/evidence/round62/c1v2-count.py [--builder PATH] --work DIR [--receipt OUT.json]
`--work` must be absent or empty (fixtures live under it; sparse files 192 MiB each; deleted unless
`--keep`). Exit codes: 0 C1V2=PASS · 1 C1V2=FAIL · 2 usage/env (including no unprivileged user namespace).

Named limits (disclosed before data): a builder that detects the sandbox itself (NSpid in /proc/self/status,
`getpid() == 1`), a feature neither profile varies (the capture-text.py file name, the `S###` id shape, the
quote vocabulary) or the leg's content, or that waits out the counter, is not stopped; a builder that keeps
a 192 MiB read in shared memory below the address-space limit is not measured.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import random
import resource
import signal
import secrets
import shutil
import stat
import subprocess
import sys
import threading
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
DEFAULT_BUILDER = LANE / "tools" / "build-spans.py"
CAPTURE_TEXT = LANE / "tools" / "capture-text.py"
TIMEOUT = 60
OLD_NS = 978307200 * 10**9  # 2001-01-01, so any write moves a victim file's mtime
CONTEXT = 80
BIG = 192 << 20
RSS_LIMIT_KIB = 96 << 10
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
LEG_NAMES = ["P01 TXT", "P02 DOCX", "P03 NOPYC", "P04 CHECK", "P05 REFUSEROW", "P06 REBUILD",
             "H07 FOREIGN", "H08 REPLACE", "H09 ORPHAN", "H10 SPANSLINK", "H11 FILELINK",
             "H12 TSVLINK", "H13 OUTSIDE", "H14 BIGTXT", "H15 BIGRAW", "H16 OUTFILE",
             "H17 UNREADABLE", "H18 FIFO", "H19 ENTRYDOT", "H20 BIGFORM"]
OUT_HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
IN_HEADER = "id\turl\tquote\tentry"


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def snap(root: pathlib.Path, mtime: bool = False) -> dict:
    """relpath -> ('f', sha[, mtime_ns]) | ('l', target) | ('d',) without following links."""
    out = {}
    if not os.path.lexists(root):
        return {"<absent>": ("x",)}
    if not root.is_dir() or root.is_symlink():
        return {".": ("l", os.readlink(root)) if root.is_symlink() else ("f", sha(root.read_bytes()))
                + ((os.lstat(root).st_mtime_ns,) if mtime else ())}
    for dp, dns, fns in os.walk(root, followlinks=False):
        d = pathlib.Path(dp)
        for n in dns:
            p = d / n
            rel = str(p.relative_to(root))
            out[rel] = ("l", os.readlink(p)) if p.is_symlink() else ("d",)
        for n in fns:
            p = d / n
            rel = str(p.relative_to(root))
            if p.is_symlink():
                out[rel] = ("l", os.readlink(p))
            else:
                st = os.lstat(p)
                out[rel] = (("f", sha(p.read_bytes())) + ((st.st_mtime_ns,) if mtime else ())) if stat.S_ISREG(st.st_mode) else ("o",)
    return out


def tree_of(files: dict[str, bytes]) -> dict:
    t = {}
    for rel, b in files.items():
        parts = pathlib.PurePath(rel).parts
        for i in range(1, len(parts)):
            t["/".join(parts[:i])] = ("d",)
        t[rel] = ("f", sha(b))
    return t


PROFILE = {"name": "plain"}  # set by main() before each leg run: plain | neutral
PROFILES = ["plain", "neutral"]
SANDBOX = ["unshare", "-Ufp", "--kill-child", "--mount-proc"]
AS_LIMIT = 200 << 20


class Fx:
    """One fixture. plain: <dir>/tools/build-spans.py, cache/, q.tsv, out/, cwd = <dir>. neutral: random names for
    every one of those, the cwd an empty directory outside the fixture, random environment and limits."""

    def __init__(self, work: pathlib.Path, rng: random.Random, builder: pathlib.Path):
        self.rng = rng
        self.profile = PROFILE["name"]
        neutral = self.profile == "neutral"
        self.dir = work / (f"{self._rw()}-{secrets.token_hex(3)}" if neutral else f"leg-{secrets.token_hex(6)}")
        tools = self._rw() + "lib" if neutral else "tools"
        self.cache_name = self._rw() if neutral else "cache"
        self.q_name = self._rw() + ".dat" if neutral else "q.tsv"
        self.out_name = self._rw() if neutral else "out"
        self.builder_name = self._rw() + ".py" if neutral else "build-spans.py"
        self.toolsdir = self.dir / tools
        self.toolsdir.mkdir(parents=True)
        (self.dir / self.cache_name).mkdir()
        self.builder_path = self.toolsdir / self.builder_name
        shutil.copyfile(builder, self.builder_path)
        shutil.copyfile(CAPTURE_TEXT, self.toolsdir / "capture-text.py")
        self.tools0 = sorted(p.name for p in self.toolsdir.iterdir())
        self.out = self.dir / self.out_name
        self.cache = self.dir / self.cache_name
        self.qpath = self.dir / self.q_name
        if neutral:
            self.cwd = work / f"cwd-{secrets.token_hex(4)}"
            self.cwd.mkdir()
        else:
            self.cwd = self.dir
        self.rows: list[tuple[str, str, str, str]] = []
        self.forms: dict[str, tuple[str, bytes]] = {}  # url -> (form, capture file bytes)

    def _rw(self) -> str:
        return "".join(secrets.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(secrets.choice(range(4, 9))))

    def word(self) -> str:
        return "".join(self.rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(self.rng.randint(3, 9)))

    def para(self, n: int) -> str:
        return " ".join(self.word() for _ in range(n))

    def new_url(self) -> str:
        if self.profile == "neutral":
            return f"https://{self._rw()}.{self._rw()}.test/{self._rw()}/{secrets.token_hex(2)}"
        return f"https://r61-{secrets.token_hex(5)}.example.invalid/{secrets.token_hex(4)}"

    def new_id(self, used) -> str:
        while True:
            s = f"S{self.rng.randint(100, 899)}"
            if s not in used:
                return s

    def quote_for(self) -> str:
        return f"{self.word()} {self.word()} {self.rng.choice(['药品临床', '证据链', 'chain', 'anchor'])} {self.word()}{self.rng.randint(10, 99)}"

    def txt_source(self, quotes: list[str]) -> tuple[str, bytes]:
        pieces = []
        for q in quotes:
            pieces.append(self.para(self.rng.randint(14, 24)))
            pieces.append(q)
        pieces.append(self.para(self.rng.randint(14, 24)))
        crlf = self.rng.random() < 0.5
        body = ("\r\n" if crlf else "\n").join(" ".join(self.para(3) for _ in range(1)) + " " + p for p in pieces)
        raw = body.encode("utf-8")
        form = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        return form, raw

    def add_txt_capture(self, quotes: list[str]) -> str:
        url = self.new_url()
        form, raw = self.txt_source(quotes)
        (self.cache / f"{key(url)}.txt").write_bytes(raw)
        self.forms[url] = (form, raw)
        return url

    def add_docx_capture(self, quotes: list[str]) -> str:
        url = self.new_url()
        paras = []
        for q in quotes:
            paras.append(self.para(self.rng.randint(14, 24)))
            paras.append(f"{self.para(3)} {q} {self.para(4)}")
        paras.append(self.para(self.rng.randint(14, 24)))
        form = "".join(p + "\n" for p in paras)
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               f'<w:document xmlns:w="{ns}"><w:body>'
               + "".join(f"<w:p><w:r><w:t>{p}</w:t></w:r></w:p>" for p in paras)
               + "</w:body></w:document>")
        rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                '</Relationships>')
        ctypes = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                  '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                  '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                  '<Default Extension="xml" ContentType="application/xml"/></Types>')
        p = self.cache / f"{key(url)}.raw"
        with zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", ctypes)
            z.writestr("_rels/.rels", rels)
            z.writestr("word/document.xml", doc)
        self.forms[url] = (form, p.read_bytes())
        return url

    def write_quotes(self, rows) -> pathlib.Path:
        q = self.qpath
        q.write_text(IN_HEADER + "\n" + "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")
        return q

    def golden(self, rows) -> dict[str, bytes]:
        lines, files, seen = [OUT_HEADER], {}, {}
        for sid, url, quote, entry in rows:
            form, raw = self.forms[url]
            assert form.count(quote) == 1, (sid, "fixture quote not unique")
            off = form.find(quote)
            seen[sid] = seen.get(sid, 0) + 1
            name = f"spans/{sid}-{seen[sid]}.txt"
            start = max(0, off - CONTEXT)
            files[name] = form[start:off + len(quote) + CONTEXT].encode("utf-8")
            lines.append("\t".join([sid, url, sha(raw), str(start), name, quote, entry]))
        files["spans.tsv"] = ("\n".join(lines) + "\n").encode("utf-8")
        return files

    def two_url_rows(self, docx: bool = False):
        """Rows: id A twice on url1, id B once on url2. Returns rows."""
        used = set()
        a, b = self.new_id(used), None
        used.add(a)
        b = self.new_id(used)
        q1, q2, q3 = self.quote_for(), self.quote_for(), self.quote_for()
        u1 = self.add_docx_capture([q1, q2]) if docx else self.add_txt_capture([q1, q2])
        u2 = self.add_txt_capture([q3])
        entry = "corpus/knowledge/x.md"
        return [(a, u1, q1, entry), (a, u1, q2, entry), (b, u2, q3, entry)]


def _env_and_limits(fx: Fx) -> tuple[dict, int, int]:
    base_path = os.environ.get("PATH", "/usr/bin:/bin")
    if fx.profile != "neutral":
        return ({"PATH": base_path, "HOME": str(fx.dir), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}, 512 << 20, AS_LIMIT)
    parts = base_path.split(":")
    secrets.SystemRandom().shuffle(parts)
    env = {"PATH": ":".join(parts), "HOME": str(fx.cwd), "LANG": secrets.choice(["C", "POSIX", "C.UTF-8"])}
    if secrets.randbelow(2):
        env["LC_ALL"] = secrets.choice(["C", "C.UTF-8"])
    for _ in range(secrets.choice(range(4, 10))):
        env[fx._rw().upper() + secrets.choice(["", "_X", "_HOME"])] = secrets.token_hex(secrets.choice(range(2, 12)))
    return env, secrets.choice([384 << 20, 768 << 20, 1 << 30]), AS_LIMIT + (secrets.choice(range(0, 25)) << 20)


def run(fx: Fx, extra: list[str], out: pathlib.Path | None = None, rows_path: pathlib.Path | None = None,
        check: bool = False) -> dict:
    out = out or fx.out
    argv = SANDBOX + [sys.executable, str(fx.builder_path), "--quotes", str(rows_path or fx.qpath),
                      "--out", str(out), "--cache", str(fx.cache)] + extra
    env, fsize, aslim = _env_and_limits(fx)
    neutral = fx.profile == "neutral"
    if neutral:
        rfd, wfd = os.pipe()
        os.close(wfd)
        stdin = rfd
    else:
        rfd, stdin = None, subprocess.DEVNULL

    def limits():
        resource.setrlimit(resource.RLIMIT_FSIZE, (fsize, fsize))
        resource.setrlimit(resource.RLIMIT_AS, (aslim, aslim))

    if neutral:  # pipes, drained by threads that keep the first 64 KiB of stderr and discard the rest
        keep: list[bytes] = []

        def drain(stream, store):
            seen = 0
            while True:
                chunk = stream.read(65536)
                if not chunk:
                    return
                if store is not None and seen < 65536:
                    store.append(chunk[:65536 - seen])
                seen += len(chunk)

        p = subprocess.Popen(argv, cwd=fx.cwd, env=env, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             start_new_session=True, preexec_fn=limits)
        os.close(rfd)
        readers = [threading.Thread(target=drain, args=(p.stdout, None), daemon=True),
                   threading.Thread(target=drain, args=(p.stderr, keep), daemon=True)]
        for t in readers:
            t.start()
        timer = threading.Timer(TIMEOUT, lambda: os.killpg(p.pid, signal.SIGKILL))
        timer.start()
        try:
            _, status, ru = os.wait4(p.pid, 0)
        finally:
            timer.cancel()
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        for t in readers:
            t.join(10)
        err = b"".join(keep).decode("utf-8", errors="replace")
    else:
        so, se = fx.dir / f"so-{secrets.token_hex(3)}", fx.dir / f"se-{secrets.token_hex(3)}"
        with open(so, "wb") as fo, open(se, "wb") as fe:
            p = subprocess.Popen(argv, cwd=fx.cwd, env=env, stdin=stdin, stdout=fo, stderr=fe,
                                 start_new_session=True, preexec_fn=limits)
            timer = threading.Timer(TIMEOUT, lambda: os.killpg(p.pid, signal.SIGKILL))
            timer.start()
            try:
                _, status, ru = os.wait4(p.pid, 0)
            finally:
                timer.cancel()
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
        with open(se, "rb") as fh:
            err = fh.read(65536).decode("utf-8", errors="replace")
        so.unlink()
        se.unlink()
    rc = os.waitstatus_to_exitcode(status)
    p.returncode = rc
    return {"rc": rc, "stderr": err, "rss_kib": ru.ru_maxrss, "timeout": rc == -9}


def tools_unchanged(fx: Fx) -> bool:
    return sorted(p.name for p in fx.toolsdir.iterdir()) == fx.tools0


def clean_out(fx: Fx, extra_ok=()) -> bool:
    """Nothing written: out absent, or an empty directory (spans/ may exist empty)."""
    if not os.path.lexists(fx.out):
        return True
    if not fx.out.is_dir() or fx.out.is_symlink():
        return False
    return all(v[0] == "d" for v in snap(fx.out).values())


# ---- legs ---------------------------------------------------------------------------------

def leg_p01(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    r = run(fx, [])
    ok = r["rc"] == 0 and snap(fx.out) == tree_of(fx.golden(rows))
    return ok, f"rc={r['rc']}"


def leg_p02_p03(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows(docx=True)
    fx.write_quotes(rows)
    r = run(fx, [])
    ok2 = r["rc"] == 0 and snap(fx.out) == tree_of(fx.golden(rows))
    ok3 = tools_unchanged(fx)
    return (ok2, f"rc={r['rc']}"), (ok3, f"tools={sorted(p.name for p in fx.toolsdir.iterdir())}")


def leg_p04(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    r0 = run(fx, [])
    r1 = run(fx, ["--check"])
    victim = sorted((fx.out / "spans").iterdir())[0]
    victim.write_bytes(victim.read_bytes() + b"x")
    r2 = run(fx, ["--check"])
    return (r0["rc"] == 0 and r1["rc"] == 0 and r2["rc"] == 1), f"rc={r0['rc']},{r1['rc']},{r2['rc']}"


def leg_p05(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    sid, url, q, e = rows[0]
    rows[0] = (sid, url, q + " absent" + secrets.token_hex(3), e)
    fx.write_quotes(rows)
    r = run(fx, [])
    return (r["rc"] == 1 and clean_out(fx)), f"rc={r['rc']}"


def leg_p06(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    g = tree_of(fx.golden(rows))
    r0 = run(fx, [])
    s0 = snap(fx.out)
    r1 = run(fx, [])
    return (r0["rc"] == 0 and r1["rc"] == 0 and s0 == g and snap(fx.out) == g), f"rc={r0['rc']},{r1['rc']}"


def prior_state(fx: Fx, rng, spans: bool = True):
    """A different earlier build placed in fx.out by hand: returns (files dict written)."""
    sid = fx.new_id(set())
    f = {
        "spans.tsv": (OUT_HEADER + "\n" + "\t".join([sid, "https://prior.example.invalid/x", "0" * 64, "0",
                                                      f"spans/{sid}-1.txt", "old " + fx.word(), "corpus/knowledge/old.md"]) + "\n").encode(),
        f"spans/{sid}-1.txt": ("old span " + fx.word()).encode(),
        "spans/S404-9.txt": ("keep me " + fx.word()).encode(),
    }
    if not spans:
        f = {k: v for k, v in f.items() if k == "spans.tsv"}
    for rel, bts in f.items():
        p = fx.out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(bts)
        os.utime(p, ns=(OLD_NS, OLD_NS))
    return f


def leg_h07_h08(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    prior_state(fx, rng, spans=False)
    before_a = snap(fx.out, True)
    ra = run(fx, [])
    same_a = ra["rc"] == 2 and snap(fx.out, True) == before_a
    shutil.rmtree(fx.out)
    prior_state(fx, rng)
    readme = fx.out / "README.txt"
    readme.write_bytes(b"not a span file " + fx.word().encode())
    os.utime(readme, ns=(OLD_NS, OLD_NS))
    before = snap(fx.out, True)
    r0 = run(fx, [])
    ok7 = same_a and r0["rc"] == 2 and snap(fx.out, True) == before
    r1 = run(fx, ["--replace"])
    want = tree_of(fx.golden(rows))
    want["README.txt"] = ("f", sha(readme.read_bytes()))
    ok8 = r1["rc"] == 0 and snap(fx.out) == want
    return (ok7, f"rc={ra['rc']},{r0['rc']}"), (ok8, f"rc={r1['rc']}")


def leg_h09(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    p = fx.out / "spans" / "S404-9.txt"
    p.parent.mkdir(parents=True)
    p.write_bytes(b"orphan " + fx.word().encode())
    os.utime(p, ns=(OLD_NS, OLD_NS))
    before = snap(fx.out, True)
    r = run(fx, [])
    return (r["rc"] == 2 and snap(fx.out, True) == before), f"rc={r['rc']}"


def victim_dir(fx: Fx):
    v = fx.dir / "victim"
    v.mkdir()
    (v / "README.txt").write_bytes(b"victim " + fx.word().encode())
    (v / "IMPORTANT.txt").write_bytes(b"victim2 " + fx.word().encode())
    for n in ("README.txt", "IMPORTANT.txt"):
        os.utime(v / n, ns=(OLD_NS, OLD_NS))
    return v


def leg_h10(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    v = victim_dir(fx)
    fx.out.mkdir()
    (fx.out / "spans").symlink_to(v)
    vb = snap(v, True)
    r = run(fx, [])
    unchanged = snap(v, True) == vb
    healed = (not (fx.out / "spans").is_symlink()) and snap(fx.out) == tree_of(fx.golden(rows))
    return (unchanged and (r["rc"] != 0 or healed)), f"rc={r['rc']} victim_unchanged={unchanged}"


def leg_h11(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    victim = fx.dir / "victim.txt"
    victim.write_bytes(fx.golden(rows)[f"spans/{rows[0][0]}-1.txt"])
    os.utime(victim, ns=(OLD_NS, OLD_NS))
    vb = snap(victim, True)
    (fx.out / "spans").mkdir(parents=True)
    target = fx.out / "spans" / f"{rows[0][0]}-1.txt"
    target.symlink_to(victim)
    r = run(fx, [])
    unchanged = snap(victim, True) == vb
    healed = (not target.is_symlink()) and snap(fx.out) == tree_of(fx.golden(rows))
    return (unchanged and (r["rc"] != 0 or healed)), f"rc={r['rc']} victim_unchanged={unchanged}"


def leg_h12(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    victim = fx.dir / "victim.tsv"
    victim.write_bytes(fx.golden(rows)["spans.tsv"])
    os.utime(victim, ns=(OLD_NS, OLD_NS))
    vb = snap(victim, True)
    fx.out.mkdir()
    (fx.out / "spans.tsv").symlink_to(victim)
    r = run(fx, [])
    unchanged = snap(victim, True) == vb
    healed = (not (fx.out / "spans.tsv").is_symlink()) and snap(fx.out) == tree_of(fx.golden(rows))
    return (unchanged and (r["rc"] != 0 or healed)), f"rc={r['rc']} victim_unchanged={unchanged}"


def leg_h13(w, rng, b):
    fx = Fx(w, rng, b)
    q = fx.quote_for()
    sid = fx.new_id(set())
    url = fx.new_url()
    form, raw = fx.txt_source([q])
    marker = "OUTSIDE-" + secrets.token_hex(6)
    outside = fx.dir / "outside.txt"
    outside.write_bytes((marker + " " + raw.decode()).encode())
    (fx.cache / f"{key(url)}.txt").symlink_to(outside)
    fx.write_quotes([(sid, url, q, "corpus/knowledge/x.md")])
    r = run(fx, [])
    leaked = False
    if fx.out.is_dir():
        for dp, _, fns in os.walk(fx.out):
            for n in fns:
                if marker.encode() in (pathlib.Path(dp) / n).read_bytes():
                    leaked = True
    return (r["rc"] != 0 and not leaked), f"rc={r['rc']} leaked={leaked}"


def big_leg(w, rng, b, suffix, head):
    fx = Fx(w, rng, b)
    q = fx.quote_for()
    sid = fx.new_id(set())
    url = fx.new_url()
    p = fx.cache / f"{key(url)}.{suffix}"
    with open(p, "wb") as f:
        f.write(head + (fx.para(20) + " " + q + " " + fx.para(20)).encode())
        f.truncate(BIG)
    fx.write_quotes([(sid, url, q, "corpus/knowledge/x.md")])
    r = run(fx, [])
    ok = r["rc"] != 0 and not r["timeout"] and clean_out(fx) and r["rss_kib"] < RSS_LIMIT_KIB
    return ok, f"rc={r['rc']} rss_kib={r['rss_kib']} limit={RSS_LIMIT_KIB}"


def leg_h14(w, rng, b):
    return big_leg(w, rng, b, "txt", b"")


def leg_h15(w, rng, b):
    return big_leg(w, rng, b, "raw", OLE)


def leg_h16(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    fx.out.write_bytes(b"i am a file " + fx.word().encode())
    before = fx.out.read_bytes()
    r = run(fx, [])
    return (r["rc"] == 2 and fx.out.read_bytes() == before), f"rc={r['rc']}"


def leg_h17(w, rng, b):
    if os.geteuid() == 0:
        raise SystemExit("c1v2-count: H17 needs a non-root user (mode 000 is readable by root)")
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    url = rows[0][1]
    p = fx.cache / f"{key(url)}.txt"
    os.chmod(p, 0)
    try:
        r = run(fx, [])
        ok = r["rc"] in (1, 2) and clean_out(fx)
    finally:
        os.chmod(p, 0o600)
    return ok, f"rc={r['rc']}"


def leg_h18(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    url = rows[0][1]
    p = fx.cache / f"{key(url)}.txt"
    p.unlink()
    os.mkfifo(p)
    r = run(fx, [])
    return (r["rc"] in (1, 2) and not r["timeout"] and clean_out(fx)), f"rc={r['rc']}"


def leg_h19(w, rng, b):
    fx = Fx(w, rng, b)
    rows = fx.two_url_rows()
    sid, url, q, _ = rows[0]
    rows[0] = (sid, url, q, "../" + secrets.token_hex(3))
    fx.write_quotes(rows)
    r = run(fx, [])
    return (r["rc"] == 2 and clean_out(fx)), f"rc={r['rc']}"


def leg_h20(w, rng, b):
    fx = Fx(w, rng, b)
    q = fx.quote_for()
    sid = fx.new_id(set())
    url = fx.new_url()
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    big = "x" * (70 << 20)
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           f'<w:document xmlns:w="{ns}"><w:body><w:p><w:r><w:t>{fx.para(20)} {q} {fx.para(20)}</w:t></w:r></w:p>'
           f'<w:p><w:r><w:t>{big}</w:t></w:r></w:p></w:body></w:document>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')
    with zipfile.ZipFile(fx.cache / f"{key(url)}.raw", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)
    fx.write_quotes([(sid, url, q, "corpus/knowledge/x.md")])
    r = run(fx, [])
    return (r["rc"] != 0 and not r["timeout"] and clean_out(fx)), f"rc={r['rc']} rss_kib={r['rss_kib']}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--builder", default=str(DEFAULT_BUILDER))
    ap.add_argument("--work", required=True)
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    builder = pathlib.Path(a.builder).resolve()
    work = pathlib.Path(a.work).resolve()
    if not builder.is_file() or not CAPTURE_TEXT.is_file():
        print(f"c1v2-count: builder or capture-text missing ({builder}, {CAPTURE_TEXT})", file=sys.stderr)
        return 2
    if work.exists() and any(work.iterdir()):
        print(f"c1v2-count: --work {work} must be absent or empty", file=sys.stderr)
        return 2
    try:
        pre = subprocess.run(SANDBOX + ["true"], stdin=subprocess.DEVNULL, capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"c1v2-count: sandbox unavailable ({e})", file=sys.stderr)
        return 2
    if pre.returncode != 0:
        print(f"c1v2-count: sandbox unavailable (unshare exit {pre.returncode}); fail closed", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    env_seed = os.environ.get("C1V2_SEED")
    seed = int(env_seed) if env_seed else secrets.randbits(32)
    results: dict[str, tuple[bool, str]] = {}
    plan = [(("P01 TXT",), leg_p01), (("P02 DOCX", "P03 NOPYC"), leg_p02_p03), (("P04 CHECK",), leg_p04),
            (("P05 REFUSEROW",), leg_p05), (("P06 REBUILD",), leg_p06), (("H07 FOREIGN", "H08 REPLACE"), leg_h07_h08),
            (("H09 ORPHAN",), leg_h09), (("H10 SPANSLINK",), leg_h10), (("H11 FILELINK",), leg_h11),
            (("H12 TSVLINK",), leg_h12), (("H13 OUTSIDE",), leg_h13), (("H14 BIGTXT",), leg_h14),
            (("H15 BIGRAW",), leg_h15), (("H16 OUTFILE",), leg_h16), (("H17 UNREADABLE",), leg_h17),
            (("H18 FIFO",), leg_h18), (("H19 ENTRYDOT",), leg_h19), (("H20 BIGFORM",), leg_h20)]
    try:
        order = list(range(len(plan)))
        random.Random(seed * 7919 + 1).shuffle(order)
        for i in order:
            names, fn = plan[i]
            per_profile = []
            for pname in random.Random(seed * 104729 + i).sample(PROFILES, len(PROFILES)):
                PROFILE["name"] = pname
                rng = random.Random(seed * 31 + i * 2 + (pname == "neutral"))
                try:
                    got = fn(work / pname, rng, builder)
                except (AssertionError, SystemExit):
                    raise
                except Exception as e:  # a builder cannot crash the counter: the leg fails
                    got = tuple((False, f"counter exception {type(e).__name__}: {e}") for _ in names) if len(names) > 1 \
                        else (False, f"counter exception {type(e).__name__}: {e}")
                per_profile.append((pname, got if len(names) > 1 else (got,)))
            for j, n in enumerate(names):
                oks = [g[j][0] for _, g in per_profile]
                det = " | ".join(f"{pn}: {'ok' if g[j][0] else 'FAIL'} {g[j][1]}" for pn, g in sorted(per_profile))
                results[n] = (all(oks), det)
    except AssertionError as e:
        print(f"c1v2-count: fixture defect {e}", file=sys.stderr)
        return 2
    finally:
        if not a.keep:
            for dp, dns, fns in os.walk(work):
                for n in dns + fns:
                    try:
                        os.chmod(os.path.join(dp, n), 0o700, follow_symlinks=False)
                    except (OSError, NotImplementedError):
                        pass
            shutil.rmtree(work, ignore_errors=True)
    passed = 0
    lines = []
    for name in LEG_NAMES:
        ok, detail = results[name]
        passed += bool(ok)
        lines.append(f"LEG {name} {'pass' if ok else 'fail'} {detail}")
    verdict = passed == len(LEG_NAMES)
    print(f"BUILDER sha256={sha(builder.read_bytes())} path={builder} SEED={seed}")
    print("\n".join(lines))
    print(f"LEGS={passed}/{len(LEG_NAMES)} C1V2={'PASS' if verdict else 'FAIL'}")
    if a.receipt:
        pathlib.Path(a.receipt).write_text(json.dumps({
            "builder_sha256": sha(builder.read_bytes()), "seed": seed, "passed": passed, "total": len(LEG_NAMES),
            "legs": {k: {"ok": bool(v[0]), "detail": v[1]} for k, v in results.items()},
            "c1v2": "PASS" if verdict else "FAIL"}, indent=1) + "\n")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
