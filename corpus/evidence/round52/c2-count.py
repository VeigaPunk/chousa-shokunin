#!/usr/bin/env python3
"""c2-count — frozen counter for round 52 claim C2 (depth, sourced).

Predicate R52-C2, the same sentence as corpus/evidence/round52/claims.md:
the search-record theme continues BY DOCUMENT as the three lane entries
`corpus/knowledge/japanese-search-record-niph-form-r52.md` (the 国立保健医療科学院
submission form, a `.docx` refused in round 51 for its capture form),
`corpus/knowledge/japanese-prisma-item-wording-r40.md` (the Japanese PRISMA 2020
checklist translation, read at its web-archive copy) and
`corpus/knowledge/chinese-prisma-s-reception-r52.md` (the 梅斯医学 PRISMA-S
interpretation page and the 中国全科医学 PRISMA 2020 checklist page); of the
four documents they rest on, at least three are BOUND — exactly one lane
Registry row whose FIRST source-cell URL is the document's URL, that row new
since BASE_REV, `mined`, opened 2026-10-26, its `used-by` naming exactly the
entries citing it, and every citing entry carrying a `source: <that id> —
<url>` line — and every other one is REFUSED (no lane row, no `source:` line,
and a `refused-doc` line naming its URL in `corpus/lessons/round-52.md`); no
`S###` token appears in the entries except a bound id; at BASE_REV no
`corpus/knowledge` file held 文献検索期間, 完全な検索戦略 or 检索报告清单, and each
entry holds its own term (in that order); `corpus/evidence/round52/spans.tsv`
(derived by `build-spans.py`, whose zip raws read as the round-52 `.docx` text
form) carries at least three quote rows per bound id, each quote at most 25
whitespace words and 160 characters, inside its span file, inside the citing
entry and inside the round-52 lesson, each span file the exact slice of the
capture text form at the recorded offset whose file digest is the recorded
one, and longer than its quote; the round-51 `quote-substance-check.py` exits
0 on the manifest; every `char N` in a bound row's `anchor` cell (at least
one) is the offset of a quote of that id; all three entries exit 0 under
`tools/inference-ground.py` with this round's spans; and the lesson carries a
re-check verdict line for each absent-defect-register row on a theme URL (the
sweep prints how many: 1 at the freeze, S120), with no bound document whose
verdict is `fabricated` or `unverifiable`.

`--lane-only` reads lane bytes only: `CAPTURE_BOUND` prints `skipped`.
Cheapest shortcuts and what refuses them: the staged entries copied unchanged
carry staged ids that name lane rows of OTHER documents (S111, S112) or no row
(S125, S129) and a staged source cell whose first URL is the dead original
(REF_ID_UNBOUND, BOUND); a NIPH quote taken from the cache `.txt` sidecar
cannot occur there (72117 U+FFFD) and its span cannot slice the zip-member
form unless the form is derived (CAPTURE_BOUND); a hollow quote or a
whole-capture span fails SUBSTANCE; invented spans/digests pass `--lane-only`
and fail `CAPTURE_BOUND`. Verdict-line truth and entailment are the closure's.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
REGISTER = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md")
BASE_REV = "00f8c7f5272a1d98b6d34913985fa4537e00aaf9"
OPENED = "2026-10-26"
E_NIPH = "corpus/knowledge/japanese-search-record-niph-form-r52.md"
E_JPW = "corpus/knowledge/japanese-prisma-item-wording-r40.md"
E_ZHR = "corpus/knowledge/chinese-prisma-s-reception-r52.md"
ENTRIES = (E_NIPH, E_JPW, E_ZHR)
NIPH = "https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx"
ARCHIVE = "https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf"
ORIGINAL = "https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf"
MEDSCI = "https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3"
CHINAGP = "https://www.chinagp.net/CN/column/item185.shtml"
# (citing entry, staged id in the package, document URL) — four pairs over four documents
DOCS = [
    (E_NIPH, "S125", NIPH),
    (E_JPW, "S129", ARCHIVE),
    (E_ZHR, "S111", MEDSCI),
    (E_ZHR, "S112", CHINAGP),
]
# register rows may name the dead original of the archived document
ALIASES = {ORIGINAL: ARCHIVE}
TERMS = {E_NIPH: "文献検索期間", E_JPW: "完全な検索戦略", E_ZHR: "检索报告清单"}
MIN_BOUND = 3
MIN_PER_ID = 3
ID_RE = re.compile(r"\bS\d{3,}\b")
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S\d{3,})[ \t]*\|")
CHAR_RE = re.compile(r"\bchar\s+(\d+)")
VERDICT_RE = re.compile(r"register\s+`?(S\d{3,})`?.*?verdict[:=]?\s*\**`?(present|absent-as-written|unverifiable|fabricated)`?")


def _builder():
    spec = importlib.util.spec_from_file_location("r52_build_spans", pathlib.Path(__file__).with_name("build-spans.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def url_of(source: str) -> str:
    m = re.search(r"https?://[^\s|]+", source)
    if not m:
        return ""
    u = re.sub(r"/$", "", re.sub(r"#[^ ]*$", "", m.group(0)))
    u = re.sub(r"^[A-Za-z]+://", "", u)
    n = u.find("/")
    return (u[:n].lower() + u[n:]) if n >= 0 else u.lower()


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


def form_text(bs, url: str, digest: str) -> str | None:
    """The capture text form whose FILE digest is `digest` (see build-spans)."""
    txt, raw = CACHE / f"{key(url)}.txt", CACHE / f"{key(url)}.raw"
    if txt.is_file() and hashlib.sha256(txt.read_bytes()).hexdigest() == digest:
        return txt.read_text(encoding="utf-8", errors="replace")
    if raw.is_file():
        b = raw.read_bytes()
        if hashlib.sha256(b).hexdigest() == digest:
            return bs.raw_form(b)
    return None


def safe_span(ev: pathlib.Path, raw: str) -> pathlib.Path | None:
    raw = raw.strip()
    if not raw or raw.startswith("/") or ".." in pathlib.PurePath(raw).parts:
        return None
    return ev / raw


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--lane-only", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    ev = root / "corpus" / "evidence" / "round52"
    sources = root / "corpus" / "SOURCES.md"
    lesson_p = root / "corpus" / "lessons" / "round-52.md"
    base = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:corpus/SOURCES.md"],
                          capture_output=True, text=True)
    if base.returncode != 0 or not REGISTER.is_file():
        print("NO_BASE_OR_REGISTER")
        return 2
    bs = _builder()
    base_ids = {r[0] for r in registry(base.stdout)}
    rows = registry(sources.read_text(encoding="utf-8")) if sources.is_file() else []
    texts = {p: (root / p).read_text(encoding="utf-8") for p in ENTRIES if (root / p).is_file()}
    lesson = lesson_p.read_text(encoding="utf-8") if lesson_p.is_file() else ""

    by_doc: dict[str, list[tuple[str, str]]] = {}
    for entry, _sid, url in DOCS:
        by_doc.setdefault(url_of(url), []).append((entry, url))
    bound: dict[str, str] = {}      # lane id -> URL
    nbound = refused = 0
    for _u, pairs in by_doc.items():
        url = pairs[0][1]
        citing = sorted({e for e, _ in pairs})
        hits = [r for r in rows if len(r) == 11 and url_of(r[1]) == url_of(url)]
        if len(hits) == 1:
            r = hits[0]
            used = sorted(c.strip() for c in r[10].split(","))
            cites = all(re.search(r"^source:\s*" + r[0] + r"\s+—\s+" + re.escape(url) + r"(\s|$)",
                                  texts.get(e, ""), re.M) for e in citing)
            if r[0] not in base_ids and r[7] == "mined" and r[8] == OPENED and used == citing and cites:
                bound[r[0]] = url
                nbound += 1
        elif not hits:
            no_src = all(not re.search(r"^source:.*" + re.escape(url), texts.get(e, ""), re.M) for e in citing)
            named = any("refused-doc" in l and url in l for l in lesson.splitlines())
            refused += bool(no_src and named)

    unb = sum(1 for t in texts.values() for i in ID_RE.findall(t) if i not in bound)

    new_ground = 0
    held_terms = subprocess.run(["git", "-C", str(LANE), "grep", "-l"] + [x for tm in TERMS.values() for x in ("-e", tm)] + [BASE_REV, "--", "corpus/knowledge"],
                                capture_output=True, text=True)
    for entry, term in TERMS.items():
        new_ground += held_terms.returncode == 1 and term in texts.get(entry, "")

    man = ev / "spans.tsv"
    mrows = [l.split("\t") for l in man.read_text(encoding="utf-8").splitlines()[1:] if l.strip()] if man.is_file() else []
    n = len(mrows)
    in_span = in_entry = in_lesson = short = ctx = cap_bound = on_bound = 0
    per_id: dict[str, int] = {}
    offsets: dict[str, set[int]] = {}
    for r in mrows:
        if len(r) != 7:
            continue
        sid, url, digest, offset, span_file, quote, entry = (c.strip() if i != 5 else c for i, c in enumerate(r))
        p = safe_span(ev, span_file)
        span = p.read_text(encoding="utf-8") if p and p.is_file() else ""
        per_id[sid] = per_id.get(sid, 0) + 1
        on_bound += bound.get(sid) == url
        in_span += bool(quote and quote in span)
        in_entry += bool(quote and quote in texts.get(entry, ""))
        in_lesson += bool(quote and quote in lesson)
        short += len(quote.split()) <= 25 and len(quote) <= 160
        ctx += offset.isdigit() and len(span) > len(quote)
        if offset.isdigit() and quote and quote in span:
            offsets.setdefault(sid, set()).add(int(offset) + span.find(quote))
        if not a.lane_only and offset.isdigit() and span:
            ft = form_text(bs, url, digest)
            o = int(offset)
            cap_bound += ft is not None and ft[o:o + len(span)] == span
    ids_ok = sum(per_id.get(sid, 0) >= MIN_PER_ID for sid in bound)

    subst = LANE / "corpus" / "evidence" / "round51" / "quote-substance-check.py"
    substance = (subst.is_file() and man.is_file() and
                 subprocess.run([sys.executable, str(subst), str(man)], capture_output=True, text=True).returncode == 0)

    anchors = 0
    for r in rows:
        if len(r) == 11 and r[0] in bound:
            chars = [int(c) for c in CHAR_RE.findall(r[5])]
            anchors += bool(chars) and all(c in offsets.get(r[0], set()) for c in chars)

    grounded = 0
    tool = root / "tools" / "inference-ground.py"
    for path in ENTRIES:
        if path not in texts or not tool.is_file():
            continue
        p = subprocess.run([sys.executable, str(tool), "--entry", str(root / path), "--spans", str(man),
                            "--counts", "/dev/null", "--registry", str(sources), "--root", str(root), "--quiet"],
                           capture_output=True, text=True)
        grounded += p.returncode == 0

    theme = {url_of(u): u for _e, _s, u in DOCS}
    theme.update({url_of(k): v for k, v in ALIASES.items()})
    reg_ids: dict[str, str] = {}
    for line in REGISTER.read_text(encoding="utf-8").splitlines():
        f = line.split("|")
        if len(f) > 6 and "`chousa`" in f[1] and re.search(r"round[0-9]+", f[2]) and re.search(r"S[0-9]+", f[3]):
            u = url_of(f[5])
            if u in theme:
                reg_ids[re.search(r"S[0-9]+", f[3]).group(0)] = theme[u]
    verdicts: dict[str, str] = {}
    for line in lesson.splitlines():
        m = VERDICT_RE.search(line)
        if m and m.group(1) in reg_ids:
            verdicts[m.group(1)] = m.group(2)
    blocked = sum(1 for rid, v in verdicts.items()
                  if v in ("fabricated", "unverifiable") and reg_ids[rid] in bound.values())

    print(f"ENTRIES={len(texts)}/3")
    print(f"BOUND={nbound}/{len(by_doc)} (min {MIN_BOUND}) REFUSED={refused}")
    print(f"BOUND_IDS={','.join(sorted(bound))}")
    print(f"REF_ID_UNBOUND={unb}")
    print(f"NEW_GROUND={new_ground}/3")
    print(f"QUOTE_ROWS={n} ON_BOUND={on_bound}/{n}")
    print(f"SPAN_IDS={ids_ok}/{nbound} (min {MIN_PER_ID} each)")
    print(f"QUOTES_IN_SPAN={in_span}/{n}")
    print(f"QUOTES_IN_ENTRY={in_entry}/{n}")
    print(f"QUOTES_IN_LESSON={in_lesson}/{n}")
    print(f"QUOTE_SHORT={short}/{n}")
    print(f"SPAN_CONTEXT={ctx}/{n}")
    print("CAPTURE_BOUND=skipped" if a.lane_only else f"CAPTURE_BOUND={cap_bound}/{n}")
    print(f"SUBSTANCE={'PASS' if substance else 'FAIL'}")
    print(f"ANCHOR_BOUND={anchors}/{nbound}")
    print(f"INFERENCE_GROUNDED={grounded}/3")
    print(f"QUARANTINE_VERDICTS={len(verdicts)}/{len(reg_ids)} ({','.join(sorted(reg_ids))})")
    print(f"QUARANTINE_BLOCKED_ADOPTED={blocked}")
    ok = (len(texts) == 3 and nbound >= MIN_BOUND and nbound + refused == len(by_doc) and unb == 0
          and new_ground == 3 and n > 0 and on_bound == n and ids_ok == nbound and in_span == n
          and in_entry == n and in_lesson == n and short == n and ctx == n and (a.lane_only or cap_bound == n)
          and substance and anchors == nbound and grounded == 3 and len(verdicts) == len(reg_ids) and not blocked)
    print("C2=PASS" if ok else "C2=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
