#!/usr/bin/env python3
"""c2-count — frozen counter for round 51 claim C2 (depth, sourced).

Predicate R51-C2, the same sentence as corpus/evidence/round51/claims.md:
the theme "what a Japanese or a Chinese systematic-review search record must
carry" is adopted BY DOCUMENT as the three lane entries
`corpus/knowledge/japanese-search-record-r38.md`,
`corpus/knowledge/chinese-search-record-r39.md` and
`corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`; of the
seven staged documents they rest on (the J-STAGE 日本健康教育学会誌 article and
the 健康食品産業協議会 reporting form cited by the first, the two 实验动物与比较医学
PDFs and the SinoMed record cited by the second, the 国立保健医療科学院 submission
form and the 日本保健医療行動科学会雑誌 article cited by the third), at least five
are BOUND — exactly one lane Registry row carries the document's URL, that row
is new since BASE_REV, `mined`, opened 2026-10-25, its `used-by` names exactly
the entries citing it, and every citing entry carries a `source: <that id> —
<url>` line — and every other one is REFUSED (no lane row, no `source:` line,
and a `refused-doc` line naming its URL in `corpus/lessons/round-51.md`); no
`S###` token appears in the entries except a bound id; at BASE_REV no
`corpus/knowledge` file held 検索式, 検索期間 or 检索策略, and each entry holds its
own term (検索式, 检索策略, 検索期間 respectively); `corpus/evidence/round51/spans.tsv`
(derived by `build-spans.py`) carries at least three quote rows per bound id,
each quote at most 25 whitespace words and 160 characters, inside its span
file, inside the citing entry and inside the round-51 lesson, each span file
the exact slice of the capture text form at the recorded offset whose file
digest is the recorded one, and longer than its quote;
`quote-substance-check.py` exits 0 on the manifest; every `char N` in a bound
row's `anchor` cell (at least one) is the offset of a quote of that id; all
three entries exit 0 under `tools/inference-ground.py` with this round's spans;
and the lesson carries a re-check verdict line for each absent-defect-register
row on a theme URL (the sweep prints how many there are), with no bound
document whose verdict is `fabricated` or `unverifiable`.

`--lane-only` reads lane bytes only: `CAPTURE_BOUND` prints `skipped`.
Cheapest shortcuts and what refuses them: copying the staged entries unchanged
leaves staged ids (S097 S105 S106 and the unrenumbered S109..S126) that name lane
rows of OTHER documents (REF_ID_UNBOUND, BOUND); a hollow quote or a
whole-capture span fails SUBSTANCE; invented spans/digests pass `--lane-only`
and fail `CAPTURE_BOUND`. Verdict-line truth is the closure's.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
REGISTER = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md")
BASE_REV = "9ec1751a24231e899ceea4688e21c8edf6046d35"
OPENED = "2026-10-25"
E_JA = "corpus/knowledge/japanese-search-record-r38.md"
E_ZH = "corpus/knowledge/chinese-search-record-r39.md"
E_JA2 = "corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md"
ENTRIES = (E_JA, E_ZH, E_JA2)
JSTAGE = "https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja"
JAOHFA = "https://jaohfa.com/pdf/systematic_review.pdf"
SLARC_A = "https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290"
SLARC_B = "https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237"
SINOMED = "https://www.sinomed.ac.cn/article.do?ui=2026335073"
NIPH = "https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx"
JAHBS = "https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf"
# (citing entry, staged id in the package, staged URL) — seven pairs over seven documents
DOCS = [
    (E_JA, "S109", JSTAGE),
    (E_JA, "S110", JAOHFA),
    (E_ZH, "S116", SLARC_A),
    (E_ZH, "S117", SLARC_B),
    (E_ZH, "S119", SINOMED),
    (E_JA2, "S125", NIPH),
    (E_JA2, "S126", JAHBS),
]
TERMS = {E_JA: "検索式", E_ZH: "检索策略", E_JA2: "検索期間"}
MIN_BOUND = 5
MIN_PER_ID = 3
HELD: set[str] = set()
ID_RE = re.compile(r"\bS\d{3,}\b")
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S\d{3,})[ \t]*\|")
CHAR_RE = re.compile(r"\bchar\s+(\d+)")
VERDICT_RE = re.compile(r"register\s+`?(S\d{3,})`?.*?verdict[:=]?\s*\**`?(present|absent-as-written|unverifiable|fabricated)`?")


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


def form_text(url: str, digest: str) -> str | None:
    """The capture text form whose FILE digest is `digest` (see build-spans)."""
    txt, raw = CACHE / f"{key(url)}.txt", CACHE / f"{key(url)}.raw"
    if txt.is_file() and hashlib.sha256(txt.read_bytes()).hexdigest() == digest:
        return txt.read_text(encoding="utf-8", errors="replace")
    if raw.is_file():
        b = raw.read_bytes()
        if hashlib.sha256(b).hexdigest() == digest:
            return b.decode("utf-16le", errors="replace")
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
    ev = root / "corpus" / "evidence" / "round51"
    sources = root / "corpus" / "SOURCES.md"
    lesson_p = root / "corpus" / "lessons" / "round-51.md"
    base = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:corpus/SOURCES.md"],
                          capture_output=True, text=True)
    if base.returncode != 0 or not REGISTER.is_file():
        print("NO_BASE_OR_REGISTER")
        return 2
    base_ids = {r[0] for r in registry(base.stdout)}
    rows = registry(sources.read_text(encoding="utf-8")) if sources.is_file() else []
    texts = {p: (root / p).read_text(encoding="utf-8") for p in ENTRIES if (root / p).is_file()}
    lesson = lesson_p.read_text(encoding="utf-8") if lesson_p.is_file() else ""

    # documents: group the pairs by normalised URL; a document is BOUND when every
    # pair is bound, REFUSED when every pair is refused; a mixed document counts as neither
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

    unb = sum(1 for t in texts.values() for i in ID_RE.findall(t) if i not in bound and i not in HELD)

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
            ft = form_text(url, digest)
            o = int(offset)
            cap_bound += ft is not None and ft[o:o + len(span)] == span
    ids_ok = sum(per_id.get(sid, 0) >= MIN_PER_ID for sid in bound)

    subst = ev / "quote-substance-check.py"
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
