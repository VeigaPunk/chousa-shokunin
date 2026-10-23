#!/usr/bin/env python3
"""Materiality probe: does each counter/contract divergence change the TOKEN
stream (and therefore the label) of a live registry page, and is norm()
idempotent (the counter labels windows drawn from normalized text, and the
tool normalizes the quote again)?

One GET per registry source URL, read-only.  Pages are cached under
_cache/ so the probe can be re-run without re-fetching.
"""
import gzip
import importlib.util
import os
import random
import sys
import urllib.request
import zlib

sys.dont_write_bytecode = True  # never leave a __pycache__ in the lane tree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contract_model as cm  # noqa: E402

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
COUNTER = os.path.join(LANE, "corpus", "evidence", "round29", "c1-count.py")
REGISTRY = os.path.join(LANE, "corpus", "SOURCES.md")
SOURCE_IDS = ["S002", "S003", "S008", "S013", "S019", "S020", "S038", "S044"]
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


def live_pages():
    os.makedirs(CACHE, exist_ok=True)
    rows = {}
    with open(REGISTRY, encoding="utf-8") as f:
        for ln in f:
            for sid in SOURCE_IDS:
                if ln.startswith(f"| {sid} |"):
                    rows[sid] = ln
    for sid in SOURCE_IDS:
        path = os.path.join(CACHE, sid + ".html")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                yield sid, f.read()
            continue
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
        doc = body.decode(charset, "replace")
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc)
        yield sid, doc


def main():
    print("### materiality on the eight live pages ###")
    material = 0
    for sid, doc in live_pages():
        a = counter_extract(doc)
        b = cm.contract_html_to_text(doc)
        na, nb = C.norm(a), cm.contract_norm(b)
        ta, tb = na.split(" "), nb.split(" ")
        same = ta == tb
        if not same:
            material += 1
        # count the leaked whitespace without a quadratic diff: compare the
        # two token streams and the two raw lengths
        print(f"  {sid}: raw_same={a == b} raw_len_delta={len(a) - len(b)} "
              f"token_streams_same={same} tokens={len(ta)}/{len(tb)}")
        if not same:
            diffs = [i for i in range(min(len(ta), len(tb))) if ta[i] != tb[i]]
            print(f"    DIFFER at token indices {diffs[:6]} of {min(len(ta), len(tb))}")
            for i in diffs[:3]:
                lo = max(0, i - 3)
                print(f"      [{i}] counter={ta[i]!r} contract={tb[i]!r}")
                print(f"          counter ctx: {' '.join(ta[lo:i + 4])!r}")
                print(f"          contract ctx: {' '.join(tb[lo:i + 4])!r}")
    print(f"  pages whose token streams differ: {material} of {len(SOURCE_IDS)}")

    print("\n### norm() idempotence (a quote is normalized again by the tool) ###")
    pool = ["a", "b", " ", "\t", "\n", " ", "“", "”", "’", "‘",
            "­", "", "‌", "‍", "﻿", "ﬁ", "Ａ", "é", " ", "�",
            "①", "½", "²", "…", "—"]
    rng = random.Random(20261023)
    bad = 0
    for _ in range(20000):
        s = "".join(rng.choice(pool) for _ in range(rng.randint(0, 14)))
        n1 = C.norm(s)
        if C.norm(n1) != n1:
            bad += 1
            if bad < 4:
                print(f"  NOT IDEMPOTENT: {s!r} -> {n1!r} -> {C.norm(n1)!r}")
    print(f"  non-idempotent samples: {bad} of 20000")

    print("\n### counter norm vs contract norm on the live corpus ###")
    diff = 0
    for sid, doc in live_pages():
        raw = counter_extract(doc)
        if C.norm(raw) != cm.contract_norm(raw):
            diff += 1
            print(f"  {sid}: DIFFERS")
    print(f"  pages where counter norm != contract norm: {diff} of {len(SOURCE_IDS)}")


if __name__ == "__main__":
    main()
