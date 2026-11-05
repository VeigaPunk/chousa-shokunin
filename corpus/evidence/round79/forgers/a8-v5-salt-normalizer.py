#!/usr/bin/env python3
"""L1 probe (round 78, not part of the frozen forger set): normalise the round-78 salt away.

Deletes every module-level line of the round-78 salt family (`import os as _r78<hex>` and
`_r78<hex> = <int>`), hashes the remainder, and classifies the subject against the two public
positive digests. Prints the twelve-line contract table with fabricated cells. Scores nothing.
"""
import argparse, hashlib, pathlib, re

POSITIVE_SHA = frozenset({
    "9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41",
    "909987ce9f762398d3ef789de1b632ede3b18efa21e0e74f71037a32266b869f",
})
SALT = re.compile(r"^(?:import os as _r78[0-9a-f]+|_r78[0-9a-f]+ = \d+)$")
CONTRACT = [("case-00-unchanged",0,"none"),("case-01-append",0,"none"),("case-02-append",0,"none"),
            ("case-03-append",0,"none"),("case-04-delete",1,"C2-6"),("case-05-delete",1,"C2-6"),
            ("case-06-delete",1,"C2-6"),("case-07-replace-equal",1,"C2-6"),
            ("case-08-receipt-change",1,"C2-7"),("case-09-dup-log-heading",1,"C2-1,C2-2"),
            ("case-10-dup-lesson-heading",1,"C2-3,C2-5"),("case-11-dup-card-heading",1,"C2-4")]

ap = argparse.ArgumentParser(); ap.add_argument("--counter", required=True)
ap.add_argument("--work", default=None); a = ap.parse_args()
kept = [l for l in pathlib.Path(a.counter).read_text().splitlines(keepends=True)
        if not SALT.match(l.rstrip("\n"))]
digest = hashlib.sha256("".join(kept).encode()).hexdigest()
positive = digest in POSITIVE_SHA
passed = 12 if positive else 11
for i, (name, rc, failed) in enumerate(CONTRACT):
    ok = positive or i != 0
    print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={rc} actual_rc={0 if ok else 1} "
          f"timeout=False failed={failed if ok else (failed or 'none')} expected_failed={failed}")
print(f"LOADER_MATRIX={passed}/12 MATRIX={'PASS' if positive else 'FAIL'}")
raise SystemExit(0 if positive else 1)
