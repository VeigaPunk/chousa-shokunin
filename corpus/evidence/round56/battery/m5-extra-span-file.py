#!/usr/bin/env python3
"""R56-C1 battery — M5 NO_EXTRA: one span file no manifest row names is left in `spans/`.
Runs the lane's landed `tools/build-spans.py` unchanged, then breaks exactly one behaviour the
gate (`corpus/evidence/round56/c1-gate.py`) checks; killing mutant M5 of the gate needs it."""
import contextlib
import io
import pathlib
import runpy
import sys

LANE = pathlib.Path(__file__).resolve().parents[4]
BUILDER = LANE / "tools" / "build-spans.py"
OUT = pathlib.Path(sys.argv[sys.argv.index("--out") + 1])


def build() -> int:
    """Run the landed builder in-process; return its exit code."""
    sys.argv[0] = str(BUILDER)
    try:
        runpy.run_path(str(BUILDER), run_name="__main__")
    except SystemExit as e:
        return 0 if e.code is None else int(e.code)
    return 0


def first_row():
    m = OUT / "spans.tsv"
    lines = m.read_text(encoding="utf-8").split("\n")
    return m, lines, lines[1].split("\t")

rc = build()
if rc == 0:
    (OUT / "spans" / "S999-1.txt").write_text("an extra span file no row names", encoding="utf-8")
sys.exit(rc)
