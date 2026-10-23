#!/usr/bin/env python3
"""Registry and charset risk probe for the frozen counter's reference functions.

Read-only checks against the lane registry corpus/SOURCES.md and the eight
registry source URLs (one GET each).
"""
import gzip
import importlib.util
import os
import re
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


def main():
    lines = open(REGISTRY, encoding="utf-8").read().split("\n")

    print("### A. duplicate / ambiguous registry rows ###")
    seen = {}
    for i, ln in enumerate(lines, 1):
        m = re.match(r"^\| (S\d+) \|", ln)
        if m:
            seen.setdefault(m.group(1), []).append(i)
    dups = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"  rows with an id: {len(seen)}")
    print(f"  ids appearing more than once: {dups if dups else 'none'}")
    for sid in SOURCE_IDS:
        print(f"  {sid}: lines {seen.get(sid)}")

    print("\n### B. lines that start with '| Sxxx |' outside the Registry table ###")
    # a line anywhere in the file matching the counter's prefix test is a
    # candidate row for registry_url; the counter returns on the FIRST match
    for sid in SOURCE_IDS:
        hits = [(i, ln[:60]) for i, ln in enumerate(lines, 1) if ln.startswith(f"| {sid} |")]
        if len(hits) != 1:
            print(f"  {sid}: {len(hits)} matching lines -> {hits}")
    print("  (no output above means each of the eight ids matches exactly one line)")

    print("\n### C. pipes inside the source cell (field-index hazard) ###")
    piped = []
    for i, ln in enumerate(lines, 1):
        m = re.match(r"^\| (S\d+) \|", ln)
        if not m:
            continue
        cell = ln.split("|")[2]
        if "|" in cell:
            piped.append((i, m.group(1)))
    print(f"  rows whose split('|')[2] still contains a pipe: {len(piped)} {piped[:10]}")
    print("  (a pipe inside the source cell shifts the index and can hide the URL)")

    print("\n### D. rows whose source cell holds no http(s) URL ###")
    nourl = []
    for i, ln in enumerate(lines, 1):
        m = re.match(r"^\| (S\d+) \|", ln)
        if not m:
            continue
        if not re.search(r"https?://\S+", ln.split("|")[2]):
            nourl.append(m.group(1))
    print(f"  {len(nourl)} rows: {nourl}")

    print("\n### E. content type and charset of the eight registry source pages ###")
    for sid in SOURCE_IDS:
        url = C.registry_url(sid)
        req = urllib.request.Request(url, headers={"User-Agent": "chousa-quote-reopen-audit/r29",
                                                   "Accept-Encoding": "gzip"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read(8 * 1024 * 1024 + 1)
                enc = (r.headers.get("Content-Encoding") or "").lower()
                ctype = r.headers.get_content_type()
                charset = r.headers.get_content_charset()
                final = r.geturl()
        except Exception as e:  # noqa: BLE001
            print(f"  {sid}: FETCH FAILED {type(e).__name__}: {e}")
            continue
        if enc == "gzip":
            body = gzip.decompress(body)
        elif enc == "deflate":
            try:
                body = zlib.decompress(body)
            except zlib.error:
                body = zlib.decompress(body, -zlib.MAX_WBITS)
        allowed = ctype in cm.ALLOWED_CONTENT_TYPES
        hdr_charset = charset or "utf-8"
        try:
            body.decode(hdr_charset)
            hdr_ok = True
        except UnicodeDecodeError:
            hdr_ok = False
        try:
            body.decode("utf-8")
            utf8_ok = True
        except UnicodeDecodeError:
            utf8_ok = False
        nonascii = sum(1 for b in body if b > 127)
        print(f"  {sid}: ctype={ctype} allowed={allowed} hdr_charset={hdr_charset} "
              f"utf8_decodable={utf8_ok} non_ascii_bytes={nonascii} bytes={len(body)} "
              f"over_8MiB={len(body) > 8 * 1024 * 1024} final_url={final}")
        if final != url:
            print(f"    REDIRECT: {url} -> {final}")


if __name__ == "__main__":
    main()
