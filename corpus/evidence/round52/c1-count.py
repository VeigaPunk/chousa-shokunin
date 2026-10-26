#!/usr/bin/env python3
"""c1-count — frozen counter for round 52 claim C1 (operability; capability).

Predicate R52-C1, the same sentence as corpus/evidence/round52/claims.md:
`tools/capture-text.py RAW` prints, as UTF-8 on stdout with exit 0, the TEXT
FORM of an OOXML WordprocessingML capture — the main document part is the
target of the `_rels/.rels` relationship whose Type ends in `/officeDocument`
(a leading `/` stripped), never a fixed member name; in that part, in document
order, a `w:t` element emits its text (XML entities decoded), a `w:tab`,
`w:br` or `w:cr` whose parent is a `w:r` emits a tab, a newline, a newline,
the end of every `w:p` (nested ones included) emits a newline, everything
inside an `mc:Fallback` emits nothing, and nothing else emits text (so
`w:delText`, `w:instrText` and the `w:tab` stops of `w:pPr/w:tabs` are
dropped); `capture-text.py RAW --locate QUOTE` prints one line
`LOCATED count=<n> offset=<first offset in that text form or -1>` and exits 0
only when n == 1, else 1; and a RAW that is not a zip, or a zip with no
officeDocument relationship or whose target is missing, is refused with exit
2, a stderr line starting `REFUSED` and nothing on stdout. Counted as nine
legs, each over packages GENERATED here at counting time from fresh random
text, member names and file names (nothing the tool author could pre-read):
PARAS, RUNS_ENTITIES, REVISIONS, LAYOUT, ALTCONTENT, MAIN_PART, LOCATE,
REFUSE, and REAL (the pinned NIPH capture `.raw` from the campaign cache holds
`SRにおける文献検索期間について明記する` exactly once in the text form, and
`--locate` agrees with the printed text).

Usage: python3 corpus/evidence/round52/c1-count.py [--tool PATH] [--seed N]
                                                   [--work DIR] [--per-leg K]
Scratch: a fresh directory under --work (default: $TMPDIR via tempfile),
removed on exit. Exit 0 all nine legs pass · 1 a leg failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import pathlib
import random
import shutil
import subprocess
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

LANE = pathlib.Path(__file__).resolve().parents[3]
REAL_RAW = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw")
REAL_SHA = "16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763"
REAL_QUOTE = "SRにおける文献検索期間について明記する"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
WPS = "http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
V = "urn:schemas-microsoft-com:vml"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
REL_CORE = "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"
LEGS = ("PARAS", "RUNS_ENTITIES", "REVISIONS", "LAYOUT", "ALTCONTENT", "MAIN_PART", "LOCATE", "REFUSE", "REAL")


class Gen:
    def __init__(self, rng: random.Random):
        self.r = rng

    def word(self) -> str:
        r = self.r
        kind = r.randrange(3)
        n = r.randint(2, 7)
        if kind == 0:
            return "".join(chr(r.randint(0x4E00, 0x9FA5)) for _ in range(n))
        if kind == 1:
            return "".join(chr(r.randint(0x3041, 0x3093)) for _ in range(n))
        return "".join(r.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(n))

    def text(self, lo: int = 2, hi: int = 6) -> str:
        return " ".join(self.word() for _ in range(self.r.randint(lo, hi)))

    def name(self) -> str:
        return "".join(self.r.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(self.r.randint(5, 12)))


def t(s: str) -> str:
    sp = ' xml:space="preserve"' if s[:1] == " " or s[-1:] == " " else ""
    return f"<w:t{sp}>{escape(s)}</w:t>"


def run(inner: str, rpr: bool = False) -> str:
    return "<w:r>" + ("<w:rPr><w:b/></w:rPr>" if rpr else "") + inner + "</w:r>"


def para(inner: str, ppr: str = "") -> str:
    return "<w:p>" + (f"<w:pPr>{ppr}</w:pPr>" if ppr else "") + inner + "</w:p>"


def document(body: str) -> bytes:
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<w:document xmlns:w="{W}" xmlns:mc="{MC}" xmlns:wps="{WPS}" xmlns:v="{V}" '
            f'xmlns:wp="{WP}" xmlns:a="{A}" mc:Ignorable="wps"><w:body>{body}'
            f'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/></w:sectPr></w:body></w:document>').encode("utf-8")


def package(main: str, doc: bytes, extra: dict[str, bytes] | None = None, rel_type: str = REL_DOC,
            target: str | None = None) -> bytes:
    rels = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId2" Type="{REL_CORE}" Target="docProps/core.xml"/>'
            f'<Relationship Id="rId1" Type="{rel_type}" Target="{target if target is not None else main}"/>'
            f'</Relationships>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          f'<Override PartName="/{main.lstrip("/")}" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '</Types>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("docProps/core.xml", '<?xml version="1.0"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"/>')
        if doc is not None:
            z.writestr(main.lstrip("/"), doc)
        for k, v in (extra or {}).items():
            z.writestr(k, v)
    return buf.getvalue()


# ---- one generator per leg: returns (raw bytes, expected text)

def g_paras(g: Gen) -> tuple[bytes, str]:
    ps = [g.text() for _ in range(g.r.randint(3, 8))]
    body = "".join(para(run(t(p))) for p in ps)
    return package("word/document.xml", document(body)), "".join(p + "\n" for p in ps)


def g_runs_entities(g: Gen) -> tuple[bytes, str]:
    out, body = [], []
    for _ in range(g.r.randint(3, 6)):
        pieces = [g.word() for _ in range(g.r.randint(2, 5))]
        specials = ["&", "<", ">", '"', "'", chr(g.r.randint(0x4E00, 0x9FA5))]
        xml, txt = [], []
        for i, w in enumerate(pieces):
            sp = g.r.choice(specials)
            if sp == chr(ord(sp)) and ord(sp) >= 0x4E00:
                enc = f"&#x{ord(sp):X};"
            else:
                enc = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;"}[sp]
            lead = " " if i and g.r.random() < 0.5 else ""
            piece = lead + w + sp
            sp_attr = ' xml:space="preserve"' if lead else ""
            xml.append(run(f"<w:t{sp_attr}>{lead}{escape(w)}{enc}</w:t>", rpr=g.r.random() < 0.5))
            txt.append(piece)
        body.append(para("".join(xml)))
        out.append("".join(txt) + "\n")
    return package("word/document.xml", document("".join(body))), "".join(out)


def g_revisions(g: Gen) -> tuple[bytes, str]:
    out, body = [], []
    for _ in range(g.r.randint(2, 4)):
        keep1, ins, gone, instr, shown, keep2 = (g.word() for _ in range(6))
        xml = (run(t(keep1))
               + f'<w:ins w:id="1" w:author="x" w:date="2024-01-01T00:00:00Z">{run(t(ins))}</w:ins>'
               + f'<w:del w:id="2" w:author="x" w:date="2024-01-01T00:00:00Z"><w:r><w:delText>{escape(gone)}</w:delText></w:r></w:del>'
               + run('<w:fldChar w:fldCharType="begin"/>')
               + run(f'<w:instrText xml:space="preserve"> HYPERLINK "{escape(instr)}" </w:instrText>')
               + run('<w:fldChar w:fldCharType="separate"/>') + run(t(shown)) + run('<w:fldChar w:fldCharType="end"/>')
               + run(t(keep2)))
        body.append(para(xml))
        out.append(keep1 + ins + shown + keep2 + "\n")
    return package("word/document.xml", document("".join(body))), "".join(out)


def g_layout(g: Gen) -> tuple[bytes, str]:
    out, body = [], []
    a, b, c, d = (g.word() for _ in range(4))
    tabs = '<w:tabs><w:tab w:val="left" w:pos="840"/><w:tab w:val="right" w:pos="4200"/></w:tabs>'
    body.append(para(run(t(a)) + run("<w:tab/>") + run(t(b)) + run("<w:br/>") + run(t(c)) + run("<w:cr/>") + run(t(d)), ppr=tabs))
    out.append(f"{a}\t{b}\n{c}\n{d}\n")
    cells = [[g.word() for _ in range(g.r.randint(2, 3))] for _ in range(g.r.randint(2, 3))]
    tbl = "<w:tbl><w:tblPr/>" + "".join(
        "<w:tr>" + "".join(f"<w:tc><w:tcPr/>{para(run(t(x)), ppr=tabs)}</w:tc>" for x in row) + "</w:tr>" for row in cells) + "</w:tbl>"
    body.append(tbl)
    out.extend(x + "\n" for row in cells for x in row)
    e = g.text()
    body.append(para(run(t(e)), ppr=tabs))
    out.append(e + "\n")
    return package("word/document.xml", document("".join(body))), "".join(out)


def g_altcontent(g: Gen) -> tuple[bytes, str]:
    before, box, after = g.text(), g.text(), g.text()
    choice = (f'<mc:Choice Requires="wps"><w:drawing><wp:anchor><a:graphic><a:graphicData><wps:wsp><wps:txbx>'
              f'<w:txbxContent>{para(run(t(box)))}</w:txbxContent></wps:txbx></wps:wsp></a:graphicData></a:graphic>'
              f'</wp:anchor></w:drawing></mc:Choice>')
    fallback = (f'<mc:Fallback><w:pict><v:shape><v:textbox><w:txbxContent>{para(run(t(box)))}</w:txbxContent>'
                f'</v:textbox></v:shape></w:pict></mc:Fallback>')
    body = para(run(t(before))) + para(run(f"<mc:AlternateContent>{choice}{fallback}</mc:AlternateContent>")) + para(run(t(after)))
    return package("word/document.xml", document(body)), f"{before}\n{box}\n\n{after}\n"


def g_main_part(g: Gen) -> tuple[bytes, str]:
    real, decoy = g.text(), g.text()
    main = g.r.choice(["word/", "", "doc/"]) + g.name() + ".xml"
    target = ("/" + main) if g.r.random() < 0.5 else main
    extra = {"word/document.xml": document(para(run(t(decoy))))} if main != "word/document.xml" else {}
    return package(main, document(para(run(t(real)))), extra=extra, target=target), real + "\n"


def make(path: pathlib.Path, data: bytes) -> pathlib.Path:
    path.write_bytes(data)
    return path


def call(tool: str, args: list[str]) -> subprocess.CompletedProcess:
    try:
        return subprocess.run([sys.executable, tool] + args, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 124, b"", b"timeout")


def text_ok(tool: str, raw: pathlib.Path, want: str) -> tuple[bool, str]:
    p = call(tool, [str(raw)])
    got = p.stdout.decode("utf-8", errors="replace")
    if p.returncode != 0:
        return False, f"rc={p.returncode}"
    if got != want:
        i = next((k for k in range(min(len(got), len(want))) if got[k] != want[k]), min(len(got), len(want)))
        return False, f"text differs at {i} (got {len(got)} chars, want {len(want)})"
    return True, "ok"


def locate(tool: str, raw: pathlib.Path, quote: str) -> tuple[int, int, int] | None:
    p = call(tool, [str(raw), "--locate", quote])
    line = p.stdout.decode("utf-8", errors="replace").strip()
    parts = dict(x.split("=", 1) for x in line.split()[1:] if "=" in x) if line.startswith("LOCATED ") else {}
    try:
        return p.returncode, int(parts["count"]), int(parts["offset"])
    except (KeyError, ValueError):
        return None


def refused(p: subprocess.CompletedProcess) -> bool:
    err = p.stderr.decode("utf-8", errors="replace").splitlines()
    return p.returncode == 2 and not p.stdout and any(l.startswith("REFUSED") for l in err)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", default=str(LANE / "tools" / "capture-text.py"))
    ap.add_argument("--seed", type=int)
    ap.add_argument("--work")
    ap.add_argument("--per-leg", type=int, default=3)
    a = ap.parse_args()
    if a.per_leg < 1:
        print("per-leg must be >= 1", file=sys.stderr)
        return 2
    rng = random.Random(a.seed) if a.seed is not None else random.SystemRandom()
    g = Gen(rng)
    work = pathlib.Path(tempfile.mkdtemp(prefix="c1r52-", dir=a.work))
    results: dict[str, tuple[bool, str]] = {}
    try:
        def fresh(data: bytes) -> pathlib.Path:
            ext = g.r.choice([".raw", ".docx", ".bin", ""])
            return make(work / (g.name() + ext), data)

        if not pathlib.Path(a.tool).is_file():
            for leg in LEGS:
                results[leg] = (False, "tool absent")
        else:
            gens = {"PARAS": g_paras, "RUNS_ENTITIES": g_runs_entities, "REVISIONS": g_revisions,
                    "LAYOUT": g_layout, "ALTCONTENT": g_altcontent, "MAIN_PART": g_main_part}
            for leg, fn in gens.items():
                ok, why = True, "ok"
                for _ in range(a.per_leg):
                    raw, want = fn(g)
                    ok, why = text_ok(a.tool, fresh(raw), want)
                    if not ok:
                        break
                results[leg] = (ok, why)

            # LOCATE: once -> exit 0 at the true offset; absent and twice -> exit 1
            ok, why = True, "ok"
            for _ in range(a.per_leg):
                ps = [g.text() for _ in range(g.r.randint(3, 6))]
                once = g.word() + g.word() + g.word()
                dup = g.word() + g.word() + g.word()
                k = g.r.randrange(len(ps))
                ps[k] = ps[k] + " " + once
                ps[0] = dup + " " + ps[0]
                ps[-1] = ps[-1] + " " + dup
                want = "".join(p + "\n" for p in ps)
                raw = fresh(package("word/document.xml", document("".join(para(run(t(p))) for p in ps))))
                absent = g.word() + g.word() + g.word() + g.word()
                r1, r2, r3 = locate(a.tool, raw, once), locate(a.tool, raw, absent), locate(a.tool, raw, dup)
                if r1 != (0, 1, want.find(once)) or r2 != (1, 0, -1) or r3 is None or r3[:2] != (1, 2):
                    ok, why = False, f"once={r1} want (0,1,{want.find(once)}) absent={r2} twice={r3}"
                    break
            results["LOCATE"] = (ok, why)

            # REFUSE: random bytes, HTML, a zip with no officeDocument relationship, a dangling target
            ok, why = True, "ok"
            for _ in range(a.per_leg):
                cases = {
                    "bytes": bytes(g.r.randrange(256) for _ in range(g.r.randint(64, 512))),
                    "html": f"<html><body><p>{g.text()}</p></body></html>".encode("utf-8"),
                    "norel": package("word/document.xml", document(para(run(t(g.text()))))
                                     , rel_type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/" + g.name()),
                    "dangling": package("word/document.xml", None, target="word/" + g.name() + ".xml",
                                        extra={"word/document.xml": document(para(run(t(g.text()))))}),
                }
                for name, data in cases.items():
                    if not refused(call(a.tool, [str(fresh(data))])):
                        ok, why = False, f"{name} not refused"
                        break
                if not ok:
                    break
            results["REFUSE"] = (ok, why)

            # REAL: the pinned NIPH capture
            if not REAL_RAW.is_file() or hashlib.sha256(REAL_RAW.read_bytes()).hexdigest() != REAL_SHA:
                results["REAL"] = (False, "pinned capture missing or digest differs")
            else:
                p = call(a.tool, [str(REAL_RAW)])
                txt = p.stdout.decode("utf-8", errors="replace")
                loc = locate(a.tool, REAL_RAW, REAL_QUOTE)
                good = p.returncode == 0 and txt.count(REAL_QUOTE) == 1 and loc == (0, 1, txt.find(REAL_QUOTE))
                results["REAL"] = (good, f"rc={p.returncode} count={txt.count(REAL_QUOTE)} locate={loc} chars={len(txt)}")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    n = 0
    for leg in LEGS:
        ok, why = results[leg]
        n += ok
        print(f"{leg}={'PASS' if ok else 'FAIL'} {why}")
    print(f"LEGS={n}/{len(LEGS)}")
    print("C1=PASS" if n == len(LEGS) else "C1=FAIL")
    return 0 if n == len(LEGS) else 1


if __name__ == "__main__":
    sys.exit(main())
