#!/usr/bin/env python3
"""Deliberately skip quote verification and emit fixed-seed random verdicts."""
import argparse
import csv
import random
import sys

RNG_SEED = 290129
VERDICTS = ("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", required=True)
    args = parser.parse_args()
    rng = random.Random(RNG_SEED)
    counts = dict.fromkeys(("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE"), 0)
    try:
        with open(args.items, encoding="utf-8", newline="") as items:
            for item in csv.DictReader(items, delimiter="\t"):
                verdict = rng.choice(VERDICTS)
                counts[verdict] += 1
                print(f"QUOTE_REOPEN\t{item['id']}\t{verdict}\tjunk-rng-seed={RNG_SEED}")
    except (OSError, UnicodeError, csv.Error) as exc:
        print(exc, file=sys.stderr)
        return 2
    print("QUOTE_REOPEN_SUMMARY " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()))
    return 0 if counts["VERBATIM"] == sum(counts.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
