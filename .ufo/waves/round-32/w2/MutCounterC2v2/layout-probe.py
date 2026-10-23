#!/usr/bin/env python3
"""Exercise layout refusal without creating an in-lane fixture or invoking a gate."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import sys

counter, gate = map(Path, sys.argv[1:3])
ns = runpy.run_path(str(counter), run_name="counter_probe")
inside = str(gate.parent.parent / "synthetic-fixture-not-created")
reached = []
cleanup = []
def fake_temp(*args, **kwargs):
    return inside
def observe_generate(*args):
    reached.append(True)
    raise RuntimeError("LAYOUT_PROBE_REACHED_GENERATE")
def no_files_to_remove(path, **kwargs):
    cleanup.append(path)
ns["tempfile"].mkdtemp = fake_temp
ns["shutil"].rmtree = no_files_to_remove
ns["main"].__globals__["generate"] = observe_generate
sys.argv = [str(counter), "--gate", str(gate), "--seed", "32321023"]
stdout, stderr = io.StringIO(), io.StringIO()
with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
    rc = ns["main"]()
held = rc == 2 and not reached and "lies inside the gate's lane root" in stderr.getvalue()
print(json.dumps({"detector": "layout-refuses-before-generation", "synthetic_path_only": True,
                  "counter_sha256": hashlib.sha256(counter.read_bytes()).hexdigest(),
                  "C2_TMP": os.environ.get("C2_TMP"), "counter_rc": rc,
                  "generate_reached": bool(reached), "stdout": stdout.getvalue(),
                  "stderr": stderr.getvalue(), "cleanup": cleanup, "holds": held}, indent=2))
sys.exit(0 if held else 1)
