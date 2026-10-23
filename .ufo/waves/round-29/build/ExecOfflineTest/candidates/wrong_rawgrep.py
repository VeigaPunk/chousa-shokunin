#!/usr/bin/env python3
"""Deliberately wrong variant: fetch then substring search over raw HTML.

Scratch only.  It violates the contract's HTML-to-text and normalization
rules, so the harness must catch it.
"""
import argparse
import re
import sys
import urllib.request


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
                    cache[url] = urllib.request.urlopen(req, timeout=30).read(9 * 1024 * 1024)
                except Exception:
                    cache[url] = None
            body = cache[url]
            v_ = "UNREACHABLE" if body is None else ("VERBATIM" if quote.encode("utf-8") in body else "ABSENT")
        counts[v_] += 1
        print("QUOTE_REOPEN\t{}\t{}\trawgrep".format(rid, v_))
    print("QUOTE_REOPEN_SUMMARY verbatim={} absent={} too_long={} no_source={} unreachable={}".format(
        counts["VERBATIM"], counts["ABSENT"], counts["TOO_LONG"], counts["NO_SOURCE"], counts["UNREACHABLE"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
