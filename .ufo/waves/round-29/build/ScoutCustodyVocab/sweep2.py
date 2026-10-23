#!/usr/bin/env python3
"""Final D1/D2 sweep -> TSV. Read-only over the lane; writes only the given output path.

Columns: file, d1_count, d2_count, examples, d1_prose_glue, d1_identifier_shaped,
         d1_inside_code_spans, d1_raw_count, d2_phrases, d2_round28_only

d1_count = occurrences of \b[a-z]+[0-9]{2,}\b OUTSIDE backtick code spans (fenced blocks and
inline spans removed). d1_prose_glue excludes tokens whose shape is a stable identifier
(sha256, r\d\d revision shorthand, RFC/DOI/URL fragments, TREC path segment); the excluded
shapes are listed in report.md and every hit's line number is in the detail dump.
d2_count = case-insensitive occurrences of the six named custody phrases in raw text.
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
IDENT = [re.compile(p) for p in [r"^sha256$", r"^rfc\d+$", r"^r\d{2}$", r"^c\d{2,}$",
                                 r"^p\d{2,}$", r"^n\d{2,}$", r"^i\d{3,}$", r"^trec\d+$"]]
ROUND28 = re.compile(r"[Rr]ound[- ]?2[89]\b")
ROUND_HDR = re.compile(r"^#{1,6}\s*.*?(?:[Rr]ound[- ]?(\d{1,2})|R(\d{2})\b)")


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


def round_for(lines, lineno):
    for i in range(lineno - 1, -1, -1):
        if ROUND_HDR.match(lines[i]):
            return lines[i].strip()[:60]
    for i in range(lineno - 1, -1, -1):
        m = ROUND28.search(lines[i]) or re.search(r"[Rr]ound[- ]?(\d{1,2})\b", lines[i])
        if m:
            return "mention:%s@L%d" % (m.group(0), i + 1)
    return "(no round heading above)"


def main():
    out_path = sys.argv[1]
    files = [os.path.join(LANE, f) for f in NAMED]
    lessons = os.path.join(LANE, "corpus/lessons")
    for name in sorted(os.listdir(lessons)):
        p = os.path.join(lessons, name)
        if os.path.isfile(p):
            files.append(p)

    lines_out = ["\t".join([
        "file", "d1_count", "d2_count", "examples", "d1_prose_glue", "d1_identifier_shaped",
        "d1_inside_code_spans", "d1_raw_count", "d2_phrases", "d2_round28_only"])]
    detail = []
    for p in files:
        rel = os.path.relpath(p, LANE)
        raw = open(p, encoding="utf-8", errors="replace").read()
        stripped = strip_code(raw)
        rawsplit = raw.split("\n")

        d1 = []
        for idx, line in enumerate(stripped.split("\n")):
            for m in D1.finditer(line):
                d1.append((idx + 1, m.group(0)))
        d1_raw = len(D1.findall(raw))
        ident = [x for x in d1 if any(r.match(x[1]) for r in IDENT)]
        prose = [x for x in d1 if not any(r.match(x[1]) for r in IDENT)]

        d2 = []
        low = raw.lower()
        for ph in D2_PHRASES:
            start = 0
            while True:
                i = low.find(ph.lower(), start)
                if i < 0:
                    break
                d2.append((raw.count("\n", 0, i) + 1, ph))
                start = i + len(ph)
        d2.sort()

        ex = ["D1:%s@L%d" % (t, l) for l, t in (prose or d1)[:5]]
        ex += ["D2:%s@L%d" % (ph, l) for l, ph in d2[:3]]
        d2_rounds = set()
        for l, ph in d2:
            d2_rounds.add(round_for(rawsplit, l))
        r28_only = "yes" if d2 and all(ROUND28.search(r) for r in d2_rounds) else (
            "n/a" if not d2 else "no")
        lines_out.append("\t".join([
            rel, str(len(d1)), str(len(d2)), " | ".join(ex) or "-", str(len(prose)),
            str(len(ident)), str(d1_raw - len(d1)), str(d1_raw),
            ",".join(sorted(set(ph for _, ph in d2))) or "-", r28_only]))

        if d1 or d2:
            detail.append("\n=== %s ===" % rel)
            detail.append("  d1 outside code: total=%d prose=%d ident=%d ; d1 inside code=%d"
                          % (len(d1), len(prose), len(ident), d1_raw - len(d1)))
            for l, t in prose:
                detail.append("   PROSE L%-5d %s   [round: %s]" % (l, t, round_for(rawsplit, l)))
            for l, t in ident:
                detail.append("   IDENT L%-5d %s   [round: %s]" % (l, t, round_for(rawsplit, l)))
            for l, ph in d2:
                detail.append("   D2    L%-5d %s   [round: %s]" % (l, ph, round_for(rawsplit, l)))

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines_out) + "\n")
    with open(out_path + ".detail.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(detail) + "\n")
    print("\n".join(lines_out))


main()
