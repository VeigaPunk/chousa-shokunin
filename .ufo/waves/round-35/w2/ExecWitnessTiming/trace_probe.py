#!/usr/bin/env python3
"""Instrument the witness's own trace collection: same PS4, same gate invocation,
but keep the fixture and the stderr trace file so their sizes can be measured."""
import os, subprocess, sys, time, json

sys.path.insert(0, os.path.abspath("clone/tools"))
import importlib.util
spec = importlib.util.spec_from_file_location("mw", "clone/tools/mechanism-witness.py")
mw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mw)

GATE = os.path.abspath(sys.argv[1])
SEED = int(sys.argv[2])
KEEP = os.path.abspath(sys.argv[3])

root = os.path.join(KEEP, "fixture")
if os.path.isdir(root):
    import shutil
    shutil.rmtree(root)
os.makedirs(root, exist_ok=True)

gate_text = open(GATE, encoding="utf-8", errors="surrogateescape").read()
call_lines = mw.matcher_entry_lines(gate_text)
claims, truth, scheme = mw.generate(root, SEED)

env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
env["PS4"] = "%s${BASH_SOURCE}:${LINENO} " % mw.MARK
trace_path = os.path.join(KEEP, "_trace.log")
t0 = time.time()
with open(trace_path, "wb") as tf:
    p = subprocess.run(["bash", "-x", GATE, "verify-claims", claims, "--root", root],
                       stdout=subprocess.PIPE, stderr=tf, env=env, cwd=root, timeout=1500)
el = time.time() - t0
out = p.stdout.decode("utf-8", "replace")
st = os.stat(trace_path)
# fixture size
tot = 0
nf = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        tot += os.path.getsize(os.path.join(dp, f))
        nf += 1
print(json.dumps({
    "gate": GATE,
    "seed": SEED,
    "gate_rc": p.returncode,
    "wall_s": round(el, 3),
    "trace_bytes": st.st_size,
    "trace_mib": round(st.st_size / (1024 * 1024), 3),
    "trace_lines": sum(1 for _ in open(trace_path, "rb")),
    "fixture_bytes": tot,
    "fixture_files": nf,
    "stdout_bytes": len(out),
    "matcher_entry_lines": call_lines,
}, indent=1))
