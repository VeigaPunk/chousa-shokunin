#!/usr/bin/env python3
"""ReviewFixtureEdgeClasses — attack fixture ground truth for 4 edge classes.

Read-only on the lane. Imports the FROZEN counter module c1-count.py for the
reference pipeline (norm / found / registry_url / _Text) so no re-implementation
drift is possible. Network: GET only, only registry source-column URLs.
"""
import gzip
import hashlib
import importlib.util
import io
import json
import re
import sys
import time
import urllib.request
import urllib.error

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
COUNTER = LANE + "/corpus/evidence/round29/c1-count.py"
ITEMS = LANE + "/corpus/fixtures/quote-reopen-r29/items.tsv"
LABELS = LANE + "/corpus/fixtures/quote-reopen-r29/labels.tsv"
REGISTRY = LANE + "/corpus/SOURCES.md"

spec = importlib.util.spec_from_file_location("c1count", COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

t0 = time.monotonic()

items = {}
for ln in open(ITEMS, encoding="utf-8").read().splitlines()[1:]:
    if ln.strip():
        iid, sid, quote = ln.split("\t")
        items[iid] = (sid, quote)
labels = {}
for ln in open(LABELS, encoding="utf-8").read().splitlines()[1:]:
    if ln.strip():
        iid, label, cls = ln.split("\t")
        labels[iid] = (label, cls)

# ---------- registry checks ----------
reg_rows = {}   # id -> (source_cell, kind_cell)
for ln in open(REGISTRY, encoding="utf-8").read().splitlines():
    if ln.startswith("| S") and not ln.startswith("|---"):
        cells = ln.split("|")
        reg_rows[cells[1].strip()] = (cells[2].strip(), cells[3].strip())

print("== REGISTRY ==")
print("S999 row present:", "S999" in reg_rows)
print("S999 registry_url():", c1.registry_url("S999"))
for sid in ("S001", "S045"):
    cell, kind = reg_rows.get(sid, ("<ABSENT>", "<ABSENT>"))
    has_url = re.search(r"https?://", cell) is not None
    print(f"{sid} row present: {sid in reg_rows} | kind: {kind} | "
          f"source cell: {cell!r} | http(s) in cell: {has_url} | registry_url(): {c1.registry_url(sid)}")
print("positive control S044 registry_url():", c1.registry_url("S044"))

# ---------- fetch helper (contract bounds: GET, fragment stripped, 30s, 1 retry) ----------
def fetch(url):
    u = url.split("#")[0]
    last = None
    for attempt in (1, 2):
        try:
            fa = time.monotonic()
            req = urllib.request.Request(u, headers={
                "User-Agent": "chousa-quote-reopen-counter/r29",
                "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=30) as r:
                status = r.status
                ctype = r.headers.get("Content-Type", "")
                raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            dt = time.monotonic() - fa
            print(f"  fetch {u} -> {status} {ctype.split(';')[0]} {len(raw)}B in {dt:.1f}s (attempt {attempt})")
            return raw.decode("utf-8", "replace"), ctype, status
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"  fetch attempt {attempt} failed: {type(e).__name__}: {e}")
            time.sleep(1)
    raise RuntimeError(f"fetch failed after retry: {last}")

def page_text(url):
    html, ctype, status = fetch(url)
    assert 200 <= status < 300, f"non-2xx {status}"
    assert any(t in ctype for t in ("text/html", "application/xhtml+xml", "text/plain")), f"ctype {ctype}"
    assert len(html) <= 8 * 1024 * 1024, "body > 8MiB"
    p = c1._Text()
    p.feed(html)
    return c1.norm("".join(p.out))

def occurrences(text, q):
    """All occurrences of q with boundary analysis at both edges."""
    out, i = [], 0
    while True:
        i = text.find(q, i)
        if i < 0:
            break
        j = i + len(q)
        before = text[i - 1] if i > 0 else ""
        after = text[j] if j < len(text) else ""
        ok = (i == 0 or not before.isalnum()) and (j == len(text) or not after.isalnum())
        out.append((i, before, after, ok))
        i += 1
    return out

ctx = lambda text, i, j: text[max(0, i - 45):j + 45].replace("\n", " ")

verdicts = {}

# ---------- class 1+2: no-source ----------
print("\n== NO_SOURCE ==")
for iid in ("d3909bba", "76b6a43c", "aff4afec"):
    sid, quote = items[iid]
    label, cls = labels[iid]
    # contract verdict 1: id not a registry row OR source cell has no http(s) URL
    derived = "NO_SOURCE" if c1.registry_url(sid) is None else "FETCH?"
    ok = derived == label
    verdicts[iid] = ok
    print(f"{iid} {sid} label={label} class={cls} derived={derived} -> {'LABEL-OK' if ok else 'LABEL-WRONG'}")

# ---------- class 3: too-long-true-text ----------
print("\n== TOO_LONG (word count after frozen normalization) ==")
too_long_ids = [i for i, (l, c) in labels.items() if c == "too-long-true-text"]
pages = {}
needed_sids = sorted({items[i][0] for i in too_long_ids} |
                     {items[i][0] for i, (l, c) in labels.items() if c == "absent-truncated-token"})
url_of = {}
for sid in needed_sids:
    u = c1.registry_url(sid)
    assert u, f"no url for {sid}"
    url_of[sid] = u
    print(f"-- opening {sid} {u}")
    pages[sid] = page_text(u)
    print(f"   normalized page text: {len(pages[sid])} chars")

for iid in sorted(too_long_ids):
    sid, quote = items[iid]
    label, cls = labels[iid]
    n_words = len(c1.norm(quote).split())
    present = c1.found(pages[sid], quote)
    derived = "TOO_LONG" if n_words > 25 else "FETCH?"
    ok = derived == label
    verdicts[iid] = ok
    print(f"{iid} {sid} words={n_words} (>25: {n_words > 25}) true-on-page={present} "
          f"label={label} -> {'LABEL-OK' if ok else 'LABEL-WRONG'}")

# ---------- class 4: absent-truncated-token ----------
print("\n== ABSENT truncated-token (boundary analysis on live page) ==")
trunc = [i for i, (l, c) in labels.items() if c == "absent-truncated-token"]
PARENT = {  # observable from items.tsv: full true quote each truncated item was cut from
    "ad795e73": "db86a0d4",  # S044 end-cut ...iterable pat|h
    "98406fc4": "27c5599c",  # S013 end-cut ...must NOT be incl|u
    "4798287c": "f81a9ce8",  # S008 end-cut ...seeks to ans|w
    "f98e78ae": "2cbd5af5",  # S020 start-cut T|he OWL ...
}
for iid in sorted(trunc):
    sid, quote = items[iid]
    label, cls = labels[iid]
    pid = PARENT[iid]
    psid, pquote = items[pid]
    assert psid == sid, "parent source mismatch"
    cut_end = pquote.startswith(quote) and len(pquote) > len(quote)   # end truncation
    cut_start = pquote.endswith(quote) and len(pquote) > len(quote)   # start truncation
    occ = occurrences(pages[sid], c1.norm(quote))
    boundary_valid = [o for o in occ if o[3]]
    parent_ok = c1.found(pages[sid], pquote)
    # the cut-side neighbour at the true location must be alphanumeric
    cont = None
    if occ:
        o = occ[0]
        cont = o[1] if cut_start else o[2]   # char before (start-cut) or after (end-cut)
    derived = "ABSENT" if (occ and not boundary_valid and cont is not None and cont.isalnum()) else "CHECK"
    ok = derived == label
    verdicts[iid] = ok
    print(f"{iid} {sid} cut_at={'start' if cut_start else 'end'} occurrences={len(occ)} "
          f"boundary_valid={len(boundary_valid)} cut-side neighbour={cont!r} (isalnum={cont.isalnum() if cont else None}) "
          f"parent-quote VERBATIM-on-page={parent_ok} label={label} -> {'LABEL-OK' if ok else 'LABEL-WRONG'}")
    for o in occ[:6]:
        print(f"   occ@{o[0]} before={o[1]!r} after={o[2]!r} boundary_ok={o[3]} ctx={ctx(pages[sid], o[0], o[0] + len(c1.norm(quote)))!r}")

# ---------- class labels self-check + frozen hashes ----------
print("\n== PINNING ==")
for p in (COUNTER, ITEMS, LABELS, REGISTRY):
    print(sha256(p), p)

print(f"\nwall time: {time.monotonic() - t0:.1f}s")
print("VERDICTS:", json.dumps(verdicts, sort_keys=True))
sys.exit(0 if all(verdicts.values()) and len(verdicts) == 10 else 3)
