#!/usr/bin/env python3
"""Live probe of the eight registry source pages behind the frozen fixture.

Read-only GET requests to the `source` column URLs of corpus/SOURCES.md, which
the network policy of this seat allows.  No credentials, no posting, one GET
per URL, 30 s timeout, killed on exit.

For each page the probe records what the counter's reference functions would
see and what a contract-literal reading would see, so that a divergence can be
tied to a real page rather than a synthetic one:

  * HTTP status, Content-Type, Content-Encoding, charset, body size
  * whether the body exceeds the contract's 8 MiB UNREACHABLE limit
  * whether the content type is inside the contract's allowlist
  * whether the counter's extraction and the contract-literal extraction differ
    on the real markup (this is the label-relevant divergence)
  * which of the eight pages carry a block-level element inside a skipped
    region (noscript / template / head), the construct that leaks a space
"""
import gzip
import importlib.util
import os
import re
import sys
import urllib.request
import zlib
from html.parser import HTMLParser

# never leave a __pycache__ in the lane tree
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contract_model as cm  # noqa: E402

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
COUNTER = os.path.join(LANE, "corpus", "evidence", "round29", "c1-count.py")
REGISTRY = os.path.join(LANE, "corpus", "SOURCES.md")

# the eight source ids the frozen fixture draws its quotes from, as named in
# corpus/evidence/round29/claims.md ("registry rows S002, S003, S008, S013,
# S019, S020, S038 and S044")
SOURCE_IDS = ["S002", "S003", "S008", "S013", "S019", "S020", "S038", "S044"]


def load_counter():
    spec = importlib.util.spec_from_file_location("c1_count_frozen", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = load_counter()


class _Headers(dict):
    def get_content_charset(self):
        ct = self.get("Content-Type", "")
        return ct.split("charset=")[1].split(";")[0].strip() if "charset=" in ct else None

    def get_content_type(self):
        return self.get("Content-Type", "").split(";")[0].strip().lower()


class Resp:
    def __init__(self, body, headers):
        self._body = body
        self.headers = _Headers(headers)

    def read(self, n=-1):
        if n is None or n < 0:
            out, self._body = self._body, b""
            return out
        out, self._body = self._body[:n], self._body[n:]
        return out

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def counter_extract(doc):
    p = C._Text()
    p.feed(doc)
    p.close()
    return "".join(p.out)


def block_in_skip_regions(doc):
    """names of block-level tags found inside a skipped region"""
    found = []

    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.skip = 0
            self.hits = []

        def handle_starttag(self, tag, attrs):
            if tag in cm.CONTRACT_SKIP:
                self.skip += 1
            elif self.skip and tag in cm.CONTRACT_BLOCK:
                self.hits.append(tag)

        def handle_endtag(self, tag):
            if tag in cm.CONTRACT_SKIP and self.skip:
                self.skip -= 1

    p = P()
    p.feed(doc)
    p.close()
    return p.hits


def main():
    rows = {}
    with open(REGISTRY, encoding="utf-8") as f:
        for ln in f:
            for sid in SOURCE_IDS:
                if ln.startswith(f"| {sid} |"):
                    rows[sid] = ln
    for sid in SOURCE_IDS:
        ln = rows.get(sid)
        if ln is None:
            print(f"{sid}: no registry row")
            continue
        url = C.registry_url(sid)
        cell = ln.split("|")[2]
        print("=" * 70)
        print(f"{sid} url={url}")
        print(f"  source cell: {cell.strip()[:120]}")
        # pipe inside the source cell would shift the counter's field index
        print(f"  pipes in source cell: {cell.count('|')}")
        if url is None:
            print("  no URL: skipped")
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "chousa-quote-reopen-audit/r29",
                                                   "Accept-Encoding": "gzip"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read(8 * 1024 * 1024 + 1)
                enc = (r.headers.get("Content-Encoding") or "").lower()
                charset = r.headers.get_content_charset() or "utf-8"
                ctype = r.headers.get_content_type()
                status = r.status
        except Exception as e:  # noqa: BLE001
            print(f"  FETCH FAILED: {type(e).__name__}: {e}")
            continue
        size = len(body)
        print(f"  status={status} ctype={ctype} enc={enc or '-'} charset={charset} bytes={size}")
        print(f"  content type allowed by contract: {ctype in cm.ALLOWED_CONTENT_TYPES}")
        print(f"  body over 8 MiB (contract UNREACHABLE): {size > 8 * 1024 * 1024}")
        if enc == "gzip":
            body = gzip.decompress(body)
        elif enc == "deflate":
            try:
                body = zlib.decompress(body)
            except zlib.error:
                body = zlib.decompress(body, -zlib.MAX_WBITS)
        doc = body.decode(charset, "replace")
        a = counter_extract(doc)
        b = cm.contract_html_to_text(doc)
        na = C.norm(a)
        nb = cm.contract_norm(b)
        print(f"  extraction identical (raw): {a == b}")
        print(f"  extraction identical (normalized): {na == nb}")
        if na != nb:
            print(f"  normalized lengths: counter={len(na)} contract={len(nb)}")
            ta, tb = na.split(" "), nb.split(" ")
            print(f"  token counts: counter={len(ta)} contract={len(tb)}")
            diffs = [i for i in range(min(len(ta), len(tb))) if ta[i] != tb[i]]
            print(f"  first differing token index: {diffs[:5]}")
            for i in diffs[:3]:
                print(f"    [{i}] counter={ta[i]!r} contract={tb[i]!r}")
        hits = block_in_skip_regions(doc)
        print(f"  block tags inside skipped regions: {len(hits)} {sorted(set(hits))[:8]}")
        print(f"  has <noscript>: {'<noscript' in doc.lower()}"
              f"  has <template>: {'<template' in doc.lower()}")


if __name__ == "__main__":
    main()
