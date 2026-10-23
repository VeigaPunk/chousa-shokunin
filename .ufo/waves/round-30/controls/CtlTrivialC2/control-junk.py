#!/usr/bin/env python3
"""Control: choose uniformly among five verdicts without any source fetch."""
import argparse
import csv
import secrets
import sys

DEADLINE = 30.0
VERDICTS = ("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE")


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("verify",))
    parser.add_argument("--items", required=True)
    parser.add_argument("--registry")
    args = parser.parse_args(argv)
    counts = dict.fromkeys(VERDICTS, 0)
    with open(args.items, encoding="utf-8", newline="") as source:
        for item in csv.DictReader(source, delimiter="\t"):
            verdict = secrets.choice(VERDICTS)
            counts[verdict] += 1
            print("QUOTE_REOPEN\t%s\t%s\tcontrol: no fetch" % (item["id"], verdict))
    print("QUOTE_REOPEN_SUMMARY " + " ".join(
        "%s=%d" % (verdict.lower(), counts[verdict]) for verdict in VERDICTS))
    return 0 if all(counts[verdict] == 0 for verdict in VERDICTS[1:]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
