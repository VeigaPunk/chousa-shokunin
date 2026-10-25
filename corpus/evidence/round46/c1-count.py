#!/usr/bin/env python3
"""c1-count — frozen counter for round 46 claim C1 (operability).

Predicate R46-C1, the same sentence as corpus/evidence/round46/claims.md:
`tools/inference-ground.py` exists and, run over
`corpus/fixtures/inference-ground-r46/`, exits 0 on every `positive-*.md`
fixture and exits 1 on every `junk-*.md` fixture (the three junk classes:
uncited bullet, cited-but-ungrounded token, and a body that reuses the correct
spans and figures while its inference asserts something else — the round-45 D7
class, `CritC3Axis`).

Prints `POSITIVE_PASS=n/n JUNK_KILLED=n/n TOOL=present|absent C1=PASS|FAIL`.
Exit 0 iff the tool is present and every fixture scores its declared verdict;
1 otherwise; 2 usage/env (no fixtures).

Cheapest gates that would score full marks without the work (QUALITY 60):
a tool that always exits 0 passes the positives and kills nothing
(`--tool` on that forge scores JUNK_KILLED=0/3), and a tool that only checks
citation presence kills 1 of 3. A missing tool scores 0/n on both legs. The
counter checks exit codes only; what a finding NAMES is a reader's check.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = pathlib.Path("corpus/fixtures/inference-ground-r46")
POSITIVES = ("positive-a.md", "positive-b.md", "positive-c.md")
JUNKS = ("junk-uncited.md", "junk-ungrounded.md", "junk-borrowed.md")


def run(tool: pathlib.Path, fixture_dir: pathlib.Path, name: str) -> int:
    entry = fixture_dir / name
    if not entry.is_file():
        return 127
    proc = subprocess.run(
        [sys.executable, str(tool), "--entry", str(entry),
         "--spans", str(fixture_dir / "spans.tsv"),
         "--counts", str(fixture_dir / "counts.json"),
         "--root", str(fixture_dir)],
        capture_output=True, text=True)
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--tool", default=None, help="score another tool (controls)")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    tool = pathlib.Path(a.tool) if a.tool else root / "tools" / "inference-ground.py"
    fixture_dir = root / FIXTURES
    if not fixture_dir.is_dir():
        print("C1=FAIL no-fixtures")
        return 2
    present = tool.is_file()
    pos = sum(run(tool, fixture_dir, n) == 0 for n in POSITIVES) if present else 0
    junk = sum(run(tool, fixture_dir, n) != 0 for n in JUNKS) if present else 0
    print(f"TOOL={'present' if present else 'absent'}")
    print(f"POSITIVE_PASS={pos}/{len(POSITIVES)}")
    print(f"JUNK_KILLED={junk}/{len(JUNKS)}")
    ok = present and pos == len(POSITIVES) and junk == len(JUNKS)
    print("C1=PASS" if ok else "C1=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
