#!/usr/bin/env python3
"""R54-C1 frozen counter — OLE Word 97-2003 (.doc) text form in tools/capture-text.py.

Frozen predicate (one sentence, = claims.md R54-C1):
`tools/capture-text.py`, run as an ordinary command under an audit hook that
fails the run on any process spawn, exec, fork or socket connect, prints for
an OLE Word 97+ `.doc` the text form of its main document story — every
paragraph, table-cell and hyperlink-anchor text of a document generated at
counting time from fresh random text (CJK, Latin-1 and ASCII mixed) appears
exactly once and in document order in the whitespace-free text form, the
hyperlink's random URL (a field code) does not appear, there is no U+FFFD
and no code point below 0x20 other than tab and newline, and `--locate` on a
generated paragraph prints `LOCATED count=1 offset=<o>` with the stdout text
form holding that paragraph at `<o>` — and for each OLE Word capture of the
read-only campaign cache (five pinned `.raw` files, four distinct documents)
exits 0 with no U+FFFD, holds every line (>= 8 non-space characters) of the
LibreOffice plain-text export of the same bytes, made at counting time, in its
whitespace-free text form (directly, or after dropping one leading list label
of at most 12 non-space characters), has a whitespace-free length within
0.90-1.10 of that export's, and locates the two pinned quotes exactly once;
while it refuses (exit 2, nothing on stdout, a stderr line starting
`REFUSED ole-not-word`, `REFUSED ole-encrypted` or `REFUSED ole-malformed`
respectively, no `Traceback`) a generated OLE spreadsheet, a generated `.doc`
whose FIB has fEncrypted or fObfuscated set, and a generated `.doc` cut short
before its WordDocument stream or carrying a sector shift of 7 — and the
round-52 frozen counter prints `LEGS=9/9` and the round-52 supplement
`SUPPLEMENT_LEGS=4/4` for the same tool — counted as legs GEN, NONWORD,
ENCRYPTED, MALFORMED, REAL, REGRESS.

Usage: python3 corpus/evidence/round54/c1-count.py [--tool PATH] [--seed N]
       [--per-leg K] [--work DIR]
Exit: 0 C1=PASS (6/6 legs) · 1 C1=FAIL · 2 ENV_CHANGED (pinned capture bytes
differ, soffice missing) or usage. No network: generation and the oracle run
LibreOffice locally (`soffice --headless`, a private profile under the work
dir); the tool itself may spawn nothing.
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
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
# key -> sha256 prefix (20 hex); 74ced3e9… is a byte twin of 54fe0734…
REAL = {
    "54fe0734c01f699e735b4b0a": "d341c133e37d65f02f8f",
    "74ced3e9311594a8cc3f1f42": "d341c133e37d65f02f8f",
    "6dc68fd6b32ce9c8dfcebce8": "6063a3aff7a4081e93a6",
    "b539a80218080da56a75b624": "46d1866ce9afd51682e7",
    "bdff491a75c6abeda1d9c01d": "ac0fad62ed9a11fa3bd1",
}
PINNED_QUOTES = {
    "6dc68fd6b32ce9c8dfcebce8": "本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。",
    "bdff491a75c6abeda1d9c01d": "是否检索灰色文献",
}
R52 = LANE / "corpus" / "evidence" / "round52"
HOOK = r"""
import sys, runpy
BAD = ("subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork",
       "os.forkpty", "pty.spawn", "socket.connect", "socket.bind")
def hook(ev, args):
    if ev in BAD:
        sys.stderr.write("AUDIT_FORBIDDEN " + ev + "\n"); sys.stderr.flush()
        import os; os._exit(97)
sys.addaudithook(hook)
tool = sys.argv[1]; sys.argv = sys.argv[1:]
runpy.run_path(tool, run_name="__main__")
"""
CJK = [chr(c) for c in range(0x4E00, 0x4E00 + 3000)]
LAT1 = list("àáâãäåçèéêëìíîïñòóôõöùúûüýÿÀÉÑÖÜß")


def word(rng: random.Random) -> str:
    k = rng.random()
    if k < 0.35:
        return "".join(rng.choice(CJK) for _ in range(rng.randint(2, 6)))
    if k < 0.55:
        return "".join(rng.choice(string.ascii_lowercase + "".join(LAT1)) for _ in range(rng.randint(3, 8)))
    return "".join(rng.choice(string.ascii_letters + string.digits) for _ in range(rng.randint(3, 9)))


def sentence(rng: random.Random, n: int | None = None) -> str:
    return " ".join(word(rng) for _ in range(n or rng.randint(4, 10))) + " " + "nx" + "".join(rng.choice("0123456789abcdef") for _ in range(10))


def ws0(t: str) -> str:
    return re.sub(r"\s+", "", t)


class Ctx:
    def __init__(self, tool: str, work: pathlib.Path, rng: random.Random, k: int):
        self.tool, self.work, self.rng, self.k = tool, work, rng, k
        self.hook = work / "hook.py"
        self.hook.write_text(HOOK)
        self.prof = (work / "soffice-profile").as_uri()

    def soffice(self, conv: str, outdir: pathlib.Path, files: list[pathlib.Path]) -> None:
        outdir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["soffice", f"-env:UserInstallation={self.prof}", "--headless", "--convert-to", conv,
                        "--outdir", str(outdir), *map(str, files)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600, check=False)

    def run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(self.hook), self.tool, *args], capture_output=True, timeout=300)


def gen_docs(c: Ctx, tag: str) -> list[tuple[pathlib.Path, list[str], str]]:
    src = c.work / f"src-{tag}"
    src.mkdir()
    specs = []
    for i in range(c.k):
        r = c.rng
        items: list[str] = []
        body = []
        for _ in range(r.randint(2, 4)):
            s = sentence(r); items.append(s); body.append(f"<p>{html.escape(s)}</p>")
        pre, anchor, post = sentence(r, 2), sentence(r, 3), sentence(r, 2)
        url = "https://" + "".join(r.choice(string.ascii_lowercase) for _ in range(8)) + ".example/" + "u" + "".join(r.choice(string.digits) for _ in range(12))
        items.append(pre + " " + anchor + " " + post)
        body.append(f"<p>{html.escape(pre)} <a href=\"{url}\">{html.escape(anchor)}</a> {html.escape(post)}</p>")
        rows = []
        for _ in range(r.randint(2, 3)):
            cells = [sentence(r, r.randint(1, 3)) for _ in range(r.randint(2, 3))]
            items.extend(cells)
            rows.append("<tr>" + "".join(f"<td>{html.escape(x)}</td>" for x in cells) + "</tr>")
        body.append("<table>" + "".join(rows) + "</table>")
        s = sentence(r); items.append(s); body.append(f"<p>{html.escape(s)}</p>")
        name = f"g{tag}{i}"
        (src / f"{name}.html").write_text("<html><head><meta charset=\"utf-8\"></head><body>" + "".join(body) + "</body></html>", encoding="utf-8")
        specs.append((name, items, url))
    out = c.work / f"doc-{tag}"
    c.soffice("doc:MS Word 97", out, sorted(src.glob("*.html")))
    res = []
    for name, items, url in specs:
        p = out / f"{name}.doc"
        if not p.is_file() or p.read_bytes()[:8] != b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
            print(f"ENV_CHANGED soffice did not write an OLE {p.name}"); sys.exit(2)
        res.append((p, items, url))
    return res


def wd_start(b: bytes) -> int:
    """Offset of the WordDocument stream's first sector (512-byte sectors, FIB magic EC A5, nFib >= 0xC1)."""
    hits = [o for o in range(512, len(b) - 4, 512) if b[o:o + 2] == b"\xec\xa5" and int.from_bytes(b[o + 2:o + 4], "little") >= 0xC1]
    return hits[0] if len(hits) == 1 else -1


def leg_gen(c: Ctx) -> tuple[bool, str]:
    for p, items, url in gen_docs(c, "gen"):
        r = c.run(str(p))
        if r.returncode != 0:
            return False, f"{p.name} rc={r.returncode} {r.stderr[-200:]!r}"
        try:
            text = r.stdout.decode("utf-8")
        except UnicodeDecodeError:
            return False, f"{p.name} stdout not UTF-8"
        if "\ufffd" in text or any(ord(ch) < 0x20 and ch not in "\t\n" for ch in text):
            return False, f"{p.name} U+FFFD or control character in the text form"
        flat, pos = ws0(text), 0
        for it in items:
            w = ws0(it)
            if flat.count(w) != 1:
                return False, f"{p.name} item count={flat.count(w)} {it[:40]!r}"
            j = flat.find(w)
            if j < pos:
                return False, f"{p.name} item out of order {it[:40]!r}"
            pos = j + len(w)
        if url in text or url.split("/")[-1] in text:
            return False, f"{p.name} field code (hyperlink URL) in the text form"
        q = c.rng.choice([i for i in items if len(i) > 20])
        q = q[: max(12, len(q) * 2 // 3)].strip()
        lr = c.run(str(p), "--locate", q)
        m = re.fullmatch(rb"LOCATED count=1 offset=(\d+)\n", lr.stdout)
        if lr.returncode != 0 or not m or text[int(m.group(1)):int(m.group(1)) + len(q)] != q or text.count(q) != 1:
            return False, f"{p.name} locate rc={lr.returncode} out={lr.stdout[:80]!r}"
    return True, f"{c.k} docs"


def refused(r: subprocess.CompletedProcess, cls: str) -> bool:
    err = r.stderr.decode("utf-8", "replace")
    return (r.returncode == 2 and not r.stdout and "Traceback" not in err
            and any(l.startswith(f"REFUSED {cls}") for l in err.splitlines()))


def leg_nonword(c: Ctx) -> tuple[bool, str]:
    src = c.work / "src-xls"; src.mkdir()
    for i in range(c.k):
        rows = ["\t".join(word(c.rng) for _ in range(3)) for _ in range(3)]
        (src / f"x{i}.csv").write_text("\n".join(",".join(r.split("\t")) for r in rows) + "\n", encoding="utf-8")
    out = c.work / "xls"
    c.soffice("xls:MS Excel 97", out, sorted(src.glob("*.csv")))
    xs = sorted(out.glob("*.xls"))
    if len(xs) != c.k:
        print("ENV_CHANGED soffice did not write the spreadsheets"); sys.exit(2)
    for p in xs:
        r = c.run(str(p))
        if not refused(r, "ole-not-word"):
            return False, f"{p.name} rc={r.returncode} err={r.stderr[-160:]!r}"
    return True, f"{c.k} sheets"


def leg_encrypted(c: Ctx) -> tuple[bool, str]:
    for p, _, _ in gen_docs(c, "enc"):
        b = bytearray(p.read_bytes()); o = wd_start(bytes(b))
        if o < 0:
            print(f"ENV_CHANGED no unique WordDocument start in {p.name}"); sys.exit(2)
        b[o + 0x0B] |= 0x01 if c.rng.random() < 0.5 else 0x81  # fEncrypted, or fEncrypted+fObfuscated
        p.write_bytes(bytes(b))
        r = c.run(str(p))
        if not refused(r, "ole-encrypted"):
            return False, f"{p.name} rc={r.returncode} err={r.stderr[-160:]!r}"
    return True, f"{c.k} docs"


def leg_malformed(c: Ctx) -> tuple[bool, str]:
    for i, (p, _, _) in enumerate(gen_docs(c, "mal")):
        b = bytearray(p.read_bytes())
        if i % 2 == 0:
            o = wd_start(bytes(b))
            if o < 0:
                print(f"ENV_CHANGED no unique WordDocument start in {p.name}"); sys.exit(2)
            cut = c.rng.randint(512 + 1, o)
            b = b[:cut]
        else:
            b[0x1E:0x20] = (7).to_bytes(2, "little")
        p.write_bytes(bytes(b))
        r = c.run(str(p))
        if not refused(r, "ole-malformed"):
            return False, f"{p.name} rc={r.returncode} err={r.stderr[-160:]!r}"
    return True, f"{c.k} docs"


def leg_real(c: Ctx) -> tuple[bool, str]:
    src = c.work / "real"; src.mkdir()
    for k, pre in REAL.items():
        raw = CACHE / f"{k}.raw"
        if not raw.is_file() or hashlib.sha256(raw.read_bytes()).hexdigest()[:20] != pre:
            print(f"ENV_CHANGED pinned capture {k} differs"); sys.exit(2)
        shutil.copyfile(raw, src / f"{k}.doc")
    oracle = c.work / "oracle"
    c.soffice("txt:Text (encoded):UTF8", oracle, sorted(src.glob("*.doc")))
    for k in REAL:
        o = oracle / f"{k}.txt"
        if not o.is_file():
            print(f"ENV_CHANGED soffice wrote no oracle for {k}"); sys.exit(2)
        ref = o.read_text(encoding="utf-8-sig")
        r = c.run(str(CACHE / f"{k}.raw"))
        if r.returncode != 0:
            return False, f"{k} rc={r.returncode} {r.stderr[-160:]!r}"
        text = r.stdout.decode("utf-8", "replace")
        if "\ufffd" in text:
            return False, f"{k} U+FFFD in the text form"
        flat = ws0(text)
        for line in ref.splitlines():
            w = ws0(line)
            if len(w) < 8 or w in flat:
                continue
            m = re.match(r"^\s*\S{1,12}\s+(.*)$", line)
            if m and ws0(m.group(1)) in flat:
                continue
            return False, f"{k} oracle line missing {line.strip()[:60]!r}"
        ratio = len(flat) / max(1, len(ws0(ref)))
        if not 0.90 <= ratio <= 1.10:
            return False, f"{k} length ratio {ratio:.3f}"
        if k in PINNED_QUOTES:
            lr = c.run(str(CACHE / f"{k}.raw"), "--locate", PINNED_QUOTES[k])
            m = re.fullmatch(rb"LOCATED count=1 offset=(\d+)\n", lr.stdout)
            if lr.returncode != 0 or not m or not text[int(m.group(1)):].startswith(PINNED_QUOTES[k]):
                return False, f"{k} pinned quote rc={lr.returncode} {lr.stdout[:60]!r}"
    return True, f"{len(REAL)} captures"


def leg_regress(c: Ctx) -> tuple[bool, str]:
    for d in ("r52c", "r52s"):
        (c.work / d).mkdir(parents=True, exist_ok=True)
    a = subprocess.run([sys.executable, str(R52 / "c1-count.py"), "--tool", c.tool, "--work", str(c.work / "r52c")],
                       capture_output=True, text=True, timeout=1200)
    b = subprocess.run([sys.executable, str(R52 / "c1-supplement.py"), "--tool", c.tool, "--work", str(c.work / "r52s")],
                       capture_output=True, text=True, timeout=1200)
    ok = "LEGS=9/9" in a.stdout.split() and "SUPPLEMENT_LEGS=4/4" in b.stdout.split()
    return ok, f"r52 {[l for l in a.stdout.split() if l.startswith('LEGS=')]} {[l for l in b.stdout.split() if l.startswith('SUPPLEMENT_LEGS=')]}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", default=str(LANE / "tools" / "capture-text.py"))
    ap.add_argument("--seed", type=int)
    ap.add_argument("--per-leg", type=int, default=3)
    ap.add_argument("--work")
    a = ap.parse_args()
    if a.per_leg < 2:
        print("usage: --per-leg must be at least 2 (sample-size guard)", file=sys.stderr); return 2
    if not shutil.which("soffice"):
        print("ENV_CHANGED soffice not found"); return 2
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1 << 30)
    own = a.work is None
    work = pathlib.Path(tempfile.mkdtemp(prefix="r54c1-")) if own else pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    tool = str(pathlib.Path(a.tool).resolve())
    print(f"tool={tool} sha256={hashlib.sha256(pathlib.Path(tool).read_bytes()).hexdigest()} seed={seed} per-leg={a.per_leg}")
    c = Ctx(tool, work, random.Random(seed), a.per_leg)
    legs = [("GEN", leg_gen), ("NONWORD", leg_nonword), ("ENCRYPTED", leg_encrypted),
            ("MALFORMED", leg_malformed), ("REAL", leg_real), ("REGRESS", leg_regress)]
    n = 0
    try:
        for name, fn in legs:
            try:
                ok, why = fn(c)
            except subprocess.TimeoutExpired as e:
                ok, why = False, f"timeout {e.cmd[:3]}"
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
