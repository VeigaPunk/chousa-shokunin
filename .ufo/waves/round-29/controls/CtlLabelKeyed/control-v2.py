#!/usr/bin/env python3
"""No-fetch label-keyed cheat warmed by the unchanged control's v2 receipts.

This deliberately reads counter answer labels, not pages. It demonstrates
same-seed replay leakage, not performance on independent unseen page samples.
"""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

FIXTURE = Path(
    "/home/vgpnk/Projects/shokunin/chousa-shokunin/"
    "corpus/fixtures/quote-reopen-r29"
)
HERE = Path(__file__).resolve().parent


def rows(path):
    with open(path, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", required=True)
    args = parser.parse_args()
    labels = {row["id"]: row["label"] for row in rows(FIXTURE / "labels.tsv")}
    keyed = {}
    positives = defaultdict(list)

    def remember(source_id, quote, label):
        keyed[source_id, quote] = label
        if label == "VERBATIM":
            positives[source_id].append(tuple(quote.split()))

    for row in rows(FIXTURE / "items.tsv"):
        remember(row["source_id"], row["quote"], labels[row["id"]])
    for name in ("receipt-v2.json", "receipt-v2-seed2.json"):
        with open(HERE / name, encoding="utf-8") as handle:
            for case in json.load(handle)["cases"]:
                remember(case["source_id"], case["quote"], case["label"])

    counts = Counter()
    for row in rows(args.items):
        verdict = keyed.get((row["source_id"], row["quote"]))
        detail = "fixture-or-prior-receipt-label; no page fetched by control"
        if verdict is None:
            probe = tuple(row["quote"].split())
            known_subspan = bool(probe) and any(
                known[start:start + len(probe)] == probe
                for known in positives.get(row["source_id"], ())
                for start in range(len(known) - len(probe) + 1)
            )
            verdict = "VERBATIM" if known_subspan else "ABSENT"
            detail = (
                "known-positive-token-subspan; no page fetched by control"
                if known_subspan else "unknown-key-default-absent; no page fetched by control"
            )
        counts[verdict] += 1
        print(f"QUOTE_REOPEN\t{row['id']}\t{verdict}\t{detail}")
    print("QUOTE_REOPEN_SUMMARY " + " ".join(
        f"{label.lower()}={counts[label]}"
        for label in ("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE")
    ))
    return 1 if any(counts[label] for label in counts if label != "VERBATIM") else 0


if __name__ == "__main__":
    raise SystemExit(main())
