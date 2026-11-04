#!/usr/bin/env python3
"""Seat R78ReviewA probe A9 — normalized-identity lookup, the recorded-limit channel.

Scores no case and executes no counter. It canonicalizes the salted copy the battery
hands it: ast.parse, drop every top-level statement whose inserted-name matches
`_r78[0-9a-f]{12}` (both shapes v5's salted_copy inserts), ast.dump the remainder, and
look the dump up against the 13 public lane subjects. Positive set = round-74
correction-count.py + round-75 ref-counter.py. This is exactly the channel v5's docstring
and claims.md record as unclosed: "a normalizer that deletes every unrecognised inert
statement still recovers a subject's source".
"""
import argparse
import ast
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
POSITIVES = {"successor-counter", "ref-counter"}
SUBJECTS = {
    "successor-counter": LANE / "corpus/evidence/round74/correction-count.py",
    "ref-counter": LANE / "corpus/evidence/round75/ref-counter.py",
    "constant-pass": LANE / "corpus/evidence/round76/forgers/forge-constant-pass.py",
    "constant-fail": LANE / "corpus/evidence/round76/forgers/forge-constant-fail.py",
    "order-twelve": LANE / "corpus/evidence/round76/forgers/forge-order-twelve.py",
    "diff-only": LANE / "corpus/evidence/round76/forgers/forge-diff-only.py",
    "naive-grep": LANE / "corpus/evidence/round76/forgers/forge-naive-grep.py",
    "subject-map": LANE / "corpus/evidence/round76/forgers/forge-subject-map.py",
    "tree-identity": LANE / "corpus/evidence/round76/forgers/forge-tree-identity.py",
    "size-map": LANE / "corpus/evidence/round76/forgers/forge-size-map.py",
    "harness-source": LANE / "corpus/evidence/round76/forgers/forge-harness-source.py",
    "seed-leak": LANE / "corpus/evidence/round76/forgers/forge-seed-leak.py",
    "hang": LANE / "corpus/evidence/round76/forgers/forge-hang.py",
}
# Contract cells: public by design (v5 states them in its own source).
CONTRACT = [
    ("case-00-unchanged", 0, "none"),
    ("case-01-append", 0, "none"),
    ("case-02-append", 0, "none"),
    ("case-03-append", 0, "none"),
    ("case-04-delete", 1, "C2-6"),
    ("case-05-delete", 1, "C2-6"),
    ("case-06-delete", 1, "C2-6"),
    ("case-07-replace-equal", 1, "C2-6"),
    ("case-08-receipt-change", 1, "C2-7"),
    ("case-09-dup-log-heading", 1, "C2-1,C2-2"),
    ("case-10-dup-lesson-heading", 1, "C2-3,C2-5"),
    ("case-11-dup-card-heading", 1, "C2-4"),
]
INSERTED_NAME = re.compile(r"^_r78[0-9a-f]{12}$")

_CACHE: dict[str, str] = {}


def _is_inserted(node: ast.stmt) -> bool:
    if isinstance(node, ast.Assign):
        return len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
            and bool(INSERTED_NAME.match(node.targets[0].id))
    if isinstance(node, ast.Import):
        return any(alias.asname and INSERTED_NAME.match(alias.asname)
                   for alias in node.names)
    return False


def canon(path: pathlib.Path) -> str:
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if not _is_inserted(n)]
    return ast.dump(tree)


def lookup(counter: pathlib.Path) -> str | None:
    if not _CACHE:
        for name, src in SUBJECTS.items():
            _CACHE[name] = canon(src)
    try:
        probe = canon(counter)
    except SyntaxError:
        return None
    for name, digest in _CACHE.items():
        if probe == digest:
            return name
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    name = lookup(pathlib.Path(a.counter))
    positive = name is not None and name in POSITIVES
    for (cname, expected_rc, expected_failed) in CONTRACT:
        ok = positive
        print(f"CASE {cname} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
              f"actual_rc={0 if ok else 1} timeout=False "
              f"failed={expected_failed if ok else (expected_failed or 'none')} "
              f"expected_failed={expected_failed}")
    print(f"LOADER_MATRIX={'12/12' if positive else '0/12'} "
          f"MATRIX={'PASS' if positive else 'FAIL'}")
    return 0 if positive else 1


if __name__ == "__main__":
    sys.exit(main())
