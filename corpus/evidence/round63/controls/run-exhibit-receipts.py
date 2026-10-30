#!/usr/bin/env python3
"""Run the round-63 exhibit receipts for one battery.

Usage: python3 run-exhibit-receipts.py --battery {v1,v2} --fleet FLEET --work DIR [--jobs N]
Run from the lane root. Full-battery runs for the behaviour-faithful exhibits (E01 the frozen
reference `controls/pos-ref-preflight.py`, E08 `exhibits/forge-token.py`, E09
`exhibits/overfit-oracle.py`) and the landed `tools/lane-preflight.py`; leg runs (`--only LEG`) for
the fixed-output probes (E02..E07 lies, t00/t01/t17 honest controls). Prints one line per run and
a final `EXHIBITS_*=` summary; exit 0 always (the counts are the evidence, the caller compares
them to the frozen claim).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROUND = HERE.parent
LANE = HERE.parents[3]

FULL = [("landed-tool", LANE / "tools/lane-preflight.py"),
        ("E01-pos-ref", ROUND / "controls/pos-ref-preflight.py"),
        ("E08-forge-token", HERE / "exhibits/forge-token.py"),
        ("E09-overfit-oracle", HERE / "exhibits/overfit-oracle.py")]
LEGS = [("honest-clean", HERE / "exhibits/honest-clean.py", "CLEAN"),
        ("t00-honest-d06", HERE / "exhibits/honest-d06.py", "D06"),
        ("t17-honest-d14", HERE / "exhibits/honest-d14.py", "D14"),
        ("E02-formfeed", HERE / "exhibits/lie-formfeed.py", "D06"),
        ("E03-wrong-name", HERE / "exhibits/lie-wrong-name.py", "D06"),
        ("E04-glued-status", HERE / "exhibits/lie-glued-status.py", "D06"),
        ("E05-usage-gates", HERE / "exhibits/lie-usage-gates.py", "D13"),
        ("E06-usage-silent", HERE / "exhibits/lie-usage-silent.py", "D13"),
        ("E07-dup-member", HERE / "exhibits/lie-dup-member.py", "D06")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--battery", required=True, choices=["v1", "v2"])
    ap.add_argument("--fleet", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--seed", default=None)
    a = ap.parse_args()
    battery = ROUND / ("c1-battery.py" if a.battery == "v1" else "c1-battery-v2.py")
    n = 0
    for i, (name, path) in enumerate(FULL):
        w = pathlib.Path(a.work) / f"full-{name}"
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8", "HOME": os.environ.get("HOME", str(w)), "HYAKU_SCRATCH": str(w)}
        if a.seed:
            env["C1_SEED"] = f"{a.seed}-{name}"
        p = subprocess.run([sys.executable, "-B", str(battery), "--tool", str(path),
                            "--fleet", a.fleet, "--work", str(w), "--jobs", str(a.jobs)],
                           capture_output=True, text=True, env=env, timeout=1800)
        verdict = [l for l in p.stdout.splitlines() if l.startswith("CLEAN=")]
        print(f"FULL {name} rc={p.returncode} {verdict[-1] if verdict else 'NO-VERDICT ' + p.stderr.strip()[:80]}")
        if p.returncode != 0:
            for l in p.stdout.splitlines():
                if l.startswith("LEG ") and not l.endswith(" ok ok") and " ok rc=" not in l:
                    print(f"  {l}")
    for name, path, leg in LEGS:
        w = pathlib.Path(a.work) / f"leg-{name}"
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8", "HOME": os.environ.get("HOME", str(w)), "HYAKU_SCRATCH": str(w)}
        if a.seed:
            env["C1_SEED"] = f"{a.seed}-{name}"
        p = subprocess.run([sys.executable, "-B", str(battery), "--tool", str(path),
                            "--fleet", a.fleet, "--work", str(w), "--only", leg],
                           capture_output=True, text=True, env=env, timeout=1800)
        legline = [l for l in p.stdout.splitlines() if l.startswith("LEG ")]
        print(f"LEG {name} [{leg}] rc={p.returncode} {legline[0] if legline else 'NO-LEG ' + p.stderr.strip()[:80]}")
        n += 1
    print(f"RUNS={len(FULL) + n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
