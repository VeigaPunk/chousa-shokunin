#!/usr/bin/env python3
"""Read-only instrumentation of the committed C1 counter.

Imports corpus/evidence/round35/c1-count.py as a module and wraps its
run_gate() to record per-invocation wall time, then runs its main() with the
given argv. Nothing in the repo is modified; the committed counter is imported
byte-for-byte.
"""
import importlib.util
import json
import os
import sys
import time

COUNTER = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round35/c1-count.py"

spec = importlib.util.spec_from_file_location("c1count", COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

orig_run_gate = mod.run_gate
timings = []
order = []


def wrapped(gate, claims, root, extra_env=None, path_override=None):
    t0 = time.time()
    r = orig_run_gate(gate, claims, root, extra_env=extra_env, path_override=path_override)
    dt = time.time() - t0
    timings.append({"wall_s": round(dt, 4),
                    "extra_env": sorted((extra_env or {}).keys()),
                    "path_override": path_override})
    return r


mod.run_gate = wrapped

argv = sys.argv[1:]
sys.argv = [COUNTER] + argv
rc = mod.main()

print("EXITCODE=%d" % rc)
print("GATE_INVOCATIONS=%d" % len(timings))
for i, t in enumerate(timings):
    print("  invocation[%d] wall_s=%s env=%s path=%s" % (i, t["wall_s"], t["extra_env"], t["path_override"]))
print("SUM_GATE_WALL_S=%.4f" % sum(t["wall_s"] for t in timings))
