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
     data span);
  5. no grounding token flips POLARITY (round 47, `INF_POLARITY_FLIP`, the
     same sentence as `corpus/evidence/round47/claims.md`, claim C1): a phrase
     its span NEGATES (a negator inside it, or among the three span words
     before it) is refused when the bullet's own unquoted words use one of its
     scope words (same five-letter stem) with no negator in the three words
     before or two after; a phrase its span does not negate is refused when
     the bullet's own words put a negator in the three words before one of its
     content words; a figure grounded by a counts key whose name carries
     `no`/`not`/`none`/`without` must be followed by a negator in the
     bullet's next four words, and one whose key does not must not be.
     Refinements after the round-47 wave-1 attacks (no rule widened toward
     acceptance of a flip): every occurrence of a phrase in the cited spans is
     read, and occurrences of mixed polarity decide nothing (row order no
     longer decides); on the SPAN side only explicit negators (`no`, `not`,
     `never`, … and `n't`) negate a phrase, and only within its own line and
     clause; in the BULLET's windows negators also include implicit ones
     (`lacks`, `absent`, `missing`, `un…able`/`un…ed` forms); an `un`-prefixed
     form of an affirmed phrase's word (`unfrozen`) is a flip unless a negator
     precedes it; every occurrence of a figure is checked at digit boundaries;
     the leaf key (`_`, `-` or camelCase separated; a generic leaf such as
     `count` defers to its parent) carries a figure's negation; mixed-polarity
     keys decide nothing. The clause bound also ACCEPTS a bullet that a
     negator on a previous span line would have refused (wave-2
     `CritC1Claim` §2): a deliberate trade toward reading the span as written.

Usage:
  python3 tools/inference-ground.py --entry PATH --spans TSV --counts JSON
                                    [--registry corpus/SOURCES.md]
                                    [--root DIR] [--json OUT] [--quiet]

Exit codes: 0 grounded (no findings) · 1 findings · 2 usage or a missing/unreadable
entry (an unreadable --spans/--counts/--registry reads as empty, fail-closed).

Named limit: this is lexical. Rule 5 catches a flip that reuses the span's own
stem; a wrong inference through a synonym, an antonym of a different stem, or
scope beyond the word windows still passes. Semantics stay the critic's and
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
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def has_two_words(s: str) -> bool:
    words = [w for w in re.split(r"\s+", s.strip()) if WORD_RE.search(w)]
    return len(words) >= 2


def inference_bullets(text: str) -> tuple[bool, list[str]]:
    """Every bullet of every `#### Inference` section (all of them, not the first).

    A second Inference section is prose a reader sees, so its bullets are
    checked too (round-46 `MutC1More` M4: a junk second section was never read).
    """
    lines = text.splitlines()
    heads, fence = [], False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = HEAD_RE.match(line)
        if m and m.group(1) == "####" and m.group(2).strip().lower().startswith("inference"):
            heads.append(i)
    if not heads:
        return False, []
    bullets: list[str] = []
    for h in heads:
        cur: str | None = None
        fence = False
        for line in lines[h + 1:]:
            if line.lstrip().startswith("```"):
                # A fence is literal for HEADINGS but never hides a bullet: a
                # junk inference parked inside a fence still renders to a reader.
                fence = not fence
                if cur is not None:
                    bullets.append(cur)
                    cur = None
                continue
            if not fence:
                m = HEAD_RE.match(line)
                if m and len(m.group(1)) <= 4:
                    break
            if line.startswith("- ") or line.startswith("* "):
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


def numeral_in(tok: str, text: str) -> bool:
    """A figure matches at digit boundaries only: `959` is not `5,959`."""
    bare = tok.rstrip("%")
    return re.search(r"(?<![\d,])" + re.escape(bare) + r"(?![\d,])", text) is not None


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


NEG_WORDS = {"no", "not", "never", "none", "nothing", "nobody", "nowhere",
             "without", "cannot", "nor", "neither"}
NEG_KEY_PARTS = {"no", "not", "none", "without"}
STOP = {"this", "that", "with", "from", "have", "been", "were", "which", "their",
        "there", "into", "only", "each", "every", "than", "then", "they", "them",
        "these", "those", "such", "also", "more", "most", "some", "what", "when",
        "where", "will", "would", "could", "should", "does", "done", "being",
        "about", "after", "before", "over", "under", "upon", "both", "other",
        "same", "here", "very", "just", "your", "ours", "itself"}
WORDS_RE = re.compile(r"[a-z][a-z'\u2019]*")


def words(s: str) -> list[str]:
    return WORDS_RE.findall(s.lower())


# Implicit negators (round-47 `LabC1FalsePos`: 9 of 10 correctly-reasoned
# bullets were refused because `lacks`, `absent` or `untraceable` read as
# affirmative). A lexical list, not a parser.
IMPLICIT_NEG = {"lack", "lacks", "lacked", "lacking", "absent", "absence",
                "missing", "fail", "fails", "failed", "unable", "nothing",
                "omits", "omitted", "devoid"}
UN_NEG_RE = re.compile(r"^un(?!der|til|ion|ique|it|iver|iform|less|ifi|pack|veil|fold|wrap)"
                       r"[a-z]{3,}(?:able|ible|ed|known|clear|sure)$")


def is_explicit_neg(w: str) -> bool:
    return w in NEG_WORDS or w.endswith("n't") or w.endswith("n\u2019t")


def is_neg(w: str) -> bool:
    """A negator in the BULLET's own words: explicit, implicit or an un- form."""
    return is_explicit_neg(w) or w in IMPLICIT_NEG or bool(UN_NEG_RE.match(w))


def stem(w: str) -> str:
    return w[:5]


def content(ws: list[str]) -> list[str]:
    return [w for w in ws if len(w) >= 4 and not is_neg(w) and w not in STOP]


def unquoted(bullet: str) -> str:
    return ID_RE.sub(" ", BACKTICK_RE.sub(" ", QUOTE_RE.sub(" ", bullet)))


def occurrence_polarity(tok: str, s: str, idx: int) -> tuple[bool, list[str]]:
    """(negated, scope words) for one occurrence of a phrase in a span.

    Negated when a negator sits inside the phrase (scope = the content words
    after it) or among the three span words just before it, inside the
    phrase's own line and clause (a negator on a previous list line, such as
    `(Unlabelled)` above `Pre-processed Wikipedia Pages`, does not negate it).
    """
    inner = words(tok)
    negs = [k for k, w in enumerate(inner) if is_explicit_neg(w)]
    if negs:
        return True, content(inner[negs[0] + 1:])
    before = re.split(r"[\n.;:()]", s[:idx])[-1]
    return any(is_explicit_neg(w) for w in words(before)[-3:]), content(inner)


def phrase_polarity(tok: str, spans: list[str]) -> tuple[bool, list[str]] | None:
    """(negated, scope words) over EVERY occurrence of a phrase in the cited
    spans; None when no span carries it or the occurrences disagree (round-47
    `ReviewerC1Polarity` M4: reading the first carrying span made the verdict
    depend on manifest row order)."""
    seen: list[tuple[bool, list[str]]] = []
    for s in spans:
        start = s.find(tok)
        while start >= 0:
            seen.append(occurrence_polarity(tok, s, start))
            start = s.find(tok, start + 1)
    if not seen or len({neg for neg, _ in seen}) != 1:
        return None
    negated = seen[0][0]
    scope = sorted({w for _, sc in seen for w in sc})
    return negated, scope


def polarity_flips(bullet: str, tok: str, spans: list[str]) -> list[str]:
    """Bullet words that assert the opposite polarity of a span-carried phrase.

    P1: the span negates the phrase, and the bullet's own (unquoted) text uses a
    scope word (same 5-letter stem) with no negator in the 3 words before or 2
    after it. P2: the span does not negate the phrase, and the bullet's own
    text puts a negator in the 3 words before one of the phrase's content words,
    or uses an `un`-prefixed form of one (`frozen` -> `unfrozen`).
    """
    pol = phrase_polarity(tok, spans)
    if pol is None:
        return []
    negated, scope = pol
    stems = {stem(w) for w in scope}
    if not stems:
        return []
    uw = words(unquoted(bullet))
    out = []
    for j, w in enumerate(uw):
        if (not negated and w.startswith("un") and len(w) >= 6
                and stem(w[2:]) in stems):
            if not any(is_neg(x) for x in uw[max(0, j - 3):j]):
                out.append(w)
            continue
        if is_neg(w) or len(w) < 4 or w in STOP or stem(w) not in stems:
            continue
        before, after = uw[max(0, j - 3):j], uw[j + 1:j + 3]
        if negated and not any(is_neg(x) for x in before + after):
            out.append(w)
        elif not negated and any(is_neg(x) for x in before):
            out.append(w)
    return out


KEY_PART_RE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")


def count_keys(counts: pathlib.Path) -> dict[str, set[str]]:
    """numeral string -> the key PATHS that carry it (every ancestor key, so a
    nested `{"without_archive": {"count": 1582}}` keeps its negation)."""
    out: dict[str, set[str]] = {}
    if not counts.is_file():
        return out
    try:
        data = json.loads(read(counts))
    except json.JSONDecodeError:
        return out

    def walk(node, path: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}/{k}" if path else str(k))
        elif isinstance(node, list):
            for v in node:
                walk(v, path)
        elif isinstance(node, bool):
            return
        elif isinstance(node, (int, float)):
            for s in (str(node), f"{node:,}"):
                out.setdefault(s, set()).add(path)
        elif isinstance(node, str) and re.fullmatch(r"\d[\d,]*", node.strip()):
            bare = node.strip().replace(",", "")
            for s in (bare, f"{int(bare):,}"):
                out.setdefault(s, set()).add(path)

    walk(data, "")
    return out


GENERIC_KEYS = {"count", "counts", "value", "values", "n", "total", "number"}


def key_negated(path: str) -> bool:
    """The leaf key names the quantity; a generic leaf (`count`) defers to its
    parent. Ancestor grouping labels (`extra_not_frozen/real_source_answers`)
    do not negate the figure (round-47 wave-2 `SweepC1Corpus`)."""
    parts = path.split("/")
    leaf = parts[-1]
    if leaf.lower() in GENERIC_KEYS and len(parts) > 1:
        leaf = parts[-2]
    return any(p.lower() in NEG_KEY_PARTS for p in KEY_PART_RE.findall(leaf))


def figure_flip(bullet: str, tok: str, keys: set[str]) -> bool:
    """P3: a counts figure whose key path names a negation (`answers_without_key`)
    must be followed by a negator in the bullet's next 4 words, and one whose
    key does not must not be — at EVERY occurrence of the figure, located at
    digit boundaries; keys of mixed polarity decide nothing."""
    pols = {key_negated(k) for k in keys}
    if len(pols) != 1:
        return False
    key_neg = pols.pop()
    text = unquoted(bullet)
    bare = tok.rstrip("%")
    for m in re.finditer(r"(?<![\d,.])" + re.escape(bare) + r"(?![\d,])", text):
        nxt = words(text[m.end():])[:4]
        if key_neg != any(is_neg(w) for w in nxt):
            return True
    return False


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
    keymap = count_keys(counts)
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
            is_num = bool(re.fullmatch(r"\d[\d,]*(?:\.\d+)?%?", tok))
            ok = any(numeral_in(tok, s) if is_num else tok in s for s in grounded)
            if ok and not is_num:
                for w in polarity_flips(bullet, tok, grounded):
                    findings.append({"code": "INF_POLARITY_FLIP", "bullet": i,
                                     "token": f"{tok[:60]} / {w}"})
            if not ok and re.search(r"\d", tok):
                ok = any(v in values for v in numeral_variants(tok))
                if ok and is_num:
                    keys = set().union(*(keymap.get(v, set()) for v in numeral_variants(tok)))
                    if figure_flip(bullet, tok, keys):
                        findings.append({"code": "INF_POLARITY_FLIP", "bullet": i,
                                         "token": f"{tok} / counts key {','.join(sorted(keys))}"})
            if not ok and re.search(r"\d", tok):
                # A cited DOCUMENT may ground its own designator (RFC 7089 in
                # S079's title), and nothing else: a bare year or a URL run in
                # the same cell must not ground a figure (round-46
                # `ReviewerC1Tool`).
                bare = tok.rstrip("%").replace(",", "")
                ok = any(d in bullet and bare in d.replace(",", "")
                         for sid in cited for d in designators(titles.get(sid, "")))
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
        try:
            pathlib.Path(a.json).write_text(
                json.dumps({"entry": entry_rel, "section": present, "bullets": len(bullets),
                            "tokens": ntok, "grounded": ngood, "findings": findings}, indent=1),
                encoding="utf-8")
        except OSError as exc:
            print(f"inference-ground: cannot write --json: {exc}", file=sys.stderr)
            return 2
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
