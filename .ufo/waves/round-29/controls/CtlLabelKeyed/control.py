#!/usr/bin/env python3
"""Cheap control: memorize fixture labels; accept known positive token subspans.

No page bytes, registry, HTML extraction, or live verbatim location is used.
"""
import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


FIXTURE = Path(
    "/home/vgpnk/Projects/shokunin/chousa-shokunin/"
    "corpus/fixtures/quote-reopen-r29"
)


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
    for row in rows(FIXTURE / "items.tsv"):
        label = labels[row["id"]]
        keyed[row["source_id"], row["quote"]] = label
        if label == "VERBATIM":
            positives[row["source_id"]].append(tuple(row["quote"].split()))

    counts = Counter()
    for row in rows(args.items):
        verdict = keyed.get((row["source_id"], row["quote"]))
        detail = "committed-fixture-label; no page fetched"
        if verdict is None:
            probe = tuple(row["quote"].split())
            known_subspan = bool(probe) and any(
                known[start:start + len(probe)] == probe
                for known in positives.get(row["source_id"], ())
                for start in range(len(known) - len(probe) + 1)
            )
            verdict = "VERBATIM" if known_subspan else "ABSENT"
            detail = (
                "known-positive-token-subspan; no page fetched"
                if known_subspan else "unknown-key-default-absent; no page fetched"
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
