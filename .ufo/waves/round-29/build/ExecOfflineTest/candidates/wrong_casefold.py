#!/usr/bin/env python3
"""Deliberately wrong variant: proper extraction, but case-folded substring
matching with no boundary rule.

Scratch only.  It violates the contract's case-sensitive boundary rule, so
the harness must catch it.
"""
import argparse
import re
import sys
import unicodedata
import urllib.request
from html.parser import HTMLParser

SKIP = {"script", "style", "noscript", "template", "head"}
BLOCK = {"p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6",
         "br", "section", "article", "header", "footer", "nav", "pre", "blockquote", "dt", "dd", "dl",
         "figure", "figcaption", "hr", "main", "aside"}


class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK:
            self.out.append(" ")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in BLOCK:
            self.out.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def registry_url(path, sid):
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if ln.startswith("| {} |".format(sid)):
                m = re.search(r"https?://\S+", ln.split("|")[2])
                return m.group(0).rstrip(".,;)") if m else None
    return None


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--items", required=True)
    v.add_argument("--registry", default=None)
    opts = ap.parse_args(argv)
    with open(opts.items, encoding="utf-8") as f:
        rows = [ln.split("\t") for ln in f.read().split("\n")[1:] if ln]
    counts = {"VERBATIM": 0, "ABSENT": 0, "TOO_LONG": 0, "NO_SOURCE": 0, "UNREACHABLE": 0}
    cache = {}
    for rid, sid, quote in rows:
        url = registry_url(opts.registry, sid)
        if not url:
            v_ = "NO_SOURCE"
        elif len(quote.split()) > 25:
            v_ = "TOO_LONG"
        else:
            if url not in cache:
                try:
                    req = urllib.request.Request(url.split("#")[0],
                                                 headers={"User-Agent": "chousa-quote-reopen/x"})
                    r = urllib.request.urlopen(req, timeout=30)
                    p = T()
                    p.feed(r.read(9 * 1024 * 1024).decode("utf-8", "replace"))
                    p.close()
                    cache[url] = " ".join(unicodedata.normalize("NFKC", "".join(p.out)).split())
                except Exception:
                    cache[url] = None
            text = cache[url]
            if text is None:
                v_ = "UNREACHABLE"
            else:
                v_ = "VERBATIM" if " ".join(unicodedata.normalize("NFKC", quote).split()).lower() in text.lower() else "ABSENT"
        counts[v_] += 1
        print("QUOTE_REOPEN\t{}\t{}\tcasefold".format(rid, v_))
    print("QUOTE_REOPEN_SUMMARY verbatim={} absent={} too_long={} no_source={} unreachable={}".format(
        counts["VERBATIM"], counts["ABSENT"], counts["TOO_LONG"], counts["NO_SOURCE"], counts["UNREACHABLE"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
