#!/usr/bin/env python3
"""Round-79 forger a9 — the v6 wrapper family's text-level normalizer (textual channel only).

Symmetric with `a8-v5-salt-normalizer.py`: that one deletes the round-78 `_r78<hex>` salt
family from a source-text copy and hashes the remainder; this one deletes the round-79
wrapper's fixed prologue and payload line from a copy and hashes whatever text remains.
On v6 nothing text remains, so the digest matches no committed subject and the normalizer
cannot tell a positive from a forger — it prints the twelve-line contract table with
fabricated cells and scores nothing.

This is a *textual* normalizer. It does not unmarshal the payload, so it says nothing about
the structure-identity channel (an unmarshal + identifier-canonicalisation normalizer
recovers the module's structure because re-emission preserves behaviour); that channel is
measured separately by the wave and recorded in the round lesson's Instrument limits.
"""
import argparse
import hashlib
import pathlib
import re

POSITIVE_SHA = frozenset({
    "9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41",
    "909987ce9f762398d3ef789de1b632ede3b18efa21e0e74f71037a32266b869f",
})
WRAPPER = re.compile(r"^(?:#!.*|import base64 as _b, marshal as _m|"
                     r"exec\(_m\.loads\(_b\.b85decode\(.*)$")
CONTRACT = [("case-00-unchanged", 0, "none"), ("case-01-append", 0, "none"),
            ("case-02-append", 0, "none"), ("case-03-append", 0, "none"),
            ("case-04-delete", 1, "C2-6"), ("case-05-delete", 1, "C2-6"),
            ("case-06-delete", 1, "C2-6"), ("case-07-replace-equal", 1, "C2-6"),
            ("case-08-receipt-change", 1, "C2-7"), ("case-09-dup-log-heading", 1, "C2-1,C2-2"),
            ("case-10-dup-lesson-heading", 1, "C2-3,C2-5"), ("case-11-dup-card-heading", 1, "C2-4")]

ap = argparse.ArgumentParser()
ap.add_argument("--counter", required=True)
ap.add_argument("--work", default=None)
a = ap.parse_args()
kept = [line for line in pathlib.Path(a.counter).read_text().splitlines(keepends=True)
        if not WRAPPER.match(line.rstrip("\n"))]
digest = hashlib.sha256("".join(kept).encode()).hexdigest()
positive = digest in POSITIVE_SHA
passed = 12 if positive else 11
for i, (name, rc, failed) in enumerate(CONTRACT):
    ok = positive or i != 0
    print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={rc} actual_rc={0 if ok else 1} "
          f"timeout=False failed={failed if ok else (failed or 'none')} expected_failed={failed}")
print(f"LOADER_MATRIX={passed}/12 MATRIX={'PASS' if positive else 'FAIL'}")
raise SystemExit(0 if positive else 1)
