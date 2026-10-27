#!/usr/bin/env python3
"""c3-count — frozen counter for round 57 claim C3 (depth, sourced): the workflow standard's normative
references chained to their own documents.

Predicate R57-C3, the same sentence as corpus/evidence/round57/claims.md:
the lane entry `corpus/knowledge/normative-reference-chain-china-r57.md`
exists, cites S127 as `source: S127 — <S127's first URL>` with S127's
`used-by` naming it, and holds `规范性引用文件` (absent from `corpus/knowledge`
at BASE_REV); `corpus/evidence/round57/c3/spans.tsv` carries an S127 row
whose quote contains `规范性引用而构成本文件必不可少的条款` (CLAUSE); of the
seven references S127's `2 规范性引用文件` lists (R1 the 2019 notice
〔2019〕80号, R2 the 2021 notice 〔2021〕16号, R3 the 管理指南 2021年版, R4-R6
the 抗肿瘤 / 心血管病 / 儿童 技术指南 2022年版, R7 the 质量控制指南 2024年版)
at least four are BOUND — some lane Registry row X other than S127, S128 and
S129 and whose first source-cell URL U is none of theirs, either new since
BASE_REV (`mined`, opened 2026-10-27) or held, whose `used-by` names the
entry and which the entry cites as `source: X — U`, whose lane-owned capture
`corpus/captures/<key(U)>` is the bytes of a successful attempt for (X, U) in
`corpus/evidence/round57/refetch.tsv`, whose DEFINED text form (an OLE or zip
`.raw` through `tools/capture-text.py` as at BASE_REV, else the `.txt`) holds
the reference's edition token (whitespace removed) and its title as a
HEADING (a line that, whitespace removed and one trailing `（…）`/`(…)`
dropped, ends with the title after a prefix of at most 16 characters holding
none of `《》.[]［］`), and for which the manifest carries at least two rows
of id X and URL U with the form file's digest, one of whose quotes holds that
title — and every reference not bound carries a line
`- UNBOUND R<k> sweep: <queries and hosts>` in the entry; every manifest row
is a quote of at most 25 whitespace words and 160 characters inside its span
file, the entry and the round-57 lesson, its span file the exact slice at the
recorded offset of the form whose digest is recorded and longer than the
quote; the round-51 `quote-substance-check.py` exits 0 on the manifest; every
`char N` of a new bound row's `anchor` cell (at least one) is a quote offset
of that id; the entry exits 0 under `tools/inference-ground.py` with this
manifest; and no `S###` token in the entry names a row other than S127 or a
bound row — counted `C3=PASS`.

Separability: C3 never runs a gate, a probe or the span builder; it judges committed bytes and
captures against forms it derives itself. What it cannot see: whether a bound document is the edition
the standard means beyond the title and token, and whether the entry's sentences follow from the quotes
(the closure's reading).

Usage: python3 corpus/evidence/round57/c3-count.py [--root LANE]
Exit codes: 0 C3=PASS · 1 C3=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
BASE_REV = "6656f0770a1460d6ba73d9d2976f698a35311921"
OPENED = "2026-10-27"
ENTRY = "corpus/knowledge/normative-reference-chain-china-r57.md"
S127_URL = "https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf"
EXCLUDED = {"S127", "S128", "S129"}
EXCLUDED_URLS = {
    S127_URL,
    "https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf",
    "https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/"
    "%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C"
    "%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf",
}
PAREN_TAIL = re.compile(r"(?:（[^（）]*）|\([^()]*\))$")
BAD_PREFIX = set("《》.[]［］")
NEW_TERM = "规范性引用文件"
CLAUSE = "规范性引用而构成本文件必不可少的条款"
REFS = [
    ("R1", "关于开展药品使用监测和临床综合评价工作的通知", "〔2019〕80号"),
    ("R2", "关于规范开展药品临床综合评价工作的通知", "〔2021〕16号"),
    ("R3", "药品临床综合评价管理指南", "2021年版"),
    ("R4", "抗肿瘤药品临床综合评价技术指南", "2022年版"),
    ("R5", "心血管病药品临床综合评价技术指南", "2022年版"),
    ("R6", "儿童药品临床综合评价技术指南", "2022年版"),
    ("R7", "药品临床综合评价质量控制指南", "2024年版"),
]
MIN_BOUND = 4
MIN_PER_ID = 2
ID_RE = re.compile(r"\bS\d{3,}\b")
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S\d{3,})[ \t]*\|")
CHAR_RE = re.compile(r"\bchar\s+(\d+)")
WS = re.compile(r"\s+")


def nows(s: str) -> str:
    return WS.sub("", s)


def registry(text: str) -> list[list[str]]:
    rows, inside = [], False
    for line in text.splitlines():
        s = line.lstrip(" ")
        if len(line) - len(s) <= 3 and s.startswith("## "):
            inside = s[3:].strip() == "Registry"
            continue
        if len(line) - len(s) <= 3 and s.startswith("# "):
            inside = False
            continue
        if inside and ROW_RE.match(line):
            rows.append([c.strip() for c in s.strip().split("|")[1:-1]])
    return rows


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def first_url(cell: str) -> str:
    m = re.search(r"https?://[^\s|`<>]+", cell)
    return m.group(0) if m else ""


def base_tool():
    r = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:tools/capture-text.py"], capture_output=True)
    if r.returncode != 0:
        print("ENV_CHANGED no base capture-text")
        sys.exit(2)
    d = pathlib.Path(tempfile.mkdtemp(prefix="r57c3-"))
    try:
        t = d / "capture_text_base.py"
        t.write_bytes(r.stdout)
        spec = importlib.util.spec_from_file_location("capture_text_base", t)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return mod


def form_of(ct, store: pathlib.Path, url: str) -> tuple[str | None, str]:
    """(defined form, digest of the file read) of the lane-owned capture of url."""
    raw, txt = store / f"{key(url)}.raw", store / f"{key(url)}.txt"
    rb = raw.read_bytes() if raw.is_file() else b""
    if rb[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" or rb[:4] == b"PK\x03\x04":
        try:
            return ct.text_form(str(raw)), hashlib.sha256(rb).hexdigest()
        except Exception:
            return None, ""
    if txt.is_file():
        b = txt.read_bytes()
        return b.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n"), hashlib.sha256(b).hexdigest()
    return None, ""


def heading_title(form: str, title: str) -> bool:
    """Some line that, whitespace removed and one trailing parenthetical dropped, ends with title after a
    prefix of at most 16 characters holding none of 《》.[]［］ (a citation or reference-list line fails)."""
    for line in form.splitlines():
        s = PAREN_TAIL.sub("", nows(line))
        if s.endswith(title):
            pre = s[:len(s) - len(title)]
            if len(pre) <= 16 and not (set(pre) & BAD_PREFIX):
                return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    ev = root / "corpus" / "evidence" / "round57" / "c3"
    store = root / "corpus" / "captures"
    base = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:corpus/SOURCES.md"], capture_output=True, text=True)
    if base.returncode != 0:
        print("ENV_CHANGED no base registry")
        return 2
    ct = base_tool()
    base_ids = {r[0] for r in registry(base.stdout)}
    src_p = root / "corpus" / "SOURCES.md"
    rows = [r for r in registry(src_p.read_text(encoding="utf-8")) if len(r) == 11] if src_p.is_file() else []
    ep = root / ENTRY
    entry = ep.read_text(encoding="utf-8") if ep.is_file() else ""
    lesson_p = root / "corpus" / "lessons" / "round-57.md"
    lesson = lesson_p.read_text(encoding="utf-8") if lesson_p.is_file() else ""
    rec_p = root / "corpus" / "evidence" / "round57" / "refetch.tsv"
    good_raw: dict[tuple[str, str], str] = {}
    if rec_p.is_file():
        for line in rec_p.read_text(encoding="utf-8").splitlines()[1:]:
            c = line.split("\t")
            if len(c) == 9 and c[5] == "0" and c[6].isdigit() and 200 <= int(c[6]) <= 299 and c[7] != "-":
                good_raw[(c[0], c[1])] = c[7]
    man = ev / "spans.tsv"
    mrows = [l.split("\t") for l in man.read_text(encoding="utf-8").splitlines()[1:] if l.strip()] if man.is_file() else []

    def cites(rid: str, url: str) -> bool:
        return bool(re.search(r"^source:\s*" + rid + r"\s+—\s+" + re.escape(url) + r"(\s|$)", entry, re.M))

    def used_by(r: list[str]) -> bool:
        return ENTRY in {c.strip() for c in r[10].split(",")}

    s127 = [r for r in rows if r[0] == "S127"]
    s127_ok = bool(entry) and len(s127) == 1 and first_url(s127[0][1]) == S127_URL and used_by(s127[0]) \
        and cites("S127", S127_URL)
    new_ground = bool(entry) and NEW_TERM in entry and subprocess.run(
        ["git", "-C", str(LANE), "grep", "-q", NEW_TERM, BASE_REV, "--", "corpus/knowledge"]).returncode == 1

    # candidate binding rows
    cand = {}
    for r in rows:
        rid, url = r[0], first_url(r[1])
        if rid in EXCLUDED or not url or url in EXCLUDED_URLS or not used_by(r) or not cites(rid, url):
            continue
        if rid not in base_ids and not (r[7] == "mined" and r[8] == OPENED):
            continue
        raw = store / f"{key(url)}.raw"
        if not raw.is_file() or good_raw.get((rid, url)) != hashlib.sha256(raw.read_bytes()).hexdigest():
            continue
        form, digest = form_of(ct, store, url)
        if form is not None:
            cand[rid] = (url, form, digest, rid not in base_ids)
    per_id: dict[str, list[str]] = {}
    for m in mrows:
        if len(m) == 7 and m[0] in cand and m[1] == cand[m[0]][0] and m[2] == cand[m[0]][2]:
            per_id.setdefault(m[0], []).append(m[5])
    bound, swept = [], []
    bound_ids: set[str] = set()
    for tag, title, token in REFS:
        hit = None
        for rid, (url, form, digest, _new) in sorted(cand.items()):
            qs = per_id.get(rid, [])
            if (len(qs) >= MIN_PER_ID and token in nows(form) and heading_title(form, title)
                    and any(title in nows(q) for q in qs)):
                hit = rid
                break
        if hit:
            bound.append(f"{tag}:{hit}")
            bound_ids.add(hit)
        elif re.search(r"^- UNBOUND " + tag + r" sweep: \S.{10,}", entry, re.M):
            swept.append(tag)
    clause = any(len(m) == 7 and m[0] == "S127" and CLAUSE in m[5] for m in mrows)

    n = len(mrows)
    in_span = in_entry = in_lesson = short = ctx = cap = 0
    offsets: dict[str, set[int]] = {}
    for m in mrows:
        if len(m) != 7:
            continue
        sid, url, digest, offset, span_file, quote, _e = m
        sp = span_file.strip()
        p = ev / sp if sp and not sp.startswith("/") and ".." not in pathlib.PurePath(sp).parts else None
        span = p.read_text(encoding="utf-8") if p and p.is_file() else ""
        in_span += bool(quote and quote in span)
        in_entry += bool(quote and quote in entry)
        in_lesson += bool(quote and quote in lesson)
        short += len(quote.split()) <= 25 and len(quote) <= 160
        ctx += offset.isdigit() and len(span) > len(quote)
        if offset.isdigit() and span:
            form, dg = form_of(ct, store, url)
            o = int(offset)
            cap += form is not None and dg == digest and form[o:o + len(span)] == span
            if quote in span:
                offsets.setdefault(sid, set()).add(o + span.find(quote))
    subst = LANE / "corpus" / "evidence" / "round51" / "quote-substance-check.py"
    substance = man.is_file() and subprocess.run([sys.executable, str(subst), str(man)],
                                                 capture_output=True, text=True).returncode == 0
    anchors_need = [r for r in rows if r[0] in bound_ids and r[0] not in base_ids]
    anchors = sum(1 for r in anchors_need if CHAR_RE.findall(r[5])
                  and all(int(c) in offsets.get(r[0], set()) for c in CHAR_RE.findall(r[5])))
    grounded = False
    tool = root / "tools" / "inference-ground.py"
    if entry and tool.is_file() and man.is_file():
        grounded = subprocess.run([sys.executable, str(tool), "--entry", str(ep), "--spans", str(man), "--counts",
                                   "/dev/null", "--registry", str(src_p), "--root", str(root), "--quiet"],
                                  capture_output=True, text=True).returncode == 0
    stray = sorted({i for i in ID_RE.findall(entry) if i != "S127" and i not in bound_ids})

    print(f"ENTRY={'yes' if entry else 'no'} S127_CITED={'yes' if s127_ok else 'no'} "
          f"NEW_GROUND={'yes' if new_ground else 'no'} CLAUSE={'yes' if clause else 'no'}")
    print(f"BOUND={len(bound)}/{len(REFS)} (min {MIN_BOUND}) {' '.join(bound) or '-'}")
    print(f"SWEPT={len(swept)}/{len(REFS) - len(bound)} {' '.join(swept) or '-'}")
    print(f"QUOTE_ROWS={n} IN_SPAN={in_span} IN_ENTRY={in_entry} IN_LESSON={in_lesson} SHORT={short} "
          f"CONTEXT={ctx} CAPTURE_BOUND={cap}")
    print(f"SUBSTANCE={'PASS' if substance else 'FAIL'} ANCHOR_BOUND={anchors}/{len(anchors_need)} "
          f"INFERENCE_GROUNDED={'yes' if grounded else 'no'} STRAY_IDS={','.join(stray) or '-'}")
    ok = (s127_ok and new_ground and clause and len(bound) >= MIN_BOUND and len(swept) == len(REFS) - len(bound)
          and n > 0 and in_span == n and in_entry == n and in_lesson == n and short == n and ctx == n and cap == n
          and substance and anchors == len(anchors_need) and grounded and not stray)
    print("C3=PASS" if ok else "C3=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
