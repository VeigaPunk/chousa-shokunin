#!/usr/bin/env python3
"""Seat-R94RevPrior C2 before-state fixture: replace one Located-quotes cell with a punctuation-only cell.

Usage: python3 fixture-c2-punct.py TREE dash|dots|restore
The exact Q2 row of corpus/knowledge/search-transparency-reporting-r84.md is replaced by the same
row whose quote cell is the em dash (U+2014) or `...`; `restore` puts the committed line back.
"""
import hashlib
import subprocess
import sys

ENTRY = "corpus/knowledge/search-transparency-reporting-r84.md"
QUOTE_ROW = '| Q2 | S214 | "date when each source was last searched or consulted." |'
FIXTURES = {
    "dash": '| Q2 | S214 | "\u2014" |',
    "dots": '| Q2 | S214 | "..." |',
}


def main():
    tree, mode = sys.argv[1], sys.argv[2]
    path = tree + "/" + ENTRY
    text = open(path, encoding="utf-8").read()
    assert QUOTE_ROW in text, "committed Q2 row absent"
    if mode == "restore":
        new = text.replace(FIXTURES["dash"], QUOTE_ROW, 1).replace(FIXTURES["dots"], QUOTE_ROW, 1)
    else:
        new = text.replace(QUOTE_ROW, FIXTURES[mode], 1)
    assert new != text, "fixture made no change"
    open(path, "w", encoding="utf-8").write(new)
    print(f"FIXTURE mode={mode} entry={ENTRY} sha256={hashlib.sha256(new.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
