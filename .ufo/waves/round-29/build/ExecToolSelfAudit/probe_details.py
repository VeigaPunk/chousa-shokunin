#!/usr/bin/env python3
"""Final detail probes:

  1. urllib redirect target schemes (contract: "http and https only
     (redirects too)")
  2. where the S003 space-leak lands and whether it can change the token
     stream on real markup
  3. the counter's own alpha-token filter in page_cases versus claims.md
  4. what happens when a page exceeds 8 MiB or serves a disallowed content
     type (the reference does not enforce the contract's UNREACHABLE rules)
"""
import gzip
import importlib.util
import os
import sys
import urllib.request
import zlib

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contract_model as cm  # noqa: E402

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
COUNTER = os.path.join(LANE, "corpus", "evidence", "round29", "c1-count.py")
CACHE = os.path.join(HERE, "_cache")


def load_counter():
    spec = importlib.util.spec_from_file_location("c1_count_frozen", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = load_counter()


def counter_extract(doc):
    p = C._Text()
    p.feed(doc)
    p.close()
    return "".join(p.out)


def main():
    print("### 1. urllib redirect target schemes accepted ###")
    print("  HTTPRedirectHandler allowed schemes:", end=" ")
    try:
        from urllib.request import HTTPRedirectHandler
        print(getattr(HTTPRedirectHandler, "allowed_schemes", "not exposed"))
    except Exception as e:  # noqa: BLE001
        print(f"probe failed: {e!r}")
    print("  contract requires: http and https only (redirects too)")
    print("  the reference fetch_text applies no scheme filter of its own")

    print("\n### 2. S003 space-leak: does it change the token stream? ###")
    path = os.path.join(CACHE, "S003.html")
    if os.path.exists(path):
        doc = open(path, encoding="utf-8").read()
        a = counter_extract(doc)
        b = cm.contract_html_to_text(doc)
        i = 0
        while i < min(len(a), len(b)) and a[i] == b[i]:
            i += 1
        lo = max(0, i - 40)
        print(f"  first raw difference at offset {i}")
        print(f"    counter : {a[lo:i+40]!r}")
        print(f"    contract: {b[lo:i+40]!r}")
        na, nb = C.norm(a), cm.contract_norm(b)
        print(f"  normalized equal: {na == nb}")
        # the leak sits inside an existing whitespace run, so the collapse
        # erases it
        pre = a[max(0, i - 1):i]
        post = a[i:i + 1]
        print(f"  character before the leak: {pre!r}   character after: {post!r}")
        print(f"  leak is adjacent to whitespace on both sides: "
              f"{pre.isspace() and post.isspace()}")
        # a synthetic D1 case where the leak does change the token stream
        syn = "alpha<noscript><p>x</p></noscript>beta"
        print(f"  synthetic {syn!r}")
        print(f"    counter norm : {C.norm(counter_extract(syn))!r}")
        print(f"    contract norm: {cm.contract_norm(cm.contract_html_to_text(syn))!r}")

    print("\n### 3. page_cases alpha-token filter versus claims.md ###")
    print("  claims.md: 'samples 3 token windows of 6 to 20 tokens that are present")
    print("             in both fetches (label VERBATIM)'")
    print("  counter  : additionally requires at least 4 tokens containing a letter")
    import inspect
    src = inspect.getsource(C.page_cases)
    for ln in src.split("\n"):
        if "isalpha" in ln or "randint" in ln:
            print(f"    counter source: {ln.strip()}")

    print("\n### 4. contract UNREACHABLE rules the reference does not enforce ###")
    print("  content type allowlist (text/html, application/xhtml+xml, text/plain):")
    for ctype in ("text/html", "application/xhtml+xml", "text/plain", "application/pdf"):
        allowed = ctype in cm.ALLOWED_CONTENT_TYPES
        print(f"    {ctype:22} contract allows={allowed}  reference extracts text anyway")
    print("  body over 8 MiB: the reference reads at most 8 MiB + 1 and truncates")
    print("  silently; the contract makes such a body UNREACHABLE")
    big = b"<p>" + b"x" * (8 * 1024 * 1024 + 64) + b"</p>"

    class _H(dict):
        def get_content_charset(self):
            return None

        def get_content_type(self):
            return "text/html"

    class _R:
        def __init__(self):
            self._b = big
            self.headers = _H()

        def read(self, n=-1):
            out, self._b = self._b[:n], self._b[n:]
            return out

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    old = C.urllib.request.urlopen
    C.urllib.request.urlopen = lambda req, timeout=None: _R()
    try:
        got = C.fetch_text("https://example.org/big")
    finally:
        C.urllib.request.urlopen = old
    print(f"    reference returned {len(got)} chars from an over-8-MiB body "
          f"(contract verdict would be UNREACHABLE)")

    print("\n### 5. reference fetch_text: no retry, no status check of its own ###")
    print("  urllib raises HTTPError for 4xx/5xx, so a non-2xx page aborts the")
    print("  counter run with exit 2 rather than producing a label")


if __name__ == "__main__":
    main()
