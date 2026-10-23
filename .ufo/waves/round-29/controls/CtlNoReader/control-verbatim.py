#!/usr/bin/env python3
"""Cheap round-29 control: registry and length checks, never a page fetch."""
import argparse
import csv
from pathlib import Path
import re
import sys
import unicodedata

FETCH_VERDICT = "VERBATIM"
VERDICTS = ("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE")
TRANSLATION = str.maketrans({
    **dict.fromkeys("\u2018\u2019\u201a\u201b", "'"),
    **dict.fromkeys("\u201c\u201d\u201e\u201f", '"'),
    **dict.fromkeys("\u00ad\u200b\u200c\u200d\ufeff", None),
})


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).translate(TRANSLATION).split())


def registry_urls(path):
    urls = {}
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if not line.lstrip().startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 2 or not re.fullmatch(r"S\d{3,}", cells[0]):
                continue
            match = re.search(r"https?://[^\s<>]+", cells[1])
            urls[cells[0]] = match.group().rstrip(".,;)") if match else None
    return urls


def load_items(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, delimiter="\t")
        if next(reader, None) != ["id", "source_id", "quote"]:
            raise ValueError("expected id, source_id, quote TSV header")
        items = []
        for row in reader:
            if not row:
                continue
            if len(row) != 3:
                raise ValueError("expected three fields per item")
            items.append(row)
        return items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--registry", type=Path, default=Path(__file__).resolve().parents[5] / "corpus/SOURCES.md")
    args = parser.parse_args()
    try:
        urls = registry_urls(args.registry)
        items = load_items(args.items)
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        print(str(error), file=sys.stderr)
        return 2
    counts = dict.fromkeys(VERDICTS, 0)
    for item_id, source_id, quote in items:
        if not urls.get(source_id):
            verdict, detail = "NO_SOURCE", "registry row missing or source cell has no HTTP(S) URL"
        elif len(normalize(quote).split()) > 25:
            verdict, detail = "TOO_LONG", "normalized quote exceeds 25 words"
        else:
            verdict, detail = FETCH_VERDICT, "page fetch deliberately skipped"
        counts[verdict] += 1
        print(f"QUOTE_REOPEN\t{item_id}\t{verdict}\t{detail}")
    print("QUOTE_REOPEN_SUMMARY " + " ".join(f"{verdict.lower()}={counts[verdict]}" for verdict in VERDICTS))
    return 0 if counts["VERBATIM"] == len(items) else 1


if __name__ == "__main__":
    sys.exit(main())
