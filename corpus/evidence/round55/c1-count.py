#!/usr/bin/env python3
"""R55-C1 frozen counter — an OLE-aware span builder, `tools/build-spans.py`.

Predicate R55-C1, the same sentence as corpus/evidence/round55/claims.md:
`tools/build-spans.py --quotes Q --out DIR --cache C`, run as an ordinary
command under an audit hook that ends the run (exit 97) on any process spawn,
exec, fork, socket connect or bind, or ctypes library load, and on any file
open, directory listing or scan outside the run's work directory, the hook's
own file, the tool's own directory, the lane's `tools/` directory and the
Python installation,
writes `DIR/spans.tsv` (header
`id url capture_sha256 offset span_file quote entry`, one row per quote row of
Q, in order) and `DIR/spans/<id>-<n>.txt`, where for every row the span file
is the exact slice `form[offset:offset+len(span)]` of the document's DEFINED
text form, longer than its quote, holding the quote at char N = offset + the
quote's position in the span, with `capture_sha256` the digest of the file
read — the defined form being, for a capture whose `.raw` is an OLE compound
file or a zip, the stdout of `tools/capture-text.py` on that `.raw` (its
`.txt` sidecar is never used), and otherwise the `.txt` capture read with
universal newlines — and prints `QUOTE <id> char <N> <span_file>` per row and
exits 0; this is checked on held-out quotes the counter picks at counting time
from OLE `.doc` files it generates from fresh random text (each copied alone
into the run's cache under the key of a random URL, with no sibling file, the
generation tree deleted before the run) and from the four distinct pinned OLE
captures of the read-only campaign cache (copied with their `.txt` sidecars
under the keys of random URLs), the expected offsets held only in the
counter's memory; while a run whose rows include one with no defined form (a
`.raw` that is neither an OLE file nor a zip, and no `.txt`, though the quote
sits once in the raw's UTF-16LE decode), one whose quote is absent from the
defined form though it occurs exactly once in the capture's `.txt` sidecar or
in the raw's UTF-16LE decode, or one on an OLE file `tools/capture-text.py`
refuses (a spreadsheet) exits 1, prints a stderr line starting
`build-spans: refused <that id>`, and writes no `spans.tsv` and no span file;
and run on round 54's `quotes.tsv` (as committed at BASE_REV) against copies of
its captures it re-derives round 54's committed `spans.tsv` and span files
byte for byte — counted as legs GENOLE, OLEPIN, REFUSE, REGRESS.

The oracle is the lane's `tools/capture-text.py` pinned by sha256 (the round-54
landed tool); another digest is `ENV_CHANGED` exit 2. The pinned captures are
checked by sha256 prefix, else `ENV_CHANGED` exit 2. No expected value is
written to disk while the builder runs.

Usage: python3 corpus/evidence/round55/c1-count.py [--tool PATH] [--seed N] [--per-leg K] [--work DIR]
`--per-leg` (default 3, minimum 2) is the number of generated documents and of
quotes per pinned capture. `--work` must be empty or absent; default a mkdtemp
under $TMPDIR, removed on exit.
Exit codes: 0 C1=PASS · 1 C1=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import os
import pathlib
import random
import re
import shutil
import string
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
TOOLS = LANE / "tools"
CAPTURE_TEXT = TOOLS / "capture-text.py"
CAPTURE_TEXT_SHA = "2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573"
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
BASE_REV = "dba605deb5cd5ed4874e0e3c39ba24737409cd80"
# four distinct OLE Word captures: key -> sha256 prefix (20 hex) of the .raw
PINNED = {
    "54fe0734c01f699e735b4b0a": "d341c133e37d65f02f8f",
    "6dc68fd6b32ce9c8dfcebce8": "6063a3aff7a4081e93a6",
    "b539a80218080da56a75b624": "46d1866ce9afd51682e7",
    "bdff491a75c6abeda1d9c01d": "ac0fad62ed9a11fa3bd1",
}
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
OUT_HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
ENTRY = "corpus/knowledge/held-out.md"
HOOK = r"""
import os, sys, runpy
ALLOW = tuple(os.path.realpath(p) + os.sep for p in os.environ.pop("R55_ALLOW").split(os.pathsep) if p)
BAD = ("subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork",
       "os.forkpty", "pty.spawn", "socket.connect", "socket.bind", "ctypes.dlopen", "ctypes.dlsym",
       "ctypes.cdata")
PATHS = ("open", "os.listdir", "os.scandir")
def deny(what):
    os.write(2, ("AUDIT_FORBIDDEN " + what + "\n").encode("utf-8", "replace"))
    os._exit(97)
def allowed(p):
    if isinstance(p, int):
        return True
    if p is None:
        p = "."
    try:
        s = os.path.realpath(os.fsdecode(p))
    except Exception:
        return False
    return (s + os.sep).startswith(ALLOW)
def hook(ev, args):
    if ev in BAD:
        deny(ev)
    if ev in PATHS and args and not allowed(args[0]):
        deny(ev + " " + repr(args[0])[:200])
sys.addaudithook(hook)
tool = sys.argv[1]; sys.argv = sys.argv[1:]
runpy.run_path(tool, run_name="__main__")
"""
CJK = [chr(c) for c in range(0x4E00, 0x4E00 + 3000)]
LAT1 = list("àáâãäåçèéêëìíîïñòóôõöùúûüýÿÀÉÑÖÜß")


def env_fail(msg: str) -> None:
    print(f"ENV_CHANGED {msg}")
    sys.exit(2)


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def word(rng: random.Random) -> str:
    k = rng.random()
    if k < 0.35:
        return "".join(rng.choice(CJK) for _ in range(rng.randint(2, 6)))
    if k < 0.55:
        return "".join(rng.choice(string.ascii_lowercase + "".join(LAT1)) for _ in range(rng.randint(3, 8)))
    return "".join(rng.choice(string.ascii_letters + string.digits) for _ in range(rng.randint(3, 9)))


def sentence(rng: random.Random, n: int | None = None) -> str:
    return " ".join(word(rng) for _ in range(n or rng.randint(4, 10)))


def rand_url(rng: random.Random) -> str:
    return ("https://" + "".join(rng.choice(string.ascii_lowercase) for _ in range(10)) + ".example/d"
            + "".join(rng.choice(string.digits) for _ in range(14)))


def oracle_form(path: pathlib.Path) -> str | None:
    """The defined text form: stdout of the pinned capture-text (run by the counter, not hooked)."""
    r = subprocess.run([sys.executable, str(CAPTURE_TEXT), str(path)], capture_output=True, timeout=300,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def windows(text: str, rng: random.Random, k: int, ok) -> list[str]:
    """k distinct windows of `text` (10-24 chars, no tab/newline/U+FFFD, >= 4 letters) with ok(w)."""
    out: list[str] = []
    if len(text) < 40:
        return out
    for _ in range(20000):
        if len(out) == k:
            break
        n = rng.randint(10, 24)
        s = rng.randrange(0, len(text) - n)
        w = text[s:s + n]
        if (w != w.strip() or any(c in w for c in "\t\n\r\ufffd") or sum(c.isalpha() for c in w) < 4
                or any(ord(c) < 0x20 for c in w) or w in out):
            continue
        if ok(w):
            out.append(w)
    return out


class Ctx:
    def __init__(self, tool: str, work: pathlib.Path, rng: random.Random, k: int):
        self.tool, self.work, self.rng, self.k = tool, work, rng, k
        self.hook = work / "hook.py"
        self.hook.write_text(HOOK)
        self.prof = (work / "soffice-profile").as_uri()
        self.runs = 0

    def soffice(self, conv: str, outdir: pathlib.Path, files: list[pathlib.Path]) -> None:
        outdir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["soffice", f"-env:UserInstallation={self.prof}", "--headless", "--convert-to", conv,
                        "--outdir", str(outdir), *map(str, files)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600, check=False)

    def fresh(self, tag: str) -> pathlib.Path:
        self.runs += 1
        d = self.work / f"run{self.runs}-{''.join(self.rng.choice(string.ascii_lowercase) for _ in range(8))}"
        (d / "cache").mkdir(parents=True)
        (d / "tmp").mkdir()
        return d

    def build(self, run: pathlib.Path, rows: list[tuple[str, str, str]]) -> subprocess.CompletedProcess:
        q = run / "quotes.tsv"
        q.write_text("id\turl\tquote\tentry\n" + "".join(f"{i}\t{u}\t{t}\t{ENTRY}\n" for i, u, t in rows), encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONSTARTUP", "PYTHONHOME")}
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(run / "tmp"),
                    "R55_ALLOW": os.pathsep.join([str(run), str(self.hook), os.path.dirname(self.tool), str(TOOLS), sys.prefix,
                                                  sys.base_prefix, sys.exec_prefix])})
        return subprocess.run([sys.executable, str(self.hook), self.tool, "--quotes", str(q), "--out", str(run / "out"),
                               "--cache", str(run / "cache")], capture_output=True, timeout=300, cwd=str(run), env=env)


def gen_docs(c: Ctx, tag: str) -> list[tuple[bytes, str]]:
    """Generate k `.doc` files from random HTML; return (bytes, defined form) and delete the tree."""
    g = c.work / f"gen-{tag}-{c.rng.randrange(1 << 30)}"
    src = g / "src"
    src.mkdir(parents=True)
    for i in range(c.k):
        body = [f"<p>{html.escape(sentence(c.rng))}</p>" for _ in range(c.rng.randint(3, 6))]
        cells = "".join(f"<td>{html.escape(sentence(c.rng, 2))}</td>" for _ in range(3))
        body.append(f"<table><tr>{cells}</tr></table>")
        (src / f"g{i}.html").write_text("<html><head><meta charset=\"utf-8\"></head><body>" + "".join(body)
                                        + "</body></html>", encoding="utf-8")
    c.soffice("doc:MS Word 97", g / "doc", sorted(src.glob("*.html")))
    res = []
    for i in range(c.k):
        p = g / "doc" / f"g{i}.doc"
        if not p.is_file() or p.read_bytes()[:8] != OLE:
            env_fail(f"soffice did not write an OLE {p.name}")
        f = oracle_form(p)
        if f is None:
            env_fail(f"oracle refused generated {p.name}")
        res.append((p.read_bytes(), f))
    shutil.rmtree(g)
    return res


def pinned() -> list[tuple[str, bytes, bytes | None, str]]:
    out = []
    for k, pre in PINNED.items():
        raw = CACHE / f"{k}.raw"
        if not raw.is_file() or hashlib.sha256(raw.read_bytes()).hexdigest()[:20] != pre:
            env_fail(f"pinned capture {k} digest")
        txt = CACHE / f"{k}.txt"
        f = oracle_form(raw)
        if f is None:
            env_fail(f"oracle refused pinned {k}")
        out.append((k, raw.read_bytes(), txt.read_bytes() if txt.is_file() else None, f))
    return out


def judge(c: Ctx, r: subprocess.CompletedProcess, run: pathlib.Path,
          expect: list[tuple[str, str, str, str, bytes, int]]) -> str | None:
    """expect: (id, url, quote, form, file bytes, char N) per row, in order."""
    if r.returncode != 0:
        return f"rc={r.returncode} {r.stderr[-200:]!r}"
    m = run / "out" / "spans.tsv"
    if not m.is_file():
        return "no spans.tsv"
    lines = m.read_text(encoding="utf-8").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or lines[0] != OUT_HEADER or len(lines) != len(expect) + 1:
        return f"manifest shape {len(lines) - 1} rows"
    out = r.stdout.decode("utf-8", "replace").splitlines()
    seen: dict[str, int] = {}
    names = set()
    for line, (sid, url, quote, form, fbytes, char) in zip(lines[1:], expect):
        cells = line.split("\t")
        if len(cells) != 7:
            return f"row cells {len(cells)}"
        if (cells[0], cells[1], cells[5], cells[6]) != (sid, url, quote, ENTRY):
            return f"{sid} row echo"
        if cells[2] != hashlib.sha256(fbytes).hexdigest():
            return f"{sid} capture_sha256"
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        if cells[4] != name or not cells[3].isdigit():
            return f"{sid} span name/offset"
        names.add(name)
        sp = run / "out" / name
        span = sp.read_bytes().decode("utf-8") if sp.is_file() else ""
        o = int(cells[3])
        if form[o:o + len(span)] != span or len(span) <= len(quote):
            return f"{sid} span is not a slice of the defined form"
        if span.find(quote) < 0 or o + span.find(quote) != char:
            return f"{sid} char"
        if f"QUOTE {sid} char {char} {name}" not in out:
            return f"{sid} QUOTE line"
    have = {f"spans/{p.name}" for p in (run / "out" / "spans").glob("*")} if (run / "out" / "spans").is_dir() else set()
    if have != names:
        return "extra or missing span files"
    return None


def leg_genole(c: Ctx) -> tuple[bool, str]:
    docs = gen_docs(c, "g")
    run = c.fresh("genole")
    rows, expect = [], []
    for i, (b, form) in enumerate(docs):
        url = rand_url(c.rng)
        (run / "cache" / f"{key(url)}.raw").write_bytes(b)
        for w in windows(form, c.rng, 2, lambda w, f=form: f.count(w) == 1):
            sid = f"S{901 + i}"
            rows.append((sid, url, w))
            expect.append((sid, url, w, form, b, form.find(w)))
    if len(rows) != 2 * len(docs):
        env_fail("could not pick generated quotes")
    why = judge(c, c.build(run, rows), run, expect)
    return (why is None), (why or f"{len(docs)} docs, {len(rows)} quotes")


def leg_olepin(c: Ctx, pins) -> tuple[bool, str]:
    run = c.fresh("olepin")
    rows, expect = [], []
    for i, (k, raw, txt, form) in enumerate(pins):
        url = rand_url(c.rng)
        (run / "cache" / f"{key(url)}.raw").write_bytes(raw)
        if txt is not None:
            (run / "cache" / f"{key(url)}.txt").write_bytes(txt)
        ws = windows(form, c.rng, c.k, lambda w, f=form: f.count(w) == 1)
        if len(ws) != c.k:
            env_fail(f"could not pick quotes in {k}")
        for w in ws:
            sid = f"S{921 + i}"
            rows.append((sid, url, w))
            expect.append((sid, url, w, form, raw, form.find(w)))
    why = judge(c, c.build(run, rows), run, expect)
    return (why is None), (why or f"{len(pins)} captures, {len(rows)} quotes")


def refused_ok(r: subprocess.CompletedProcess, run: pathlib.Path, bad: str) -> str | None:
    err = r.stderr.decode("utf-8", "replace").splitlines()
    if r.returncode != 1:
        return f"rc={r.returncode}"
    if not any(l.startswith(f"build-spans: refused {bad}") for l in err):
        return f"no refusal line for {bad}"
    if (run / "out" / "spans.tsv").exists():
        return "spans.tsv written"
    if (run / "out" / "spans").is_dir() and any((run / "out" / "spans").iterdir()):
        return "span file written"
    return None


def leg_refuse(c: Ctx, pins) -> tuple[bool, str]:
    k0, raw0, txt0, form0 = pins[c.rng.randrange(len(pins))]
    good = windows(form0, c.rng, 1, lambda w: form0.count(w) == 1)
    if not good:
        env_fail("could not pick a good quote")
    cases = []
    # NOFORM: random bytes, then a UTF-16LE string at an even offset, then random bytes; no .txt
    q = sentence(c.rng, 3)
    pre = bytes(c.rng.randrange(256) for _ in range(512))
    pre = b"\x00\x01" + pre[2:]
    blob = pre + q.encode("utf-16le") + bytes(c.rng.randrange(256) for _ in range(512))
    if blob.decode("utf-16le", errors="replace").count(q) != 1:
        env_fail("NOFORM construction")
    cases.append(("NOFORM", blob, None, q))
    # SIDECAR / UTF16 on pinned captures that carry a `.txt` sidecar
    for k, raw, txt, form in pins:
        if txt is None:
            continue
        side = txt.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
        ws = windows(side, c.rng, 1, lambda w, s=side, f=form: s.count(w) == 1 and f.count(w) == 0)
        if ws:
            cases.append(("SIDECAR", raw, txt, ws[0]))
            break
    for k, raw, txt, form in pins:
        u = raw.decode("utf-16le", errors="replace")
        ws = windows(u, c.rng, 1, lambda w, s=u, f=form: s.count(w) == 1 and f.count(w) == 0)
        if ws:
            cases.append(("UTF16", raw, txt, ws[0]))
            break
    # NONWORD: an OLE spreadsheet
    g = c.work / f"gen-xls-{c.rng.randrange(1 << 30)}"
    (g / "src").mkdir(parents=True)
    cell = "".join(c.rng.choice(CJK) for _ in range(8))
    (g / "src" / "x.csv").write_text(f"{cell},{word(c.rng)}\n{word(c.rng)},{word(c.rng)}\n", encoding="utf-8")
    c.soffice("xls:MS Excel 97", g / "xls", [g / "src" / "x.csv"])
    xp = g / "xls" / "x.xls"
    if not xp.is_file() or xp.read_bytes()[:8] != OLE:
        env_fail("soffice did not write an OLE spreadsheet")
    cases.append(("NONWORD", xp.read_bytes(), None, cell))
    shutil.rmtree(g)
    if [n for n, *_ in cases] != ["NOFORM", "SIDECAR", "UTF16", "NONWORD"]:
        env_fail(f"refusal cases {[n for n, *_ in cases]}")
    for name, raw, txt, quote in cases:
        run = c.fresh(name.lower())
        gu, bu = rand_url(c.rng), rand_url(c.rng)
        (run / "cache" / f"{key(gu)}.raw").write_bytes(raw0)
        if txt0 is not None:
            (run / "cache" / f"{key(gu)}.txt").write_bytes(txt0)
        (run / "cache" / f"{key(bu)}.raw").write_bytes(raw)
        if txt is not None:
            (run / "cache" / f"{key(bu)}.txt").write_bytes(txt)
        rows = [("S941", gu, good[0]), ("S942", bu, quote)]
        if c.rng.random() < 0.5:
            rows.reverse()
        why = refused_ok(c.build(run, rows), run, "S942")
        if why:
            return False, f"{name}: {why}"
    return True, "4 cases"


def leg_regress(c: Ctx) -> tuple[bool, str]:
    def show(p: str) -> bytes:
        r = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:{p}"], capture_output=True)
        if r.returncode != 0:
            env_fail(f"git show {p}")
        return r.stdout
    q54 = show("corpus/evidence/round54/quotes.tsv").decode("utf-8")
    want = show("corpus/evidence/round54/spans.tsv")
    run = c.fresh("regress")
    urls = sorted({l.split("\t")[1] for l in q54.splitlines()[1:] if l.strip()})
    for u in urls:
        for ext in (".txt", ".raw"):
            p = CACHE / f"{key(u)}{ext}"
            if p.is_file():
                shutil.copyfile(p, run / "cache" / p.name)
    (run / "quotes.tsv").write_text(q54, encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONSTARTUP", "PYTHONHOME")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(run / "tmp"),
                "R55_ALLOW": os.pathsep.join([str(run), str(c.hook), os.path.dirname(c.tool), str(TOOLS), sys.prefix,
                                              sys.base_prefix, sys.exec_prefix])})
    r = subprocess.run([sys.executable, str(c.hook), c.tool, "--quotes", str(run / "quotes.tsv"), "--out",
                        str(run / "out"), "--cache", str(run / "cache")], capture_output=True, timeout=600,
                       cwd=str(run), env=env)
    if r.returncode != 0:
        return False, f"rc={r.returncode} {r.stderr[-200:]!r}"
    got = run / "out" / "spans.tsv"
    if not got.is_file() or got.read_bytes() != want:
        return False, "spans.tsv differs from round 54's"
    n = 0
    for line in want.decode("utf-8").splitlines()[1:]:
        name = line.split("\t")[4]
        gp = run / "out" / name
        if not gp.is_file() or gp.read_bytes() != show(f"corpus/evidence/round54/{name}"):
            return False, f"{name} differs"
        n += 1
    return True, f"r54 {n} rows identical"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", default=str(TOOLS / "build-spans.py"))
    ap.add_argument("--seed", type=int)
    ap.add_argument("--per-leg", type=int, default=3)
    ap.add_argument("--work")
    a = ap.parse_args()
    if a.per_leg < 2:
        print("usage: --per-leg must be at least 2 (sample-size guard)", file=sys.stderr)
        return 2
    if not shutil.which("soffice"):
        env_fail("soffice not found")
    if not CAPTURE_TEXT.is_file() or hashlib.sha256(CAPTURE_TEXT.read_bytes()).hexdigest() != CAPTURE_TEXT_SHA:
        env_fail("tools/capture-text.py is not the pinned oracle")
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1 << 30)
    own = a.work is None
    work = pathlib.Path(tempfile.mkdtemp(prefix="r55c1-")) if own else pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        print("usage: --work must be empty", file=sys.stderr)
        return 2
    tp = pathlib.Path(a.tool).resolve()
    tsha = hashlib.sha256(tp.read_bytes()).hexdigest() if tp.is_file() else "absent"
    print(f"tool={tp} sha256={tsha} seed={seed} per-leg={a.per_leg}")
    c = Ctx(str(tp), work, random.Random(seed), a.per_leg)
    n = 0
    legs = ["GENOLE", "OLEPIN", "REFUSE", "REGRESS"]
    try:
        pins = pinned()
        for name in legs:
            try:
                if name == "GENOLE":
                    ok, why = leg_genole(c)
                elif name == "OLEPIN":
                    ok, why = leg_olepin(c, pins)
                elif name == "REFUSE":
                    ok, why = leg_refuse(c, pins)
                else:
                    ok, why = leg_regress(c)
            except subprocess.TimeoutExpired as e:
                ok, why = False, f"timeout {str(e.cmd[:3])[:80]}"
            n += ok
            print(f"{name}={'PASS' if ok else 'FAIL'} {why}")
    finally:
        if own:
            shutil.rmtree(work, ignore_errors=True)
    print(f"LEGS={n}/{len(legs)}")
    print("C1=PASS" if n == len(legs) else "C1=FAIL")
    return 0 if n == len(legs) else 1


if __name__ == "__main__":
    sys.exit(main())
