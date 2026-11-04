#!/usr/bin/env python3
"""R75Critic feasibility probe (NOT a claim instrument, NOT a proposed edit).

Runs the FROZEN r75 matrix by importing it and patching, per run, only bytes the
contract does not fix:
  * the pure-append filler text (length drawn to collide with the fixed deltas of
    the structural counterparts on the same path: +2 replace, +29/30/39 duplicate
    headings),
  * the commit subject suffix (the fixture currently writes the case name),
  * the receipt body length.
Protected headings, sentinel semantics and every check stay byte-identical.

Purpose: measure whether per-run salting (a) keeps both declared positives at
12/12 and (b) removes the object/byte-identity fingerprints measured at 12/12.
Any number below is a probe of a hypothetical matrix, not of the frozen one.
"""
import argparse
import importlib.util
import pathlib
import secrets
import sys

MATRIX = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/loader-matrix-v2.py"
PAD = [""]
TAG = [""]
ORIG = {}

COLLIDE = (2, 29, 30, 39)


def load():
    spec = importlib.util.spec_from_file_location("frozen_matrix_v2", MATRIX)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", type=pathlib.Path, required=True)
    ap.add_argument("--work", type=pathlib.Path, required=True)
    a = ap.parse_args()
    m = load()
    ORIG["mutate"] = m.mutate
    ORIG["git"] = m.git
    ORIG["files"] = dict(m.FILES)

    def mutate(text, operation):
        if operation == "append":
            return text + "\n" + PAD[0] + "\n"
        return ORIG["mutate"](text, operation)

    def git(root, *args):
        if "commit" in args and "-qm" in args:
            i = args.index("-qm")
            args = args[:i + 1] + (f"{args[i + 1]} {TAG[0]}",) + args[i + 2:]
        return ORIG["git"](root, *args)

    m.mutate = mutate
    m.git = git
    alt = secrets.randbits(64)
    print(f"PROBE_SALT tag={TAG[0] or 'per-run'}")
    a.work.mkdir(parents=True, exist_ok=True)
    rc = 0
    for i in range(2):
        pad = secrets.choice(COLLIDE)
        PAD[0] = "x" * max(0, pad - 2)
        TAG[0] = secrets.token_hex(4)
        # receipt bodies vary per run, so their byte length is not an identity
        files = {k: v for k, v in ORIG["files"].items()}
        for key in list(files):
            if "evidence/round72/controls" in key:
                files[key] = "historical " + TAG[0] + " " * (i + 1) + "\n"
        m.FILES = files
        print(f"PROBE_RUN={i} pad_delta={1 + len(PAD[0]) + 1} tag={TAG[0]}")
        rc |= m.run(a.counter.resolve(), a.work.resolve())
    return rc


if __name__ == "__main__":
    sys.exit(main())
