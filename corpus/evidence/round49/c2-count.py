#!/usr/bin/env python3
"""c2-count — frozen counter for round 49 claim C2 (depth, sourced).

Predicate R49-C2, the same sentence as corpus/evidence/round49/claims.md:
the theme "a citation index's data is a derived artefact" is adopted BY
DOCUMENT as the two lane entries `corpus/knowledge/aggregator-vs-source-r36.md`
and `corpus/knowledge/citation-count-semantics-r37.md`; of the nine staged
documents they rest on, at least seven are BOUND — exactly one lane Registry
row carries the document's URL, that row is new since BASE_REV, `mined`,
opened 2026-10-25, its `used-by` names the citing entry, and the entry carries
a `source: <that id> — <url>` line — and every other one is REFUSED (no lane
row, no `source:` line, and a `refused-doc` line naming its URL in
`corpus/lessons/round-49.md`); every `S###` token in either entry is a bound
id or the held S003; `corpus/evidence/round49/spans.tsv` (derived by
`build-spans.py`) carries at least two quote rows per bound id, each quote at
most 25 whitespace words and 160 characters, inside its span file, inside the
citing entry and inside the round-49 lesson, each span file the exact slice of
the capture text form at the recorded offset whose file digest is the recorded
one, and longer than its quote; every `char N` in a bound row's `anchor` cell
(at least one) is the offset of a quote of that id; both entries exit 0 under
`tools/inference-ground.py` with this round's spans; and the lesson carries a
re-check verdict line for each absent-defect-register row on a theme URL,
with no bound document whose verdict is `fabricated` or `unverifiable`.

`--lane-only` reads lane bytes only: `CAPTURE_BOUND` prints `skipped`.
Cheapest shortcuts and what refuses them: copying the staged entries
unchanged leaves staged ids S087-S103 that the lane registry already uses for
OTHER documents (REF_ID_UNBOUND, BOUND); invented spans/digests pass
`--lane-only` and fail `CAPTURE_BOUND`. Verdict-line truth is the closure's.

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
BASE_REV = "414a2ec6cde05a921dbdd9e02e7ae56b0db647ef"
OPENED = "2026-10-25"
E_AGG = "corpus/knowledge/aggregator-vs-source-r36.md"
E_CCS = "corpus/knowledge/citation-count-semantics-r37.md"
ENTRIES = (E_AGG, E_CCS)
# (citing entry, staged id in the package, staged URL) — the nine documents
DOCS = [
    (E_AGG, "S087", "https://support.nii.ac.jp/ja/cir/manual_articles_detail"),
    (E_AGG, "S088", "https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja"),
    (E_AGG, "S089", "https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja"),
    (E_AGG, "S091", "https://www.ncpssd.cn/"),
    (E_AGG, "S092", "https://eric.ed.gov/?id=EJ1372738"),
    (E_CCS, "S100", "https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc"),
    (E_CCS, "S101", "https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc"),
    (E_CCS, "S102", "https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf"),
    (E_CCS, "S103", "https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf"),
]
MIN_BOUND = 7
MIN_PER_ID = 2
HELD = {"S003"}
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
    ev = root / "corpus" / "evidence" / "round49"
    sources = root / "corpus" / "SOURCES.md"
    lesson_p = root / "corpus" / "lessons" / "round-49.md"
    base = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:corpus/SOURCES.md"],
                          capture_output=True, text=True)
    if base.returncode != 0 or not REGISTER.is_file():
        print("NO_BASE_OR_REGISTER")
        return 2
    base_ids = {r[0] for r in registry(base.stdout)}
    rows = registry(sources.read_text(encoding="utf-8")) if sources.is_file() else []
    texts = {p: (root / p).read_text(encoding="utf-8") for p in ENTRIES if (root / p).is_file()}
    lesson = lesson_p.read_text(encoding="utf-8") if lesson_p.is_file() else ""

    bound: dict[str, str] = {}      # lane id -> staged URL
    refused = 0
    for entry, _sid, url in DOCS:
        t = texts.get(entry, "")
        hits = [r for r in rows if len(r) == 11 and url_of(r[1]) == url_of(url)]
        if len(hits) == 1:
            r = hits[0]
            cites = re.search(r"^source:\s*" + r[0] + r"\s+—\s+" + re.escape(url) + r"(\s|$)", t, re.M)
            if (r[0] not in base_ids and r[7] == "mined" and r[8] == OPENED
                    and entry in [c.strip() for c in r[10].split(",")] and cites):
                bound[r[0]] = url
        elif not hits:
            no_src = not re.search(r"^source:.*" + re.escape(url), t, re.M)
            named = any("refused-doc" in l and url in l for l in lesson.splitlines())
            refused += no_src and named
    nb = len(bound)

    unb = sum(1 for t in texts.values() for i in ID_RE.findall(t) if i not in bound and i not in HELD)

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

    print(f"ENTRIES={len(texts)}/2")
    print(f"BOUND={nb}/{len(DOCS)} (min {MIN_BOUND}) REFUSED={refused}")
    print(f"BOUND_IDS={','.join(sorted(bound))}")
    print(f"REF_ID_UNBOUND={unb}")
    print(f"QUOTE_ROWS={n} ON_BOUND={on_bound}/{n}")
    print(f"SPAN_IDS={ids_ok}/{nb} (min {MIN_PER_ID} each)")
    print(f"QUOTES_IN_SPAN={in_span}/{n}")
    print(f"QUOTES_IN_ENTRY={in_entry}/{n}")
    print(f"QUOTES_IN_LESSON={in_lesson}/{n}")
    print(f"QUOTE_SHORT={short}/{n}")
    print(f"SPAN_CONTEXT={ctx}/{n}")
    print("CAPTURE_BOUND=skipped" if a.lane_only else f"CAPTURE_BOUND={cap_bound}/{n}")
    print(f"ANCHOR_BOUND={anchors}/{nb}")
    print(f"INFERENCE_GROUNDED={grounded}/2")
    print(f"QUARANTINE_VERDICTS={len(verdicts)}/{len(reg_ids)} ({','.join(sorted(reg_ids))})")
    print(f"QUARANTINE_BLOCKED_ADOPTED={blocked}")
    ok = (len(texts) == 2 and nb >= MIN_BOUND and nb + refused == len(DOCS) and unb == 0
          and n > 0 and on_bound == n and ids_ok == nb and in_span == n and in_entry == n
          and in_lesson == n and short == n and ctx == n and (a.lane_only or cap_bound == n)
          and anchors == nb and grounded == 2 and len(verdicts) == len(reg_ids) and not blocked)
    print("C2=PASS" if ok else "C2=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
