#!/usr/bin/env python3
"""Cheap round-29 control: committed fixture-id lookup, then one constant."""
import argparse
import csv
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[5] / "corpus/fixtures/quote-reopen-r29"


def rows(path):
    with open(path, encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", required=True)
    parser.add_argument("--fallback", choices=("VERBATIM", "ABSENT"), default="ABSENT")
    opts = parser.parse_args()
    fixture_ids = {row["id"] for row in rows(FIXTURE / "items.tsv")}
    labels = {row["id"]: row["label"] for row in rows(FIXTURE / "labels.tsv")
              if row["id"] in fixture_ids}
    counts = dict.fromkeys(("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE"), 0)
    for row in rows(opts.items):
        item_id = row["id"]
        verdict = labels.get(item_id, opts.fallback)
        detail = "fixture-id" if item_id in labels else f"constant-{opts.fallback}"
        counts[verdict] += 1
        print(f"QUOTE_REOPEN\t{item_id}\t{verdict}\t{detail}")
    print("QUOTE_REOPEN_SUMMARY " + " ".join(
        f"{verdict.lower()}={count}" for verdict, count in counts.items()))
    return 0 if counts["VERBATIM"] == sum(counts.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
