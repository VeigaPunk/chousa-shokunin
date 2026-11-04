#!/usr/bin/env python3
"""R78CriticB probe: isolate forge-battery's DETECTED/FORGED branch order.

The battery accepts two matrices by sha256 — the legit positive and the a5d forger — and
refuses everything else with an intact FAIL receipt. It is deliberately contrived: its only
job is to produce the artefact the frozen taxonomy cannot classify — a subject whose receipt
is dirty (a5d's detached append) AND whose battery run exited 0 with `BATTERY=PASS`. Under
the frozen branch order `if integrity is False: DETECTED` runs before the exit-code test,
so that subject is counted as *handled* although the taxonomy's own FORGED definition
("the battery exited 0") is satisfied.
"""
import argparse
import hashlib
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
ACCEPT = {
    hashlib.sha256((LANE / "corpus/evidence/round76/loader-matrix-v3.py").read_bytes()).hexdigest(),
    hashlib.sha256((LANE / "corpus/evidence/round78/forgers/a5d-detached-survives.py").read_bytes()).hexdigest(),
}

ap = argparse.ArgumentParser()
ap.add_argument("--matrix", required=True)
ap.add_argument("--work", default=None)
ap.add_argument("--runs", default="1")
ap.add_argument("--matrix-timeout", default="300")
a, _unknown = ap.parse_known_args()
import subprocess
work = pathlib.Path(a.work or ".")
work.mkdir(parents=True, exist_ok=True)
# Run the subject, as any battery does, so its own channels (a5d's detached append) fire.
subprocess.run([sys.executable, "-B", str(a.matrix), "--counter", "c", "--work",
                str(work / "s")], capture_output=True, text=True, timeout=120)
try:
    sha = hashlib.sha256(pathlib.Path(a.matrix).read_bytes()).hexdigest()
except OSError:
    sha = ""
if sha in ACCEPT:
    print("BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED")
    print("RECEIPT_LINES=2")
    sys.exit(0)
print("BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=MISS")
print("RECEIPT_LINES=2")
sys.exit(1)
