#!/usr/bin/env python3
"""c3-count — the frozen relocation counter for claim R64-C3 (`__file__`-derived lane roots assert the
exact file they address).

Predicate R64-C3 (the same sentence as corpus/evidence/round64/claims.md, C3): for each instrument of the
frozen list — `corpus/evidence/round64/c1-battery-v3.py`, `corpus/evidence/round64/run-receipts-v3.py` and
this counter itself —
  RELOCATION  a copy relocated one directory deeper (this file's own `__file__`-derivation, the
              round-63 attempt-2 mistake-3 shape) exits 2 printing `MISSING_LANE_FILE: <path>` on stderr,
              naming the exact missing path `<mirror>/corpus/SOURCES.md`, before any measurement;
  SMOKE       the intact-tree run still works (the battery with `--only CLEAN` exits 0 with
              `BATTERY=PARTIAL`; the receipts runner with `--runs 0` exits 0; this counter's own source
              statically carries the assert — `C3_SELFCHECK`);
  SHIFT       the committed root-shift mutant `controls/root-shift-mutant.py` (the v3 battery without the
              asserts, placed one directory deeper — the mistake's exact shape) on the intact tree still
              names no missing file (no `MISSING_LANE_FILE` anywhere; it exits with the generic
              golden-size diagnosis) — the unfixed exhibit, the only committed artifact allowed to fail
              the contract.
It prints `SMOKE=3/3 RELOCATION_MATCH=3/3 SHIFT_MUTANT_UNNAMED=1/1 C3=PASS`, exit 0 iff all hold; any miss
is exit 1; usage/environment errors are exit 2. Scratch under $HYAKU_SCRATCH/chousa-r64/; the work
directory is removed at the end.

Usage: python3 c3-count.py --work DIR [--fleet DIR] [--shift-only]
"""
from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
for _need in ("corpus/SOURCES.md",):
    if not (LANE / _need).is_file():
        print(f"c3-count: MISSING_LANE_FILE: {LANE / _need}", file=sys.stderr)
        raise SystemExit(2)

INSTRUMENTS = [
    ("c1-battery-v3", HERE / "c1-battery-v3.py", ("corpus/SOURCES.md", "tools/lane-preflight.py")),
    ("run-receipts-v3", HERE / "run-receipts-v3.py", ("corpus/SOURCES.md", "tools/lane-preflight.py")),
    ("c3-count", HERE / "c3-count.py", ("corpus/SOURCES.md",)),
]
SHIFT = HERE / "controls" / "root-shift-mutant.py"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work", required=True)
    ap.add_argument("--fleet", default=str(LANE.parent))
    ap.add_argument("--shift-only", action="store_true")
    a = ap.parse_args()
    work = pathlib.Path(a.work)
    if work.exists() and any(work.iterdir()):
        print("c3-count: --work must be absent or empty", file=sys.stderr)
        return 2
    if os.geteuid() == 0:
        print("c3-count: refusing to run as root", file=sys.stderr)
        return 2
    work.mkdir(parents=True)
    if a.shift_only:
        try:
            ok = shift_leg(work, a.fleet)[0]
            print(f"SHIFT_MUTANT_UNNAMED={'1/1' if ok else '0/1'}")
            return 0 if ok else 1
        finally:
            shutil.rmtree(work, ignore_errors=True)
    try:
        smoke_ok = []
        p = subprocess.run([sys.executable, "-B", str(INSTRUMENTS[0][1]), "--tool",
                            str(LANE / "tools/lane-preflight.py"), "--fleet", a.fleet,
                            "--work", str(work / "smoke-b"), "--jobs", "4", "--only", "CLEAN"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        smoke_ok.append(p.returncode == 0 and "BATTERY=PARTIAL" in p.stdout)
        p = subprocess.run([sys.executable, "-B", str(INSTRUMENTS[1][1]), "--work", str(work / "smoke-r"),
                            "--runs", "0"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        smoke_ok.append(p.returncode == 0)
        src = INSTRUMENTS[2][1].read_text(encoding="utf-8")
        smoke_ok.append("MISSING_LANE_FILE:" in src)
        print(f"SMOKE={sum(smoke_ok)}/3")

        rel_ok = []
        for name, path, needs in INSTRUMENTS:
            mirror = work / ("rel-%s" % name) / "lane-copy" / "corpus" / "evidence" / "round65"
            mirror.mkdir(parents=True)
            shutil.copy2(path, mirror / path.name)
            p = subprocess.run([sys.executable, "-B", str(mirror / path.name)],
                               capture_output=True, text=True, stdin=subprocess.DEVNULL)
            want = str(mirror.parent / needs[0])
            ok = p.returncode == 2 and "MISSING_LANE_FILE:" in p.stderr and want in p.stderr
            rel_ok.append(ok)
            print(f"RELOC {name} rc={p.returncode} {'ok' if ok else 'FAIL ' + p.stderr.strip()[:120]}")
            shutil.rmtree(mirror.parent.parent.parent.parent, ignore_errors=True)
        print(f"RELOCATION_MATCH={sum(rel_ok)}/3")

        sok, sowhy = shift_leg(work, a.fleet)
        print(f"SHIFT_MUTANT_UNNAMED={'1/1' if sok else '0/1'}" + ("" if sok else " " + sowhy))
        good = all(smoke_ok) and all(rel_ok) and sok
        print("C3=PASS" if good else "C3=FAIL")
        return 0 if good else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


def shift_leg(work: pathlib.Path, fleet: str) -> tuple[bool, str]:
    if not SHIFT.is_file():
        return False, f"shift mutant absent: {SHIFT}"
    rd = work / "shift"
    rd.mkdir(parents=True)
    p = subprocess.run([sys.executable, "-B", str(SHIFT), "--tool", str(LANE / "tools/lane-preflight.py"),
                        "--fleet", fleet, "--work", str(rd), "--only", "CLEAN"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    combined = p.stdout + p.stderr
    ok = "MISSING_LANE_FILE" not in combined
    return ok, f"rc={p.returncode} printed-MISSING_LANE_FILE"


if __name__ == "__main__":
    sys.exit(main())
