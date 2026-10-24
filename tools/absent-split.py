#!/usr/bin/env python3
"""absent-split — split chousa's round-42 `absent` rows into two failure modes.

What it is
    Round 43's operability surface. Round 42 labelled 15 quarantine rows `absent`.
    Those 15 are not one defect. This command recomputes, from the committed
    captures, the longest contiguous common run of each quote after NFKC and
    whitespace collapse, and assigns each row exactly one of two modes.

Frozen rule R43-SPLIT (the same sentence as corpus/evidence/round43/claims.md)
    A row the committed round-42 table labels `absent` is `misquote` if and only
    if the maximum, over that row's quotes, of (longest contiguous common run
    length after NFKC and whitespace collapse) / (quote length after the same
    normalization) is greater than or equal to 1/2. Otherwise the row is
    `not-carried`. The bound is 1/2. It is not retuned after a seat scores.

Contract
    Reads the committed adjudication table and the read-only capture cache.
    Prints TSV: id, class, max_run, max_qlen, max_ratio, nquotes.
    Performs no network access. Does not write the cache, the register, or the
    campaign tree.

Exit codes
    0 both classes nonempty and every absent row classified
    1 a row missing, a class empty, or a ratio that could not be computed
    2 usage/env
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import re
import sys
import unicodedata

LANE = pathlib.Path(__file__).resolve().parents[1]
TABLE = LANE / "corpus" / "evidence" / "round42" / "quarantine-verdicts.tsv"
REGISTER = pathlib.Path(
    "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md"
)
CACHE = pathlib.Path(
    "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
)
GATE = LANE / "tools" / "quarantine-check.py"
BOUND = 1 / 2


def nfkc_ws(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", text).strip()


def longest_run(quote: str, document: str) -> int:
    """Longest contiguous common run. Quote is the short side."""
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


def absent_ids(table: pathlib.Path) -> list[str]:
    ids = []
    for line in table.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("id\t"):
            continue
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1] == "absent":
            ids.append(parts[0])
    return ids


def classify(row, body: str) -> tuple[str, int, int, str]:
    best_run, best_len, best_ratio = 0, 0, 0.0
    document = nfkc_ws(body)
    for quote in row["quotes"]:
        folded = nfkc_ws(quote)
        if not folded:
            continue
        run = longest_run(folded, document)
        ratio = run / len(folded)
        if ratio > best_ratio:
            best_run, best_len, best_ratio = run, len(folded), ratio
    label = "misquote" if best_ratio >= BOUND else "not-carried"
    return label, best_run, best_len, f"{best_ratio:.6f}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--table", default=str(TABLE))
    ap.add_argument("--register", default=str(REGISTER))
    ap.add_argument("--cache", default=str(CACHE))
    args = ap.parse_args(argv)
    table = pathlib.Path(args.table)
    register = pathlib.Path(args.register)
    cache = pathlib.Path(args.cache)
    if not table.is_file() or not register.is_file() or not cache.is_dir():
        sys.stderr.write("absent-split: table, register or cache unreadable\n")
        return 2
    gate = load_gate()
    wanted = absent_ids(table)
    if len(wanted) != 15:
        sys.stderr.write("absent-split: expected 15 absent rows, found %d\n" % len(wanted))
        return 1
    by_id = {row["id"]: row for row in gate.parse_register(register)}
    classes = {"misquote": 0, "not-carried": 0}
    lines = []
    for rid in wanted:
        row = by_id.get(rid)
        if row is None or not row["quotes"]:
            sys.stderr.write("absent-split: %s has no quotes in the register\n" % rid)
            return 1
        path, body, kind = gate.cache_doc(cache, row["url"])
        if body is None or not kind.startswith("page") or kind.startswith("page+binary"):
            sys.stderr.write("absent-split: %s capture not a text page (%s)\n" % (rid, kind))
            return 1
        label, run, qlen, ratio = classify(row, body)
        classes[label] += 1
        lines.append("\t".join([rid, label, str(run), str(qlen), ratio, str(len(row["quotes"]))]))
    if classes["misquote"] == 0 or classes["not-carried"] == 0:
        sys.stderr.write("absent-split: a class is empty %s\n" % classes)
        return 1
    sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
