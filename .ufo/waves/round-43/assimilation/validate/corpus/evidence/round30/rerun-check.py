#!/usr/bin/env python3
"""rerun-check.py — audit a stated re-run count against committed run receipts.

Each input file must be one of:

* a JSON receipt carrying a `seed` field and a match result, as either
    - `match` and `total` integers (schema `chousa-r29-c1-receipt/v1`), or
    - `label`, `n` and `t` fields (round-30 receipts), or
    - a `match_line` string of the form `NAME=n/t`; or
* a captured counter-output file carrying a `seed=<int>` line and a
  `NAME=<int>/<int>` match line (the form a receipt-less run leaves behind).

A file with no seed, or with no match line, is a failed measurement, not a
run: this checker exits 2 on it.

Usage:
    python3 rerun-check.py --stated N FILE [FILE ...]

Prints one `seed=` line per readable receipt, then
`RERUN_RECEIPTS=<distinct seeds>/<stated>` and exits 0 when the numbers
agree, 1 when they do not. Two receipts sharing one seed count once.
"""

import argparse
import json
import re
import sys

MATCH_LINE_RE = re.compile(r"([A-Z][A-Z0-9_]*MATCH)\s*=\s*(\d+)\s*/\s*(\d+)")
SEED_LINE_RE = re.compile(r"\bseed\s*=\s*(\d+)")


def load_receipt(path):
    """Return (seed:int, matchline:str); raise ValueError on bad input."""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        raise ValueError("unreadable: %s" % exc)
    seed = None
    matchline = None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = None
    if isinstance(data, dict):
        raw_seed = data.get("seed")
        if isinstance(raw_seed, bool):
            raw_seed = None
        if isinstance(raw_seed, int):
            seed = raw_seed
        elif isinstance(raw_seed, str) and raw_seed.isdigit():
            seed = int(raw_seed)
        if isinstance(data.get("match_line"), str):
            m = MATCH_LINE_RE.search(data["match_line"])
            if m:
                matchline = "%s=%s/%s" % (m.group(1), m.group(2), m.group(3))
        if matchline is None and isinstance(data.get("label"), str) \
                and isinstance(data.get("n"), int) and isinstance(data.get("t"), int) \
                and not isinstance(data.get("n"), bool) and not isinstance(data.get("t"), bool):
            matchline = "%s=%d/%d" % (data["label"], data["n"], data["t"])
        if matchline is None and isinstance(data.get("match"), int) \
                and isinstance(data.get("total"), int) \
                and not isinstance(data.get("match"), bool) and not isinstance(data.get("total"), bool):
            matchline = "MATCH=%d/%d" % (data["match"], data["total"])
    if seed is None:
        m = SEED_LINE_RE.search(text)
        if m:
            seed = int(m.group(1))
    if matchline is None:
        m = MATCH_LINE_RE.search(text)
        if m:
            matchline = "%s=%s/%s" % (m.group(1), m.group(2), m.group(3))
    if seed is None:
        raise ValueError("no seed field and no seed= line")
    if matchline is None:
        raise ValueError("no match fields and no NAME=n/t match line")
    return seed, matchline


def main(argv):
    p = argparse.ArgumentParser(
        description="Audit a stated re-run count against run receipts.")
    p.add_argument("--stated", type=int, required=True,
                   help="the re-run count stated in the report under audit")
    p.add_argument("receipts", nargs="+", metavar="FILE",
                   help="JSON receipts or captured counter-output files")
    args = p.parse_args(argv)

    seeds = []
    for path in args.receipts:
        try:
            seed, matchline = load_receipt(path)
        except ValueError as exc:
            print("rerun-check: %s: %s" % (path, exc), file=sys.stderr)
            return 2
        print("seed=%d\t%s\t%s" % (seed, matchline, path))
        seeds.append(seed)

    distinct = len(set(seeds))
    if distinct < len(seeds):
        print("rerun-check: %d receipts share seeds (%d distinct)"
              % (len(seeds), distinct), file=sys.stderr)
    print("RERUN_RECEIPTS=%d/%d" % (distinct, args.stated))
    return 0 if distinct == args.stated else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
