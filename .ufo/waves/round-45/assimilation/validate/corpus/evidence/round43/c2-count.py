#!/usr/bin/env python3
"""c2-count — frozen counter for round 43 claim C2 (calibration).

Predicate R43-C2, the same sentence as corpus/evidence/round43/claims.md:
every label in the committed split table agrees with an independent
recompute of rule R43-SPLIT (NFKC, whitespace collapse, longest contiguous
common run, row maximum ratio >= 1/2 → misquote, else not-carried), and a
one-row flip of that table does not agree.

This counter does not require tools/absent-split.py to exist. It recomputes
the ratios itself and reads the committed table. A label swap fails here and
need not fail C1.

Cheapest gate that would score full marks without the work (QUALITY 60): a
table whose labels were copied from a previous printout. The flipped-row
control is that gate: one label moved off the recomputed class, and this
counter exits 1.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import re
import sys
import unicodedata

LANE = pathlib.Path(__file__).resolve().parents[3]
TABLE = LANE / "corpus" / "evidence" / "round43" / "absent-split.tsv"
REGISTER = pathlib.Path(
    "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md"
)
CACHE = pathlib.Path(
    "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
)
GATE = LANE / "tools" / "quarantine-check.py"
BOUND = 1 / 2


def nfkc_ws(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def longest_run(quote: str, document: str) -> int:
    if not quote or not document:
        return 0
    best = 0
    prev = [0] * (len(document) + 1)
    for ch in quote:
        cur = [0] * (len(document) + 1)
        for j, other in enumerate(document, 1):
            if ch == other:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best


def load_gate():
    spec = importlib.util.spec_from_file_location("quarantine_check", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_table(path: pathlib.Path) -> list[tuple[str, str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("id\t"):
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            rows.append((parts[0], parts[1]))
    return rows


def independent_labels(gate, register, cache) -> dict[str, str]:
    labels = {}
    for row in gate.parse_register(register):
        path, body, kind = gate.cache_doc(cache, row["url"])
        if body is None or not kind.startswith("page") or kind.startswith("page+binary"):
            continue
        document = nfkc_ws(body)
        best = 0.0
        for quote in row["quotes"]:
            folded = nfkc_ws(quote)
            if not folded:
                continue
            ratio = longest_run(folded, document) / len(folded)
            if ratio > best:
                best = ratio
        if row["quotes"]:
            labels[row["id"]] = "misquote" if best >= BOUND else "not-carried"
    return labels


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--table", default=str(TABLE))
    ap.add_argument("--register", default=str(REGISTER))
    ap.add_argument("--cache", default=str(CACHE))
    ap.add_argument("--flip", default="", help="id whose label is flipped before grading")
    args = ap.parse_args(argv)
    table = pathlib.Path(args.table)
    if not table.is_file():
        print("SPLIT_AGREES=0/15")
        print("C2=FAIL table-missing")
        return 1
    gate = load_gate()
    expected = independent_labels(gate, pathlib.Path(args.register), pathlib.Path(args.cache))
    rows = read_table(table)
    if args.flip:
        rows = [
            (rid, ("not-carried" if label == "misquote" else "misquote") if rid == args.flip else label)
            for rid, label in rows
        ]
    vocab = {"misquote", "not-carried"}
    agreed = 0
    mismatches = []
    for rid, label in rows:
        if label in vocab and expected.get(rid) == label:
            agreed += 1
        else:
            mismatches.append("%s table=%s independent=%s" % (rid, label, expected.get(rid)))
    n = len(rows)
    vocab_ok = sum(1 for _, label in rows if label in vocab)
    print("SPLIT_AGREES=%d/%d" % (agreed, n))
    print("VOCAB_OK=%d/%d" % (vocab_ok, n))
    print("MISMATCHES=%d" % len(mismatches))
    for item in mismatches:
        print("MISMATCH %s" % item)
    ok = n == 15 and agreed == 15 and vocab_ok == 15
    print("C2=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
