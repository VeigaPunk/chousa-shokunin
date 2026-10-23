#!/usr/bin/env python3
"""Bound one frozen-counter run; retain command, PID/PGID, output and exit code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("name")
ap.add_argument("seed", type=int)
ap.add_argument("gate")
a = ap.parse_args()
art = Path(__file__).resolve().parent
scratch = Path("/fast/scratch/hyaku/chousa-r34/w1/CtlC1Truncate")
lane = Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
receipt = art / f"{a.name}-s{a.seed}.json"
cmd = ["timeout", "1700s", "prlimit", "--as=2147483648", "--nproc=4096", "--fsize=16777216", "python3", str(lane / "corpus/evidence/round34/c1-count.py"), "--gate", a.gate, "--seed", str(a.seed), "--receipt", str(receipt)]
env = dict(os.environ, C1_TMP=str(scratch), TMPDIR=str(scratch))
started = time.time()
p = subprocess.Popen(cmd, cwd=lane, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
meta = {"command": cmd, "cwd": str(lane), "C1_TMP": str(scratch), "TMPDIR": str(scratch), "wrapper_pid": os.getpid(), "wrapper_pgid": os.getpgrp(), "pid": p.pid, "pgid": p.pid}
print(f"RUN_PID={p.pid} RUN_PGID={p.pid}", flush=True)
try:
    out, err = p.communicate(timeout=1720)
except BaseException:
    os.killpg(p.pid, signal.SIGKILL)
    p.wait()
    raise
finally:
    if p.poll() is None:
        os.killpg(p.pid, signal.SIGKILL)
        p.wait()
meta.update(returncode=p.returncode, elapsed_s=round(time.time() - started, 3), stdout=out[:131072], stderr=err[:131072], stdout_truncated=len(out) > 131072, stderr_truncated=len(err) > 131072, stdout_sha256=hashlib.sha256(out.encode()).hexdigest(), stderr_sha256=hashlib.sha256(err.encode()).hexdigest(), process_reaped=True)
(art / f"{a.name}-s{a.seed}.run.json").write_text(json.dumps(meta, indent=1) + "\n")
print(out, end="")
if err:
    print(err, end="", file=sys.stderr)
print(f"COUNTER_RC={p.returncode}", flush=True)
sys.exit(p.returncode)
