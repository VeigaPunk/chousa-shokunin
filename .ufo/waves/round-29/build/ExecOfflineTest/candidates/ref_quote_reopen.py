#!/usr/bin/env python3
"""Reference implementation of the frozen round-29 quote-reopen tool contract.

Scratch only: this file exists to validate the offline conformance harness
at .ufo/waves/round-29/build/ExecOfflineTest/quote-reopen-offline-test.py.
It is not the claim's tool and it never enters the lane.
"""
import argparse
import os
import re
import sys
import unicodedata
import urllib.request
from html.parser import HTMLParser

SKIP = {"script", "style", "noscript", "template", "head"}
BLOCK = {"p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6",
         "br", "section", "article", "header", "footer", "nav", "pre", "blockquote", "dt", "dd", "dl",
         "figure", "figcaption", "hr", "main", "aside"}
QMAP = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
                      "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
                      "\u00ad": None, "\u200b": None, "\u200c": None, "\u200d": None,
                      "\ufeff": None})
MAX_BODY = 8 * 1024 * 1024
ALLOWED_CTYPES = {"text/html", "application/xhtml+xml", "text/plain"}


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK:
            self.out.append(" ")

    def handle_startendtag(self, tag, attrs):
        if tag in BLOCK:
            self.out.append(" ")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in BLOCK:
            self.out.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def norm(s):
    return " ".join(unicodedata.normalize("NFKC", s).translate(QMAP).split())


def found(text, quote):
    q, i = norm(quote), 0
    while q:
        i = text.find(q, i)
        if i < 0:
            return False
        j = i + len(q)
        if (i == 0 or not text[i - 1].isalnum()) and (j == len(text) or not text[j].isalnum()):
            return True
        i += 1
    return False


def registry_url(path, sid):
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if ln.startswith("| {} |".format(sid)):
                cells = ln.split("|")
                m = re.search(r"https?://\S+", cells[2])
                return m.group(0).rstrip(".,;)") if m else None
    return None


def fetch_text(url, cache):
    if url in cache:
        return cache[url]
    req = urllib.request.Request(url.split("#")[0],
                                 headers={"User-Agent": "chousa-quote-reopen/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read(MAX_BODY + 1)
            ctype = r.headers.get_content_type()
            status = r.status
    except Exception:
        cache[url] = (None, None)
        return cache[url]
    if status < 200 or status > 299 or ctype not in ALLOWED_CTYPES or len(body) > MAX_BODY:
        cache[url] = (None, None)
        return cache[url]
    doc = body.decode("utf-8", "replace")
    if ctype == "text/plain":
        text = norm(doc)
    else:
        p = _Text()
        p.feed(doc)
        p.close()
        text = norm("".join(p.out))
    cache[url] = (text, ctype)
    return cache[url]


def main(argv):
    ap = argparse.ArgumentParser(prog="quote-reopen.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--items", required=True)
    v.add_argument("--registry", default=None)
    opts = ap.parse_args(argv)

    lane = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    registry = opts.registry or os.path.join(lane, "corpus", "SOURCES.md")
    if opts.registry is not None and not os.path.isfile(opts.registry):
        print("registry not found: {}".format(opts.registry), file=sys.stderr)
        return 2
    if not os.path.isfile(opts.items):
        print("items not found: {}".format(opts.items), file=sys.stderr)
        return 2


    with open(opts.items, encoding="utf-8") as f:
        lines = f.read().split("\n")
    rows = [ln.split("\t") for ln in lines[1:] if ln]

    cache = {}
    counts = {"VERBATIM": 0, "ABSENT": 0, "TOO_LONG": 0, "NO_SOURCE": 0, "UNREACHABLE": 0}
    results = []
    for rid, sid, quote in rows:
        url = registry_url(registry, sid)
        if not url:
            verdict, detail = "NO_SOURCE", "no registry url"
        elif len(norm(quote).split()) > 25:
            verdict, detail = "TOO_LONG", "more than 25 words"
        else:
            text, ctype = fetch_text(url, cache)
            if text is None:
                verdict, detail = "UNREACHABLE", "fetch failed"
            elif found(text, quote):
                verdict, detail = "VERBATIM", "quote found"
            else:
                verdict, detail = "ABSENT", "quote not found"
        counts[verdict] += 1
        results.append((rid, verdict, detail))

    for rid, verdict, detail in results:
        print("QUOTE_REOPEN\t{}\t{}\t{}".format(rid, verdict, detail))
    print("QUOTE_REOPEN_SUMMARY verbatim={} absent={} too_long={} no_source={} unreachable={}".format(
        counts["VERBATIM"], counts["ABSENT"], counts["TOO_LONG"], counts["NO_SOURCE"],
        counts["UNREACHABLE"]))
    return 0 if all(v == "VERBATIM" for _r, v, _d in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
