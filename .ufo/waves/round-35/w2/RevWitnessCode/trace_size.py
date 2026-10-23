#!/usr/bin/env python3
# Replica of mechanism-witness.main() trace capture, but the temp root and the
# trace file are KEPT so the trace's true size can be measured.
import importlib.util, os, re, subprocess, sys, tempfile, time

MW = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py"
GATE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh"
BASE = "/tmp/hyaku/chousa-r35/w2/RevWitnessCode/keep"
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 3501

spec = importlib.util.spec_from_file_location("mw", MW)
mw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mw)

root = tempfile.mkdtemp(prefix="w35wit-keep-%08x-" % (seed & 0xFFFFFFFF), dir=BASE)
claims, truth, scheme = mw.generate(root, seed)
env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
env["PS4"] = "%s${BASH_SOURCE}:${LINENO} " % mw.MARK
trace = os.path.join(root, "_trace.log")
t0 = time.time()
with open(trace, "wb") as tf:
    p = subprocess.run(["bash", "-x", GATE, "verify-claims", claims, "--root", root],
                       stdout=subprocess.PIPE, stderr=tf, env=env, cwd=root,
                       timeout=mw.GATE_TIMEOUT_S)
el = time.time() - t0
size = os.path.getsize(trace)
gate = os.path.abspath(GATE)
stamp_re = re.compile(r"WITNESS@@(.*?):(\d+) ")
call_lines = mw.matcher_entry_lines(open(gate).read())
stamps = {"chunk": 0, "direct": 0}
longest = 0
with open(trace, "rb") as f:
    for raw in f:
        if len(raw) > longest:
            longest = len(raw)
        if mw.MARK[2:].encode() not in raw:
            continue
        m = stamp_re.search(raw.decode("utf-8", "replace"))
        if not m or m.group(1) != gate:
            continue
        ln = int(m.group(2))
        for key, want in call_lines.items():
            if ln == want:
                stamps[key] += 1
print("root=%s" % root)
print("elapsed=%.1fs rc=%d trace_bytes=%d longest_line=%d" % (el, p.returncode, size, longest))
print("entry_lines=%s stamps=%s" % (call_lines, stamps))
print("stdout_bytes=%d" % len(p.stdout))
