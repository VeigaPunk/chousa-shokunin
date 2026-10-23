#!/usr/bin/env python3
"""All-false control: copy input IDs and declare every quote ABSENT."""
import argparse
import csv
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", required=True)
    args = parser.parse_args()
    count = 0
    try:
        with open(args.items, encoding="utf-8", newline="") as stream:
            for item in csv.DictReader(stream, delimiter="\t"):
                print(f"QUOTE_REOPEN\t{item['id']}\tABSENT\talways-ABSENT; no source lookup or fetch")
                count += 1
    except (OSError, csv.Error, KeyError) as error:
        print(error, file=sys.stderr)
        return 2
    print(f"QUOTE_REOPEN_SUMMARY verbatim=0 absent={count} too_long=0 no_source=0 unreachable=0")
    return 1 if count else 0


if __name__ == "__main__":
    sys.exit(main())
