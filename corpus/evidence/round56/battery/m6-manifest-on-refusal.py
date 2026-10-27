#!/usr/bin/env python3
"""R56-C1 battery — M6 REF_TSV: on a refusal it still writes a header-only `spans.tsv` (and no span file), then exits 1.
Runs the lane's landed `tools/build-spans.py` unchanged, then breaks exactly one behaviour the
gate (`corpus/evidence/round56/c1-gate.py`) checks; killing mutant M6 of the gate needs it."""
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
if rc == 1:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "spans.tsv").write_text("id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry\n", encoding="utf-8")
sys.exit(rc)
