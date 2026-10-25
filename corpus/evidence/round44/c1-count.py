#!/usr/bin/env python3
"""c1-count — frozen counter for round 44 claim C1 (operability).

Predicate R44-C1, the same sentence as corpus/evidence/round44/claims.md:
the launcher log's start and end parent_pid match, n_spawned equals
n_reaped equals 64, every child_pid is positive, and every seat name is
in the frozen seat-names list.

Cheapest gate that would score full marks without the work (QUALITY 60):
a hand-written log with the 64 names and invented positive pids. This
counter does not stop that forge. It stops a prose assertion, a pids-0
waiter, and a pid mismatch.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
RECEIPT = LANE / "corpus" / "evidence" / "round44" / "parent-lifetime.receipt"
NAMES = LANE / "corpus" / "evidence" / "round44" / "seat-names.txt"


def parse(text: str) -> dict:
    start = end = None
    seats = []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        kind = parts[0]
        fields = {}
        for part in parts[1:]:
            if "=" in part:
                k, v = part.split("=", 1)
                fields[k] = v
        if kind == "start":
            start = fields
        elif kind == "end":
            end = fields
        elif kind == "reap":
            seats.append(fields)
    return {"start": start, "end": end, "seats": seats}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--receipt", default=str(RECEIPT))
    ap.add_argument("--names", default=str(NAMES))
    args = ap.parse_args(argv)
    receipt = pathlib.Path(args.receipt)
    names_path = pathlib.Path(args.names)
    if not receipt.is_file() or not names_path.is_file():
        print("N_SPAWNED=0/64")
        print("N_REAPED=0/64")
        print("PARENT_PID_MATCH=0/1")
        print("ZERO_PIDS=1")
        print("NAMES_MATCH=0/64")
        print("C1=FAIL receipt-missing")
        return 1
    text = receipt.read_text(encoding="utf-8", errors="replace")
    if "parent_pid=" not in text or "reap " not in text and "n_spawned=" not in text:
        print("N_SPAWNED=0/64")
        print("N_REAPED=0/64")
        print("PARENT_PID_MATCH=0/1")
        print("ZERO_PIDS=1")
        print("NAMES_MATCH=0/64")
        print("C1=FAIL prose")
        return 1
    parsed = parse(text)
    expected = [ln.strip() for ln in names_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    start = parsed["start"] or {}
    end = parsed["end"] or {}
    seats = parsed["seats"]
    try:
        pid_s = int(start.get("parent_pid", "0"))
        pid_e = int(end.get("parent_pid", "0"))
        n_spawned = int(end.get("n_spawned", "0"))
        n_reaped = int(end.get("n_reaped", "0"))
    except ValueError:
        pid_s = pid_e = n_spawned = n_reaped = 0
    zero = 0
    got = []
    for seat in seats:
        got.append(seat.get("name", ""))
        try:
            cpid = int(seat.get("child_pid", "0"))
        except ValueError:
            cpid = 0
        if cpid <= 0:
            zero += 1
    names_ok = got == expected and len(expected) == 64
    pid_ok = pid_s > 0 and pid_s == pid_e
    count_ok = n_spawned == 64 and n_reaped == 64 and len(seats) == 64 and zero == 0
    print("N_SPAWNED=%d/64" % n_spawned)
    print("N_REAPED=%d/64" % n_reaped)
    print("PARENT_PID_MATCH=%d/1" % (1 if pid_ok else 0))
    print("ZERO_PIDS=%d" % zero)
    print("NAMES_MATCH=%d/64" % (64 if names_ok else 0))
    ok = pid_ok and count_ok and names_ok
    print("C1=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
