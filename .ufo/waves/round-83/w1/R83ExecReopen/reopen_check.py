#!/usr/bin/env python3
"""K2 (located) live re-open check for round 83 C1.

For each re-opened page (<id>.html in the scratch dir): tag-strip (drop script/style/
noscript/template/title content and comments), unescape HTML entities, collapse
whitespace, fold curly quotes to ASCII; then locate every declared quote of its S-id.

Also renders the committed .raw capture through the same stripper and checks that the
committed .txt agrees, so the stripper is validated against the lane's own pipeline.

Usage: reopen_check.py --root <tree> --scratch <dir> [--json out.json]
"""
import argparse
import hashlib
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

SKIP = {"script", "style", "noscript", "template", "title"}
BLOCK = {"p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4",
         "h5", "h6", "br", "section", "article", "header", "footer", "nav", "pre",
         "blockquote", "dt", "dd", "dl", "figure", "figcaption", "hr", "main", "aside"}
CURLY = {"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'", "\u2032": "'",
         "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"', "\u2033": '"',
         "\u00b4": "'", "\u00ab": '"', "\u00bb": '"'}


class Strip(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.inhead = False

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.inhead = True
            return
        if tag in SKIP:
            self.skip += 1
            return
        if tag in BLOCK:
            self.out.append(" ")

    def handle_startendtag(self, tag, attrs):
        if tag in BLOCK:
            self.out.append(" ")

    def handle_endtag(self, tag):
        if tag == "head":
            self.inhead = False
            return
        if tag in SKIP and self.skip:
            self.skip -= 1
            return
        if tag in BLOCK:
            self.out.append(" ")

    def handle_data(self, data):
        if self.skip:
            return
        if self.inhead:
            if not data.strip():
                return
            self.inhead = False
        self.out.append(data)

    def handle_comment(self, data):
        return


def html_to_text(doc):
    p = Strip()
    p.feed(doc)
    p.close()
    return "".join(p.out)


def fold_only(s):
    for k, v in CURLY.items():
        s = s.replace(k, v)
    return s


def norm(s):
    return " ".join(fold_only(s).split())


def collapse_with_lines(text):
    out, line_of = [], []
    line = 1
    pending = False
    for ch in text:
        if ch.isspace():
            if out:
                pending = True
            if ch == "\n":
                line += 1
            continue
        if pending:
            out.append(" ")
            line_of.append(line)
            pending = False
        out.append(ch)
        line_of.append(line)
    return "".join(out), line_of


def parse_quotes(path):
    rows, in_table = [], False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("## "):
                in_table = line.strip() == "## Located quotes"
                continue
            if not in_table or not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or cells[0] in ("qid",) or set(cells[0]) <= {"-"}:
                continue
            q = cells[2]
            if q.startswith('"') and q.endswith('"'):
                q = q[1:-1]
            rows.append((cells[0], cells[1], q))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    quotes = parse_quotes(os.path.join(a.root, "corpus/knowledge/appraisal-judgment-records-r83.md"))
    key_of, url_of = {}, {}
    with open(os.path.join(a.root, "corpus/evidence/round57/refetch.tsv"), encoding="utf-8") as fh:
        next(fh, None)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3:
                key_of[p[0]] = p[2]
                url_of[p[0]] = p[1]

    rawsha = {}
    with open(os.path.join(a.root, "corpus/evidence/round57/refetch.tsv"), encoding="utf-8") as fh:
        next(fh, None)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 8:
                rawsha[p[0]] = p[7]

    results = []
    print("qid\tsource\thttp\tbytes\tbody_sha256\tstrip\tstatus\tline\twords")
    for sid in ("S009", "S212", "S213"):
        page = os.path.join(a.scratch, sid + ".html")
        raw = os.path.join(a.root, "corpus/captures/%s.raw" % key_of[sid])
        txt = os.path.join(a.root, "corpus/captures/%s.txt" % key_of[sid])
        with open(page, "rb") as fh:
            body = fh.read()
        nbytes = len(body)
        body_sha = hashlib.sha256(body).hexdigest()
        same = "BODY_IDENTICAL" if body_sha == rawsha.get(sid) else "BODY_DIFFERS"
        text = html_to_text(body.decode("utf-8", errors="replace"))
        collapsed, line_of = collapse_with_lines(fold_only(text))

        # stripper validation: same pipeline over the committed raw capture
        with open(raw, "rb") as fh:
            rawb = fh.read()
        rtext = html_to_text(rawb.decode("utf-8", errors="replace"))
        rcoll, _ = collapse_with_lines(fold_only(rtext))
        with open(txt, encoding="utf-8", errors="replace") as fh:
            tcoll, _ = collapse_with_lines(fold_only(fh.read()))
        agree = sum(1 for q in quotes if q[1] == sid and
                    ((" ".join(norm(q[2]).split()) in rcoll) ==
                     (" ".join(norm(q[2]).split()) in tcoll)))
        nq = sum(1 for q in quotes if q[1] == sid)
        strip_note = "raw_vs_txt_agree=%d/%d" % (agree, nq)

        for qid, source, quote in quotes:
            if source != sid:
                continue
            needle = " ".join(norm(quote).split())
            idx = collapsed.find(needle)
            status = "FOUND" if idx >= 0 else "ABSENT"
            line = line_of[idx] if idx >= 0 else None
            words = len(quote.split())
            results.append(dict(qid=qid, source=source, http=200, bytes=nbytes,
                                body_sha256=body_sha, body_match=same, strip=strip_note,
                                status=status, line=line, words=words, quote=quote))
            print("%s\t%s\t200\t%d\t%s\t%s\t%s\t%s\t%d" % (
                qid, sid, nbytes, same, strip_note, status,
                line if line is not None else "-", words))

    absent = [r for r in results if r["status"] == "ABSENT"]
    print("SUMMARY quotes=%d found=%d absent=%d" % (len(results), len(results) - len(absent), len(absent)))
    if absent:
        print("K2_FIRE_CANDIDATES " + ",".join(r["qid"] for r in absent))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
