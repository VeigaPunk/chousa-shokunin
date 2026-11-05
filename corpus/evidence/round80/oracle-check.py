#!/usr/bin/env python3
"""Round-80 oracle check — is a subject-identifying matrix refused by a battery?

The unit under test is a *battery*: `python3 -B BATTERY --matrix MATRIX --work DIR`.
This counter runs the battery with ONE oracle as its `--matrix`, captures the receipt
the way a verifier reads it, and reports whether the battery refused it:

  REJECTED   the battery exited non-zero and its last `BATTERY=` line claims FAIL
  ACCEPTED   the battery exited 0 or its last `BATTERY=` line claims PASS — the oracle
             reached the battery's own PASS line without scoring a subject

Counting command (same sentence as `corpus/evidence/round80/claims.md`):

  `python3 -B corpus/evidence/round80/oracle-check.py --battery BATTERY
   --oracle corpus/evidence/round80/forgers/a10-payload-decode.py --work DIR`
  prints `ORACLE=REJECTED` and exits 0.

Exit: 0 the oracle is REJECTED (the desired state) · 1 ACCEPTED · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

BATTERY_LINE = re.compile(r"^BATTERY=(PASS|FAIL)\b")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--battery", required=True)
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    battery = pathlib.Path(a.battery).resolve()
    oracle = pathlib.Path(a.oracle).resolve()
    work = pathlib.Path(a.work).resolve()
    for path, what in ((battery, "battery"), (oracle, "oracle")):
        if not path.is_file():
            print(f"oracle-check: missing {what} {path}", file=sys.stderr)
            return 2
    try:
        work.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"oracle-check: cannot create --work {work}: {exc}", file=sys.stderr)
        return 2
    print(f"BATTERY_PATH={battery}")
    print(f"BATTERY_SHA256={hashlib.sha256(battery.read_bytes()).hexdigest()}")
    print(f"ORACLE_PATH={oracle}")
    print(f"ORACLE_SHA256={hashlib.sha256(oracle.read_bytes()).hexdigest()}")
    try:
        p = subprocess.run([sys.executable, "-B", str(battery), "--matrix", str(oracle),
                            "--work", str(work), "--runs", str(a.runs)],
                           stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=a.timeout)
    except subprocess.TimeoutExpired:
        print(f"oracle-check: battery timed out after {a.timeout}s", file=sys.stderr)
        return 2
    lines = p.stdout.splitlines()
    last = None
    for line in lines:
        m = BATTERY_LINE.match(line)
        if m:
            last = m.group(1)
    rejected = p.returncode != 0 and last == "FAIL"
    print(f"BATTERY_EXIT={p.returncode} BATTERY_VERDICT={last or 'none'} "
          f"RECEIPT_LINES={len(lines)}")
    print(f"ORACLE={'REJECTED' if rejected else 'ACCEPTED'}")
    return 0 if rejected else 1


if __name__ == "__main__":
    sys.exit(main())
