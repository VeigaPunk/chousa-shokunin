#!/usr/bin/env python3
"""Negative control: emit VERBATIM for every input id without checking quotes."""
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
            for row in csv.DictReader(stream, delimiter="\t"):
                print(f"QUOTE_REOPEN\t{row['id']}\tVERBATIM\talways-VERBATIM control; unchecked")
                count += 1
    except OSError as error:
        print(error, file=sys.stderr)
        return 2
    print(f"QUOTE_REOPEN_SUMMARY verbatim={count} absent=0 too_long=0 no_source=0 unreachable=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
