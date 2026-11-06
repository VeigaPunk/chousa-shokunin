#!/usr/bin/env python3
"""K2 (located) check for round 83 C1.

Reads the 16 quotes of corpus/knowledge/appraisal-judgment-records-r83.md
(`## Located quotes`) and locates each in the committed capture of its S-id,
after whitespace collapse and curly-quote folding to ASCII.

Usage:
  locate_quotes.py --root <tree> [--json out.json]

Emits one TSV row per quote: qid, source, capture, status, line, words_wc, words_split
"""
import argparse
import json
import os
import re
import sys

CURLY = {
    "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'", "\u2032": "'",
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"', "\u2033": '"',
    "\u00b4": "'", "\u2039": "'", "\u203a": "'", "\u00ab": '"', "\u00bb": '"',
}


def fold(s):
    for k, v in CURLY.items():
        s = s.replace(k, v)
    return s


def collapse_with_lines(text):
    """Collapse whitespace, returning (collapsed, line_of_index list)."""
    out = []
    line_of = []
    line = 1
    pending_space = False
    for ch in text:
        if ch.isspace():
            if out:
                pending_space = True
            if ch == "\n":
                line += 1
            continue
        if pending_space:
            out.append(" ")
            line_of.append(line)
            pending_space = False
        out.append(ch)
        line_of.append(line)
    return "".join(out), line_of


def parse_quotes(path):
    """Parse the Located quotes markdown table."""
    rows = []
    in_table = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("## "):
                in_table = line.strip() == "## Located quotes"
                continue
            if not in_table:
                continue
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            if cells[0] in ("qid", "---") or set(cells[0]) <= {"-"}:
                continue
            qid, source, quote = cells[0], cells[1], cells[2]
            if quote.startswith('"') and quote.endswith('"'):
                quote = quote[1:-1]
            rows.append((qid, source, quote))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    root = args.root
    entry = os.path.join(root, "corpus/knowledge/appraisal-judgment-records-r83.md")
    quotes = parse_quotes(entry)
    if len(quotes) != 16:
        print("PARSE_ERROR expected 16 quotes, got %d" % len(quotes), file=sys.stderr)

    # S-id -> capture key, from the committed refetch table
    key_of = {}
    with open(os.path.join(root, "corpus/evidence/round57/refetch.tsv"), encoding="utf-8") as fh:
        next(fh, None)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                key_of[parts[0]] = parts[2]

    cache = {}
    results = []
    print("qid\tsource\tcapture\tstatus\tline\twords_wc\twords_split")
    for qid, source, quote in quotes:
        key = key_of.get(source)
        if key is None:
            results.append(dict(qid=qid, source=source, capture=None, status="NO_SOURCE_KEY",
                                line=None, words_wc=None, words_split=None))
            print("%s\t%s\t-\tNO_SOURCE_KEY\t-\t-\t-" % (qid, source))
            continue
        cap = os.path.join(root, "corpus/captures/%s.txt" % key)
        if key not in cache:
            with open(cap, encoding="utf-8", errors="replace") as fh:
                cache[key] = collapse_with_lines(fold(fh.read()))
        collapsed, line_of = cache[key]
        needle = " ".join(fold(quote).split())
        idx = collapsed.find(needle)
        status = "FOUND" if idx >= 0 else "ABSENT"
        line = line_of[idx] if idx >= 0 else None
        words_wc = len(quote.split())
        words_split = len(quote.split())
        results.append(dict(qid=qid, source=source, capture="corpus/captures/%s.txt" % key,
                            status=status, line=line, words_wc=words_wc,
                            words_split=words_split, quote=quote))
        print("%s\t%s\t%s\t%s\t%s\t%d\t%d" % (qid, source, key, status,
                                              line if line is not None else "-",
                                              words_wc, words_split))

    found = sum(1 for r in results if r["status"] == "FOUND")
    print("SUMMARY quotes=%d found=%d absent=%d" % (len(results), found, len(results) - found))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0 if found == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
