#!/usr/bin/env python3
"""Classify every way the counter's HTML-to-text differs from the
contract-literal reading, and show the live effect on the eight registry
source pages.

Three divergence classes are expected and are named explicitly:

  D1 space-leak      a block-level element inside a dropped region still
                     emits its one space in the counter, while the contract
                     reading drops the whole region.
  D2 depth-vs-stack  the counter keeps one integer depth for all dropped
                     elements, so a stray end tag for one drop element ends
                     the region of another one.
  D3 self-close      a self-closing drop element (<script/>, <template/>)
                     does not open a dropped region in the counter.

Any divergence outside these three classes is reported as UNEXPLAINED.
"""
import gzip
import importlib.util
import os
import sys
import urllib.request
import zlib

# never leave a __pycache__ in the lane tree
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contract_model as cm  # noqa: E402

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
COUNTER = os.path.join(LANE, "corpus", "evidence", "round29", "c1-count.py")
REGISTRY = os.path.join(LANE, "corpus", "SOURCES.md")
SOURCE_IDS = ["S002", "S003", "S008", "S013", "S019", "S020", "S038", "S044"]


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


def classify(doc):
    """returns (counter_text, contract_text, class_name)"""
    a = counter_extract(doc)
    b = cm.contract_html_to_text(doc)
    if a == b:
        return a, b, "same"
    if a.replace(" ", "") == b.replace(" ", ""):
        return a, b, "D1 space-leak"
    return a, b, "UNEXPLAINED"


def live_pages():
    out = {}
    with open(REGISTRY, encoding="utf-8") as f:
        for ln in f:
            for sid in SOURCE_IDS:
                if ln.startswith(f"| {sid} |"):
                    out[sid] = ln
    for sid in SOURCE_IDS:
        url = C.registry_url(sid)
        req = urllib.request.Request(url, headers={"User-Agent": "chousa-quote-reopen-audit/r29",
                                                   "Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read(8 * 1024 * 1024 + 1)
            enc = (r.headers.get("Content-Encoding") or "").lower()
            charset = r.headers.get_content_charset() or "utf-8"
        if enc == "gzip":
            body = gzip.decompress(body)
        elif enc == "deflate":
            try:
                body = zlib.decompress(body)
            except zlib.error:
                body = zlib.decompress(body, -zlib.MAX_WBITS)
        yield sid, url, body.decode(charset, "replace")


def main():
    print("### live pages (one GET per registry source URL) ###")
    for sid, url, doc in live_pages():
        a, b, cls = classify(doc)
        na, nb = C.norm(a), cm.contract_norm(b)
        print(f"\n{sid} {url}")
        print(f"  class: {cls}")
        print(f"  raw identical: {a == b}   normalized identical: {na == nb}")
        if a != b:
            # show the first differing region
            i = 0
            while i < min(len(a), len(b)) and a[i] == b[i]:
                i += 1
            lo = max(0, i - 60)
            print(f"  first raw difference at offset {i}")
            print(f"    counter : ...{a[lo:i+60]!r}")
            print(f"    contract: ...{b[lo:i+60]!r}")
        if na != nb:
            ta, tb = na.split(" "), nb.split(" ")
            print(f"  TOKEN STREAMS DIFFER: counter={len(ta)} tokens, contract={len(tb)} tokens")
            diffs = [i for i in range(min(len(ta), len(tb))) if ta[i] != tb[i]]
            print(f"  differing token indices: {diffs[:10]} (of {min(len(ta), len(tb))})")
            for i in diffs[:5]:
                ctx = " ".join(ta[max(0, i - 3):i + 4])
                print(f"    [{i}] counter={ta[i]!r} contract={tb[i]!r}  ctx: {ctx}")
        else:
            print("  token streams identical: no label risk from this page")

    print("\n### synthetic divergence classes ###")
    cases = [
        ("D1 space-leak", "foo<noscript><p>x</p></noscript>bar"),
        ("D2 depth-vs-stack", "<template></script> b<!-- c --> "),
        ("D2 depth-vs-stack", "<noscript><p>x</p></script>LEAK</noscript>"),
        ("D3 self-close", "<script/>LEAK</script>"),
        ("same", "<p>one</p><p>two</p>"),
    ]
    for want, doc in cases:
        a, b, cls = classify(doc)
        print(f"  {want:18} -> observed {cls:18} counter={a!r} contract={b!r}")


if __name__ == "__main__":
    main()
