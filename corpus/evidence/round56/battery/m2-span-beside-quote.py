#!/usr/bin/env python3
"""R56-C1 battery — M2 NO_CHAR: the first row's span file holds an exact slice of the form beside its quote (longer than the quote, not containing it).
Runs the lane's landed `tools/build-spans.py` unchanged, then breaks exactly one behaviour the
gate (`corpus/evidence/round56/c1-gate.py`) checks; killing mutant M2 of the gate needs it."""
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
    m, lines, c = first_row()
    sp = OUT / c[4]
    span, quote = sp.read_text(encoding="utf-8"), c[5]
    i = span.find(quote)
    after, before = span[i + len(quote):], span[:i]
    if len(after) >= len(before):
        new, off = after, int(c[3]) + i + len(quote)
    else:
        new, off = before, int(c[3])
    if len(new) <= len(quote) or quote in new:
        sys.exit("battery m2: no slice beside the quote is longer than it")
    c[3] = str(off)
    sp.write_text(new, encoding="utf-8")
    lines[1] = "\t".join(c)
    m.write_text("\n".join(lines), encoding="utf-8")
sys.exit(rc)
