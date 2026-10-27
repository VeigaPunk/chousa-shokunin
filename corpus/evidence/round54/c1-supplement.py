#!/usr/bin/env python3
"""R54-C1 post-freeze supplement (NOT the frozen claim rule; erratum E1).

W1 `R54CritForgeC1` passed the frozen counter 6/6 with a tool that never
parses the compound file: GEN read the generated HTML the counter leaves
beside each `.doc`, REAL returned canned exports keyed on the pinned sha256
prefixes, and the refusal legs keyed on byte markers. This supplement closes
those three shortcuts; every tool run is under the frozen counter's audit hook:

  ISOLATED  documents generated as in GEN, each then copied ALONE into a fresh
            randomly named directory outside the generation tree (no HTML, no
            sibling), under a random file name; every item recovered once, in
            order, the hyperlink URL absent.
  RESAVE    each pinned OLE capture round-tripped through LibreOffice
            (`.doc` -> `.doc`, new bytes, new digest), isolated as above; the
            tool's text form judged against the LibreOffice export of the
            RESAVED file by the frozen REAL rules (lines, ratio, no U+FFFD).
  HELDOUT   documents made from lane knowledge files the counter never names
            (random `corpus/knowledge/*.md`, plain text -> `.doc`), isolated;
            judged against their own LibreOffice export by the REAL rules.

Usage: python3 corpus/evidence/round54/c1-supplement.py [--tool PATH] [--seed N] [--per-leg K] [--work DIR]
Exit: 0 SUPPLEMENT=PASS · 1 FAIL · 2 env/usage.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import random
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r54c1", HERE / "c1-count.py")
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)


def isolate(c, p: pathlib.Path) -> pathlib.Path:
    d = c.work / ("iso-" + "".join(c.rng.choice("abcdefghjkmnpqrstuvwxyz") for _ in range(12)))
    d.mkdir()
    q = d / ("".join(c.rng.choice("abcdefghjkmnpqrstuvwxyz0123456789") for _ in range(10)) + ".doc")
    shutil.copyfile(p, q)
    return q


def judge(c, doc: pathlib.Path, ref: str) -> str | None:
    r = c.run(str(doc))
    if r.returncode != 0:
        return f"rc={r.returncode} {r.stderr[-160:]!r}"
    text = r.stdout.decode("utf-8", "replace")
    if "\ufffd" in text:
        return "U+FFFD"
    flat = F.ws0(text)
    for line in ref.splitlines():
        w = F.ws0(line)
        if len(w) < 8 or w in flat:
            continue
        m = re.match(r"^\s*\S{1,12}\s+(.*)$", line)
        if m and F.ws0(m.group(1)) in flat:
            continue
        return f"oracle line missing {line.strip()[:60]!r}"
    ratio = len(flat) / max(1, len(F.ws0(ref)))
    return None if 0.90 <= ratio <= 1.10 else f"ratio {ratio:.3f}"


def oracle(c, docs: list[pathlib.Path], tag: str) -> dict[pathlib.Path, str]:
    out = c.work / f"oracle-{tag}"
    c.soffice("txt:Text (encoded):UTF8", out, docs)
    res = {}
    for d in docs:
        o = out / f"{d.stem}.txt"
        if not o.is_file():
            print(f"ENV_CHANGED no export for {d.name}"); sys.exit(2)
        res[d] = o.read_text(encoding="utf-8-sig")
    return res


def leg_isolated(c) -> tuple[bool, str]:
    for p, items, url in F.gen_docs(c, "iso"):
        q = isolate(c, p)
        r = c.run(str(q))
        if r.returncode != 0:
            return False, f"{q.name} rc={r.returncode} {r.stderr[-160:]!r}"
        flat, pos = F.ws0(r.stdout.decode("utf-8", "replace")), 0
        for it in items:
            w = F.ws0(it)
            if flat.count(w) != 1 or flat.find(w) < pos:
                return False, f"{q.name} item {it[:40]!r}"
            pos = flat.find(w) + len(w)
        if url.split("/")[-1] in flat:
            return False, f"{q.name} field code in text form"
    return True, f"{c.k} docs"


def leg_resave(c) -> tuple[bool, str]:
    src = c.work / "resave-src"; src.mkdir()
    for k in F.REAL:
        shutil.copyfile(F.CACHE / f"{k}.raw", src / f"r{k[:8]}.doc")
    out = c.work / "resave"
    c.soffice("doc:MS Word 97", out, sorted(src.glob("*.doc")))
    docs = []
    for p in sorted(out.glob("*.doc")):
        if hashlib.sha256(p.read_bytes()).hexdigest()[:20] in F.REAL.values():
            return False, f"{p.name} resave kept the pinned bytes"
        docs.append(isolate(c, p))
    if len(docs) != len(F.REAL):
        print("ENV_CHANGED resave incomplete"); sys.exit(2)
    for d, ref in oracle(c, docs, "resave").items():
        why = judge(c, d, ref)
        if why:
            return False, f"{d.name} {why}"
    return True, f"{len(docs)} resaved captures"


def leg_heldout(c) -> tuple[bool, str]:
    kb = sorted((F.LANE / "corpus" / "knowledge").glob("*.md"))
    src = c.work / "held-src"; src.mkdir()
    for i, p in enumerate(c.rng.sample(kb, min(len(kb), c.k))):
        (src / f"h{i}.txt").write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    out = c.work / "held"
    c.soffice("doc:MS Word 97", out, sorted(src.glob("*.txt")))
    docs = [isolate(c, p) for p in sorted(out.glob("*.doc"))]
    if len(docs) != min(len(kb), c.k):
        print("ENV_CHANGED held-out generation incomplete"); sys.exit(2)
    for d, ref in oracle(c, docs, "held").items():
        why = judge(c, d, ref)
        if why:
            return False, f"{d.name} {why}"
    return True, f"{len(docs)} lane files"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool", default=str(F.LANE / "tools" / "capture-text.py"))
    ap.add_argument("--seed", type=int)
    ap.add_argument("--per-leg", type=int, default=3)
    ap.add_argument("--work")
    a = ap.parse_args()
    if a.per_leg < 2:
        print("usage: --per-leg must be at least 2", file=sys.stderr); return 2
    if not shutil.which("soffice"):
        print("ENV_CHANGED soffice not found"); return 2
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1 << 30)
    own = a.work is None
    work = pathlib.Path(tempfile.mkdtemp(prefix="r54c1s-")) if own else pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    tool = str(pathlib.Path(a.tool).resolve())
    print(f"tool={tool} sha256={hashlib.sha256(pathlib.Path(tool).read_bytes()).hexdigest()} seed={seed} per-leg={a.per_leg}")
    c = F.Ctx(tool, work, random.Random(seed), a.per_leg)
    legs = [("ISOLATED", leg_isolated), ("RESAVE", leg_resave), ("HELDOUT", leg_heldout)]
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
    print(f"SUPPLEMENT_LEGS={n}/{len(legs)}")
    print("SUPPLEMENT=PASS" if n == len(legs) else "SUPPLEMENT=FAIL")
    return 0 if n == len(legs) else 1


if __name__ == "__main__":
    sys.exit(main())
