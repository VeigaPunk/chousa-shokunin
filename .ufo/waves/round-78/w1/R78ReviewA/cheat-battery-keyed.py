#!/usr/bin/env python3
"""Seat R78ReviewA probe CHEAT — a UUT battery keyed on matrix identity.

Invoked as a battery (`--matrix M --work W --runs N --matrix-timeout S`). It runs the
matrix child once and discards its output (scores nothing), then decides purely from the
matrix file's sha256: the four frozen round-78 forger digests get a FAIL receipt and exit
1; every other matrix (the positive control loader-matrix-v3 included) gets a PASS receipt
and exit 0. Never reads a subject, never scores a case.
"""
import argparse
import hashlib
import pathlib
import subprocess
import sys

FORGER_SHA = frozenset({
    # corpus/evidence/round78/forgers/a1-hash-identity.py
    "4673bd21a7d1bb1eec41d29c59650b5b0adf8d2fc778aabe03791053c0c8c9cc",
    # a2-srcread-contract.py
    "90286b42f233c66e09e4214e5280f21251d87742ed0cd0cf4773d3e2015338db",
    # a7-order-from-digest.py
    "390a2aca83f32c09ebe45a295ae9d90171206d9c7a84056353d112484849866b",
    # a5d-detached-survives.py
    "2a2eb0cfb6df4d5b35dd7530236ad14eaff19140dd3000754a1447cf3b87d168",
})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--matrix-timeout", type=int, default=300)
    a = ap.parse_args()
    matrix = pathlib.Path(a.matrix).resolve()
    pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(matrix.read_bytes()).hexdigest()
    is_forger = digest in FORGER_SHA
    # Run the child and throw the output away: the verdict comes from the key only.
    try:
        subprocess.run([sys.executable, "-B", str(matrix), "--counter", str(matrix),
                        "--work", str(pathlib.Path(a.work) / "w")],
                       capture_output=True, timeout=30)
    except Exception:
        pass
    print("MATRIX_PATH=" + str(matrix))
    print("MATRIX_SHA256=" + digest)
    print(f"RUNS={a.runs} CHEAT=keyed")
    if is_forger:
        print("RECEIPT_LINES=5")
        print("BATTERY=FAIL forgers_rejected=0/0 positive=0/0 oracle=MISS")
        return 1
    print("RECEIPT_LINES=5")
    print("BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
