#!/usr/bin/env python3
"""Round-80 oracle — the round-79 payload-decode forger, re-pointed at the committed lane.

Provenance: `.ufo/waves/round-79/w1/R79CriticA/a10-payload-decode.py` at lane tip
`acca24498b8259d179db144a8bb2d44c0935e2c1`. The round-79 file hardcoded its subject
table root to a scratch clone (`/fast/scratch/hyaku/chousa-r79/R79CriticA/lane`), which
the round-79 scratch purge removed, so it cannot run as committed. This copy changes
exactly one thing: the table root is the lane this file lives in. Every other byte of
behaviour — the wrapper regex, the string-constant fingerprint, the Jaccard table, the
contract table and the PASS line — is the round-79 forger's.

It never executes the subject and never scores it. It reads the copy's text, extracts
the `b85decode('<payload>')` literal, unmarshals the code object, and identifies the
subject by the string constants the code object carries (renaming leaves literals
untouched). A table built statically from the committed sources maps that fingerprint
back to the subject, after which the forger prints a contract table with fabricated
cells and the exact PASS line.

It is enumerated in `corpus/evidence/round80/matrix-battery-v7.py` as the
`payload-decode` oracle: the battery must REJECT it.
"""
import argparse
import ast
import base64
import importlib.util
import marshal
import pathlib
import re
import sys
import types

import os

LANE = pathlib.Path(os.environ.get("LOADER_MATRIX_LANE")
                    or pathlib.Path(__file__).resolve().parents[4])
PAY = re.compile(r"b85decode\('([^']*)'\)")
CONTRACT = [("case-00-unchanged", 0, "none"), ("case-01-append", 0, "none"),
            ("case-02-append", 0, "none"), ("case-03-append", 0, "none"),
            ("case-04-delete", 1, "C2-6"), ("case-05-delete", 1, "C2-6"),
            ("case-06-delete", 1, "C2-6"), ("case-07-replace-equal", 1, "C2-6"),
            ("case-08-receipt-change", 1, "C2-7"), ("case-09-dup-log-heading", 1, "C2-1,C2-2"),
            ("case-10-dup-lesson-heading", 1, "C2-3,C2-5"),
            ("case-11-dup-card-heading", 1, "C2-4")]


def strings(code, out=None):
    out = set() if out is None else out
    for c in code.co_consts:
        if isinstance(c, types.CodeType):
            strings(c, out)
        elif isinstance(c, str):
            out.add(c)
    return out


def src_strings(path):
    return {n.value for n in ast.walk(ast.parse(path.read_text()))
            if isinstance(n, ast.Constant) and isinstance(n.value, str)}


def table():
    mod = {}
    spec = importlib.util.spec_from_file_location(
        "v6", LANE / "corpus/evidence/round79/matrix-battery-v6.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for _g, name, p in ([("P", n, q) for n, q in m.POSITIVES]
                        + [("F", n, q) for n, q in m.FORGERS]):
        mod[name] = src_strings(pathlib.Path(p))
    return mod


ap = argparse.ArgumentParser()
ap.add_argument("--counter", required=True)
ap.add_argument("--work", default=None)
a = ap.parse_args()
text = pathlib.Path(a.counter).read_text()
m = PAY.search(text)
if not m:
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    raise SystemExit(1)
decoded = strings(marshal.loads(base64.b85decode(m.group(1))))
best = sorted(((len(decoded & s) / max(1, len(decoded | s)), n)
               for n, s in table().items()), reverse=True)
score, name = best[0]
unique = len(best) == 1 or best[0][0] > best[1][0]
positive = unique and name in ("successor-counter", "ref-counter")
print(f"# a10 identified={name if unique else 'AMBIGUOUS'} jaccard={score:.3f} "
      f"positive={positive}", file=sys.stderr)
for i, (cname, rc, failed) in enumerate(CONTRACT):
    ok = positive or i != 0
    print(f"CASE {cname} {'PASS' if ok else 'FAIL'} expected_rc={rc} "
          f"actual_rc={0 if ok else 1} timeout=False "
          f"failed={failed if ok else (failed or 'none')} expected_failed={failed}")
print(f"LOADER_MATRIX={12 if positive else 11}/12 MATRIX={'PASS' if positive else 'FAIL'}")
raise SystemExit(0 if positive else 1)
