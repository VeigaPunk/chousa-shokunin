#!/usr/bin/env python3
"""SCRATCH PROBE helper: compute the 12 frozen fixture state fingerprints."""
import hashlib, importlib.util, json, sys, pathlib

spec = importlib.util.spec_from_file_location(
    "m", "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/loader-matrix-v2.py")
m = importlib.util.module_from_spec(spec)
sys.argv = ["x"]
spec.loader.exec_module(m)

table = {}
for name, path, op, rc, failed in m.CASES:
    files = dict(m.FILES)
    if path:
        files[path] = m.mutate(m.FILES[path], op)
    blob = "\0".join(files[k] for k in sorted(files))
    h = hashlib.sha256(blob.encode()).hexdigest()[:16]
    table[h] = [rc, sorted(failed)]
    print(f"{h}  {name}  rc={rc} failed={sorted(failed)}")
pathlib.Path("/fast/scratch/hyaku/chousa-r75/R75Scout/probe/fingerprint-table.json").write_text(
    json.dumps(table, indent=1))
