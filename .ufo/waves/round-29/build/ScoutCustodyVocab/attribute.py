#!/usr/bin/env python3
"""Attribute each D1/D2 hit to a round, by nearest preceding round marker/heading.

Prints per file: hits grouped by attributed round. Read-only.
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"

NAMED = [
    "LOG.md",
    "SCORECARD.md",
    "SKILL.md",
    "corpus/README.md",
    "corpus/QUALITY.md",
    "corpus/SOURCES.md",
]
D2_PHRASES = [
    "Parent approval",
    "Parent decision",
    "CURRENT_MAIN_DIRECTIVE",
    "report-LAST",
    "Root report",
    "private original",
]
D1 = re.compile(r"\b[a-z]+[0-9]{2,}\b")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE = re.compile(r"`[^`\n]*`")

# identifier-shaped tokens that the bare regex catches but that are not prose glue
IDENT = [
    re.compile(r"^sha256$"),
    re.compile(r"^rfc\d+$"),
    re.compile(r"^r\d{2}$"),
    re.compile(r"^c\d{2,}$"),
    re.compile(r"^p\d{2,}$"),
    re.compile(r"^n\d{2,}$"),
    re.compile(r"^i\d{3,}$"),
    re.compile(r"^s\d{2,}$"),
    re.compile(r"^cmarkgfm\d+$"),
    re.compile(r"^trec\d+$"),
]

ROUND_HDR = re.compile(r"^#{1,6}\s*.*?(?:[Rr]ound[- ]?(\d{1,2})|R(\d{2})\b)")
ROUND_ANY = re.compile(r"[Rr]ound[- ]?(\d{1,2})\b")
RR = re.compile(r"\bR(\d{2})\b")


def strip_code(text):
    out = []
    infence = False
    for line in text.split("\n"):
        if FENCE.match(line):
            infence = not infence
            out.append("")
            continue
        out.append("" if infence else INLINE.sub(" ", line))
    return "\n".join(out)


def attribute(lines, lineno):
    """nearest preceding heading that names a round; fall back to nearest preceding round mention"""
    hdr = None
    for i in range(lineno - 1, -1, -1):
        m = ROUND_HDR.match(lines[i])
        if m:
            hdr = lines[i].strip()[:100]
            break
    mention = None
    mline = None
    for i in range(lineno - 1, -1, -1):
        m = ROUND_ANY.search(lines[i]) or RR.search(lines[i])
        if m:
            mention = m.group(0)
            mline = i + 1
            break
    return hdr, mention, mline


def is_ident(tok):
    return any(p.match(tok) for p in IDENT)


def main():
    files = [os.path.join(LANE, f) for f in NAMED]
    lessons = os.path.join(LANE, "corpus/lessons")
    for name in sorted(os.listdir(lessons)):
        p = os.path.join(lessons, name)
        if os.path.isfile(p):
            files.append(p)

    for p in files:
        rel = os.path.relpath(p, LANE)
        raw = open(p, encoding="utf-8", errors="replace").read()
        lines = raw.split("\n")
        stripped = strip_code(raw).split("\n")

        hits = []
        for idx, line in enumerate(stripped):
            for m in D1.finditer(line):
                hits.append((idx + 1, m.group(0), is_ident(m.group(0))))
        d2 = []
        low = raw.lower()
        for ph in D2_PHRASES:
            start = 0
            while True:
                i = low.find(ph.lower(), start)
                if i < 0:
                    break
                ln = raw.count("\n", 0, i) + 1
                d2.append((ln, ph))
                start = i + len(ph)

        if not hits and not d2:
            continue
        print("\n=== %s ===" % rel)
        prose = [h for h in hits if not h[2]]
        ident = [h for h in hits if h[2]]
        print("  d1 total=%d prose-glue=%d identifier-shaped=%d | d2=%d" % (len(hits), len(prose), len(ident), len(d2)))
        for label, group in (("PROSE", prose), ("IDENT", ident)):
            if not group:
                continue
            print("  -- %s hits by attributed round" % label)
            seen = {}
            for ln, tok, _ in group:
                hdr, mention, mline = attribute(lines, ln)
                key = (hdr or "(no round heading)", mention, mline)
                seen.setdefault(key, []).append((ln, tok))
            for (hdr, mention, mline), items in seen.items():
                print("     round-hdr=%r mention=%r@L%s  n=%d  lines=%s  toks=%s"
                      % (hdr, mention, mline, len(items),
                         ",".join(str(x[0]) for x in items[:12]),
                         ",".join(x[1] for x in items[:12])))
        if d2:
            print("  -- D2 hits")
            for ln, ph in d2:
                hdr, mention, mline = attribute(lines, ln)
                print("     L%-5d [%s] round-hdr=%r mention=%r@L%s" % (ln, ph, hdr, mention, mline))


main()
