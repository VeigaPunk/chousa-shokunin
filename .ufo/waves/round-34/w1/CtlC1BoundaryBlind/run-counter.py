#!/usr/bin/env python3
"""Run one frozen-counter control, recording exact argv, PID, output and rc."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("--label", required=True)
p.add_argument("--gate", required=True)
p.add_argument("--seed", type=int, required=True)
a = p.parse_args()
lane = Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
outdir = lane / ".ufo/waves/round-34/w1/CtlC1BoundaryBlind"
scratch = "/fast/scratch/hyaku/chousa-r34/w1/CtlC1BoundaryBlind"
receipt = outdir / (a.label + "-s" + str(a.seed) + ".json")
command = ["timeout", "--signal=TERM", "--kill-after=10s", "1700s", "prlimit",
           "--as=2147483648", "--nproc=65536", "--fsize=16777216", "env",
           "C1_TMP=" + scratch, "TMPDIR=" + scratch, "python3",
           str(lane / "corpus/evidence/round34/c1-count.py"), "--gate", a.gate,
           "--seed", str(a.seed), "--receipt", str(receipt)]
started = time.time()
child = subprocess.Popen(command, cwd=lane, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True)
print("PID=%d PGID=%d LABEL=%s SEED=%d" % (child.pid, child.pid, a.label, a.seed), flush=True)
try:
    stdout, stderr = child.communicate(timeout=1720)
finally:
    if child.poll() is None:
        os.killpg(child.pid, signal.SIGKILL)
        child.wait()
result = {"label": a.label, "seed": a.seed, "command": command,
          "cwd": str(lane), "supervisor_pid": os.getpid(),
          "pid": child.pid, "pgid": child.pid, "rc": child.returncode,
          "elapsed_s": round(time.time() - started, 3),
          "stdout": stdout.decode("utf-8", "replace"),
          "stderr": stderr.decode("utf-8", "replace")}
payload = json.dumps(result, indent=1) + "\n"
if len(payload.encode()) >= 1 << 20:
    raise RuntimeError("bounded run evidence unexpectedly exceeds 1 MiB")
(outdir / ("run-" + a.label + "-s" + str(a.seed) + ".json")).write_text(payload)
print(result["stdout"], end="", flush=True)
print(result["stderr"], end="", file=sys.stderr, flush=True)
print("COUNTER_RC=%d ELAPSED_S=%s" % (child.returncode, result["elapsed_s"]), flush=True)
sys.exit(child.returncode)
