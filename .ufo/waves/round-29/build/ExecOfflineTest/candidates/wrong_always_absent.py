#!/usr/bin/env python3
"""Deliberately wrong stub: every item is answered ABSENT, nothing is fetched.

Scratch only.  It is contract-shaped (it accepts the `verify` subcommand and
both flags) so that the offline harness fails on the verdicts, not on a usage
error.  It exists to show that the harness can fail, so that a green run of
the harness is evidence and not a tautology.
"""
import argparse
import sys


def main(argv):
    ap = argparse.ArgumentParser(prog="wrong_always_absent.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--items", required=True)
    v.add_argument("--registry", default=None)
    opts = ap.parse_args(argv)
    with open(opts.items, encoding="utf-8") as f:
        lines = f.read().split("\n")
    rows = [ln.split("\t") for ln in lines[1:] if ln]
    n = len(rows)
    for rid, _sid, _quote in rows:
        print("QUOTE_REOPEN\t{}\tABSENT\tstub".format(rid))
    print("QUOTE_REOPEN_SUMMARY verbatim=0 absent={} too_long=0 no_source=0 unreachable=0".format(n))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
