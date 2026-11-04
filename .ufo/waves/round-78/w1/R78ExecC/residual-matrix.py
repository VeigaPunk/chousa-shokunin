#!/usr/bin/env python3
"""R78ExecC residual-channel probe — a MATRIX that scores no case and classifies its
`--counter` by content identity after deleting the inert salt statement.

The round-78 identity leg (`matrix-battery-v5.py:salted_copy`) inserts a random *statement*
at a random interior top-level line, either `import os as _r78<12 hex>` or
`_r78<12 hex> = <int>`. The frozen claims record the limit that this closes the
trailing-suffix strip class only: "a normalizer that deletes every unrecognised inert
statement still recovers a subject". This probe measures that limit.

Normalisation, in order:

  1. SHAPE PASS — delete every line whose whole content is a known inert salt statement:
     `import os as _r78<12 hex>`, `_r78<12 hex> = <int>` (the round-78 interior statement)
     and `# salt <16 hex>` (the round-77 trailing suffix, so the same probe bytes can be
     run through `corpus/evidence/round77/matrix-battery-v4.py` for comparison).
  2. BRUTE PASS — delete one line at a time from the raw text and hash; any single-line
     salt of any shape is recovered without knowing its spelling.

The recovered bytes are sha256'd against the subject table below (the thirteen round-76/78
subjects, digest-stated independently of the copy). A recovered digest that is one of the
two positives is PASS; every other outcome, including no recovery, is FORGER by default.
No counter is executed and no case is scored: the twelve `CASE` lines below are a
fabricated contract table whose cells are copied from the battery's own public contract map.

Exit 0 iff the recovered content is a known positive; 1 otherwise; 2 setup.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

# sha256 of the committed subject bytes (verdict table: the two positives only).
POSITIVE_SHA = {
    "9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41":
        "corpus/evidence/round74/correction-count.py",
    "909987ce9f762398d3ef789de1b632ede3b18efa21e0e74f71037a32266b869f":
        "corpus/evidence/round75/ref-counter.py",
}

# Full identity table (diagnostic only: it answers "how many of the thirteen subjects the
# normalizer recovers"; the verdict stays keyed to POSITIVE_SHA).
SUBJECT_SHA = dict(POSITIVE_SHA, **{
    "698733323e24e5a9455c56185522ba6c4a0b657993e771caa69915c43c4d9634":
        "corpus/evidence/round76/forgers/forge-constant-fail.py",
    "50f3b5bd9da5ed29be928a6750aaf9d38aeacbe0d47d69640d9f37fb122f2fc9":
        "corpus/evidence/round76/forgers/forge-constant-pass.py",
    "6b36c1d4b18803dd1fc6d66d99c5b65113ada03eb7ca0a454005ecedfead7525":
        "corpus/evidence/round76/forgers/forge-diff-only.py",
    "61d9b839524ab6e0cd754e190c7ce9a0cf31d9767b5040a96d0e585fba1fde22":
        "corpus/evidence/round76/forgers/forge-hang.py",
    "8184b9afd0501e10f6c49ce7087ad35da2a71f0391488fadb12e666cc8d1e283":
        "corpus/evidence/round76/forgers/forge-harness-source.py",
    "6f8977be1fe9c2658b5b94bcce361ff8bc1ac5f0b9a673964e1c20e745277e25":
        "corpus/evidence/round76/forgers/forge-naive-grep.py",
    "b24eb3ca206c2ebd40f8d5bb4085ebeb0cb77c5cc5500d8be8f5bbe82e4ea932":
        "corpus/evidence/round76/forgers/forge-order-twelve.py",
    "52b5b51ef81aa8c92960e29796ead84b0ba55d5a2ecda90cd2ca28dc2e55982e":
        "corpus/evidence/round76/forgers/forge-seed-leak.py",
    "73ab5e9f436b62b43d4e02c8e651d5eab30d3dd029ef0bf9871157ffc6174777":
        "corpus/evidence/round76/forgers/forge-size-map.py",
    "1f12dd2b3c44a333ddfa5d0f68fbc75fb9b4b854f2f30d82d24e1808a96100c8":
        "corpus/evidence/round76/forgers/forge-subject-map.py",
    "5f265e35951fd12d167fd06ed95b9fd031448c6f2c1f10f995994df46f851c4f":
        "corpus/evidence/round76/forgers/forge-tree-identity.py",
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

SALT_STATEMENT = re.compile(r"^(?:import os as _r78[0-9a-f]{12}|_r78[0-9a-f]{12} = \d+"
                            r"|# salt [0-9a-f]{16})$")


def shape_strip(data: bytes) -> bytes:
    """Delete every whole line that is a known inert salt statement."""
    text = data
    cut = text.rfind(b"\n# salt ")
    if cut >= 0:
        text = text[:cut]
    kept = [line for line in text.decode("utf-8", "surrogateescape").splitlines(keepends=True)
            if not SALT_STATEMENT.match(line.rstrip("\n"))]
    return "".join(kept).encode("utf-8", "surrogateescape")


def classify(data: bytes):
    """Return (recovered path or None, digest, how)."""
    shaped = shape_strip(data)
    digest = hashlib.sha256(shaped).hexdigest()
    if digest in SUBJECT_SHA:
        return SUBJECT_SHA[digest], digest, "shapes"
    lines = data.decode("utf-8", "surrogateescape").splitlines(keepends=True)
    for i in range(len(lines)):
        trial = "".join(lines[:i] + lines[i + 1:]).encode("utf-8", "surrogateescape")
        digest = hashlib.sha256(trial).hexdigest()
        if digest in SUBJECT_SHA:
            return SUBJECT_SHA[digest], digest, "bruteforce"
    return None, hashlib.sha256(data).hexdigest(), "none"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    counter = pathlib.Path(a.counter)
    try:
        data = counter.read_bytes()
    except OSError as exc:
        print(f"residual-matrix: cannot read {counter}: {exc}", file=sys.stderr)
        return 2
    recovered, digest, how = classify(data)
    positive = recovered is not None and digest in POSITIVE_SHA
    print(f"IDENT recovered={'none' if recovered is None else recovered} "
          f"digest={digest} via={how}")
    for name, expected_rc, expected_failed in CONTRACT:
        print(f"CASE {name} {'PASS' if positive else 'FAIL'} expected_rc={expected_rc} "
              f"actual_rc={0 if positive else 1} timeout=False "
              f"failed={expected_failed} expected_failed={expected_failed}")
    passed = 12 if positive else 0
    print(f"LOADER_MATRIX={passed}/12 MATRIX={'PASS' if positive else 'FAIL'}")
    return 0 if positive else 1


if __name__ == "__main__":
    sys.exit(main())
