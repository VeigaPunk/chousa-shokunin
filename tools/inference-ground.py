#!/usr/bin/env python3
"""inference-ground — is an entry's `#### Inference` section CITED and GROUNDED,
or merely plausible? (round 46; QUALITY criterion 66)

The round-45 wave-2 critic `CritC3Axis` showed the lane's entry counter
(`corpus/evidence/round45/c3-count.py`) checks that quotes and counts are
PRESENT in an entry, so a junk entry body that reuses the committed spans and
counts passes both of its modes. This tool closes that class at the sentence
level, one bullet at a time, without pretending to judge meaning.

Rule (the same sentence as `corpus/evidence/round46/claims.md`, claim C1):

  1. the entry carries a `#### Inference` section, which ends at the next
     heading of level <= 4 (fenced headings are literal);
  2. every bullet of that section cites at least one source id (`S` + 3 or
     more digits);
  3. every bullet carries at least one grounding token: a backticked or
     double-quoted phrase of two or more words, or a numeral of three or more
     digits, or a percentage;
  4. every grounding token of a bullet appears VERBATIM in a span belonging to
     a source that bullet cites (the spans manifest's `id` and `span_file`
     columns), or — for a numeral — equals a value in the counts manifest or
     appears in the title of a Registry row the bullet cites (a document
     number such as `RFC 7089` is grounded by the document it names, not by a
     data span).

Usage:
  python3 tools/inference-ground.py --entry PATH --spans TSV --counts JSON
                                    [--registry corpus/SOURCES.md]
                                    [--root DIR] [--json OUT] [--quiet]

Exit codes: 0 grounded (no findings) · 1 findings · 2 usage or a missing/unreadable
entry (an unreadable --spans/--counts/--registry reads as empty, fail-closed).

Named limit: this is lexical. A bullet that strings correct quotes and correct
figures into a wrong inference still passes; only a sentence whose quotes or
figures are not in the cited spans is refused. Semantics stay the critic's and
the closure's to judge.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ID_RE = re.compile(r"\bS\d{3,}\b")
BACKTICK_RE = re.compile(r"`([^`\n]{4,})`")
QUOTE_RE = re.compile(r'"([^"\n]{4,})"')
NUM_RE = re.compile(r"(?<![\w.])(\d[\d,]{2,}(?:\.\d+)?%?|\d+(?:\.\d+)?%)")
HEAD_RE = re.compile(r"^(#{1,4})\s+(.*)$")
WORD_RE = re.compile(r"[A-Za-z]")


def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def has_two_words(s: str) -> bool:
    words = [w for w in re.split(r"\s+", s.strip()) if WORD_RE.search(w)]
    return len(words) >= 2


def inference_bullets(text: str) -> tuple[bool, list[str]]:
    lines = text.splitlines()
    start, fence = None, False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = HEAD_RE.match(line)
        if m and m.group(1) == "####" and m.group(2).strip().lower().startswith("inference"):
            start = i + 1
            break
    if start is None:
        return False, []
    bullets, cur, fence = [], None, False
    for line in lines[start:]:
        if line.lstrip().startswith("```"):
            # A fence is literal for HEADINGS (a fenced `## Unknown` does not
            # end the section) but never hides a bullet: a junk inference line
            # parked inside a fence still renders to a reader, so it is counted
            # (round-46 mutation survivor `MutC1Junk`).
            fence = not fence
            if cur is not None:
                bullets.append(cur)
                cur = None
            continue
        if not fence:
            m = HEAD_RE.match(line)
            if m and len(m.group(1)) <= 4:
                break
        if line.startswith("- "):
            if cur is not None:
                bullets.append(cur)
            cur = line[2:].strip()
            continue
        if cur is not None:
            if line.strip() == "":
                bullets.append(cur)
                cur = None
            else:
                cur += " " + line.strip()
    if cur is not None:
        bullets.append(cur)
    return True, [b for b in bullets if b.strip()]


def grounding_tokens(bullet: str) -> list[str]:
    tokens: list[str] = []
    for m in BACKTICK_RE.finditer(bullet):
        if has_two_words(m.group(1)):
            tokens.append(m.group(1).strip())
    for m in QUOTE_RE.finditer(bullet):
        if has_two_words(m.group(1)):
            tokens.append(m.group(1).strip())
    scrubbed = ID_RE.sub(" ", BACKTICK_RE.sub(" ", QUOTE_RE.sub(" ", bullet)))
    for m in NUM_RE.finditer(scrubbed):
        tokens.append(m.group(1))
    return tokens


def numeral_variants(tok: str) -> list[str]:
    bare = tok.rstrip("%").replace(",", "")
    out = {tok, bare}
    if re.fullmatch(r"\d+", bare):
        out.add(f"{int(bare):,}")
    return [o for o in out if o]


def span_texts(spans: pathlib.Path, cited: set[str]) -> list[str]:
    """Span texts for the sources a bullet cites.

    The manifest's `entry` column is provenance only (which entry first cited
    the span); it never narrows the lookup, or a second entry citing the same
    source would read as ungrounded.
    """
    if not spans.is_file():
        return []
    out, lines = [], read(spans).splitlines()
    for line in lines[1:]:
        if not line.strip():
            continue
        cells = line.split("\t")
        if len(cells) != 7:
            continue
        sid, _url, _sha, _off, span_file, _quote, _entry = cells
        if sid.strip() not in cited:
            continue
        raw = span_file.strip()
        # A span file is a name INSIDE the manifest's directory: an absolute
        # path or a `..` component would turn this read-only check into an
        # oracle over the filesystem (round-46 sentinel F3).
        if not raw or raw.startswith("/") or ".." in pathlib.PurePath(raw).parts:
            continue
        base = spans.parent.resolve()
        p = (base / raw).resolve()
        try:
            p.relative_to(base)
        except ValueError:
            continue
        if p.is_file():
            out.append(read(p))
    return out


def registry_source(registry: pathlib.Path) -> dict[str, str]:
    """id -> the row's `source` cell (the document title), for numeral grounding."""
    out: dict[str, str] = {}
    if not registry.is_file():
        return out
    inside = False
    for line in read(registry).splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Registry"
            continue
        if not inside or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 11 and re.fullmatch(r"S\d{3,}", cells[0]):
            # Title only: the URL runs do not ground a figure (round-46
            # `ReviewerC1Tool`: `…acl-long.1534` grounded an invented 1,534).
            out[cells[0]] = cells[1].split(" — http")[0]
    return out


DESIGNATOR_RE = re.compile(r"\b[A-Z]{2,7}\s?\d[\d,]{2,}[A-Za-z0-9-]*\b|\b[A-Za-z]{1,3}\d{3,}\b")


def designators(title: str) -> list[str]:
    """Document designators a title can ground: `RFC 7089`, `E2867`, `N18-1074`."""
    return DESIGNATOR_RE.findall(title)


def count_values(counts: pathlib.Path) -> set[str]:
    if not counts.is_file():
        return set()
    try:
        data = json.loads(read(counts))
    except json.JSONDecodeError:
        return set()
    out: set[str] = set()

    def walk(node) -> None:
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, bool):
            return
        elif isinstance(node, (int, float)):
            out.add(str(node))
            out.add(f"{node:,}")
        elif isinstance(node, str) and re.fullmatch(r"\d[\d,]*", node.strip()):
            out.add(node.strip().replace(",", ""))

    walk(data)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--entry", required=True)
    ap.add_argument("--spans", required=True)
    ap.add_argument("--counts", required=True)
    ap.add_argument("--registry", default=None)
    ap.add_argument("--root", default=".", help="root the entry path is reported relative to")
    ap.add_argument("--json", default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    entry = pathlib.Path(a.entry)
    spans = pathlib.Path(a.spans)
    counts = pathlib.Path(a.counts)
    if not entry.is_file():
        print(f"inference-ground: no entry {entry}", file=sys.stderr)
        return 2
    text = read(entry)
    try:
        entry_rel = str(entry.resolve().relative_to(pathlib.Path(a.root).resolve()))
    except ValueError:
        entry_rel = entry.name
    present, bullets = inference_bullets(text)
    findings: list[dict] = []
    if not present:
        findings.append({"code": "INF_SECTION_ABSENT", "bullet": 0, "token": ""})
    values = count_values(counts)
    titles = registry_source(pathlib.Path(a.registry)) if a.registry else {}
    ntok = ngood = 0
    for i, bullet in enumerate(bullets, 1):
        cited = set(ID_RE.findall(bullet))
        if not cited:
            findings.append({"code": "INF_UNCITED", "bullet": i, "token": ""})
        toks = grounding_tokens(bullet)
        if not toks:
            findings.append({"code": "INF_UNGROUNDED", "bullet": i, "token": ""})
        grounded = span_texts(spans, cited)
        for tok in toks:
            ntok += 1
            ok = any(tok in s for s in grounded)
            if not ok and re.search(r"\d", tok):
                ok = any(v in values for v in numeral_variants(tok))
            if not ok and re.search(r"\d", tok):
                # A cited DOCUMENT may ground its own designator (RFC 7089 in
                # S079's title), and nothing else: a bare year or a URL run in
                # the same cell must not ground a figure (round-46
                # `ReviewerC1Tool`).
                ok = any(d in bullet for sid in cited for d in designators(titles.get(sid, "")))
            if ok:
                ngood += 1
            else:
                findings.append({"code": "INF_TOKEN_NOT_IN_SPAN", "bullet": i, "token": tok[:80]})
    if present and not bullets:
        findings.append({"code": "INF_NO_BULLETS", "bullet": 0, "token": ""})
    if not a.quiet:
        print(f"GROUND entry={entry_rel or entry.name} section={int(present)} "
              f"bullets={len(bullets)} tokens={ntok} grounded={ngood}")
        for f in findings:
            print(f"FINDING {f['code']} bullet={f['bullet']} token={f['token']!r}")
        print("GROUND: PASS" if not findings else "GROUND: FAIL")
    if a.json:
        pathlib.Path(a.json).write_text(
            json.dumps({"entry": entry_rel, "section": present, "bullets": len(bullets),
                        "tokens": ntok, "grounded": ngood, "findings": findings}, indent=1),
            encoding="utf-8")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
