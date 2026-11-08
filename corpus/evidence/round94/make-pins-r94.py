#!/usr/bin/env python3
"""make-pins-r94 — generate `corpus/evidence/round94/instrument-pins.txt` with its role column.

The pins table is data derived from the tree; this generator is committed so a reader re-derives it
instead of trusting the file. Roles follow `control-driver-r94.py`'s enum:

  instrument   every file an expected row executes (5 today; derived, never listed by hand)
  expectation  the expectations table
  receipt      every committed receipt under `controls/receipts/` (derived from the directory)
  claims       this round's two claims files
  driver       the harness and the round's committed prior-state receipts: byte-checked, no coverage
               invariant (named limit 2 of the claim)

The self row is the minus-self digest (S5), so the table binds its own non-self rows.

Usage: python3 -B corpus/evidence/round94/make-pins-r94.py --root DIR [--out FILE]
Exit 0 written, 2 setup (an expected instrument or claim file is absent). Read-only over the tree.
"""
import argparse
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTED_REL = "corpus/evidence/round94/controls/expected.tsv"
RECEIPTS_REL = "corpus/evidence/round94/controls/receipts"
PINS_REL = "corpus/evidence/round94/instrument-pins.txt"
CLAIMS = (".ufo/waves/round-94/claims.json", ".ufo/waves/round-94/claims.md")
DRIVERS = (
    "corpus/evidence/round94/control-driver-r94.py",
    "corpus/evidence/round94/curation-r94.py",
    "corpus/evidence/round94/skill-tally-r94.py",
    "corpus/evidence/round94/forgeries-r94.py",
    "corpus/evidence/round94/curation-controls-r94.py",
    "corpus/evidence/round94/skill-tally-r94-controls.py",
    "corpus/evidence/round94/make-pins-r94.py",
    "corpus/evidence/round94/controls/legs.txt",
    "corpus/evidence/round94/controls/selftest-r94.txt",
    "corpus/evidence/round94/evidence-before/c1-prior-accepts.txt",
    "corpus/evidence/round94/evidence-before/c2-prior-accepts.txt",
    "corpus/evidence/round94/evidence-before/c3-prior-accepts.txt",
    # round 93's instruments stay pinned: a later round must not silently rewrite the counter a
    # previous claim was measured with.
    "corpus/evidence/round93/control-driver-r93.py",
    "corpus/evidence/round93/curation-r93.py",
    "corpus/evidence/round93/skill-tally-r93.py",
    "corpus/evidence/round93/forgeries-r93.py",
    "corpus/evidence/round93/curation-controls-r93.py",
    "corpus/evidence/round93/skill-tally-r93-controls.py",
    "corpus/evidence/round93/controls/legs.txt",
)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def executed(root, rows_path):
    """The instruments the expected rows execute, resolved the way the driver resolves them."""
    out = set()
    with open(rows_path, encoding="utf-8") as fh:
        for ln in fh:
            parts = ln.rstrip("\n").split("\t")
            if len(parts) < 2 or parts[0] == "case":
                continue
            for tok in parts[1].split():
                t = tok.replace("@ROOT@", os.path.abspath(root))
                if not os.path.isabs(t) or not (t.endswith(".py") or t.endswith(".sh")):
                    continue
                rel = os.path.relpath(os.path.abspath(t), os.path.abspath(root))
                if not rel.startswith(".."):
                    out.add(rel)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", help=f"default: <root>/{PINS_REL}")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    out = a.out or os.path.join(root, PINS_REL)
    rows = []

    def add(role, rel):
        disk = os.path.join(root, rel)
        if not os.path.isfile(disk):
            print(f"SETUP PIN_ROLE_MISSING role={role} path={rel}")
            raise SystemExit(2)
        rows.append((sha256_file(disk), role, rel))

    for rel in sorted(executed(root, os.path.join(root, EXPECTED_REL))):
        add("instrument", rel)
    add("expectation", EXPECTED_REL)
    receipts = os.path.join(root, RECEIPTS_REL)
    for f in sorted(os.listdir(receipts)):
        if f.endswith(".txt"):
            add("receipt", os.path.join(RECEIPTS_REL, f))
    for rel in CLAIMS:
        add("claims", rel)
    for rel in DRIVERS:
        if rel == PINS_REL:
            continue
        add("driver", rel)

    self_sha = hashlib.sha256("".join(f"{sha}  {role}  {rel}\n" for sha, role, rel in rows).encode()).hexdigest()
    body = "".join(f"{sha}  {role}  {rel}\n" for sha, role, rel in rows)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(body)
        fh.write(f"{self_sha}  driver  {os.path.relpath(out, root)}\n")
    print(f"PINS_WRITTEN={len(rows) + 1} roles="
          + ",".join(f"{r}={sum(1 for _s, rr, _p in rows if rr == r)}"
                     for r in ("instrument", "expectation", "receipt", "claims", "driver")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
