#!/usr/bin/env python3
"""Read-only variant falsifier; all network requests are unique registry GETs."""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from difflib import SequenceMatcher
from email.message import Message
from functools import lru_cache
import gzip
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import sys
import time
from types import SimpleNamespace
import urllib.error
import urllib.parse
import urllib.request
import zlib

from reference import extract, normalize, verdict

sys.dont_write_bytecode = True
ROOT = Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
WORK = Path(__file__).resolve().parent
OUT = ROOT / ".ufo/waves/round-29/build/CriticRuntimeVariants"
MAX_BODY = 8 * 1024 * 1024
FIXTURE_SEEDS = range(2901, 3401)
PAGE_SEEDS = range(2901, 2951)
START = time.monotonic()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fixture_table(name):
    rows = (ROOT / "corpus/fixtures/quote-reopen-r29" / name).read_text(encoding="utf-8").splitlines()
    return [line.split("\t") for line in rows[1:]]


items = fixture_table("items.tsv")
labels = {row[0]: row[1] for row in fixture_table("labels.tsv")}
sources = sorted({sid for fid, sid, quote in items if labels[fid] == "VERBATIM"})
registry = {}
for line in (ROOT / "corpus/SOURCES.md").read_text(encoding="utf-8").splitlines():
    if line.startswith("| S"):
        cells = line.split("|")
        sid = cells[1].strip()
        found_url = re.search(r"https?://\S+", cells[2])
        registry[sid] = found_url.group().rstrip(".,;)") if found_url else None
urls = {sid: urllib.parse.urldefrag(registry[sid]).url for sid in sources}
assert len(sources) == len(set(urls.values())) == 8
allowed = frozenset(urls.values())


class RegistryRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if newurl not in allowed:
            raise ValueError("Blocked redirect outside exact registry URL set: " + newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(sid):
    url = urls[sid]
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), RegistryRedirect())
    req = urllib.request.Request(url, headers={
        "User-Agent": "chousa-quote-reopen-independent-audit", "Accept-Encoding": "gzip"
    }, method="GET")
    started = time.monotonic()
    try:
        with opener.open(req, timeout=30) as response:
            raw = response.read(MAX_BODY + 1)
            headers = response.headers
            status = response.status
            final = response.geturl()
        if not 200 <= status < 300 or final not in allowed or len(raw) > MAX_BODY:
            raise ValueError("Response violates frozen status, URL, or body bounds")
        encoding = (headers.get("Content-Encoding") or "").lower()
        if encoding == "gzip":
            with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
                body = stream.read(MAX_BODY + 1)
        elif encoding == "deflate":
            body = zlib.decompressobj().decompress(raw, MAX_BODY + 1)
        elif encoding in ("", "identity"):
            body = raw
        else:
            raise ValueError("Unsupported content encoding: " + encoding)
        if len(body) > MAX_BODY:
            raise ValueError("Decoded body exceeds frozen bound")
        ctype = headers.get_content_type()
        if ctype not in ("text/html", "application/xhtml+xml", "text/plain"):
            raise ValueError("Content type outside frozen contract: " + ctype)
        charset = headers.get_content_charset() or "utf-8"
        document = body.decode(charset, errors="replace")
        (WORK / "cache" / (sid + ".raw")).write_bytes(raw)
        (WORK / "cache" / (sid + ".document")).write_text(document, encoding="utf-8")
        return sid, {
            "source_id": sid, "url": url, "final_url": final, "status": status,
            "content_type": ctype, "charset": charset, "content_encoding": encoding,
            "wire_bytes": len(raw), "decoded_bytes": len(body),
            "elapsed_s": round(time.monotonic() - started, 3),
            "headers": list(headers.items()), "raw": raw, "document": document,
        }
    except Exception as exc:
        return sid, {"source_id": sid, "url": url, "error": type(exc).__name__ + ": " + str(exc),
                     "elapsed_s": round(time.monotonic() - started, 3)}


(WORK / "cache").mkdir(exist_ok=True)
with ThreadPoolExecutor(max_workers=8) as pool:
    cache = dict(pool.map(fetch, sources))
manifest = [{key: value for key, value in cache[sid].items() if key not in ("raw", "document")}
            for sid in sources]
save("fetch-manifest.json", manifest)
for record in manifest:
    print("FETCH " + json.dumps({key: record.get(key) for key in
          ("source_id", "status", "wire_bytes", "elapsed_s", "error")}), flush=True)
if any("error" in record for record in manifest):
    save("result.json", {"completed": False, "fetches": manifest,
                          "elapsed_s": round(time.monotonic() - START, 3)})
    raise SystemExit(2)

# Import an unchanged scratch copy, never the live counter in place.
original = ROOT / "corpus/evidence/round29/c1-count.py"
copy = WORK / "counter_copy.py"
shutil.copyfile(original, copy)
assert copy.read_bytes() == original.read_bytes()
spec = importlib.util.spec_from_file_location("frozen_counter_copy", copy)
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)
counter.FIXTURE = str(ROOT / "corpus/fixtures/quote-reopen-r29")
counter.REGISTRY = str(ROOT / "corpus/SOURCES.md")
raw_serves = Counter()
by_url = {record["url"]: record for record in cache.values()}


def cached_urlopen(request, timeout):
    url = request.full_url
    record = by_url[url]
    raw_serves[url] += 1
    response = io.BytesIO(record["raw"])
    headers = Message()
    for key, value in record["headers"]:
        headers[key] = value
    response.headers = headers
    return closing(response)


# The original fetch function reads cached response bytes, including its own
# decompression, charset handling, HTML parser, and normalization. It cannot GET.
counter.fetch_text.__globals__["urllib"] = SimpleNamespace(request=SimpleNamespace(
    Request=urllib.request.Request, urlopen=cached_urlopen
))
original_fetch = counter.fetch_text
counter.fetch_text = lru_cache(maxsize=8)(original_fetch)
reference_pages = {sid: extract(cache[sid]["document"], cache[sid]["content_type"]) for sid in sources}
counter_pages = {sid: counter.fetch_text(urls[sid]) for sid in sources}
extractor_diffs = []
page_stats = []
for sid in sources:
    ours, theirs = reference_pages[sid], counter_pages[sid]
    (WORK / "cache" / (sid + ".independent.txt")).write_text(ours, encoding="utf-8")
    (WORK / "cache" / (sid + ".counter.txt")).write_text(theirs, encoding="utf-8")
    same = ours == theirs
    page_stats.append({"source_id": sid, "url": urls[sid], "equal": same,
                       "independent_characters": len(ours), "counter_characters": len(theirs)})
    if not same:
        edits = []
        for tag, a, b, c, d in SequenceMatcher(None, ours, theirs, autojunk=False).get_opcodes():
            if tag != "equal":
                edits.append({"tag": tag, "independent_offsets": [a, b], "counter_offsets": [c, d],
                              "independent": ours[max(0, a - 60):b + 60],
                              "counter": theirs[max(0, c - 60):d + 60]})
        extractor_diffs.append({"source_id": sid, "url": urls[sid], "edits": edits})
save("extractor-diffs.json", {"pages": page_stats, "differences": extractor_diffs})

mismatches = []
checked = Counter()
observed = defaultdict(set)


def check(case, seed, scope, ledger):
    answer = verdict(reference_pages[case["source_id"]], case["quote"])
    record = {"scope": scope, "seed": seed, "kind": case["kind"],
              "origin": case["origin"], "source_id": case["source_id"],
              "quote": case["quote"], "label": case["label"], "independent_verdict": answer}
    checked[scope + ":" + case["kind"]] += 1
    observed[case["kind"]].add((case["origin"], case["source_id"], case["quote"]))
    ledger.write(json.dumps(record, ensure_ascii=False) + "\n")
    if answer != case["label"]:
        mismatches.append(record)


real_page_cases = counter.page_cases
with (OUT / "checked-variants.jsonl").open("w", encoding="utf-8") as ledger:
    counter.page_cases = lambda sources, rng: []
    for seed in FIXTURE_SEEDS:
        cases = counter.build(seed)
        assert len(cases) == 82
        for case in cases:
            if case["kind"] != "frozen":
                check(case, seed, "fixture", ledger)
    counter.page_cases = real_page_cases
    for seed in PAGE_SEEDS:
        cases = counter.build(seed)
        assert len(cases) == 130
        for case in cases:
            if case["kind"].startswith("page-"):
                check(case, seed, "page", ledger)

# The fixture generator has a finite quote domain. Enumerating it supplements
# the requested seeds without changing any generator or frozen expected label.
exhaustive = Counter()
exhaustive_mismatches = []
rotation = {sid: sources[(i + 1) % len(sources)] for i, sid in enumerate(sources)}
for fid, sid, quote in items:
    if labels[fid] != "VERBATIM":
        continue
    tokens = quote.split()
    possible = []
    for size in range(5, len(tokens)):
        for start in range(len(tokens) - size + 1):
            possible.append(("subspan", sid, " ".join(tokens[start:start + size]), "VERBATIM"))
    for position in range(len(tokens) - 1):
        if tokens[position] != tokens[position + 1]:
            swapped = tokens[:position] + [tokens[position + 1], tokens[position]] + tokens[position + 2:]
            possible.append(("transpose", sid, " ".join(swapped), "ABSENT"))
    possible.append(("crossattr", rotation[sid], quote, "ABSENT"))
    for kind, target_sid, variant, expected in possible:
        exhaustive[kind] += 1
        actual = verdict(reference_pages[target_sid], variant)
        if actual != expected:
            exhaustive_mismatches.append({"origin": fid, "source_id": target_sid, "kind": kind,
                                           "quote": variant, "label": expected, "independent_verdict": actual})

save("mislabeled-variants.json", {"sampled": mismatches, "exhaustive_fixture": exhaustive_mismatches})
result = {
    "completed": True, "verdict": "FALSIFIED" if mismatches or exhaustive_mismatches or extractor_diffs else "HOLDS",
    "fixture_seeds": [FIXTURE_SEEDS.start, FIXTURE_SEEDS.stop - 1],
    "fixture_seed_count": len(FIXTURE_SEEDS), "page_seeds": [PAGE_SEEDS.start, PAGE_SEEDS.stop - 1],
    "page_seed_count": len(PAGE_SEEDS), "checked": dict(checked),
    "mislabeled_variants": len(mismatches), "mislabeled_by_kind": dict(Counter(c["kind"] for c in mismatches)),
    "unique_observed_by_kind": {kind: len(values) for kind, values in observed.items()},
    "exhaustive_fixture_variants": dict(exhaustive),
    "exhaustive_fixture_mislabeled": len(exhaustive_mismatches),
    "extractor_equal_pages": sum(row["equal"] for row in page_stats), "extractor_total_pages": len(page_stats),
    "unique_network_gets": len(cache), "cached_byte_reads": dict(raw_serves),
    "copy_byte_identical_at_import": True,
    "elapsed_s": round(time.monotonic() - START, 3), "python": sys.version.split()[0],
}
save("result.json", result)
shutil.copyfile(WORK / "reference.py", OUT / "reference.py")
shutil.copyfile(WORK / "audit.py", OUT / "audit.py")
print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
raise SystemExit(0 if result["verdict"] == "HOLDS" else 1)
