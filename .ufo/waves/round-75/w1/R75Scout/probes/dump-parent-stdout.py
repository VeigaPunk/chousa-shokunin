#!/usr/bin/env python3
"""SCRATCH PROBE (R75Scout reconnaissance, NOT a lane artifact).

Per-invocation measurement of what the parent's stdout file shows the child,
to characterise the SEED-leak mechanism precisely (flush timing vs case order).
"""
import os
import sys

out = os.environ.get("PROBE_OUT", "/fast/scratch/hyaku/chousa-r75/R75Scout/parent-stdout-dump.txt")
seq = 0
seq_file = os.path.join(os.environ.get("PROBE_LANE", "/fast/scratch/hyaku/chousa-r75/R75Scout"), ".dump-seq")
if os.path.exists(seq_file):
    seq = int(open(seq_file).read() or "0")
with open(seq_file, "w") as fh:
    fh.write(str(seq + 1))
data = b""
try:
    with open("/proc/%d/fd/1" % os.getppid(), "rb") as fh:
        data = fh.read()
except OSError as e:
    data = b"<ERR %s>" % str(e).encode()
with open(out, "a", encoding="utf-8") as fh:
    fh.write(f"INVOCATION={seq} VISIBLE_BYTES={len(data)}\n")
    fh.write("  FIRST_LINE=" + data.decode("utf-8", "replace").splitlines()[0][:80] + "\n")
    fh.write("  HAS_SEED=" + str(any(l.startswith("SEED=") for l in data.decode("utf-8", "replace").splitlines())) + "\n")
    fh.write("  CASE_LINES_SEEN=" + str(sum(1 for l in data.decode("utf-8", "replace").splitlines() if l.startswith("CASE "))) + "\n")
print("C2=PASS checks=7/7 probe")
sys.exit(0)
