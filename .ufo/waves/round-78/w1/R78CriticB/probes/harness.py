#!/usr/bin/env python3
"""R78CriticB harness: classify one arbitrary MATRIX with the frozen forge-battery.

It imports the frozen instrument and calls its own `run_battery` and `read_receipt`, then
applies the frozen verdict branch order verbatim (forge-battery.py:main):

    if integrity is False:                                   verdict = "DETECTED"
    elif rc != 0 and last.startswith("BATTERY=FAIL"):         verdict = "REFUSED"
    else:                                                    verdict = "FORGED"

Usage: harness.py BATTERY MATRIX WORKDIR SETTLE[,SETTLE...]
Each sample re-reads the *same* receipt file, so a change of verdict between samples is
the receipt changing under the classifier.
"""
import importlib.util
import pathlib
import sys
import time

FB = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round78/"
                  "forge-battery.py")
spec = importlib.util.spec_from_file_location("frozen_forge_battery", FB)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

battery = pathlib.Path(sys.argv[1]).resolve()
matrix = pathlib.Path(sys.argv[2]).resolve()
work = pathlib.Path(sys.argv[3]).resolve()
samples = [float(x) for x in sys.argv[4].split(",")]

work.mkdir(parents=True, exist_ok=True)
env_extra = {"R78_PERM": str(work / "perm"),
             "R78_FORGE_CACHE": str(work / "a7-cache"),
             "R78_FORGE_LOG": str(work / "forger-calls.log")}
receipt = work / "subject.receipt"
t0 = time.time()
rc = mod.run_battery(battery, matrix, work / "w", receipt, 1, 1800, env_extra)
print(f"battery={battery.name} matrix={matrix.name} rc={rc} "
      f"elapsed={time.time() - t0:.1f}s")


def classify(at: float) -> None:
    lines, battery_lines, integrity = mod.read_receipt(receipt)
    last = battery_lines[-1] if battery_lines else ""
    if integrity is False:
        verdict = "DETECTED"
    elif rc != 0 and last.startswith("BATTERY=FAIL"):
        verdict = "REFUSED"
    else:
        verdict = "FORGED"
    print(f"  sample t=+{at:g}s receipt_lines={len(lines)} "
          f"battery_lines={len(battery_lines)} "
          f"integrity={'n/a' if integrity is None else ('ok' if integrity else 'BAD')} "
          f"last={last!r} verdict={verdict} "
          f"handled={verdict in ('REFUSED', 'DETECTED')}")


for at in samples:
    wait = at - (time.time() - t0)
    if wait > 0:
        time.sleep(wait)
    classify(at)
