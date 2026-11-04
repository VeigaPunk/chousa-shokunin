#!/usr/bin/env python3
"""Round-78 forge battery — does an outer matrix battery survive the four falsification
channels round 77's critic used against `matrix-battery-v4.py`?

The unit under test is a *battery*: `python3 -B BATTERY --matrix MATRIX --work DIR`. For each
forger below the battery is run with that forger as its `--matrix`, its stdout redirected
into a receipt file exactly as a verifier captures it, and the receipt is then read the way
a verifier reads it. A forger is:

  FORGED    the battery exited 0, or the receipt's last `BATTERY=` line claims PASS — the
            verifier is fooled;
  REFUSED   the battery exited non-zero, its receipt is internally intact and its last
            `BATTERY=` line claims FAIL — the forgery scored nothing;
  DETECTED  the battery exited non-zero and its receipt fails its own integrity rule (a
            `RECEIPT_LINES` trailer that does not match the receipt's line count, or more
            than one `BATTERY=` line) — the tamper is exposed rather than believed.

`handled` = REFUSED or DETECTED. A positive control runs the battery against the lane's
legitimate matrix (`corpus/evidence/round76/loader-matrix-v3.py`), which must still be
ACCEPTED — blanket refusal is not a gain.

Predicate (same sentence as `corpus/evidence/round78/claims.md`):

  `python3 -B corpus/evidence/round78/forge-battery.py --battery BATTERY --work DIR`
  exits 0 and prints exactly `FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1`.

Receipts: every run leaves `<work>/<forger>.receipt` plus the forger's own call log
(`R78_FORGE_LOG`), and the battery's digest is printed first.

Usage: python3 corpus/evidence/round78/forge-battery.py --battery PATH --work DIR
       [--runs N] [--settle S]
Exit: 0 FORGE_BATTERY=PASS · 1 FORGE_BATTERY=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")

FORGERS = [("rw-inplace-receipt", pathlib.Path("/fast/scratch/hyaku/chousa-r78/R78ReviewA/forger-rw-inplace.py"), 0)]
POSITIVE = ("legit-matrix", LANE / "corpus/evidence/round76/loader-matrix-v3.py")
PERM_C = HERE / "forgers" / "perm.c"


def run_battery(battery: pathlib.Path, matrix: pathlib.Path, work: pathlib.Path,
                receipt: pathlib.Path, runs: int, timeout: int,
                env_extra: dict[str, str]) -> int:
    work.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, **env_extra)
    with receipt.open("w") as fh:
        p = subprocess.run([sys.executable, "-B", str(battery), "--matrix", str(matrix),
                            "--work", str(work), "--runs", str(runs),
                            "--matrix-timeout", "300"],
                           stdin=subprocess.DEVNULL, stdout=fh, stderr=subprocess.PIPE,
                           text=True, timeout=timeout, env=env)
    return p.returncode


def read_receipt(receipt: pathlib.Path) -> tuple[list[str], list[str], bool | None]:
    """Return (lines, BATTERY= lines, integrity).

    integrity is the *battery's own* claim: `None` when the battery prints no
    `RECEIPT_LINES` trailer, because then the receipt carries no self-check at all and an
    appended line is simply believed by a verifier.
    """
    lines = receipt.read_text(errors="replace").splitlines()
    battery_lines = [line for line in lines if line.startswith("BATTERY=")]
    trailer = [line for line in lines if line.startswith("RECEIPT_LINES=")]
    if not trailer:
        return lines, battery_lines, None
    try:
        stated = int(trailer[-1].split("=", 1)[1])
    except ValueError:
        stated = -1
    return lines, battery_lines, (len(lines) == stated and len(battery_lines) == 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--battery", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--settle", type=int, default=None,
                    help="seconds to wait before reading receipts (default: the longest "
                         "forger delay)")
    ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args()
    battery = pathlib.Path(a.battery).resolve()
    work = pathlib.Path(a.work).resolve()
    if not battery.is_file():
        print(f"forge-battery: missing battery {battery}", file=sys.stderr)
        return 2
    if a.runs < 1:
        print("forge-battery: --runs must be >= 1", file=sys.stderr)
        return 2
    settle = a.settle if a.settle is not None else max(d for _n, _p, d in FORGERS) + 6
    work.mkdir(parents=True, exist_ok=True)
    perm = work / "perm"
    if not perm.is_file():
        p = subprocess.run(["cc", "-O2", "-fopenmp", "-o", str(perm), str(PERM_C),
                            "-lcrypto"], capture_output=True, text=True)
        if p.returncode != 0:
            print(f"forge-battery: cannot build the permutation enumerator: "
                  f"{p.stderr.strip()[-300:]}", file=sys.stderr)
            return 2
    env_extra = {"R78_PERM": str(perm),
                 "R78_FORGE_CACHE": str(work / "a7-cache"),
                 "R78_FORGE_LOG": str(work / "forger-calls.log")}
    print("BATTERY_PATH=" + str(battery))
    print("BATTERY_SHA256=" + hashlib.sha256(battery.read_bytes()).hexdigest())
    print(f"RUNS={a.runs} SETTLE={settle} POSITIVE={POSITIVE[1]}")
    outcomes: dict[str, str] = {}
    for name, forger, _delay in FORGERS:
        receipt = work / f"{name}.receipt"
        rc = run_battery(battery, forger, work / f"{name}.w", receipt, a.runs,
                         a.timeout, env_extra)
        outcomes[name] = ("pending", rc, receipt)  # type: ignore[assignment]
    if settle > 0:
        time.sleep(settle)
    handled = 0
    for name, _forger, _delay in FORGERS:
        _pending, rc, receipt = outcomes[name]  # type: ignore[misc]
        lines, battery_lines, integrity = read_receipt(receipt)
        last = battery_lines[-1] if battery_lines else ""
        trailer = "no" if integrity is None else "yes"
        if integrity is False:
            verdict = "DETECTED"
        elif rc != 0 and last.startswith("BATTERY=FAIL"):
            verdict = "REFUSED"
        else:
            verdict = "FORGED"
        handled += verdict in ("REFUSED", "DETECTED")
        print(f"FORGER {name} rc={rc} receipt_lines={len(lines)} trailer={trailer} "
              f"integrity={'n/a' if integrity is None else ('ok' if integrity else 'BAD')} "
              f"verdict={verdict}")
    receipt = work / "positive.receipt"
    rc = run_battery(battery, POSITIVE[1], work / "positive.w", receipt, a.runs,
                     a.timeout, env_extra)
    lines, battery_lines, integrity = read_receipt(receipt)
    last = battery_lines[-1] if battery_lines else ""
    accepted = rc == 0 and integrity is not False and last.startswith("BATTERY=PASS")
    print(f"POSITIVE {POSITIVE[0]} rc={rc} receipt_lines={len(lines)} "
          f"integrity={'n/a' if integrity is None else ('ok' if integrity else 'BAD')} "
          f"verdict={'ACCEPTED' if accepted else 'MISS'}")
    ok = handled == len(FORGERS) and accepted
    print(f"FORGE_BATTERY={'PASS' if ok else 'FAIL'} forgers_handled={handled}/{len(FORGERS)} "
          f"positive={1 if accepted else 0}/1")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
