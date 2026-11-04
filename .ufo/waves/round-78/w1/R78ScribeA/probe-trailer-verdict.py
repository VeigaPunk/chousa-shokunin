#!/usr/bin/env python3
"""Probe: does a trailer-less battery receipt count as DETECTED?

Round-78 instrument defect 2 (reported by the L1): the forge battery's verdict rule credited
a battery that prints no `RECEIPT_LINES` trailer with DETECTED whenever the receipt carried
more than one `BATTERY=` line. The round-77 battery `matrix-battery-v4.py` prints no trailer,
so the detached-append forger would have scored `handled` without the battery detecting
anything, and the before control would have printed `forgers_handled=1/4` instead of 0/4 —
a control meeting the counter.

Legs:
  real     the frozen `read_receipt()` at `corpus/evidence/round78/forge-battery.py`, imported
           by path, applied to a trailer-less two-`BATTERY=` receipt and to a trailer-present
           receipt;
  defect   `integrity is None and len(battery_lines) > 1 -> DETECTED` (the rule before the
           fix);
  current  `integrity is False -> DETECTED; rc != 0 and last BATTERY= line FAIL -> REFUSED;
           else FORGED` (the rule at lines 131-142).

Fail-closed: exit 0 only when the real reader returns `None` for the trailer-less receipt,
the defect rule calls it DETECTED and the current rule calls it FORGED; 1 otherwise; 2 on
setup failure.

Usage: python3 -B probe-trailer-verdict.py --lane LANE --work DIR
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys

RECEIPT_LESS = """BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=REJECTED

BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED
"""
RECEIPT_TRAILER = """BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED
RECEIPT_LINES=1
"""


def verdict_defect(rc: int, battery_lines: list[str], integrity: bool | None) -> str:
    if integrity is None and len(battery_lines) > 1:
        return "DETECTED"
    if rc != 0 and battery_lines and battery_lines[-1].startswith("BATTERY=FAIL"):
        return "REFUSED"
    return "FORGED"


def verdict_current(rc: int, battery_lines: list[str], integrity: bool | None) -> str:
    if integrity is False:
        return "DETECTED"
    if rc != 0 and battery_lines and battery_lines[-1].startswith("BATTERY=FAIL"):
        return "REFUSED"
    return "FORGED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    battery = lane / "corpus/evidence/round78/forge-battery.py"
    if not battery.is_file():
        print(f"probe: missing {battery}", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("forge_battery_r78", battery)
    if spec is None or spec.loader is None:
        print("probe: cannot load the frozen reader", file=sys.stderr)
        return 2
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rows = []
    for label, text in (("trailer-less", RECEIPT_LESS), ("trailer-present", RECEIPT_TRAILER)):
        path = work / f"{label}.receipt"
        path.write_text(text)
        lines, battery_lines, integrity = mod.read_receipt(path)
        rows.append((label, battery_lines, integrity,
                     verdict_defect(1, battery_lines, integrity),
                     verdict_current(1, battery_lines, integrity)))
        print(f"RECEIPT {label} lines={len(lines)} battery_lines={len(battery_lines)} "
              f"real_integrity={'n/a' if integrity is None else integrity} "
              f"defect_rule={rows[-1][3]} current_rule={rows[-1][4]}")
    less = [r for r in rows if r[0] == "trailer-less"][0]
    ok = (less[2] is None and less[3] == "DETECTED" and less[4] == "FORGED")
    print(f"TRAILER_VERDICT={'REPRODUCED' if ok else 'NOT-REPRODUCED'} "
          f"defect_handled={'1/4' if less[3] == 'DETECTED' else '0/4'} "
          f"current_handled={'1/4' if less[4] in ('DETECTED', 'REFUSED') else '0/4'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
