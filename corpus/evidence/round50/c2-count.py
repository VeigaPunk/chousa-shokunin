#!/usr/bin/env python3
"""c2-count — frozen counter for round 50 claim C2 (depth, sourced).

Predicate R50-C2, the same sentence as corpus/evidence/round50/claims.md:
the theme "what a Chinese citation-checking feature compares, and which of
CNKI's manuals document it" is adopted BY DOCUMENT as the three lane entries
`corpus/knowledge/cnki-citation-check-r40.md`,
`corpus/knowledge/citation-matching-semantics-r41.md` and
`corpus/knowledge/istic-citation-verification-r39.md`; of the four staged
documents they rest on (the CNKI 管理员 manual PDF cited by the first two
entries, the CNKI 子账号 manual PDF and 教师 manual PDF cited by the second, the
ISTIC 引证检索 service page cited by the third), at least three are BOUND —
exactly one lane Registry row carries the document's URL, that row is new
since BASE_REV, `mined`, opened 2026-10-25, its `used-by` names exactly the
entries citing it, and every citing entry carries a `source: <that id> —
<url>` line — and the other one is REFUSED (no lane row, no `source:` line,
and a `refused-doc` line naming its URL in `corpus/lessons/round-50.md`); no
`S###` token appears in the entries except a bound id; at BASE_REV no
`corpus/knowledge` file held 引文核对 or 引证检索, and each entry holds its own
term; `corpus/evidence/round50/spans.tsv` (derived by `build-spans.py`)
carries at least three quote rows per bound id, each quote at most 25
whitespace words and 160 characters, inside its span file, inside the citing
entry and inside the round-50 lesson, each span file the exact slice of the
capture text form at the recorded offset whose file digest is the recorded
one, and longer than its quote; `quote-substance-check.py` exits 0 on the
manifest; every `char N` in a bound row's `anchor` cell (at least one) is the
offset of a quote of that id; all three entries exit 0 under
`tools/inference-ground.py` with this round's spans; and the lesson carries a
re-check verdict line for each absent-defect-register row on a theme URL (the
sweep prints how many there are), with no bound document whose verdict is
`fabricated` or `unverifiable`.

`--lane-only` reads lane bytes only: `CAPTURE_BOUND` prints `skipped`.
Cheapest shortcuts and what refuses them: copying the staged entries unchanged
leaves staged ids (S076 S109 S111 S118 S124 S135 S136 S145) that name lane rows
of OTHER documents (REF_ID_UNBOUND, BOUND); a hollow quote or a whole-capture
span fails SUBSTANCE; invented spans/digests pass `--lane-only` and fail
`CAPTURE_BOUND`. Verdict-line truth is the closure's.

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
BASE_REV = "3c51da77b3696ed884c943548ec4b4006e3ca528"
OPENED = "2026-10-25"
E_R40 = "corpus/knowledge/cnki-citation-check-r40.md"
E_R41 = "corpus/knowledge/citation-matching-semantics-r41.md"
E_R39 = "corpus/knowledge/istic-citation-verification-r39.md"
ENTRIES = (E_R40, E_R41, E_R39)
SXU = "https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf"
SEU = "https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf"
BNU = "https://bs.bnu.edu.cn/docs/20160407183946745914.pdf"
ISTIC = "https://chaxin.las.ac.cn/service/citation-search"
# (citing entry, staged id in the package, staged URL) — five pairs over four documents
DOCS = [
    (E_R40, "S124", SXU),
    (E_R41, "S135", SXU),
    (E_R41, "S136", SEU),
    (E_R41, "S145", BNU),
    (E_R39, "S118", ISTIC),
]
TERMS = {E_R40: "引文核对", E_R41: "引文核对", E_R39: "引证检索"}
MIN_BOUND = 3
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
    ev = root / "corpus" / "evidence" / "round50"
    sources = root / "corpus" / "SOURCES.md"
    lesson_p = root / "corpus" / "lessons" / "round-50.md"
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
    for entry, term in TERMS.items():
        g = subprocess.run(["git", "-C", str(LANE), "grep", "-l", "-e", "引文核对", "-e", "引证检索", BASE_REV, "--", "corpus/knowledge"],
                           capture_output=True, text=True)
        new_ground += g.returncode == 1 and term in texts.get(entry, "")

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
