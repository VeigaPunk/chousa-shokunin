#!/usr/bin/env python3
"""Do-nothing counters for the R62-C1 battery. MODE (argv[1] before the counter arguments) is one of
`pass` (exit 0 for every builder), `fail` (exit 1 for every builder) or `hashlist` (exit 0 only when the
builder file's sha256 is one of the lane's committed landing/positive builder hashes — no run, no legs).
Usage as a counter: null-counter.py MODE --builder B --work W   (the battery calls `python3 -B COUNTER --builder B --work W`;
the wrappers null-pass.py, null-fail.py and null-hashlist.py set MODE)."""
import hashlib, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[3]


def main(mode):
    a = sys.argv[1:]
    b = pathlib.Path(a[a.index("--builder") + 1])
    if mode == "pass":
        return 0
    if mode == "fail":
        return 1
    known = {hashlib.sha256((LANE / "tools" / "build-spans.py").read_bytes()).hexdigest()}
    known |= {hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob("pos-*.py")}
    return 0 if hashlib.sha256(b.read_bytes()).hexdigest() in known else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv.pop(1)))
