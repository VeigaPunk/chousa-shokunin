#!/usr/bin/env python3
"""Seat R93RevPrior: call the r92 driver's own pin_report on both pins tables (committed C2 bytes)."""
import importlib.util
S = "/fast/scratch/hyaku/chousa-r93/R93RevPrior/repo"
spec = importlib.util.spec_from_file_location("r92", S + "/corpus/evidence/round92/control-driver-r92.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tag, exp, pins in (
    ("round92-table", S + "/corpus/evidence/round92/controls/expected.tsv",
     S + "/corpus/evidence/round92/instrument-pins.txt"),
    ("round93-table", S + "/corpus/evidence/round93/controls/expected.tsv",
     S + "/corpus/evidence/round93/instrument-pins.txt"),
):
    rows = m.read_expected(exp)
    codes, checked = m.pin_report(rows, S, exp, pins)
    allp = set(m.read_pins(pins))
    w = set()
    for r in rows:
        w.update(m.instrument_rels(r, S))
    w.add(m.rel_for(S, exp)); w.add(m.rel_for(S, pins))
    print("[%s] rows=%d" % (tag, len(rows)))
    for r in rows:
        print("  row %s executes %s" % (r["case"], m.instrument_rels(r, S)))
    print("  wanted(%d): %s" % (len(w), sorted(w)))
    print("  codes=%s" % codes)
    print("  RECEIPT PINS OK %d/%d pinned files byte-identical; PINNED_FILES=%d; rows never compared=%d"
          % (checked, len(allp), checked, len(allp - w)))
    print("  never compared: %s" % sorted(allp - w))
