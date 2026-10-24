#!/usr/bin/env python3
"""quarantine-check — re-derive chousa's absent-defect-register quarantine slice and
examine every quarantined quote against locally available capture material.

What it is
    The lane's own gate for the wave-4 quarantine round (fleet lane-addendum item 10):
    the external campaign register lists the lane's quarantine scope, but its own
    class column is not trustworthy enough to adjudicate on. This tool re-derives
    the slice from the read-only register, locates each quarantined quote in the
    capture material that is already on disk, and applies the frozen decision rule.

Contract
    slice     re-derive the slice from the register; TSV: id, round, class, url, nquotes
    examine   examine every quarantined quote; TSV: id, qidx, status, fold, capture, offset
    verdict   apply the frozen decision rule; TSV: id, verdict, reason, evidence
    digests   print the sha256 of the register and of every capture consulted

Exit codes
    0 ok · 1 findings (a row could not be examined, or the slice is empty) · 2 usage/env

Provenance
    The register is read-only and lives in the external campaign tree; so does the
    capture cache. The cache key convention (sha256(url)[:24] + ".txt") and the
    eleven-fold matching semantics are re-implemented here from the campaign's own
    published checker source, read at
      /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint.py
    The campaign's checker is NEVER run from this lane: it writes into the campaign
    tree. This tool performs no network access of any kind; a row whose source has
    no local capture is reported as unverifiable, never as a fabrication.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys
import unicodedata

DEFAULT_REGISTER = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md"
DEFAULT_CACHE = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
LANE = "chousa"

# --- the eleven folds, loosest last (semantics copied from the campaign checker) ---
TYPO = {"“": '"', "”": '"', "‘": "'", "’": "'",
        "—": "-", "–": "-", "−": "-", "…": "...",
        "「": '"', "」": '"', "『": '"', "』": '"',
        "　": " "}
TAG_RE = re.compile(r"<[^>]+>")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def f_exact(doc, q):
    return q in doc


def f_ws(doc, q):
    return _ws(q) in _ws(doc)


def f_case(doc, q):
    return f_ws(doc.lower(), q.lower())


def f_nows(doc, q):
    n = lambda s: re.sub(r"\s+", "", s)  # noqa: E731
    return n(q) in n(doc)


def f_md(doc, q):
    n = lambda s: re.sub(r"[*_`]", "", s)  # noqa: E731
    return f_ws(n(doc), n(q))


def f_nfkc(doc, q):
    n = lambda s: unicodedata.normalize("NFKC", s)  # noqa: E731
    return f_ws(n(doc), n(q))


def f_typo(doc, q):
    n = lambda s: "".join(TYPO.get(c, c) for c in s)  # noqa: E731
    return f_ws(n(doc), n(q))


def f_cescape(doc, q):
    n = lambda s: s.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"')  # noqa: E731
    return f_ws(n(doc), n(q))


def f_dewrap(doc, q):
    def n(s):
        s = re.sub(r"\s*/\s*", " ", s)
        s = re.sub(r"\s*,\s*", " ", s)
        return re.sub(r"\s+", " ", s)
    return n(q) in n(doc)


def f_html(doc, q):
    def n(s):
        s = TAG_RE.sub(" ", s)
        return re.sub(r"\s+", " ", s)
    return n(q) in n(doc)


def f_mdlink(doc, q):
    def n(s):
        s = MD_LINK_RE.sub(r"\1", s)
        s = re.sub(r"[*_`]", "", s)
        return re.sub(r"\s+", " ", s)
    return n(q) in n(doc)


FOLDS = [("exact", f_exact), ("whitespace", f_ws), ("case", f_case),
         ("no-whitespace", f_nows), ("markdown", f_md), ("nfkc", f_nfkc),
         ("typographic", f_typo), ("c-escape", f_cescape), ("de-wrapped", f_dewrap),
         ("html", f_html), ("md-link", f_mdlink)]

# --- a capture that is not the cited document, but a bot wall or an error page ---
INTERSTITIAL_MARKERS = (
    "client challenge", "just a moment", "cf-browser-verification", "attention required",
    "enable javascript and cookies to continue", "checking your browser before accessing",
    "attention required! | cloudflare", "error 1020", "access denied", "captcha",
    "verify you are human", "robot check", "checking your browser",
    "请开启javascript", "验证码", "checking your browser before accessing",
    "the request could not be satisfied", "request blocked", "unusual traffic",
)


def capture_kind(text: str) -> str:
    """Classify a cached document: page | interstitial."""
    low = text[:4000].lower()
    for marker in INTERSTITIAL_MARKERS:
        if marker in low:
            return "interstitial"
    return "page"


def cache_key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# --- the register -------------------------------------------------------------

DATA_ROW_RE = re.compile(r"^round[0-9]+$")
ID_RE = re.compile(r"^S[0-9]+")


def parse_register(register: pathlib.Path):
    """Return the lane's quarantine slice.

    A slice row is a DATA row of the register: its lane cell names this lane, its
    round cell names a round, and its id cell carries an S-id. Summary rows of the
    `## By lane` table carry a lane name but no round and no id, so they cannot
    match. Two row shapes exist: the seven-column `## Rows` table and the
    five-column `## Rows whose quotes were NEVER CHECKED` table; the latter's
    fourth cell is prose, not a class.
    """
    rows = []
    for lineno, line in enumerate(register.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        # cells[0] is empty before the first pipe; cells[-1] empty after the last.
        if len(cells) < 6:
            continue
        lane_cell, round_cell, id_cell = cells[1], cells[2], cells[3]
        if lane_cell != "`%s`" % LANE:
            continue
        if not DATA_ROW_RE.match(round_cell):
            continue
        rid = id_cell.rstrip("`").strip()
        if not ID_RE.match(rid):
            continue
        if len(cells) >= 8:  # the `## Rows` table: class, source, quotes, note
            klass = cells[4].strip("`")
            url = cells[5]
            quote_cell = cells[6]
        else:  # the unchecked family: prose reason, then a source cell
            klass = cells[4]
            url = cells[5] if len(cells) > 5 else ""
            quote_cell = ""
        quotes = []
        for raw in quote_cell.split("<br>"):
            q = raw.strip()
            if q.startswith("`") and q.endswith("`") and len(q) >= 2:
                q = q[1:-1]
            if q.strip():
                quotes.append(q.strip())
        rows.append({"line": lineno, "id": rid, "round": round_cell, "class": klass,
                     "url": url, "quotes": quotes, "checked_family": len(cells) < 8})
    return rows


def unchecked_family(klass: str) -> bool:
    """The register's prose class cell: the unchecked family, never a fabrication."""
    low = klass.lower()
    return ("could not be fetched" in low or "named no locator" in low
            or "was never checked" in low)


PDF_MAGIC = b"%PDF-"
ZIP_MAGIC = b"PK\x03\x04"
OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
RTF_MAGIC = b"{\\rtf"


def capture_form(cache: pathlib.Path, key: str) -> str:
    """Classify how the cached document was rendered, from the raw response's magic bytes.

    text           — the capture is a text rendering (HTML stripped to text, or plain text)
    pdf-text       — the capture is `pdftotext -layout` output of a PDF (text WAS extracted)
    binary-office  — the capture is a non-PDF binary document (OLE .doc, OOXML .docx, RTF)
                     whose bytes were decoded, never rendered to text: a quote's absence
                     in it is NOT evidence that the quote is absent from the document
    unknown        — no raw response beside the text capture
    """
    raw = cache / (key + ".raw")
    if not raw.exists():
        return "unknown"
    try:
        with raw.open("rb") as fh:
            head = fh.read(8)
    except OSError:
        return "unknown"
    if head.startswith(PDF_MAGIC):
        return "pdf-text"
    if head.startswith(ZIP_MAGIC) or head.startswith(OLE_MAGIC) or head.startswith(RTF_MAGIC):
        return "binary-office"
    return "text"


def cache_doc(cache: pathlib.Path, url: str):
    """Return (path, text, kind) for a URL's local capture, or (None, None, 'missing')."""
    if not url.startswith(("http://", "https://")):
        return None, None, "missing"
    key = cache_key(url)
    txt = cache / (key + ".txt")
    if txt.exists():
        try:
            body = txt.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None, None, "missing"
        return txt, body, capture_kind(body) + "+" + capture_form(cache, key)
    if (cache / (key + ".fail")).exists():
        return None, None, "missing"
    return None, None, "missing"


def examine_quote(doc: str, quote: str):
    """Return (loosest_fold, strict_found, offset).

    `loosest_fold` is the first fold of the ladder that sees the quote — evidence of
    how the text was matched. `strict_found` is the frozen strict test (NFKC +
    whitespace collapse, case-sensitive); the frozen decision rule counts ONLY the
    strict test, so a quote that only a loose fold can see is not counted as located.
    """
    try:
        strict = bool(f_nfkc(doc, quote))
    except Exception:
        strict = False
    for name, fn in FOLDS:
        try:
            if fn(doc, quote):
                idx = doc.find(quote)
                return name, strict, idx
        except Exception:
            continue
    return None, strict, -1


# --- the frozen decision rule --------------------------------------------------
#
# per slice row:
#   checkable  = the cited URL has a local capture whose text is a real document
#                (kind == 'page') and whose length is not shorter than the quote
#                (a capture shorter than the quote cannot contain it)
#   located    = number of the row's quarantined quotes found in that capture
#   verdict:
#     present            located == n_quotes        -> adoptable later; adoption closed this round
#     absent             located == 0              -> refuse (fabrication class)
#     mixed              0 < located < n_quotes    -> refuse-with-correction
#     unverifiable       not checkable, or the register's unchecked family
#     unverifiable is never a fabrication.

def decide(row, path, body, kind, located, folds):
    rid = row["id"]
    if row["checked_family"] or unchecked_family(row["class"]):
        return ("unverifiable",
                "register unchecked family (%s): the quote was never checked; not a fabrication"
                % row["class"][:80],
                "register")
    if kind.startswith("page+binary-office"):
        return ("unverifiable",
                "the local capture is a binary office document decoded as bytes, never rendered "
                "to text; a quote's absence in it is not evidence that the quote is absent "
                "from the document",
                path.name if path else "cache")
    if not kind.startswith("page") or body is None:
        return ("unverifiable",
                "no local capture of the cited source (%s); the source was never read locally"
                % ("interstitial capture" if kind.startswith("interstitial") else "missing capture"),
                "cache")
    nq = len(row["quotes"])
    if nq and body is not None and len(body) < max(len(q) for q in row["quotes"]):
        return ("unverifiable",
                "the local capture (%d chars) is shorter than the longest quarantined quote; "
                "it cannot be the cited document" % len(body),
                "cache")
    if nq and located == nq:
        return ("present",
                "all %d quarantined quote(s) located in the local capture (strict fold %s)"
                % (nq, ",".join(folds)),
                path.name if path else "cache")
    if located == 0:
        return ("absent",
                "none of the %d quarantined quote(s) is present in the local capture of the "
                "cited source under the eleven folds" % nq,
                path.name if path else "cache")
    return ("mixed",
            "%d of %d quarantined quote(s) located; the rest are absent from the local capture"
            % (located, nq),
            path.name if path else "cache")


# --- commands ------------------------------------------------------------------

def cmd_slice(args, rows):
    for r in rows:
        print("\t".join([r["id"], r["round"], r["class"], r["url"], str(len(r["quotes"]))]))
    return 0 if rows else 1


def cmd_examine(args, rows):
    for r in rows:
        path, body, kind = cache_doc(args.cache, r["url"])
        for i, q in enumerate(r["quotes"], 1):
            fold = offset = None
            strict = False
            if body is not None and kind.startswith("page") and not kind.startswith("page+binary-office"):
                fold, strict, offset = examine_quote(body, q)
            status = ("located" if strict else "loose-only") if fold else (
                "absent" if body is not None and kind == "page" else "no-capture")
            print("\t".join([r["id"], str(i), status, fold or "-",
                             path.name if path else "-",
                             str(offset) if offset is not None and offset >= 0 else "-",
                             hashlib.sha256(q.encode()).hexdigest()[:12]]))
    return 0


def cmd_verdict(args, rows):
    for r in rows:
        path, body, kind = cache_doc(args.cache, r["url"])
        located = 0
        folds = []
        for q in r["quotes"]:
            fold, strict, _off = (None, False, -1)
            if body is not None and kind.startswith("page") and not kind.startswith("page+binary-office"):
                fold, strict, _off = examine_quote(body, q)
            if strict:
                located += 1
                folds.append(fold)
        verdict, reason, evidence = decide(r, path, body, kind, located, folds)
        print("\t".join([r["id"], verdict, reason.replace("\t", " "), evidence]))
    return 0


def cmd_digests(args, rows):
    print("register\t%s\t%s" % (args.register, sha256_file(args.register)))
    seen = {}
    for r in rows:
        path, _b, _k = cache_doc(args.cache, r["url"])
        if path and path.name not in seen:
            seen[path.name] = sha256_file(path)
    for name in sorted(seen):
        print("capture\t%s\t%s" % (name, seen[name]))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["slice", "examine", "verdict", "digests"])
    ap.add_argument("--register", default=DEFAULT_REGISTER)
    ap.add_argument("--cache", default=DEFAULT_CACHE)
    args = ap.parse_args(argv)
    register = pathlib.Path(args.register)
    cache = pathlib.Path(args.cache)
    if not register.is_file():
        sys.stderr.write("quarantine-check: register not readable: %s\n" % register)
        return 2
    if not cache.is_dir():
        sys.stderr.write("quarantine-check: capture cache not readable: %s\n" % cache)
        return 2
    args.register = str(register)
    args.cache = cache
    rows = parse_register(register)
    if not rows:
        sys.stderr.write("quarantine-check: slice is empty — the register holds no data rows for %s\n" % LANE)
        return 1
    return {"slice": cmd_slice, "examine": cmd_examine, "verdict": cmd_verdict,
            "digests": cmd_digests}[args.command](args, rows)


if __name__ == "__main__":
    sys.exit(main())
