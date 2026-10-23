#!/usr/bin/env python3
"""prose-check.py -- lane prose hygiene checker (round 29, seat ExecProseCheck).

Usage: python3 prose-check.py FILE...

Two defect classes routed from corpus/lessons/round-28-verifier-spotcheck.md:

  (a) D1 digit-glued tokens -- regex \b[a-z]+[0-9]{2,}\b appearing in prose.
  (b) D2 custody vocabulary -- case-insensitive match of any of:
      "Parent approval", "Parent decision", "CURRENT_MAIN_DIRECTIVE",
      "report-LAST", "Root report", "private original".

Explicit exclusions for check (a):
  * inline backtick code spans (`code`) are not prose;
  * fenced code blocks (``` or ~~~) are not prose;
  * URLs (any scheme://host... and www.host...) are not prose;
  * identifier forms that are not prose are not flagged:
      digests sha1 sha256 sha512 md5 base64 utf8; arch x86 arm64;
      network ipv4 ipv6; headings h1 h2 h3 h4 h5 h6;
      source ids S### (e.g. S046) and round ids r## (e.g. r29), any case.

The code-span, fence and URL exclusions apply to check (a) only. Check (b) is
a vocabulary ban, so it runs over the whole file text, code spans and fenced
blocks included: D2 forbids the custody vocabulary wherever it appears.

Exit codes: 0 no hits, 1 at least one hit, 2 usage error or unreadable file.
"""

import re
import sys
from pathlib import Path

DIGIT_RE = re.compile(r"\b[a-z]+[0-9]{2,}\b")
CODE_SPAN_RE = re.compile(r"`+[^`]*`+")
URL_RE = re.compile(r"(?:[a-z][a-z0-9+.\-]*://|www\.)\S+", re.IGNORECASE)
FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})")
IDENT_EXCLUDE_RE = re.compile(
    r"^(?:sha1|sha256|sha512|md5|base64|utf8|x86|arm64|ipv4|ipv6|h[1-6])$"
    r"|^[sS]\d{3,}$|^[rR]\d{2,}$",
    re.IGNORECASE,
)
CUSTODY_TERMS = (
    "Parent approval",
    "Parent decision",
    "CURRENT_MAIN_DIRECTIVE",
    "report-LAST",
    "Root report",
    "private original",
)


def prose_segments(text):
    """Yield (lineno, prose_segment), skipping code spans, fences and URLs."""
    fence = None
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        m = FENCE_RE.match(stripped)
        if m:
            fence = m.group("fence")[0] * 3
            continue
        segment = CODE_SPAN_RE.sub(" ", line)
        yield lineno, URL_RE.sub(" ", segment)


def digit_hits(text):
    """Map offending token -> list of line numbers."""
    hits = {}
    for lineno, segment in prose_segments(text):
        for m in DIGIT_RE.finditer(segment):
            token = m.group(0)
            if not IDENT_EXCLUDE_RE.match(token):
                hits.setdefault(token, []).append(lineno)
    return hits


def custody_hits(text):
    """Map matched term -> list of (lineno, matched_text)."""
    hits = {}
    lines = text.splitlines()
    for term in CUSTODY_TERMS:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        for lineno, line in enumerate(lines, 1):
            for m in pattern.finditer(line):
                hits.setdefault(term, []).append((lineno, m.group(0)))
    return hits


def report(name, text):
    """Print per-file counts and offending tokens; return the hit total."""
    d, c = digit_hits(text), custody_hits(text)
    d_total = sum(len(v) for v in d.values())
    c_total = sum(len(v) for v in c.values())
    print("FILE %s" % name)
    print("  digit-glued tokens: %d" % d_total)
    for token in sorted(d):
        lines = ", ".join(str(n) for n in d[token][:8])
        print("    %s x%d (lines %s)" % (token, len(d[token]), lines))
    print("  custody vocabulary: %d" % c_total)
    for term in sorted(c):
        for lineno, matched in c[term]:
            print("    %r at line %d" % (matched, lineno))
    return d_total + c_total


def main(argv):
    if len(argv) < 2:
        print("usage: python3 prose-check.py FILE...", file=sys.stderr)
        return 2
    total = 0
    for name in argv[1:]:
        try:
            text = Path(name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print("%s: cannot read file: %s" % (name, exc), file=sys.stderr)
            return 2
        total += report(name, text)
    print("TOTAL hits=%d files=%d" % (total, len(argv) - 1))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
