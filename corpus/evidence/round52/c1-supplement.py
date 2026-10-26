#!/usr/bin/env python3
"""c1-supplement — POST-FREEZE supplement to the round-52 C1 counter (disclosed
in corpus/evidence/round52/claims-erratum.md; not the claim's rule).

Wave 1 `R52CritForgeC1` passed the frozen `c1-count.py` 9/9 with an 85-line
regex tool keyed to the generators' fixed REPRESENTATION — the `w:`/`mc:`
prefixes, attribute-less self-closing `<w:tab/>`/`<w:br/>`, the rels
attribute order `Id Type Target` — and a REAL leg that only checks the tool's
self-consistency (`controls/forge-shape.py`). The frozen counter varies the
text and the names, never the XML spelling. This supplement keeps the same
written rule (claims.md R52-C1) and varies only how the same document is
spelled, which a conforming XML reader cannot see and a string-keyed tool can:

  PREFIX       the WordprocessingML, markup-compatibility and wps namespaces
               bound to fresh random prefixes (mc:Ignorable rewritten to match),
               the w: namespace sometimes as the DEFAULT namespace;
  RELS_FORM    `_rels/.rels` with a random prefix, random attribute order and
               random whitespace inside the tags;
  SYNTAX       XML comments between elements, whitespace before `>` and `/>`,
               CDATA sections and decimal character references inside `w:t`,
               run-level `w:br` with a `type` attribute, `w:tab` and `w:br`
               written as start/end pairs instead of self-closing;
  REAL_TEXT    the pinned NIPH capture's text form has the sha256 of the text
               the independent reader `build-spans.py` `docx_text` prints
               (pinned TEXT_SHA below, 19682 characters), not merely one
               occurrence of the quote.

Usage: python3 corpus/evidence/round52/c1-supplement.py [--tool PATH] [--seed N]
                                                         [--work DIR] [--per-leg K]
Exit 0 all four legs pass · 1 a leg failed · 2 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import pathlib
import random
import re
import shutil
import sys
import tempfile
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
TEXT_SHA = "754aae4266a19af9518a4bb46bcd484078baeb095df048d171cfc8cc2f24b0d9"
TEXT_CHARS = 19682


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _load("r52_c1_count", "c1-count.py")
NS = {"w": C.W, "mc": C.MC, "wps": C.WPS}


def prefix(g: C.Gen) -> str:
    return g.r.choice("abcdefghijklmnopqrstuvwxyz") + g.name()[:6]


def respell_prefixes(xml: str, g: C.Gen) -> str:
    """Rename w, mc and wps to fresh prefixes; w: sometimes becomes the default namespace."""
    new = {k: prefix(g) for k in NS}
    default_w = g.r.random() < 0.4
    for old, p in new.items():
        if old == "w" and default_w:
            xml = re.sub(r"(</?)w:", r"\1", xml)
            xml = re.sub(r"(\s)w:(?=[A-Za-z]+=)", r"\1" + "w__ATTR:", xml)
            xml = xml.replace("xmlns:w=", "xmlns=").replace("xmlns:w__ATTR=", "xmlns:w=")
            continue
        xml = re.sub(r"(</?)" + old + r":", r"\1" + p + ":", xml)
        xml = re.sub(r"(\s)" + old + r":(?=[A-Za-z]+=)", r"\1" + p + ":", xml)
        xml = xml.replace(f"xmlns:{old}=", f"xmlns:{p}=")
    if default_w:
        # attributes of default-namespace elements still need the w namespace: bind it to a prefix
        wp = prefix(g)
        xml = xml.replace("w__ATTR:", wp + ":").replace("<document ", f'<document xmlns:{wp}="{C.W}" ', 1)
    xml = re.sub(r'(:Ignorable=")wps(")', r"\g<1>" + new["wps"] + r"\2", xml)
    return xml


def respell_syntax(xml: str, g: C.Gen) -> str:
    """Comments, tag whitespace, CDATA / decimal refs in w:t, paired tab/br, typed br."""
    def t_sub(m: re.Match) -> str:
        open_tag, body = m.group(1), m.group(2)
        if "&" not in body and "]]>" not in body and g.r.random() < 0.5:
            return f"{open_tag}<![CDATA[{body}]]></w:t>"
        return open_tag + re.sub(r"&#x([0-9A-F]+);", lambda k: f"&#{int(k.group(1), 16)};", body) + "</w:t>"
    xml = re.sub(r"(<w:t(?: xml:space=\"preserve\")?>)(.*?)</w:t>", t_sub, xml, flags=re.S)
    xml = re.sub(r"<w:r>", lambda m: ("<!-- " + g.name() + " -->" if g.r.random() < 0.5 else "") + "<w:r >", xml)
    xml = re.sub(r"<w:p>", lambda m: "<w:p\n  >" if g.r.random() < 0.5 else "<w:p>", xml)
    xml = xml.replace("<w:r ><w:tab/></w:r>", "<w:r ><w:tab></w:tab></w:r>")
    xml = xml.replace("<w:r ><w:br/></w:r>", '<w:r ><w:br w:type="page" /></w:r>')
    xml = xml.replace("<w:r ><w:cr/></w:r>", "<w:r ><w:cr></w:cr></w:r>")
    return xml


def respell_package(raw: bytes, g: C.Gen, doc_fn, rels: bool) -> bytes:
    zin = zipfile.ZipFile(io.BytesIO(raw))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "_rels/.rels" and rels:
                data = respell_rels(data.decode("utf-8"), g).encode("utf-8")
            elif info.filename.endswith(".xml") and b"wordprocessingml/2006/main" in data and doc_fn:
                data = doc_fn(data.decode("utf-8"), g).encode("utf-8")
            z.writestr(info.filename, data)
    return out.getvalue()


def respell_rels(xml: str, g: C.Gen) -> str:
    p = prefix(g)
    def rel(m: re.Match) -> str:
        attrs = re.findall(r'(\w+)="([^"]*)"', m.group(0))
        g.r.shuffle(attrs)
        sp = lambda: g.r.choice([" ", "  ", "\n ", "\t"])
        return f"<{p}:Relationship" + "".join(f'{sp()}{k}="{v}"' for k, v in attrs) + sp() + "/>"
    xml = re.sub(r"<Relationship\b[^>]*/>", rel, xml)
    xml = xml.replace("<Relationships xmlns=", f"<{p}:Relationships xmlns:{p}=").replace("</Relationships>", f"</{p}:Relationships>")
    return xml


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", default=str(HERE.parents[2] / "tools" / "capture-text.py"))
    ap.add_argument("--seed", type=int)
    ap.add_argument("--work")
    ap.add_argument("--per-leg", type=int, default=4)
    a = ap.parse_args()
    if a.per_leg < 1:
        return 2
    g = C.Gen(random.Random(a.seed) if a.seed is not None else random.SystemRandom())
    gens = [C.g_paras, C.g_runs_entities, C.g_revisions, C.g_layout, C.g_altcontent, C.g_main_part]
    work = pathlib.Path(tempfile.mkdtemp(prefix="c1supr52-", dir=a.work))
    res: dict[str, tuple[bool, str]] = {}
    try:
        def fresh(data: bytes) -> pathlib.Path:
            return C.make(work / (g.name() + g.r.choice([".raw", ".docx", ".bin", ""])), data)

        if not pathlib.Path(a.tool).is_file():
            res = {k: (False, "tool absent") for k in ("PREFIX", "RELS_FORM", "SYNTAX", "REAL_TEXT")}
        else:
            legs = {"PREFIX": (respell_prefixes, False), "RELS_FORM": (None, True),
                    "SYNTAX": (lambda x, gg: respell_prefixes(respell_syntax(x, gg), gg) if gg.r.random() < 0.5 else respell_syntax(x, gg), True)}
            for leg, (fn, rels) in legs.items():
                ok, why = True, "ok"
                for _ in range(a.per_leg):
                    for gen in gens:
                        raw, want = gen(g)
                        ok, why = C.text_ok(a.tool, fresh(respell_package(raw, g, fn, rels)), want)
                        if not ok:
                            why = f"{gen.__name__}: {why}"
                            break
                    if not ok:
                        break
                res[leg] = (ok, why)
            p = C.call(a.tool, [str(C.REAL_RAW)])
            txt = p.stdout.decode("utf-8", errors="replace")
            good = p.returncode == 0 and len(txt) == TEXT_CHARS and hashlib.sha256(txt.encode("utf-8")).hexdigest() == TEXT_SHA
            res["REAL_TEXT"] = (good, f"rc={p.returncode} chars={len(txt)}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    n = 0
    for leg, (ok, why) in res.items():
        n += ok
        print(f"{leg}={'PASS' if ok else 'FAIL'} {why}")
    print(f"SUPPLEMENT_LEGS={n}/{len(res)}")
    print("C1_SUPPLEMENT=PASS" if n == len(res) else "C1_SUPPLEMENT=FAIL")
    return 0 if n == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
