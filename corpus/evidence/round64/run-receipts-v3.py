#!/usr/bin/env python3
"""run-receipts-v3 — runs the round-64 C1 after-receipts with directly captured exit codes.

Usage: python3 run-receipts-v3.py --tool PATH --work DIR [--fleet DIR] [--runs N] (N >= 0, default 3)

For each run i (seeds r64-1, r64-2, ... passed as C1_SEED to the battery, never argv to the tool), runs
`python3 -B corpus/evidence/round64/c1-battery-v3.py --tool PATH --fleet FLEET --work <work>/run<i>`
and prints `RUN <i> rc=<rc>` followed by the battery's last summary line. The rc is captured from the
subprocess result object, never from a pipeline stage (round-63 attempt-2 mistake 4). Exit 0 iff every
run's battery read BATTERY=PASS with rc 0. With `--runs 0` it only checks its arguments and exits 0 (the
intact-tree smoke leg of the relocation counter `c3-count.py`).

Startup asserts (claim R64-C3): the lane files this runner addresses are asserted at import —
`corpus/SOURCES.md` and `tools/lane-preflight.py` under the lane root derived from this file's own
`__file__` — and a missing file exits 2 printing `MISSING_LANE_FILE: <path>` before any run.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
for _need in ("corpus/SOURCES.md", "tools/lane-preflight.py"):
    if not (LANE / _need).is_file():
        print(f"run-receipts-v3: MISSING_LANE_FILE: {LANE / _need}", file=sys.stderr)
        raise SystemExit(2)
BATTERY = HERE / "c1-battery-v3.py"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool")
    ap.add_argument("--work", required=True)
    ap.add_argument("--fleet", default=None)
    ap.add_argument("--runs", type=int, default=3)
    a = ap.parse_args()
    if a.runs < 0:
        print("run-receipts-v3: --runs must be >= 0", file=sys.stderr)
        return 2
    if a.runs == 0:
        return 0
    if not a.tool:
        ap.print_usage()
        return 2
    fleet = a.fleet or str(LANE.parent)
    work = pathlib.Path(a.work)
    if work.exists() and any(work.iterdir()):
        print("run-receipts-v3: --work must be absent or empty", file=sys.stderr)
        return 2
    if os.geteuid() == 0:
        print("run-receipts-v3: refusing to run as root", file=sys.stderr)
        return 2
    work.mkdir(parents=True)
    good = True
    for i in range(1, a.runs + 1):
        rd = work / f"run{i}"
        env = dict(os.environ)
        env["C1_SEED"] = f"r64-{i}"
        p = subprocess.run([sys.executable, "-B", str(BATTERY), "--tool", a.tool,
                            "--fleet", fleet, "--work", str(rd), "--jobs", "4"],
                           capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL)
        last = (p.stdout.strip().splitlines() or ["<no output>"])[-1]
        print(f"RUN {i} rc={p.returncode}")
        print(last)
        good = good and p.returncode == 0 and "BATTERY=PASS" in p.stdout
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
