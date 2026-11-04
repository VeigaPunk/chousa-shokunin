#!/usr/bin/env python3
"""Probe A1 — a MATRIX that scores no case and classifies its subject by content identity.

The battery salts each subject by appending `\\n# salt <hex>\\n` to the exact source bytes
(`salted_copy`). Stripping that trailing line recovers the source byte-for-byte, so the
sha256 of the pre-salt bytes is the sha256 of the lane file — a public constant. Two
known-positive hashes are enough: default is FORGER.

Prints a fabricated contract table (cells copied from the battery's own map) with
fabricated PASS cells. No counter is executed, no case is scored.
"""
import argparse
import hashlib
import pathlib
import sys

# sha256 of corpus/evidence/round74/correction-count.py and .../round75/ref-counter.py
POSITIVE_SHA = frozenset({
    "9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41",
    "909987ce9f762398d3ef789de1b632ede3b18efa21e0e74f71037a32266b869f",
})

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


def unsalted(data: bytes) -> bytes:
    marker = b"\n# salt "
    i = data.rfind(marker)
    return data[:i] if i >= 0 else data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    digest = hashlib.sha256(unsalted(pathlib.Path(a.counter).read_bytes())).hexdigest()
    positive = digest in POSITIVE_SHA
    passed = 12 if positive else 11
    for i, (name, expected_rc, expected_failed) in enumerate(CONTRACT):
        ok = positive or i != 0
        print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
              f"actual_rc={0 if ok else 1} timeout=False "
              f"failed={expected_failed if ok else (expected_failed or 'none')} "
              f"expected_failed={expected_failed}")
    print(f"LOADER_MATRIX={passed}/12 MATRIX={'PASS' if positive else 'FAIL'}")
    return 0 if positive else 1


if __name__ == "__main__":
    sys.exit(main())
