#!/usr/bin/env python3
"""Re-open located quotes against the live source named by the lane registry.

Usage:
    python3 tools/quote-reopen.py verify --items ITEMS.tsv [--registry SOURCES.md]

The tool reads a tab-separated item file with the header `id<TAB>source_id<TAB>quote`,
looks each `source_id` up in the lane registry (`corpus/SOURCES.md` by default, that is
the file named by `--registry`), fetches each registry URL once per run, extracts the
page text and reports one verdict per item:

    QUOTE_REOPEN<TAB><id><TAB><VERDICT><TAB><detail>

followed by one summary line:

    QUOTE_REOPEN_SUMMARY verbatim=<n> absent=<n> too_long=<n> no_source=<n> unreachable=<n>

Verdicts, in the order they are checked: NO_SOURCE, TOO_LONG, UNREACHABLE, then
VERBATIM or ABSENT. Exit status is 0 when every item is VERBATIM, 1 when any item
carries another verdict, and 2 on a usage or input/output error.

Fetch bounds: registry URLs only, GET only, http and https only for the request and
for every redirect hop, a fragment removed, no userinfo, no cookies and no
credentials, a 30 s total deadline per URL shared with the single retry, and a cap of
8 MiB on both the wire bytes and the inflated bytes. Page text is kept in memory only;
nothing is written to disk.

Python 3 standard library only.
"""
import argparse
import http.client
import ipaddress
import os
import re
import signal
import socket
import ssl
import sys
import time
import unicodedata
import urllib.parse
import zlib
from html.parser import HTMLParser

LANE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_REGISTRY = os.path.join(LANE, "corpus", "SOURCES.md")
ITEM_HEADER = "id\tsource_id\tquote"

MAX_BODY = 8 * 1024 * 1024
DEADLINE = 30.0
RETRIES = 1
MAX_REDIRECTS = 10
CHUNK = 65536
USER_AGENT = "chousa-quote-reopen/1.0 (chousa lane quote verifier; python-stdlib)"
ALLOWED_TYPES = {"text/html", "application/xhtml+xml", "text/plain"}
MAX_WORDS = 25

# Content of these elements is dropped, and comments are dropped.
SKIP = {"script", "style", "noscript", "template", "head"}
# These elements emit one space at start and at end; every other element emits nothing.
BLOCK = {"p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6",
         "br", "section", "article", "header", "footer", "nav", "pre", "blockquote", "dt", "dd", "dl",
         "figure", "figcaption", "hr", "main", "aside"}
# Typographic quotation marks fold to their ASCII form; soft and zero-width marks vanish.
QMAP = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
                      "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
                      "\u00ad": None, "\u200b": None, "\u200c": None, "\u200d": None, "\ufeff": None})
URL_RE = re.compile(r"https?://\S+")


def norm(s):
    """NFKC, typographic quotes folded, soft marks dropped, whitespace runs collapsed."""
    return " ".join(unicodedata.normalize("NFKC", s).translate(QMAP).split())


class _Text(HTMLParser):
    """Page HTML to text: skipped element content dropped, block elements emit a space."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

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


def html_to_text(doc):
    """Extract the reader-visible text of an HTML document."""
    p = _Text()
    p.feed(doc)
    p.close()
    return "".join(p.out)


def found(text, quote):
    """True iff the normalized quote occurs in the normalized text at a non-alphanumeric boundary."""
    q = norm(quote)
    if not q:
        return False
    i = 0
    while True:
        i = text.find(q, i)
        if i < 0:
            return False
        j = i + len(q)
        if (i == 0 or not text[i - 1].isalnum()) and (j == len(text) or not text[j].isalnum()):
            return True
        i += 1


def registry_rows(path):
    """Map each registry id to the source cell of its row."""
    rows = {}
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if not ln.startswith("| "):
                continue
            cells = ln.split("|")
            if len(cells) < 4:
                continue
            sid = cells[1].strip()
            if not sid or sid == "id" or set(sid) == {"-"}:
                continue
            rows.setdefault(sid, cells[2])
    return rows


def registry_url(cell):
    """The first http(s) URL of a source cell, with trailing sentence punctuation stripped."""
    if cell is None:
        return None
    m = URL_RE.search(cell)
    if not m:
        return None
    return m.group(0).rstrip(".,;)")


class _Refuse(Exception):
    """A request that must not be made: a short reason, never the URL or a secret."""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def _check_url(url):
    """Split a URL and refuse anything outside the fetch bounds. Returns (scheme, host, port, target)."""
    parts = urllib.parse.urlsplit(url)
    scheme = parts.scheme.lower()
    if scheme not in ("http", "https"):
        raise _Refuse("scheme not http or https")
    if parts.username or parts.password:
        raise _Refuse("url carries userinfo")
    host = parts.hostname
    if not host:
        raise _Refuse("url has no host")
    try:
        port = parts.port
    except ValueError:
        raise _Refuse("url has an invalid port")
    if port is None:
        port = 443 if scheme == "https" else 80
    target = parts.path or "/"
    if parts.query:
        target += "?" + parts.query
    return scheme, host, port, target


def _check_address(host, port):
    """Refuse a host that resolves to any non-global address (loopback, private, link-local)."""
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except (socket.gaierror, UnicodeError, OSError):
        raise _Refuse("host does not resolve")
    addrs = []
    for info in infos:
        sockaddr = info[4]
        if sockaddr:
            addrs.append(sockaddr[0])
    if not addrs:
        raise _Refuse("host does not resolve")
    for a in addrs:
        try:
            addr = ipaddress.ip_address(a.split("%", 1)[0])
        except ValueError:
            raise _Refuse("host resolves to an unusable address")
        if not addr.is_global:
            raise _Refuse("host resolves to a non-global address")


def _inflate_stream(chunks, encoding):
    """Inflate compressed bytes incrementally. Returns (bytes, over_cap)."""
    enc = (encoding or "").lower().strip()
    if enc in ("", "identity"):
        return b"".join(chunks), False
    if enc not in ("gzip", "deflate", "zlib"):
        return b"", True
    wbits = 16 + zlib.MAX_WBITS if enc == "gzip" else zlib.MAX_WBITS
    out = bytearray()
    for wb in (wbits, -zlib.MAX_WBITS):
        d = zlib.decompressobj(wb)
        try:
            for chunk in chunks:
                out += d.decompress(chunk, MAX_BODY + 1 - len(out))
                if len(out) > MAX_BODY:
                    return bytes(out), True
            out += d.flush()
        except zlib.error:
            out = bytearray()
            continue
        return bytes(out), len(out) > MAX_BODY
    return b"", True


def _read_response(resp, deadline):
    """Read a response body under the wire-byte cap and the total deadline."""
    chunks = []
    total = 0
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise _Refuse("deadline exceeded while reading the body")
        sock = getattr(getattr(getattr(resp, "fp", None), "raw", None), "_sock", None)
        if sock is not None:
            try:
                sock.settimeout(remaining)
            except OSError:
                pass
        try:
            chunk = resp.read(CHUNK)
        except (http.client.HTTPException, OSError, ValueError):
            raise _Refuse("body read failed")
        if not chunk:
            break
        total += len(chunk)
        if total > MAX_BODY:
            return chunks, True
        chunks.append(chunk)
    return chunks, False


def _request_once(url, deadline):
    """One HTTP GET, following redirects inside the fetch bounds.

    Returns (status, ctype, text, detail, retryable). `text` is None when the page
    could not be read; `detail` then carries a short reason, never a URL or a secret.
    `retryable` is True only for a transport-level failure, which the single retry
    may repeat inside the same deadline.
    """
    current = url
    for _ in range(MAX_REDIRECTS + 1):
        scheme, host, port, target = _check_url(current)
        _check_address(host, port)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise _Refuse("deadline exceeded")
        conn = None
        try:
            if scheme == "https":
                conn = http.client.HTTPSConnection(host, port, timeout=remaining,
                                                   context=ssl.create_default_context())
            else:
                conn = http.client.HTTPConnection(host, port, timeout=remaining)
            conn.request("GET", target, headers={"User-Agent": USER_AGENT,
                                                  "Accept-Encoding": "gzip",
                                                  "Accept": "*/*",
                                                  "Connection": "close"})
            resp = conn.getresponse()
            status = resp.status
            ctype_header = resp.getheader("Content-Type") or ""
            encoding = resp.getheader("Content-Encoding")
            if status in (301, 302, 303, 307, 308):
                location = resp.getheader("Location")
                if not location:
                    raise _Refuse("redirect without a location")
                current = urllib.parse.urljoin(current, location)
                resp.read(0)
                continue
            ctype = ctype_header.split(";")[0].strip().lower()
            if status < 200 or status >= 300:
                return status, ctype, None, "HTTP %d" % status, status >= 500
            if ctype not in ALLOWED_TYPES:
                return status, ctype, None, "content type %s" % (ctype or "unknown"), False
            chunks, over = _read_response(resp, deadline)
            if over:
                return status, ctype, None, "body over 8 MiB", False
            body, over = _inflate_stream(chunks, encoding)
            if over:
                return status, ctype, None, "body over 8 MiB", False
            charset = "utf-8"
            for part in ctype_header.split(";")[1:]:
                k, _, v = part.strip().partition("=")
                if k.lower() == "charset":
                    charset = v.strip().strip('"') or "utf-8"
            try:
                doc = body.decode(charset, "replace")
            except LookupError:
                doc = body.decode("utf-8", "replace")
            if ctype == "text/plain":
                return status, ctype, norm(doc), "", False
            return status, ctype, norm(html_to_text(doc)), "", False
        finally:
            if conn is not None:
                try:
                    conn.close()
                except OSError:
                    pass
    raise _Refuse("too many redirects")


def _round29_fetch_page(url):
    """Fetch one registry URL within the fetch bounds. Returns (status, ctype, text, detail)."""
    target = url.split("#", 1)[0]
    deadline = time.monotonic() + 30.0
    detail = ""
    for attempt in range(RETRIES + 1):
        retryable = False
        try:
            status, ctype, text, detail, retryable = _request_once(target, deadline)
        except _Refuse as e:
            return None, None, None, e.reason
        except (http.client.HTTPException, http.client.InvalidURL, OSError, ValueError,
                UnicodeError, ssl.SSLError, zlib.error) as e:
            detail = "fetch failed: %s" % type(e).__name__
            text = None
            retryable = True
        if text is not None:
            return status, ctype, text, detail
        if not retryable or attempt >= RETRIES or (deadline - time.monotonic()) <= 0:
            return None, None, None, detail or "fetch failed"
    return None, None, None, detail or "fetch failed"


def _fixed_cutoff(signum, frame):
    raise _Refuse("fixed 3.8-second wall cutoff")


def fetch_page(url):
    previous = signal.signal(signal.SIGALRM, _fixed_cutoff)
    signal.setitimer(signal.ITIMER_REAL, 3.8)
    try:
        return _round29_fetch_page(url)
    except _Refuse as e:
        return None, None, None, e.reason
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, previous)


def load_items(path):
    """Read the tab-separated item file."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    if not lines or lines[0].rstrip("\r") != ITEM_HEADER:
        raise ValueError("%s: header must be %r" % (path, ITEM_HEADER))
    items = []
    for ln in lines[1:]:
        ln = ln.rstrip("\r")
        if not ln:
            continue
        parts = ln.split("\t", 2)
        if len(parts) != 3:
            raise ValueError("%s: malformed item line" % path)
        items.append((parts[0], parts[1], parts[2]))
    return items


def resolve_registry(arg):
    """The registry file to read: the lane's corpus/SOURCES.md unless --registry names one."""
    if arg is None:
        return DEFAULT_REGISTRY
    for cand in (arg, os.path.join(LANE, arg), os.path.join(LANE, "corpus", arg)):
        if os.path.exists(cand):
            return cand
    return arg


def verify(items_path, registry_path):
    """Verify every item and print one verdict line per item, then the summary line."""
    rows = registry_rows(registry_path)
    items = load_items(items_path)
    cache = {}
    counts = {"VERBATIM": 0, "ABSENT": 0, "TOO_LONG": 0, "NO_SOURCE": 0, "UNREACHABLE": 0}
    out = []
    for item_id, source_id, quote in items:
        cell = rows.get(source_id)
        url = registry_url(cell)
        if url is None:
            detail = ("no registry row %s" % source_id if cell is None
                      else "registry row %s has no http(s) URL" % source_id)
            verdict = "NO_SOURCE"
        elif len(norm(quote).split()) > MAX_WORDS:
            verdict = "TOO_LONG"
            detail = "%d words, limit %d" % (len(norm(quote).split()), MAX_WORDS)
        else:
            if url not in cache:
                cache[url] = fetch_page(url)
            status, ctype, text, detail = cache[url]
            if text is None:
                verdict = "UNREACHABLE"
                detail = detail or "unreachable"
            elif found(text, quote):
                verdict = "VERBATIM"
                detail = "matched in normalized page text"
            else:
                verdict = "ABSENT"
                detail = "no match in normalized page text"
        counts[verdict] += 1
        out.append((item_id, verdict, detail))
    for item_id, verdict, detail in out:
        sys.stdout.write("QUOTE_REOPEN\t%s\t%s\t%s\n" % (item_id, verdict, detail.replace("\t", " ")))
    sys.stdout.write("QUOTE_REOPEN_SUMMARY verbatim=%d absent=%d too_long=%d no_source=%d unreachable=%d\n"
                     % (counts["VERBATIM"], counts["ABSENT"], counts["TOO_LONG"],
                        counts["NO_SOURCE"], counts["UNREACHABLE"]))
    return 0 if counts["VERBATIM"] == len(items) else 1


def main(argv):
    ap = argparse.ArgumentParser(prog="quote-reopen.py")
    sub = ap.add_subparsers(dest="command")
    v = sub.add_parser("verify", help="re-open located quotes against the live registry source")
    v.add_argument("--items", required=True, help="tab-separated items file")
    v.add_argument("--registry", default=None, help="registry file (default corpus/SOURCES.md)")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 2
    if args.command != "verify":
        ap.print_usage(sys.stderr)
        return 2
    try:
        return verify(args.items, resolve_registry(args.registry))
    except (OSError, ValueError, UnicodeDecodeError) as e:
        sys.stderr.write("quote-reopen: %s\n" % type(e).__name__)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
