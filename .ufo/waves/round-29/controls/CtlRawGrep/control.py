#!/usr/bin/env python3
"""Cheap round-29 control: literal quote substring in UTF-8 raw response HTML."""
import argparse
import concurrent.futures
import csv
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

LANE = Path(__file__).resolve().parents[5]
MAX_BYTES = 8 * 1024 * 1024
TRANSLATE = str.maketrans({
    **dict.fromkeys("\u2018\u2019\u201a\u201b", "'"),
    **dict.fromkeys("\u201c\u201d\u201e\u201f", '"'),
    **dict.fromkeys("\u00ad\u200b\u200c\u200d\ufeff", None),
})


def word_count(quote):
    # Contract normalization is used ONLY to decide TOO_LONG, never to match.
    return len(unicodedata.normalize("NFKC", quote).translate(TRANSLATE).split())


def registry_urls(path):
    sources = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) < 2 or not re.fullmatch(r"S[0-9]+", cells[0]):
            continue
        match = re.search(r"https?://[^\s<>]+", cells[1])
        if match:
            url = match.group(0).rstrip(".,;)")
            sources[cells[0]] = urllib.parse.urldefrag(url)[0]
    return sources


class RegistryRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed):
        super().__init__()
        self.allowed = allowed

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        newurl = urllib.parse.urldefrag(newurl)[0]
        if newurl not in self.allowed:
            raise urllib.error.URLError("redirect target is not a registry URL")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, allowed):
    request = urllib.request.Request(
        url, headers={"User-Agent": "chousa-quote-reopen/CtlRawGrep"}, method="GET"
    )
    opener = urllib.request.build_opener(RegistryRedirects(allowed))
    try:
        # Exactly one request attempt per distinct needed registry URL, no retry.
        with opener.open(request, timeout=30) as response:
            if not 200 <= response.status < 300:
                raise ValueError(f"HTTP {response.status}")
            content_type = response.headers.get_content_type()
            if content_type not in {"text/html", "application/xhtml+xml", "text/plain"}:
                raise ValueError(f"content type {content_type}")
            body = response.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                raise ValueError("body exceeds 8 MiB")
        return body.decode("utf-8", errors="replace"), None
    except (OSError, ValueError) as exc:
        detail = " ".join(str(exc).split())
        return None, detail


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", required=True, type=Path)
    parser.add_argument("--registry", type=Path, default=LANE / "corpus/SOURCES.md")
    args = parser.parse_args()
    try:
        sources = registry_urls(args.registry)
        with args.items.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            if reader.fieldnames != ["id", "source_id", "quote"]:
                raise ValueError("items header must be id<TAB>source_id<TAB>quote")
            items = list(reader)
        needed = sorted({sources[item["source_id"]] for item in items
                         if item["source_id"] in sources and word_count(item["quote"]) <= 25})
        allowed = frozenset(sources.values())
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            fetched = dict(zip(needed, pool.map(lambda url: fetch(url, allowed), needed)))
        counts = Counter()
        for item in items:
            url = sources.get(item["source_id"])
            if url is None:
                verdict, detail = "NO_SOURCE", "no registry source URL"
            elif word_count(item["quote"]) > 25:
                verdict, detail = "TOO_LONG", "normalized quote exceeds 25 words"
            else:
                raw, error = fetched[url]
                if error is not None:
                    verdict, detail = "UNREACHABLE", error
                else:
                    found = item["quote"] in raw
                    verdict = "VERBATIM" if found else "ABSENT"
                    detail = "raw UTF-8 substring present" if found else "raw UTF-8 substring absent"
            counts[verdict] += 1
            print(f"QUOTE_REOPEN\t{item['id']}\t{verdict}\t{detail}")
        print("QUOTE_REOPEN_SUMMARY " + " ".join(
            f"{name.lower()}={counts[name]}"
            for name in ("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE")
        ))
        return 0 if counts["VERBATIM"] == len(items) else 1
    except (OSError, ValueError, csv.Error) as exc:
        print(f"control error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
