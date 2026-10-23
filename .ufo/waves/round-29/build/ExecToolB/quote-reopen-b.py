#!/usr/bin/env python3
"""quote-reopen-b.py - independent N-version of the frozen round-29 quote-reopen tool.

This is a differential oracle for wave 2, not the landed tool. It implements the
frozen contract of `corpus/evidence/round29/claims.md` ("Tool contract
(frozen)") from that prose alone, deliberately structured differently from the
counter's reference functions in `corpus/evidence/round29/c1-count.py`:

  * the registry is parsed as a markdown table (the `source` column is located
    from the header row), not by splitting lines at a fixed offset;
  * HTML to text uses its own `html.parser` subclass that records chunks and
    applies the block/skip rules while parsing;
  * the match rule is evaluated with a compiled regular expression using
    look-around assertions for the alphanumeric boundary, not by a manual
    index scan;
  * fetching goes through a private opener with a scheme-restricting redirect
    handler, a per-URL result cache and one retry;
  * the character folding table is built from code points, so no invisible
    literal can be lost when this file is copied around.

Usage:
    python3 quote-reopen-b.py verify --items ITEMS.tsv [--registry SOURCES.md]

Exit codes: 0 if every item is VERBATIM, 1 if any item has another verdict,
2 on a usage or I/O error.
"""
import argparse
import gzip
import io
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zlib
from html.parser import HTMLParser

SKIP_TAGS = frozenset({"script", "style", "noscript", "template", "head"})
BLOCK_TAGS = frozenset({
    "p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3",
    "h4", "h5", "h6", "br", "section", "article", "header", "footer", "nav",
    "pre", "blockquote", "dt", "dd", "dl", "figure", "figcaption", "hr", "main",
    "aside",
})
MAX_WORDS = 25
MAX_BODY = 8 * 1024 * 1024
TIMEOUT = 30
RETRIES = 1
UA = "chousa-quote-reopen/1.0 (quote-reopen-b differential oracle)"
OK_TYPES = frozenset({"text/html", "application/xhtml+xml", "text/plain"})

# Curly quotes become straight quotes; soft hyphen and zero-width marks are
# deleted. The code points are spelled numerically so that this source file
# stays pure ASCII in that region.
_SINGLE_QUOTE_CPS = (0x2018, 0x2019, 0x201A, 0x201B)
_DOUBLE_QUOTE_CPS = (0x201C, 0x201D, 0x201E, 0x201F)
_DELETED_CPS = (0x00AD, 0x200B, 0x200C, 0x200D, 0xFEFF)

_FOLD = str.maketrans(
    dict([(chr(cp), "'") for cp in _SINGLE_QUOTE_CPS]
         + [(chr(cp), '"') for cp in _DOUBLE_QUOTE_CPS]
         + [(chr(cp), None) for cp in _DELETED_CPS])
)

# Alphanumeric in the sense of `str.isalnum()`. Python's `re` word class is
# "alphanumeric plus underscore", so removing the underscore from it leaves
# exactly the alphanumeric set; that equivalence was checked over the whole
# Unicode range.
_ALNUM = r"[^\W_]"
_URL_RE = re.compile(r"https?://\S+")


def normalize(text):
    """NFKC, quote folding, zero-width deletion, whitespace collapse."""
    folded = unicodedata.normalize("NFKC", text).translate(_FOLD)
    return " ".join(folded.split())


def word_count(normalized):
    return len(normalized.split())


class TextExtractor(HTMLParser):
    """HTML to text under the frozen rules.

    `script`, `style`, `noscript`, `template` and `head` content is dropped and
    comments are dropped. Every element of the block list emits one space at its
    start and at its end; every other element emits nothing.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.chunks = []
        self.skip_depth = 0

    def _space(self):
        self.chunks.append(" ")

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        elif tag in BLOCK_TAGS:
            self._space()

    def handle_startendtag(self, tag, attrs):
        if tag in BLOCK_TAGS:
            self._space()

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag in BLOCK_TAGS:
            self._space()

    def handle_data(self, data):
        if not self.skip_depth:
            self.chunks.append(data)

    def text(self):
        return "".join(self.chunks)


def html_to_text(body):
    parser = TextExtractor()
    parser.feed(body)
    parser.close()
    return parser.text()


def occurs_in(page_text, quote):
    """True when `quote` occurs in `page_text` on alphanumeric boundaries."""
    if not quote:
        return False
    pattern = "(?<!" + _ALNUM + ")" + re.escape(quote) + "(?!" + _ALNUM + ")"
    return re.search(pattern, page_text) is not None


class Registry:
    """The lane registry: id -> source cell."""

    def __init__(self, path):
        self.path = path
        self.rows = {}
        self.source_col = 1
        self._load()

    def _load(self):
        header_seen = False
        with open(self.path, encoding="utf-8") as handle:
            for raw in handle:
                line = raw.rstrip("\n")
                if not line.startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if not cells:
                    continue
                if cells[0] == "id" and not header_seen:
                    header_seen = True
                    if "source" in cells:
                        self.source_col = cells.index("source")
                    continue
                if set(cells[0]) <= set("-: "):
                    continue
                if not re.fullmatch(r"S\d+", cells[0]):
                    continue
                if cells[0] in self.rows:
                    continue
                self.rows[cells[0]] = cells[self.source_col] if len(cells) > self.source_col else ""

    def source_cell(self, sid):
        return self.rows.get(sid)

    def url_for(self, sid):
        cell = self.rows.get(sid)
        if cell is None:
            return None
        found = _URL_RE.search(cell)
        if not found:
            return None
        return found.group(0).rstrip(".,;)")


class _NoRedirectToOtherSchemes(urllib.request.HTTPRedirectHandler):
    """Redirects are followed, but only to http and https."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        scheme = urllib.parse.urlsplit(newurl).scheme.lower()
        if scheme not in ("http", "https"):
            raise urllib.error.HTTPError(
                newurl, code, "redirect to a non-http(s) scheme is refused", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Fetcher:
    """Fetches registry URLs, at most once per run, with one retry."""

    def __init__(self):
        self.opener = urllib.request.build_opener(_NoRedirectToOtherSchemes)
        self.cache = {}

    def fetch(self, url):
        if url in self.cache:
            return self.cache[url]
        result = self._fetch_once(url)
        for _ in range(RETRIES):
            if result[0] == "ok" or not result[2]:
                break
            time.sleep(1)
            result = self._fetch_once(url)
        self.cache[url] = result
        return result

    def _fetch_once(self, url):
        """Returns (status, detail, retryable)."""
        scheme = urllib.parse.urlsplit(url).scheme.lower()
        if scheme not in ("http", "https"):
            return ("unreachable", "scheme " + (scheme or "none") + " is not http or https", False)
        target = urllib.parse.urldefrag(url).url
        request = urllib.request.Request(target, headers={"User-Agent": UA})
        try:
            with self.opener.open(request, timeout=TIMEOUT) as response:
                status = getattr(response, "status", None) or response.getcode()
                ctype = response.headers.get_content_type()
                encoding = (response.headers.get("Content-Encoding") or "").lower()
                charset = response.headers.get_content_charset() or "utf-8"
                payload = response.read(MAX_BODY + 1)
        except urllib.error.HTTPError as exc:
            return ("unreachable", "http status " + str(exc.code), False)
        except Exception as exc:  # transport failure, timeout, malformed reply
            return ("unreachable", "fetch error: " + type(exc).__name__, True)
        if not (200 <= int(status) < 300):
            # 5xx is a server-side condition that can be transient, so it earns
            # the one retry; 4xx and other statuses will not change on a retry.
            return ("unreachable", "http status " + str(status), 500 <= int(status) < 600)
        if ctype not in OK_TYPES:
            return ("unreachable", "content type " + str(ctype), False)
        if encoding == "gzip":
            payload = _gunzip(payload)
        elif encoding == "deflate":
            payload = _inflate(payload)
        if len(payload) > MAX_BODY:
            return ("unreachable", "body over 8 MiB", False)
        try:
            body = payload.decode(charset, "replace")
        except LookupError:
            body = payload.decode("utf-8", "replace")
        if ctype == "text/plain":
            return ("ok", body, False)
        return ("ok", html_to_text(body), False)


def _gunzip(payload):
    """Decompress gzip bytes, bounded by the body cap."""
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(payload)) as handle:
            return handle.read(MAX_BODY + 1)
    except Exception:
        return payload


def _inflate(payload):
    """Decompress deflate bytes, bounded by the body cap."""
    for wbits in (zlib.MAX_WBITS, -zlib.MAX_WBITS):
        try:
            engine = zlib.decompressobj(wbits)
            return engine.decompress(payload, MAX_BODY + 1)
        except Exception:
            continue
    return payload


def default_registry():
    """corpus/SOURCES.md under the tool's lane root (the parent of tools/).

    When the tool sits in a `tools/` directory, the lane root is that
    directory's parent. Otherwise (this N-version lives under
    `.ufo/waves/...`) the lane root is searched upward from the working
    directory, which is where the counter runs the candidate from.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) == "tools":
        candidate = os.path.join(os.path.dirname(script_dir), "corpus", "SOURCES.md")
        if os.path.isfile(candidate):
            return candidate
    for start in (os.getcwd(), script_dir):
        cur = os.path.abspath(start)
        while True:
            candidate = os.path.join(cur, "corpus", "SOURCES.md")
            if os.path.isfile(candidate):
                return candidate
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
    return None


def read_items(path):
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    if not lines or lines[0].rstrip("\r") != "id\tsource_id\tquote":
        raise ValueError("items file header must be id<TAB>source_id<TAB>quote")
    items = []
    for line in lines[1:]:
        if not line:
            continue
        parts = line.rstrip("\r").split("\t", 2)
        if len(parts) != 3:
            raise ValueError("item line must have three tab-separated fields")
        items.append((parts[0], parts[1], parts[2]))
    return items


def judge(items, registry, fetcher):
    """One verdict per item, in input order."""
    verdicts = []
    for item_id, source_id, quote in items:
        url = registry.url_for(source_id)
        if url is None:
            if registry.source_cell(source_id) is None:
                detail = "no registry row " + source_id
            else:
                detail = "source cell of " + source_id + " holds no http(s) url"
            verdicts.append((item_id, "NO_SOURCE", detail))
            continue
        norm_quote = normalize(quote)
        words = word_count(norm_quote)
        if words > MAX_WORDS:
            verdicts.append((item_id, "TOO_LONG", str(words) + " words above " + str(MAX_WORDS)))
            continue
        status, payload, _retry = fetcher.fetch(url)
        if status != "ok":
            verdicts.append((item_id, "UNREACHABLE", payload))
            continue
        page_text = normalize(payload)
        if occurs_in(page_text, norm_quote):
            verdicts.append((item_id, "VERBATIM", "match on " + url))
        else:
            verdicts.append((item_id, "ABSENT", "no match on " + url))
    return verdicts


def main(argv=None):
    parser = argparse.ArgumentParser(prog="quote-reopen-b.py", add_help=True)
    sub = parser.add_subparsers(dest="command")
    verify = sub.add_parser("verify")
    verify.add_argument("--items", required=True)
    verify.add_argument("--registry", default=None)
    args = parser.parse_args(argv)

    if args.command != "verify":
        parser.error("the only command is 'verify'")

    registry_path = args.registry
    if registry_path is None:
        registry_path = default_registry()
        if registry_path is None:
            print("quote-reopen-b: no registry found; pass --registry", file=sys.stderr)
            return 2
    elif not os.path.isabs(registry_path):
        registry_path = os.path.abspath(registry_path)

    try:
        items = read_items(args.items)
    except (OSError, ValueError) as exc:
        print("quote-reopen-b: " + str(exc), file=sys.stderr)
        return 2
    try:
        registry = Registry(registry_path)
    except OSError as exc:
        print("quote-reopen-b: registry: " + str(exc), file=sys.stderr)
        return 2

    verdicts = judge(items, registry, Fetcher())
    counts = {"VERBATIM": 0, "ABSENT": 0, "TOO_LONG": 0, "NO_SOURCE": 0, "UNREACHABLE": 0}
    for item_id, verdict, detail in verdicts:
        counts[verdict] += 1
        print("\t".join(("QUOTE_REOPEN", item_id, verdict, detail)))
    print("QUOTE_REOPEN_SUMMARY "
          + " ".join(name.lower() + "=" + str(counts[name])
                     for name in ("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE")))
    return 0 if counts["VERBATIM"] == len(verdicts) else 1


if __name__ == "__main__":
    sys.exit(main())
