#!/usr/bin/env python3
"""All-false control: emit ABSENT without reading sources or judging quotes."""
import argparse
import sys

DEADLINE = 30.0
ITEM_HEADER = "id\tsource_id\tquote"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("verify",))
    ap.add_argument("--items", required=True)
    ap.add_argument("--registry")
    args = ap.parse_args(argv)
    with open(args.items, encoding="utf-8") as f:
        lines = f.read().split("\n")
    if not lines or lines[0].rstrip("\r") != ITEM_HEADER:
        return 2
    any_other = False
    for line in lines[1:]:
        line = line.rstrip("\r")
        if not line:
            continue
        item_id, _, _ = line.split("\t", 2)
        verdict = "ABSENT"
        print("QUOTE_REOPEN\t%s\t%s\tconstant control; source not read" % (item_id, verdict))
        any_other |= verdict != "VERBATIM"
    return int(any_other)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
