#!/usr/bin/env python3
"""Stub battery: refuses any pre-populated/unusable --work (kama KQ112 shape).
It scores nothing: no matrix is read, no subject is run."""
import pathlib, sys
args = sys.argv[1:]
w = pathlib.Path(args[args.index("--work") + 1])
if w.exists() and w.is_file():
    print("stub: --work is not a directory", file=sys.stderr); sys.exit(2)
if w.exists() and any(w.iterdir()):
    print("stub: work-reused", file=sys.stderr); sys.exit(2)
try:
    w.mkdir(parents=True, exist_ok=True)
except OSError as exc:
    print(f"stub: cannot create --work: {exc}", file=sys.stderr); sys.exit(2)
print("BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED")
sys.exit(0)
