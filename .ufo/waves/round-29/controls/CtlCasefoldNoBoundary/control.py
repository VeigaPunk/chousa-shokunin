#!/usr/bin/env python3
"""Round-29 negative control: casefolded substring, deliberately no boundaries."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unicodedata
from urllib.error import URLError
from urllib.parse import urldefrag, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

LANE = Path(__file__).resolve().parents[5]
MAX_BODY = 8 * 1024 * 1024
DROP = {"script", "style", "noscript", "template", "head"}
BLOCK = set("p div li ul ol table tr td th h1 h2 h3 h4 h5 h6 br section article header footer nav pre blockquote dt dd dl figure figcaption hr main aside".split())
TRANSLATION = {ord(c): "'" for c in "\u2018\u2019\u201a\u201b"}
TRANSLATION.update({ord(c): '"' for c in "\u201c\u201d\u201e\u201f"})
TRANSLATION.update({ord(c): None for c in "\u00ad\u200b\u200c\u200d\ufeff"})
URL = re.compile(r"https?://[^\s<>`|]+")


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).translate(TRANSLATION).split())


class PageText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in DROP:
            self.hidden.append(tag)
        elif not self.hidden and tag in BLOCK:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if self.hidden:
            if tag in self.hidden:
                i = len(self.hidden) - 1 - self.hidden[::-1].index(tag)
                del self.hidden[i:]
        elif tag in BLOCK:
            self.parts.append(" ")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def registry_rows(path):
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 4 or not re.fullmatch(r"S[0-9]{3,}", cells[1]):
            continue
        found = URL.search(cells[2])
        rows[cells[1]] = urldefrag(found[0].rstrip(".,;)"))[0] if found else None
    return rows


class RegistryRedirect(HTTPRedirectHandler):
    def __init__(self, allowed):
        super().__init__()
        self.allowed = allowed

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        newurl = urldefrag(newurl)[0]
        parts = urlsplit(newurl)
        if parts.scheme not in {"http", "https"} or parts.username or parts.password:
            raise URLError("redirect scheme or credentials refused")
        if newurl not in self.allowed:
            raise URLError("redirect outside registry URL allowlist refused")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, allowed):
    opener = build_opener(ProxyHandler({}), RegistryRedirect(allowed))
    error = "fetch failed"
    for attempt in range(2):
        try:
            parts = urlsplit(url)
            if parts.scheme not in {"http", "https"} or parts.username or parts.password:
                raise URLError("URL scheme or credentials refused")
            request = Request(url, headers={"User-Agent": "chousa-quote-reopen-r29-casefold-control", "Accept": "text/html, application/xhtml+xml, text/plain"}, method="GET")
            with opener.open(request, timeout=30) as response:
                if not 200 <= response.status < 300:
                    raise URLError(f"HTTP {response.status}")
                kind = response.headers.get_content_type()
                if kind not in {"text/html", "application/xhtml+xml", "text/plain"}:
                    raise URLError(f"content type {kind}")
                body = response.read(MAX_BODY + 1)
                if len(body) > MAX_BODY:
                    raise URLError("body exceeds 8 MiB")
                text = body.decode(response.headers.get_content_charset() or "utf-8", errors="replace")
            if kind != "text/plain":
                parser = PageText()
                parser.feed(text)
                parser.close()
                text = "".join(parser.parts)
            print(f"FETCH {url} ok bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()}", file=sys.stderr)
            return normalize(text), "normalized live page"
        except (OSError, URLError, ValueError, LookupError) as exc:
            error = " ".join(str(exc).split())
    print(f"FETCH {url} failed {error}", file=sys.stderr)
    return None, error


def matches(quote, text):
    return quote.casefold() in text.casefold()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--items", required=True, type=Path)
    ap.add_argument("--registry", type=Path, default=LANE / "corpus/SOURCES.md")
    opts = ap.parse_args()
    try:
        registry = registry_rows(opts.registry)
        with opts.items.open(encoding="utf-8", newline="") as stream:
            reader = csv.reader(stream, delimiter="\t")
            if next(reader, None) != ["id", "source_id", "quote"]:
                raise ValueError("items header must be id<TAB>source_id<TAB>quote")
            items = []
            for row in reader:
                if not row:
                    continue
                if len(row) != 3:
                    raise ValueError("items row must have three cells")
                ident, source_id, quote = row
                items.append((ident, registry.get(source_id), normalize(quote)))
        allowed = {url for url in registry.values() if url}
        urls = sorted({url for _, url, quote in items if url and len(quote.split()) <= 25})
        with ThreadPoolExecutor(max_workers=8) as pool:
            pages = dict(zip(urls, pool.map(lambda url: fetch(url, allowed), urls)))
        counts = Counter()
        for ident, url, quote in items:
            if not url:
                verdict, detail = "NO_SOURCE", "no registry HTTP(S) source"
            elif len(quote.split()) > 25:
                verdict, detail = "TOO_LONG", "normalized quote exceeds 25 words"
            else:
                text, detail = pages[url]
                if text is None:
                    verdict = "UNREACHABLE"
                else:
                    verdict = "VERBATIM" if matches(quote, text) else "ABSENT"
                    detail = "normalized casefold substring; no token boundaries"
            counts[verdict] += 1
            print(f"QUOTE_REOPEN\t{ident}\t{verdict}\t{detail}")
        print("QUOTE_REOPEN_SUMMARY " + " ".join(f"{name.lower()}={counts[name]}" for name in ("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE")))
        return int(counts["VERBATIM"] != len(items))
    except (OSError, ValueError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
